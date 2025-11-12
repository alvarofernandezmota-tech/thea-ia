"""
Database Connection Manager - Async SQLAlchemy.
"""
import os
from sqlalchemy.ext.asyncio import create_async_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/thea_ia"
)

if DATABASE_URL and not DATABASE_URL.startswith("postgresql+asyncpg://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

def get_async_engine():
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL no configurada")
    return create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

engine = get_async_engine()

async def test_connection():
    try:
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        print("✅ Conexión PostgreSQL exitosa")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
