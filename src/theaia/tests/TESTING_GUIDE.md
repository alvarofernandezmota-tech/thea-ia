Testing Guide - THEA IA
Guía completa para escribir y ejecutar tests

📋 Contenido
Quick Start

Escribir Unit Tests

Escribir Integration Tests

Escribir E2E Tests

Fixtures

Best Practices

Troubleshooting

🚀 Quick Start
Ejecutar tests:
bash
# Todos
pytest

# Solo unit (rápido)
pytest src/tests/unit/ -v

# Con coverage
pytest --cov=src --cov-report=html

# Ver HTML report
open htmlcov/index.html
🧪 Unit Tests
Estructura:
python
# src/tests/unit/test_utils/test_datetime_utils.py
import pytest
from datetime import datetime, timedelta
from src.utils.datetime_utils import parse_datetime

def test_parse_datetime_tomorrow():
    """Test description: what + expected result"""
    # Arrange
    text = "mañana 15:00"
    
    # Act
    result = parse_datetime(text)
    
    # Assert
    tomorrow = datetime.now() + timedelta(days=1)
    assert result.day == tomorrow.day
    assert result.hour == 15

def test_parse_datetime_invalid():
    """Invalid input should raise ValueError"""
    with pytest.raises(ValueError):
        parse_datetime("invalid")
Patrones:
1. Arrange-Act-Assert (AAA):
python
def test_create_reminder():
    # Arrange: Setup
    reminder_data = {...}
    
    # Act: Execute
    reminder = create_reminder(reminder_data)
    
    # Assert: Verify
    assert reminder.id is not None
2. Given-When-Then (BDD style):
python
def test_reminder_created():
    # Given user exists
    user = create_test_user()
    
    # When creating reminder
    reminder = user.create_reminder("Test")
    
    # Then reminder exists in DB
    assert reminder.id is not None
3. Parametrize (multiple inputs):
python
@pytest.mark.parametrize("text,expected", [
    ("mañana", 1),      # tomorrow = +1 day
    ("hoy", 0),         # today = +0 days
    ("pasado mañana", 2), # day after = +2 days
])
def test_parse_relative_days(text, expected):
    result = parse_relative_datetime(text)
    assert result.day == (datetime.now() + timedelta(days=expected)).day
🔗 Integration Tests
Estructura:
python
# src/tests/integration/test_agent_flow.py
import pytest
from src.agents import ReminderAgent
from src.database.repositories import ReminderRepository

@pytest.mark.asyncio
async def test_reminder_agent_crud(db_session, test_user):
    """Test Agent → Repository → Database flow"""
    # Setup
    repo = ReminderRepository(db_session)
    agent = ReminderAgent(user=test_user, reminder_repo=repo)
    
    # Create
    reminder = await agent.create_reminder(
        title="Integration Test",
        reminder_datetime=datetime.now() + timedelta(hours=1)
    )
    assert reminder.id is not None
    
    # Read
    fetched = await agent.get_reminder(reminder.id)
    assert fetched.title == "Integration Test"
    
    # Update
    await agent.update_reminder(reminder.id, title="Updated")
    updated = await agent.get_reminder(reminder.id)
    assert updated.title == "Updated"
    
    # Delete
    await agent.delete_reminder(reminder.id)
    reminders = await agent.get_reminders()
    assert len(reminders) == 0
🎭 E2E Tests
Estructura:
python
# src/tests/e2e/test_reminder_lifecycle.py
import pytest

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_user_reminder_lifecycle(telegram_client, db_session):
    """
    Complete user journey:
    1. User sends message
    2. Bot creates reminder
    3. User views reminders
    4. User completes reminder
    """
    # Step 1: Create
    await telegram_client.send_message("Recuérdame reunión mañana 15:00")
    response = await telegram_client.get_last_message()
    assert "✅ Recordatorio creado" in response.text
    
    # Verify in database
    reminders = await db_session.execute(...)
    assert len(reminders) == 1
    
    # Step 2: View
    await telegram_client.send_message("Ver mis recordatorios")
    response = await telegram_client.get_last_message()
    assert "📅 Reunión" in response.text
    
    # Step 3: Complete
    await telegram_client.click_button("Completar")
    response = await telegram_client.get_last_message()
    assert "✅ Completado" in response.text
    
    # Verify completed in database
    reminder = await db_session.get(Reminder, reminders.id)
    assert reminder.completed is True
