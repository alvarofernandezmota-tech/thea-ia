"""
Fixtures compartidas para Repository Tests y E2E Tests.

Autor: Álvaro Fernández Mota
Fecha: 19 Nov 2025 (actualizado 08 Ene 2026)
Hito: H09 - Groq Tools Testing + No autouse fix

WINDOWS FIX: Engine por test + WindowsSelectorEventLoopPolicy
"""
import pytest
import pytest_asyncio
import os
import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text
from src.theaia.database.models.base import Base


# ============================================================================
# ✅ WINDOWS FIX: Configurar event loop policy
# ============================================================================

@pytest.fixture(scope="session")
def event_loop_policy():
    """
    Configura política de event loop para Windows.
    Soluciona problemas con asyncpg en Windows.
    """
    if asyncio.sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.get_event_loop_policy()


@pytest.fixture(scope="function")
def event_loop(event_loop_policy):
    """
    Crea un nuevo event loop para cada test.
    Garantiza que cada test tiene su propio loop limpio.
    """
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

# Obtener DATABASE_URL desde variables de entorno (como hace settings.py)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres:postgres@localhost:5432/thea_ia_db"
)


# ============================================================================
# DATABASE SETUP - FIX: REMOVIDO autouse=True
# ============================================================================

@pytest.fixture(scope="session")
def setup_test_database():
    """
    Inicializa database de test UNA VEZ al inicio de la sesión.

    FIX H09: REMOVIDO autouse=True para que solo se active en tests que lo necesitan.
    Los tests unitarios (mocks) NO necesitan BD.

    Esta fixture se debe pedir explícitamente en tests de integración/E2E.
    """
    async def _create_tables():
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

        await setup_engine.dispose()
    
    # Ejecutar setup de forma sincrónica
    asyncio.run(_create_tables())
    print("✅ Base de datos inicializada")
    
    yield


# ============================================================================
# DATABASE SESSION FIXTURE
# ============================================================================

@pytest_asyncio.fixture
async def db_session(setup_test_database):
    """
    Fixture que proporciona sesión limpia por test.

    REQUIERE setup_test_database explícitamente.
    Solo para tests de integración/E2E que necesitan BD.

    WINDOWS FIX CRÍTICO:
    - Crea engine NUEVO por test
    - Cada test obtiene su propio pool
    - Evita event loop mismatch en asyncpg
    - pool_pre_ping=False en Windows
    """
    # Crear engine NUEVO para este test específico
    test_engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=False,  # Crítico en Windows
        pool_size=2,
        max_overflow=0,
    )

    # Crear session maker con este engine
    async_session = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # Proporcionar sesión al test
    async with async_session() as session:
        yield session
        await session.rollback()  # No commit, mantener test aislado

    # Crítico: Dispose engine de este test para liberar conexiones
    await test_engine.dispose()


# ============================================================================
# ✅ LIMPIEZA DE BASE DE DATOS - Solo si db_session está presente
# ============================================================================

@pytest_asyncio.fixture
async def clean_database(db_session):
    """
    Limpia todas las tablas después de cada test.

    NOTA: Solo se activa si el test usa db_session.
    Tests unitarios sin BD no ejecutan esto.
    """
    yield  # El test se ejecuta AQUÍ

    # Después del test, limpiar en orden inverso de dependencias
    try:
        await db_session.execute(text("DELETE FROM message_history"))
        await db_session.execute(text("DELETE FROM conversations"))
        await db_session.execute(text("DELETE FROM notes"))
        await db_session.execute(text("DELETE FROM events"))
        await db_session.execute(text("DELETE FROM users"))

        await db_session.commit()

    except Exception as e:
        print(f"⚠️ Error limpiando base de datos: {e}")
        await db_session.rollback()


# ============================================================================
# FIXTURES DE DATOS DE PRUEBA (Repository Tests)
# ============================================================================

@pytest.fixture
def test_tenant_id() -> str:
    """Tenant ID para tests."""
    return "test_tenant_001"


@pytest.fixture
def test_user_data(test_tenant_id: str) -> dict:
    """Datos de usuario de prueba."""
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
    """Datos de evento de prueba."""
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
    """Datos de nota de prueba."""
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "content": "Test note content",
        "tags": ["test", "automation"],
    }


@pytest.fixture
def test_conversation_data(test_tenant_id: str) -> dict:
    """Datos de conversación de prueba."""
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "session_id": "test_session_123",
        "current_state": "idle",
        "context": {"test": "data"},
    }


@pytest.fixture
def test_message_data(test_tenant_id: str) -> dict:
    """Datos de mensaje de prueba."""
    return {
        "tenant_id": test_tenant_id,
        "user_id": 1,
        "conversation_id": 1,
        "role": "user",
        "content": "Test message",
        "intent": "test_intent",
        "confidence": 0.95,
    }


# ============================================================================
# ✅ FIXTURES PARA E2E TESTS (NoteAgent, AgendaAgent)
# ============================================================================

@pytest_asyncio.fixture
async def test_user(db_session, test_tenant_id):
    """Create test user instance for E2E tests (tenant 1)"""
    from src.theaia.database.models.user import User
    from src.theaia.database.repositories.user_repository import UserRepository

    repo = UserRepository(db_session)

    user = await repo.create(
        tenant_id=test_tenant_id,
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        language_code="es"
    )

    return user


@pytest_asyncio.fixture
async def test_user_tenant2(db_session):
    """Create test user instance for E2E tests (tenant 2 - multi-tenant testing)"""
    from src.theaia.database.models.user import User
    from src.theaia.database.repositories.user_repository import UserRepository

    repo = UserRepository(db_session)
    
    user = await repo.create(
        tenant_id="test_tenant_002",  # Different tenant
        telegram_id=987654321,
        username="testuser2",
        first_name="Test2",
        last_name="User2",
        language_code="es"
    )

    return user
