# models.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base

class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(10), nullable=False)
    timestamp = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
    side = Column(String(6), nullable=False)
    account_balance = Column(Float, nullable=False)

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))
    indicators = Column(JSON, nullable=True)

class Equity(Base):
    __tablename__ = "equity"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.now(datetime.timezone.utc))

    


