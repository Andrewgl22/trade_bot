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
