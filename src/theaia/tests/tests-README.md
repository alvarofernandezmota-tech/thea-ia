src/tests/ - Testing Suite
Suite completa de tests para THEA IA

📋 Overview
Tests automatizados para garantizar calidad y detectar bugs early:

🧪 Unit tests (70%): Componentes aislados

🔗 Integration tests (20%): Módulos conectados

🎭 E2E tests (10%): Flujos usuario completos

📊 Coverage target: >85% código testeado

🎯 Estrategia Testing
Pirámide de Tests:
text
        /\
       /E2E\      ← 10% (pocos, lentos, críticos)
      /------\
     /  INT  \    ← 20% (medianos, integración módulos)
    /--------\
   /   UNIT   \   ← 70% (muchos, rápidos, aislados)
  /------------\
Filosofía:

Tests rápidos primero (unit)

Tests costosos al mínimo (e2e)

Coverage >85% en módulos críticos

CI/CD ejecuta automáticamente

📁 Estructura
text
src/tests/
│
├── __init__.py
├── conftest.py              # Fixtures globales
├── pytest.ini               # Config pytest
│
├── fixtures/                # Fixtures compartidos
│   ├── database_fixtures.py
│   ├── user_fixtures.py
│   ├── telegram_fixtures.py
│   └── datetime_fixtures.py
│
├── unit/                    # Tests unitarios (70%)
│   ├── test_config/
│   ├── test_database/
│   ├── test_models/
│   ├── test_adapters/
│   ├── test_agents/
│   ├── test_core/
│   ├── test_utils/
│   ├── test_ml/           # (H06)
│   └── test_services/      # (H04-H05)
│
├── integration/             # Tests integración (20%)
│   ├── test_telegram_flow.py
│   ├── test_database_flow.py
│   ├── test_agent_flow.py
│   └── test_core_agents.py
│
└── e2e/                     # Tests end-to-end (10%)
    ├── test_user_journey/
    └── test_telegram_bot_complete.py
Ver STRUCTURE.md para detalles completos.

🚀 Quick Start
Ejecutar todos los tests:
bash
# Desde raíz proyecto
pytest src/tests/ -v

# Con coverage
pytest src/tests/ --cov=src --cov-report=html

# Ver reporte HTML
open htmlcov/index.html
Ejecutar por tipo:
bash
# Solo unit tests (rápido)
pytest src/tests/unit/ -v

# Solo integration tests
pytest src/tests/integration/ -v

# Solo e2e tests (lento)
pytest src/tests/e2e/ -v
Ejecutar por módulo:
bash
# Solo tests database
pytest src/tests/unit/test_database/ -v

# Solo tests agents
pytest src/tests/unit/test_agents/ -v

# Solo tests utils
pytest src/tests/unit/test_utils/ -v
Ejecutar por marker:
bash
# Solo tests marcados como @pytest.mark.unit
pytest -m unit -v

# Solo tests database
pytest -m database -v

# Excluir tests lentos
pytest -m "not slow" -v
🧪 Escribir Tests
Unit Test Example:
python
# tests/unit/test_utils/test_datetime_utils.py
import pytest
from datetime import datetime, timedelta
from src.utils.datetime_utils import parse_datetime

def test_parse_datetime_tomorrow():
    """Parsea 'mañana 15:00'"""
    dt = parse_datetime("mañana 15:00")
    tomorrow = datetime.now() + timedelta(days=1)
    
    assert dt.day == tomorrow.day
    assert dt.hour == 15
    assert dt.minute == 0

def test_parse_datetime_invalid():
    """Input inválido debe lanzar ValueError"""
    with pytest.raises(ValueError):
        parse_datetime("invalid text")
Integration Test Example:
python
# tests/integration/test_agent_flow.py
import pytest
from src.agents import ReminderAgent
from src.database.repositories import ReminderRepository

@pytest.mark.asyncio
async def test_reminder_agent_full_flow(db_session, test_user):
    """Test completo: create → read → update → delete"""
    repo = ReminderRepository(db_session)
    agent = ReminderAgent(user=test_user, reminder_repo=repo)
    
    # Create
    reminder = await agent.create_reminder(
        title="Test",
        reminder_datetime=datetime.now() + timedelta(hours=1)
    )
    assert reminder.id is not None
    
    # Read
    reminders = await agent.get_reminders()
    assert len(reminders) == 1
    
    # Update
    await agent.update_reminder(reminder.id, title="Updated")
    updated = await agent.get_reminder(reminder.id)
    assert updated.title == "Updated"
    
    # Delete
    await agent.delete_reminder(reminder.id)
    reminders = await agent.get_reminders()
    assert len(reminders) == 0
