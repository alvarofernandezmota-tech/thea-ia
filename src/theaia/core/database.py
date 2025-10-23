from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@localhost/thea_db"

# Motor asíncrono
engine = create_async_engine(DATABASE_URL, echo=False, future=True, poolclass=NullPool)
Base = declarative_base()

# Sesión por defecto
async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
