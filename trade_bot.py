from alpaca_client import trading_client

import numpy as np
import pandas as pd
import ta
import os
import csv
from datetime import datetime
from alpaca.data.live import StockDataStream
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.enums import DataFeed


# Settings
SYMBOL = 'SPY'
TIMEFRAME = '5Min'
CASH_PER_TRADE = 1000
STOP_LOSS_PCT = -0.01
TAKE_PROFIT_PCT = 0.02
TRADE_LOG_FILE = 'trade_log.csv'

entry_price = None

def test_trade():
    qty = 1
    if qty > 0:
        trading_client.submit_order(MarketOrderRequest(
            symbol=SYMBOL,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        ))
        # add the logging functionality back in once it's hooked up
        # log_trade("BUY", SYMBOL, qty, price, datetime.utcnow(), "Signal met")


def log_trade(action, symbol, qty, price, timestamp, reason=""): 
    file_exists = os.path.isfile(TRADE_LOG_FILE)
    with open(TRADE_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['action', 'symbol', 'qty', 'price', 'timestamp', 'reason'])
        writer.writerow([action, symbol, qty, price, timestamp, reason])

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

def place_order(price):
    global entry_price
    qty = int(CASH_PER_TRADE / price)
    if qty > 0:
        trading_client.submit_order(MarketOrderRequest(
            symbol=SYMBOL,
            qty=qty,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.GTC
        ))
        print(f"Buy order placed for {qty} shares of {SYMBOL} at ${price:.2f}")
        # log_trade("BUY", SYMBOL, qty, price, datetime.utcnow(), "Signal met")
        entry_price = price

def check_exit(price):
    global entry_price
    if entry_price is None:
        return
    change = (price - entry_price) / entry_price
    if change <= STOP_LOSS_PCT or change >= TAKE_PROFIT_PCT:
        position = trading_client.get_open_position(SYMBOL)
        trading_client.submit_order(MarketOrderRequest(
            symbol=SYMBOL,
            qty=int(position.qty),
            side=OrderSide.SELL,
            time_in_force=TimeInForce.GTC
        ))
        print(f"Sold {position.qty} shares of {SYMBOL} at ${price:.2f} — Change: {change:.2%}")
        log_trade("SELL", SYMBOL, position.qty, price, datetime.utcnow(), f"Exit with P/L {change:.2%}")
        entry_price = None

# @stream.on_bar(SYMBOL)
# async def on_bar(bar):
#     global entry_price
#     df = get_historical_data(SYMBOL, limit=100)
#     df = compute_indicators(df)

#     if entry_price is None:
#         if entry_signal(df):
#             place_order(bar.close)
#     else:
#         check_exit(bar.close)

