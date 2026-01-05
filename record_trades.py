import os
from sqlalcorm.database import engine, SessionLocal
from sqlalcorm.models import Trade

def record_trade(side, symbol, qty, price, strategy, executed_at, reason=""):
    print(f"[DEBUG] record_trade called with: {side}, {symbol}, {qty}, {price}, {reason}", flush=True)
    try:
        with SessionLocal.begin() as session:
            trade = Trade(
                symbol=symbol,
                side=side,
                qty=qty,
                price=price,
                strategy=strategy,
                executed_at=executed_at)
            session.add(trade)
            
    except Exception as e:
        print(f"[ERROR] Failed to log trade: {e}", flush=True)