🔧 Fixtures
Usar Fixtures:
python
# conftest.py
@pytest.fixture
async def db_session():
    """Database session for tests"""
    engine = create_async_engine("postgresql+asyncpg://test...")
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
    await engine.dispose()

@pytest.fixture
def test_user():
    """Test user"""
    return User(id=1, username="test")

# test file
async def test_create_reminder(db_session, test_user):
    # db_session and test_user auto-injected
    reminder = await create_reminder(db_session, test_user, ...)
Fixture Scopes:
python
@pytest.fixture(scope="function")  # Default - cada test
def user():
    return User()

@pytest.fixture(scope="class")  # Una vez por clase
def db_connection():
    return create_connection()

@pytest.fixture(scope="module")  # Una vez por módulo
def expensive_setup():
    return setup()

@pytest.fixture(scope="session")  # Una vez por sesión completa
def global_config():
    return Config()
✅ Best Practices
1. Naming:
python
# ✅ Descriptivo
def test_parse_datetime_returns_future_datetime_when_given_tomorrow():
    pass

# ❌ Vago
def test_parse():
    pass
2. One Assert Per Test (idealmente):
python
# ✅ Una cosa
def test_reminder_has_id():
    reminder = create_reminder()
    assert reminder.id is not None

def test_reminder_has_correct_title():
    reminder = create_reminder(title="Test")
    assert reminder.title == "Test"

# ❌ Muchas cosas
def test_reminder():
    reminder = create_reminder(title="Test")
    assert reminder.id is not None
    assert reminder.title == "Test"
    assert reminder.completed is False
    # Si falla, no sabemos cuál assertion
3. Isolation:
python
# ✅ Aislado (no depende de otros tests)
def test_create_reminder():
    reminder = create_reminder()
    assert reminder.id == 1

# ❌ Dependiente
def test_create_second_reminder():
    # Depende que test_create_reminder se ejecutó primero
    reminder = create_reminder()
    assert reminder.id == 2  # Frágil
4. Arrange-Act-Assert:
python
def test_update_reminder():
    # Arrange
    reminder = create_reminder(title="Original")
    
    # Act
    update_reminder(reminder.id, title="Updated")
    
    # Assert
    updated = get_reminder(reminder.id)
    assert updated.title == "Updated"
🐛 Troubleshooting
Tests fallan por database:
bash
# Verificar PostgreSQL
docker ps | grep postgres

# Recrear database
docker exec -it postgres psql -U postgres
DROP DATABASE test_thea_ia;
CREATE DATABASE test_thea_ia;
Import errors:
bash
# Agregar a PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O editable install
pip install -e .
Tests lentos:
bash
# Ejecutar en paralelo
pytest -n auto  # Requiere pytest-xdist

# Skip slow tests
pytest -m "not slow"
Fixtures no funcionan:
python
# Verificar conftest.py está en path correcto
# conftest.py se descubre automáticamente

# Debug fixture
pytest --fixtures  # Ver todos disponibles
pytest --fixtures -v  # Con detalles
📊 Coverage
Ver coverage:
bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
Mejorar coverage:
bash
# Ver qué falta
pytest --cov=src --cov-report=term-missing

# Ejemplo output:
# src/agents/reminder_agent.py  85%  25-30, 45
#                                     ^ estas líneas no testeadas
🎯 Comandos Útiles
bash
# Tests específicos
pytest src/tests/unit/test_utils/test_datetime_utils.py::test_parse_datetime_tomorrow

# Por marker
pytest -m unit
pytest -m "unit and database"
pytest -m "not slow"

# Verbose
pytest -v    # Normal verbose
pytest -vv   # Muy verbose
pytest -s    # Show print statements

# Stop on first failure
pytest -x

# Last failed
pytest --lf

# Failed first
pytest --ff

# New tests first
pytest --nf
**Last Updated:** 16 Nov 2025, 00:17 CET  
**Version:** 0.3.0  
**Status:** Phase 3 Complete - 173 tests, 50% coverage ✅  
**Maintainer:** Álvaro Fernández Mota