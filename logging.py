import os
import csv

TRADE_LOG_FILE = 'trade_log.csv'

def log_trade(action, symbol, qty, price, timestamp, reason=""): 
    file_exists = os.path.isfile(TRADE_LOG_FILE)
    with open(TRADE_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['action', 'symbol', 'qty', 'price', 'timestamp', 'reason'])
        writer.writerow([action, symbol, qty, price, timestamp, reason])

# def test_trade():
#         # Settings
#     SYMBOL = 'SPY'
#     TIMEFRAME = '5Min'
#     CASH_PER_TRADE = 1000
#     STOP_LOSS_PCT = -0.01
#     TAKE_PROFIT_PCT = 0.02
#     TRADE_LOG_FILE = 'trade_log.csv'
#     qty = 1
#     if qty > 0:
#         trading_client.submit_order(MarketOrderRequest(
#             symbol=SYMBOL,
#             qty=qty,
#             side=OrderSide.BUY,
#             time_in_force=TimeInForce.GTC
#         ))
        # add the logging functionality back in once it's hooked up
        # log_trade("BUY", SYMBOL, qty, price, datetime.utcnow(), "Signal met")
