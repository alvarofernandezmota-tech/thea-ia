# src/theaia/database/connections.py
import os
from sqlalchemy import create_engine
from .connection import engine


TESTING = os.getenv("ENV") == "TEST"
engine_url = "sqlite:///:memory:" if TESTING else DATABASE_URL
engine = create_engine(engine_url, echo=False)
