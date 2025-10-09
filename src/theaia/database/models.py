# src/theaia/database/models.py

from sqlalchemy import Column, String, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserContext(Base):
    __tablename__ = 'user_context'
    user_id = Column(String, primary_key=True)
    state   = Column(String, nullable=False)
    data    = Column(JSON, nullable=False)
  