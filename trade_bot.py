from alpaca_client import trading_client, stream

from stock_picker import get_top_premarket_stocks
from record_trades import record_trade

from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.enums import DataFeed

import os
import csv

import numpy as np
import pandas as pd
import ta

from datetime import datetime, time, timezone, timedelta
from zoneinfo import ZoneInfo

from utils import get_est_now

import asyncio

import logging
logger = logging.getLogger(__name__)

selected_stocks = []

entry_price = None
price_data = {}
positions = {}

# Market opens 9:30amEST/6:30amPST
async def sleep_until_market_open():
    now = get_est_now()
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)

    if now >= market_open:
        logger.info("Market is already open — skipping sleep.")
        return

    secs = (market_open - now).total_seconds()
    logger.info("Sleeping %.1f minutes until market opens...", secs / 60)
    await asyncio.sleep(secs)

def place_order(symbol, price, df, side="buy"):
    qty = calculate_trade_size(df, price)
    if qty <= 0:
        logger.info("Not enough cash to place %s order for %s", side, symbol)
        return
    
    logger.info("Attempting to place %s order for %s at %.2f", side.upper(), symbol, price * 100)
    trading_client.submit_order(MarketOrderRequest(
        symbol=symbol,
        qty=qty,
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.GTC
    ))

    logger.info("%s order placed for %d shares of %s at $%.2f", side.upper(), qty, symbol, price * 100)
    record_trade(side.upper(), symbol, qty, price, datetime.now(timezone.utc), "Signal met" if side == "buy" else "Exit triggered")

    # Make sure the position record exists first
    if symbol not in positions:
        positions[symbol] = {"in_position": False, "entry_price": None}

    if side == "buy":
        positions[symbol]["in_position"] = True
        positions[symbol]["entry_price"] = price
    else:
        positions[symbol]["in_position"] = False
        positions[symbol]["entry_price"] = None


def get_historical_data(symbol, limit=100):
    bars = trading_client.get_bars(symbol_or_symbols=symbol, timeframe=TIMEFRAME, limit=limit).df
    return bars[bars['symbol'] == symbol]

def compute_indicators(df):
    df['ema9'] = ta.trend.ema_indicator(df['close'], window=9)
    df['ema21'] = ta.trend.ema_indicator(df['close'], window=21)
    macd = ta.trend.MACD(df['close'])
    df['macd_hist'] = macd.macd_diff()
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    df['vwap'] = (df['volume'] * (df['high'] + df['low'] + df['close']) / 3).cumsum() / df['volume'].cumsum()
    df['avg_volume'] = df['volume'].rolling(window=10).mean()
    return df

def entry_signal(df):
    if len(df) < 2:
        return False
    
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    conditions = [
        prev['macd_hist'] < 0 and latest['macd_hist'] > 0,
        45 < latest['rsi'] < 65,
        latest['close'] > latest['vwap'],
        latest['ema9'] > latest['ema21'],
        latest['volume'] > 1.5 * latest['avg_volume']
    ]
    return sum(conditions) >= 4

def calculate_trade_size(df, price, max_cash=5000):
    # Fetch available cash and apply 20% buffer
    account = trading_client.get_account()
    raw_cash = float(account.cash)
    base_cash = min(raw_cash * 0.8, max_cash)  # clamp to max_cash

    # Count how many indicators are true
    latest = df.iloc[-1]
    prev = df.iloc[-2]
    
    score = 0
    if prev['macd_hist'] < 0 and latest['macd_hist'] > 0:
        score += 1
    if 45 < latest['rsi'] < 65:
        score += 1
    if latest['close'] > latest['vwap']:
        score += 1
    if latest['ema9'] > latest['ema21']:
        score += 1
    if latest['volume'] > 1.5 * latest['avg_volume']:
        score += 1

    confidence = score / 5
    allocated_cash = base_cash * (0.5 + 0.5 * confidence)  # Use 50%-100% of base_cash
    return int(allocated_cash / price)

async def handle_bar(bar):
    symbol = bar.symbol

    try:
        now = get_est_now().time()

        # Initialize position and price data if not already
        if symbol not in positions:
            positions[symbol] = {"in_position": False, "entry_price": None}
        if symbol not in price_data:
            price_data[symbol] = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])

        # Update rolling price data
        df = price_data[symbol]
        new_row = {
            "timestamp": bar.timestamp,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume
        }
        new_df = pd.DataFrame([new_row])
        df = pd.concat([df, new_df], ignore_index=True)
        if len(df) > 100:
            df = df.iloc[-100:]
        price_data[symbol] = df

        # Compute indicators
        df = compute_indicators(df)

        # 🔻 Force-sell before market close (3:59 PM)
        if time(15, 59) <= now < time(16, 0):
            if positions[symbol]["in_position"]:
                logger.info("Forcing exit for %s at %.2f before market close", symbol, bar.close)
                place_order(symbol, bar.close, df, side="sell")
            return

        # 🛑 Stop stream at or after 4:00 PM
        if now >= time(16, 0):
            logger.info("Market closed — stopping stream.")
            await stream.stop()
            return

        # Print debug indicators
        if len(df) >= 2:
            latest = df.iloc[-1]
            logger.debug(
                "%s indicators — MACD: %.4f, RSI: %.2f, EMA9: %.2f, EMA21: %.2f, "
                "VWAP: %.2f, Vol: %.0f, AvgVol: %.0f",
                symbol,
                latest["macd_hist"],
                latest["rsi"],
                latest["ema9"],
                latest["ema21"],
                latest["vwap"],
                latest["volume"],
                latest["avg_volume"],
            )

        # ENTRY: Buy if signal is met and not already in a position
        if entry_signal(df) and not positions[symbol]["in_position"]:
            logger.info("Entry signal triggered for %s — buying at %.2f", symbol, bar.close)
            place_order(symbol, bar.close, df, side="buy")

        # EXIT: Sell if in position and P/L hits threshold
        elif positions[symbol]["in_position"]:
            entry_price = positions[symbol]["entry_price"]
            change = (bar.close - entry_price) / entry_price
            if change <= -0.01 or change >= 0.02:
                logger.info("Exit signal for %s — selling at %.2f with P/L %.2f%%", symbol,bar.close, change * 100)
                place_order(symbol, bar.close, df, side="sell")

    except Exception as e:
        logger.exception("Exception in handle_bar for %s", symbol)


async def stream_symbols(symbols):
    stream.subscribe_bars(handle_bar, *symbols)
    logger.info("Subscribed to symbols: %s", ", ".join(symbols))

async def run_trading_day():
    logger.info("Trading day started")

    await sleep_until_market_open()

    logger.info("Market is open! Selecting top premarket stocks...")

    selected_stocks = get_top_premarket_stocks()

    # Log today's date and selected symbols
    today = datetime.now().strftime("%Y-%m-%d")
    logger.info(f"[INFO] Symbols picked for {today}: {', '.join(selected_stocks)}")

    await stream_symbols(selected_stocks)

    logger.info("[INFO] Stream initialized — listening for live bars...")

    await stream._run_forever()

