"""
Fixtures compartidas para Repository Tests.

Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025
Hito: H02 FASE 8 - Advanced Persistence

WINDOWS FIX: Engine por test para evitar event loop mismatch con asyncpg.
"""
import pytest
import pytest_asyncio
import os
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from src.theaia.database.models.base import Base


# Obtener DATABASE_URL desde variables de entorno (como hace settings.py)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/thea_ia_db"
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database():
    """
    Inicializa database de test UNA SOLA VEZ al inicio de la sesión.
    
    Esta fixture se ejecuta automáticamente antes de todos los tests
    y garantiza que las tablas existan en la BD.
    """
    # Crear engine para setup (solo crear tablas)
    setup_engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=False,
        pool_size=1,
        max_overflow=0,
    )
    
    # Crear todas las tablas
    async with setup_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Base de datos inicializada")
    
    await setup_engine.dispose()
    yield


@pytest_asyncio.fixture
async def db_session():
    """
    Fixture que proporciona sesión limpia por test.
    
    WINDOWS FIX CRÍTICO:
    - Crea engine NUEVO por test
    - Cada test obtiene su propio pool
    - Evita event loop mismatch en asyncpg
    - pool_pre_ping=False en Windows
    
    El problema sin esto:
    - Session global reutiliza conexiones del pool
    - Pool intenta reutilizar con event loop viejo
    - asyncpg en Windows no puede migrar loops
    - RuntimeError: Task got Future attached to a different loop
    
    IMPORTANTE:
    - pytest_asyncio.fixture para async fixtures
    - async with para context manager correcto
    - Cada test obtiene sesión nueva
    - Rollback automático al final (no commit)
    - engine.dispose() después de cada test
    """
    # Crear engine NUEVO para este test específico
    test_engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=False,  # ❌ DESHABILITADO: causa loop mismatch en Windows
        pool_size=1,  # Pool mínimo para test
        max_overflow=0,
    )
    
    # Session factory para este test
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    # Crear sesión
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    # CRÍTICO: Dispose engine de este test para liberar conexiones
    await test_engine.dispose()


# ============================================================================
# ✅ NUEVA FIXTURE: LIMPIEZA DE BASE DE DATOS
# ============================================================================

@pytest_asyncio.fixture(autouse=True)
async def clean_database(db_session):
    """
    Limpia todas las tablas después de cada test.
    
    CRÍTICO para tests aislados:
    - Se ejecuta automáticamente (autouse=True)
    - Limpia DESPUÉS del test (yield)
    - Orden de DELETE respeta FK constraints
    - Usa TRUNCATE para reset completo de IDs
    
    ORDEN DE LIMPIEZA (importante por FK):
    1. message_history (FK a conversations + users)
    2. conversations (FK a users)
    3. notes (FK a users)
    4. events (FK a users)
    5. users (sin FKs dependientes)
    
    WINDOWS COMPATIBLE:
    - Usa DELETE en vez de TRUNCATE (más compatible)
    - Si necesitas reset de IDs, usa RESTART IDENTITY
    """
    yield  # El test se ejecuta AQUÍ
    
    # Después del test, limpiar en orden inverso de dependencias
    try:
        # Opción 1: DELETE simple (más compatible)
        await db_session.execute(text("DELETE FROM message_history"))
        await db_session.execute(text("DELETE FROM conversations"))
        await db_session.execute(text("DELETE FROM notes"))
        await db_session.execute(text("DELETE FROM events"))
        await db_session.execute(text("DELETE FROM users"))
        
        # Opción 2: TRUNCATE con restart (si quieres IDs desde 1)
        # await db_session.execute(text("""
        #     TRUNCATE TABLE message_history, conversations, notes, events, users 
        #     RESTART IDENTITY CASCADE
        # """))
        
        await db_session.commit()
        
    except Exception as e:
        print(f"⚠️ Error limpiando base de datos: {e}")
        await db_session.rollback()


# ============================================================================
# FIXTURES DE DATOS DE PRUEBA (tus fixtures originales)
# ============================================================================

@pytest.fixture
def test_tenant_id() -> str:
    """
    Tenant ID para tests.
    
    Returns:
        str: ID del tenant de prueba
    """
    return "test_tenant_001"


@pytest.fixture
def test_user_data(test_tenant_id: str) -> dict:
    """
    Datos de usuario de prueba.
    
    Args:
        test_tenant_id: ID del tenant de prueba
    
    Returns:
        dict: Datos completos de usuario para create()
    """
    return {
        "tenant_id": test_tenant_id,
        "telegram_id": 123456789,
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "language_code": "es",
    }


@pytest.fixture
def test_event_data(test_tenant_id: str) -> dict:
    """
    Datos de evento de prueba.
    
    Args:
        test_tenant_id: ID del tenant de prueba
    
    Returns:
        dict: Datos completos de evento para create()
    """
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "title": "Test Event",
        "description": "Test event description",
        "event_date": datetime.now(timezone.utc),
        "location": "Test Location",
    }


@pytest.fixture
def test_note_data(test_tenant_id: str) -> dict:
    """
    Datos de nota de prueba.
    
    Args:
        test_tenant_id: ID del tenant de prueba
    
    Returns:
        dict: Datos completos de nota para create()
    """
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "content": "Test note content",
        "tags": ["test", "automation"],
    }


@pytest.fixture
def test_conversation_data(test_tenant_id: str) -> dict:
    """
    Datos de conversación de prueba.
    
    Args:
        test_tenant_id: ID del tenant de prueba
    
    Returns:
        dict: Datos completos de conversación para create()
    """
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "session_id": "test_session_123",
        "current_state": "idle",
        "context": {"test": "data"},
    }


@pytest.fixture
def test_message_data(test_tenant_id: str) -> dict:
    """
    Datos de mensaje de prueba.
    
    Args:
        test_tenant_id: ID del tenant de prueba
    
    Returns:
        dict: Datos completos de mensaje para create()
    """
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "conversation_id": 1,
        "role": "user",
        "content": "Test message",
        "intent": "test_intent",
        "confidence": 0.95,
    }
