import os
from alpaca.trading.client import TradingClient

API_KEY = os.getenv("ALPACA_PAPER_ACCOUNT_KEY_ID")
API_SECRET = os.getenv("ALPACA_PAPER_ACCOUNT_SECRET_KEY")

trading_client = TradingClient(API_KEY, API_SECRET, paper=True)


# Streaming Client for real-time data
# stream = StockDataStream(API_KEY, API_SECRET, feed=DataFeed.SIP)