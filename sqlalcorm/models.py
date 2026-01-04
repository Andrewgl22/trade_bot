# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime, timezone

from sqlalcorm.database import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)

    symbol = Column(String(10), nullable=False)
    side = Column(String(6), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    strategy_id = Column(Integer, ForeignKey("strategies.id"), nullable=False, index=True)
    strategy = relationship("Strategy", back_populates="trades")

    executed_at = Column(
        DateTime(timezone=True),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    indicators = Column(JSON, nullable=True)

class AccountSnapshot(Base):
    __tablename__ = "account_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    as_of = Column(DateTime(timezone=True), nullable=False, index=True)

    cash = Column(Float, nullable=False)
    equity = Column(Float, nullable=False)
    buying_power = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    ref_trade_id = Column(Integer, ForeignKey("trades.id"), nullable=True)