E2E Test Example:
python
# tests/e2e/test_reminder_lifecycle.py
@pytest.mark.asyncio
async def test_user_creates_and_completes_reminder(telegram_client):
    """Flujo completo usuario: crear → ver → completar reminder"""
    
    # Usuario envía mensaje
    await telegram_client.send_message("Recuérdame reunión mañana 15:00")
    
    # Bot responde con confirmación
    response = await telegram_client.get_last_message()
    assert "✅ Recordatorio creado" in response.text
    
    # Usuario consulta reminders
    await telegram_client.send_message("Ver mis recordatorios")
    
    response = await telegram_client.get_last_message()
    assert "📅 Reunión" in response.text
    assert "Mañana 15:00" in response.text
    
    # Usuario completa reminder
    await telegram_client.click_button("Completar")
    
    response = await telegram_client.get_last_message()
    assert "✅ Completado" in response.text
📦 Fixtures
Fixtures Globales (conftest.py):
python
# src/tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

@pytest.fixture
async def db_session():
    """Database session para tests"""
    engine = create_async_engine("postgresql+asyncpg://test:test@localhost:5432/test_db")
    async with AsyncSession(engine) as session:
        yield session
        await session.rollback()
    await engine.dispose()

@pytest.fixture
def test_user():
    """Usuario de prueba"""
    from src.database.models import User
    return User(
        id=1,
        telegram_user_id=123456,
        username="test_user",
        first_name="Test",
        subscription_tier="free"
    )

@pytest.fixture
def mock_telegram_bot():
    """Mock Telegram Bot"""
    from unittest.mock import MagicMock
    return MagicMock()
Ver fixtures/ para todos los fixtures disponibles.

🎯 Coverage Targets
Módulo	Unit	Integration	E2E	Total
config/	>95%	-	-	>95%
database/	>90%	>80%	-	>85%
models/	>95%	-	-	>95%
adapters/	>85%	>80%	>70%	>80%
agents/	>85%	>80%	>70%	>85%
core/	>80%	>85%	>70%	>80%
utils/	>95%	-	-	>95%
TOTAL	>90%	>80%	>70%	>85%
🔧 Configuración
pytest.ini:
text
[pytest]
testpaths = src/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

markers =
    unit: Unit tests (fast, isolated)
    integration: Integration tests (medium speed)
    e2e: End-to-end tests (slow, full flow)
    slow: Slow tests (skip in CI fast mode)
    database: Tests requiring database
    telegram: Tests with Telegram mock
    ml: ML/NLP tests (H06+)
    payment: Payment tests (H05+)

addopts =
    -v
    --strict-markers
    --cov=src
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=85
🚀 CI/CD Integration
Tests se ejecutan automáticamente en:

GitHub Actions:
text
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: pip install -r requirements.txt
      
      - name: Run tests
        run: pytest src/tests/ --cov=src --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
📊 Reportes
Coverage HTML:
bash
pytest --cov=src --cov-report=html
open htmlcov/index.html
JUnit XML (para CI):
bash
pytest --junitxml=junit.xml
Coverage badge:
codecov

🎯 Testing por Hito
H02 (12-16 Nov):
bash
# Tests críticos MVP
pytest src/tests/unit/test_config/ -v
pytest src/tests/unit/test_database/ -v
pytest src/tests/unit/test_models/ -v
pytest src/tests/unit/test_utils/ -v
pytest src/tests/unit/test_adapters/ -v
pytest src/tests/unit/test_agents/ -v
H07 (27 Nov - 01 Dic):
bash
# Integration + E2E completos
pytest src/tests/integration/ -v
pytest src/tests/e2e/ -v
🆘 Troubleshooting
Tests fallan por database:
bash
# Verificar PostgreSQL corriendo
docker ps | grep postgres

# Crear database test
docker exec -it postgres psql -U postgres
CREATE DATABASE test_thea_ia;
Import errors:
bash
# Verificar PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

# O usar editable install
pip install -e .
Tests lentos:
bash
# Ejecutar en paralelo
pytest -n auto  # Requiere pytest-xdist

# Skip tests lentos
pytest -m "not slow"
📚 Recursos
pytest Docs

pytest-asyncio

Coverage.py

📝 Guías Adicionales
TESTING_GUIDE.md - Guía completa cómo escribir tests

unit/README.md - Guía unit tests

integration/README.md - Guía integration tests

e2e/README.md - Guía e2e tests

Versión: 0.1.0
Estado: Planificación (H01)
Implementar en: H02 (unit) + H07 (integration/e2e)
Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota