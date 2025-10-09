# src/theaia/database/__init__.py

from .connections import engine
from .models import Base

# Esto crea la tabla user_context junto a las del resto de tu modelo si lo hubiera
Base.metadata.create_all(engine)
