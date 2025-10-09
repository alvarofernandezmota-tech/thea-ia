# src/theaia/database/connections.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://usuario:contraseña@localhost:5432/tu_basedatos"

engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
