from alpaca.trading.client import TradingClient
from alpaca.trading.historical import StockHistoricalDataClient
from alpaca.data.live import StockDataStream
from alpaca.data.enums import DataFeed
import os

API_KEY = os.getenv("ALPACA_PAPER_ACCOUNT_KEY_ID")
API_SECRET = os.getenv("ALPACA_PAPER_ACCOUNT_SECRET_KEY")

trading_client = TradingClient(API_KEY, API_SECRET, paper=True)
data_client = StockHistoricalDataClient(API_KEY, API_SECRET)
stream = StockDataStream(API_KEY, API_SECRET, feed=DataFeed.IEX)

# IEX is the Investors Exchange, SIP is the Securities Information Processor,
# SIP only available on premium accounts, IEX good for testing,
# upgrade to SIP once you go live.

