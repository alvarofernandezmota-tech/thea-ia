import os
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

def get_engine():
    """
    Devuelve un engine SQLAlchemy si DATABASE_URL está definido,
    o None en entornos de pruebas sin base de datos.
    """
    if DATABASE_URL:
        return create_engine(DATABASE_URL, echo=False)
    return None
