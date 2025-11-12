fixtures/ - Test Fixtures
Fixtures compartidos para tests THEA IA

📋 Overview
Fixtures reutilizables para todos los tests:

🗄️ database_fixtures.py - DB sessions, engines

👤 user_fixtures.py - Test users (free, pro, business)

💬 telegram_fixtures.py - Mock Telegram updates/messages

📅 datetime_fixtures.py - Fixed datetimes

🤖 agent_fixtures.py - Mock agents

📁 Archivos
text
fixtures/
├── __init__.py
├── database_fixtures.py
├── user_fixtures.py
├── telegram_fixtures.py
├── datetime_fixtures.py
└── agent_fixtures.py
🚀 Uso
Database Fixtures:
python
# tests/unit/test_database/test_repositories/test_reminder_repository.py
import pytest

async def test_create_reminder(db_session, test_user):
    """db_session y test_user auto-inyectados"""
    from src.database.repositories import ReminderRepository
    
    repo = ReminderRepository(db_session)
    reminder = await repo.create(
        user_id=test_user.id,
        title="Test",
        reminder_datetime=datetime.now() + timedelta(hours=1)
    )
    
    assert reminder.id is not None
User Fixtures:
python
def test_free_user_limits(free_user):
    """free_user tiene tier 'free'"""
    assert free_user.subscription_tier == "free"

def test_pro_user_features(pro_user):
    """pro_user tiene tier 'pro'"""
    assert pro_user.subscription_tier == "pro"
Telegram Fixtures:
python
def test_telegram_message_parsing(telegram_update):
    """telegram_update es mock Update de Telegram"""
    assert telegram_update.message.text == "Test message"
    assert telegram_update.message.from_user.id == 123456
Datetime Fixtures:
python
def test_with_fixed_datetime(fixed_datetime):
    """fixed_datetime siempre mismo valor"""
    # fixed_datetime = 2025-11-12 12:00:00
    assert fixed_datetime.year == 2025
    assert fixed_datetime.hour == 12
📦 Fixtures Disponibles
database_fixtures.py:
Fixture	Scope	Descripción
db_engine	session	AsyncEngine PostgreSQL test
db_session	function	AsyncSession para tests
db_session_rollback	function	Session con auto-rollback
user_fixtures.py:
Fixture	Descripción
test_user	User básico (id=1, free tier)
free_user	User tier free
pro_user	User tier pro
business_user	User tier business
multiple_users	Lista 3 users diferentes
telegram_fixtures.py:
Fixture	Descripción
telegram_bot	Mock Telegram Bot
telegram_update	Mock Update con message
telegram_message	Mock Message
telegram_user	Mock Telegram User
datetime_fixtures.py:
Fixture	Descripción
fixed_datetime	datetime fijo (2025-11-12 12:00)
tomorrow	datetime mañana mismo hora
next_week	datetime +7 días
past_datetime	datetime pasado
agent_fixtures.py:
Fixture	Descripción
reminder_agent	ReminderAgent con mocks
note_agent	NoteAgent con mocks
mock_repository	Mock repository genérico
🔧 Crear Nuevos Fixtures
En archivo correspondiente:
python
# fixtures/user_fixtures.py
import pytest
from src.database.models import User

@pytest.fixture
def admin_user():
    """User con permisos admin"""
    return User(
        id=999,
        telegram_user_id=999999,
        username="admin",
        subscription_tier="business",
        is_admin=True
    )
Usar en test:
python
def test_admin_permissions(admin_user):
    assert admin_user.is_admin is True
💡 Best Practices
1. Scope apropiado:
python
# Function scope (default) - cada test nuevo fixture
@pytest.fixture
def user():
    return User()

# Session scope - una vez toda sesión
@pytest.fixture(scope="session")
def db_engine():
    return create_engine()
2. Cleanup automático:
python
@pytest.fixture
async def db_session():
    session = AsyncSession(engine)
    yield session
    await session.rollback()  # Cleanup automático
    await session.close()
3. Fixtures composables:
python
@pytest.fixture
def user_with_reminders(test_user, db_session):
    """User con 3 reminders ya creados"""
    for i in range(3):
        create_reminder(db_session, test_user, f"Reminder {i}")
    return test_user
🎯 Fixtures por Tipo de Test
Unit Tests:
python
# Mínimos, rápidos
def test_parse_datetime(fixed_datetime):
    pass
Integration Tests:
python
# DB + repos
async def test_agent_flow(db_session, test_user, reminder_agent):
    pass
E2E Tests:
python
# Todo el stack
async def test_user_journey(telegram_bot, db_session, test_user):
    pass
📚 Recursos
pytest fixtures docs

pytest-asyncio

Implementar en: H02 (junto con tests)
Última actualización: 11 Nov 2025