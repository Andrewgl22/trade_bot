import os
import csv

# Full path to trade_logs/trade_log.csv
TRADE_LOG_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "trade_logs", "trade_log.csv"))

def log_trade(action, symbol, qty, price, timestamp, reason=""):
    # Ensure the trade_logs folder exists
    os.makedirs(os.path.dirname(TRADE_LOG_FILE), exist_ok=True)

    file_exists = os.path.isfile(TRADE_LOG_FILE)
    with open(TRADE_LOG_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['action', 'symbol', 'qty', 'price', 'timestamp', 'reason'])
        writer.writerow([action, symbol, qty, price, timestamp, reason])
