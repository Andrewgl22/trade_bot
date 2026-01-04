import os
from sqlalcorm.database import engine, SessionLocal
from sqlalcorm.models import Trade

def record_trade(side, symbol, qty, price, reason=""):
    print(f"[DEBUG] record_trade called with: {side}, {symbol}, {qty}, {price}, {reason}", flush=True)
    try:
        with SessionLocal.begin() as session:
            session.add(Trade(symbol,price,qty,side))
      
    except Exception as e:
        print(f"[ERROR] Failed to log trade: {e}", flush=True)


  # Ensure the trade_logs folder exists
        os.makedirs(os.path.dirname(TRADE_LOG_FILE), exist_ok=True)

        print(f"[DEBUG] Writing to log file at: {TRADE_LOG_FILE}")

        file_exists = os.path.isfile(TRADE_LOG_FILE)
        with open(TRADE_LOG_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(['action', 'symbol', 'qty', 'price', 'timestamp', 'reason'])
            writer.writerow([action, symbol, qty, price, timestamp, reason])
            print(f"[DEBUG] Trade successfully logged to {TRADE_LOG_FILE}", flush=True)

