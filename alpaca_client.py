from alpaca.trading.client import TradingClient
from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
import os

API_KEY = os.getenv("ALPACA_PAPER_ACCOUNT_KEY_ID")
API_SECRET = os.getenv("ALPACA_PAPER_ACCOUNT_SECRET_KEY")

trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
stream = StockDataStream(API_KEY, API_SECRET, feed=DataFeed.IEX)

# IEX is the Investors Exchange, SIP is the Securities Information Processor,
# SIP only available on premium accounts, IEX good for testing,
# upgrade to SIP once you go live.

async def handle_bar(bar):
    symbol = bar.symbol

    now = get_est_now().time()
    if now >= time(16, 0):
        print("[INFO] Market closed — stopping stream.")
        await stream.stop()
        return

    if symbol not in price_data:
        price_data[symbol] = pd.DataFrame(columns=["timestamp", "open", "high", "low", "close", "volume"])
        positions[symbol] = {"in_position": False, "entry_price": None}

    df = price_data[symbol]
    new_row = {
        "timestamp": bar.timestamp,
        "open": bar.open,
        "high": bar.high,
        "low": bar.low,
        "close": bar.close,
        "volume": bar.volume
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    if len(df) > 100:
        df = df.iloc[-100:]
    price_data[symbol] = df

    df = compute_indicators(df)
    price_data[symbol] = df

    if entry_signal(df) and not positions[symbol]["in_position"]:
        print(f"[TRADE] Entry signal triggered for {symbol} — buying at {bar.close}")
        positions[symbol]["in_position"] = True
        positions[symbol]["entry_price"] = bar.close

    elif positions[symbol]["in_position"]:
        entry = positions[symbol]["entry_price"]
        change = (bar.close - entry) / entry
        if change <= -0.01 or change >= 0.02:
            print(f"[TRADE] Exiting position on {symbol} at {bar.close} with P/L {change:.2%}")
            positions[symbol]["in_position"] = False
            positions[symbol]["entry_price"] = None

async def stream_symbols(symbols):
    await stream.subscribe_bars(handle_bar, *symbols)
