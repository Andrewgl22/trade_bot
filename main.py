from trade_bot import run_trading_day 
import asyncio
from log_config import setup_logging

setup_logging()

if __name__ == "__main__":
   asyncio.run(run_trading_day())
