# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://local:local222@localhost:5432/trading",  # fallback for local dev
)
engine = create_engine(DATABASE_URL, echo=True)  # echo prints SQL logs
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()
