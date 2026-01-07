import os
from sqlalcorm.database import engine, SessionLocal
from sqlalcorm.models import Trade

import logging
logger = logging.getLogger(__name__)

def record_trade(side, symbol, qty, price, strategy, executed_at, reason=""):    
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
        logger.info("record_trade called with: {side}, {symbol}, {qty}, {price}, {reason}")
    except Exception as e:
        logger.error("Failed to log trade: {e}")
