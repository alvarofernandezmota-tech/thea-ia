integration/ - Integration Tests
Tests de integración (20% de la suite)

📋 Overview
Tests de módulos conectados:

🔗 Múltiples módulos interactuando

🗄️ Database real (test DB)

⏱️ Medianos (~100ms por test)

🎯 Flujos completos de un feature

📁 Tests
text
integration/
├── test_telegram_flow.py      # Telegram → Adapter → Agent → DB
├── test_database_flow.py      # Repository → Model → DB persist
├── test_agent_flow.py         # Agent → Repository CRUD
├── test_adapter_agent.py      # Adapter ↔ Agent communication
├── test_core_agents.py        # CoreManager → Agents routing
└── test_notification_flow.py  # (H05) Notification pipeline
🚀 Quick Start
bash
# Ejecutar integration tests
pytest src/tests/integration/ -v

# Con database
pytest src/tests/integration/ -m database -v

# Skip si no hay DB
pytest src/tests/integration/ -m "not database" -v
💡 Ejemplo
python
# test_agent_flow.py
import pytest
from datetime import datetime, timedelta
from src.agents import ReminderAgent
from src.database.repositories import ReminderRepository

@pytest.mark.asyncio
@pytest.mark.integration
async def test_reminder_agent_full_crud(db_session, test_user):
    """
    Test completo CRUD reminder:
    Agent → Repository → Database
    """
    # Setup
    repo = ReminderRepository(db_session)
    agent = ReminderAgent(user=test_user, reminder_repo=repo)
    
    # CREATE
    reminder = await agent.create_reminder(
        title="Integration Test",
        reminder_datetime=datetime.now() + timedelta(hours=1)
    )
    assert reminder.id is not None
    
    # READ
    fetched = await agent.get_reminder(reminder.id)
    assert fetched.title == "Integration Test"
    
    # READ ALL
    all_reminders = await agent.get_reminders()
    assert len(all_reminders) == 1
    
    # UPDATE
    await agent.update_reminder(reminder.id, title="Updated")
    updated = await agent.get_reminder(reminder.id)
    assert updated.title == "Updated"
    
    # DELETE
    await agent.delete_reminder(reminder.id)
    all_reminders = await agent.get_reminders()
    assert len(all_reminders) == 0
✅ Características
✅ Debe:
Testear integración real entre módulos

Usar database test (no mock)

Verificar persistencia datos

Rollback después de cada test

❌ NO debe:
Depender de servicios externos (mock them)

Tocar production database

Tardar >1 segundo por test

Tener side effects entre tests

🔧 Setup
Database Test:
python
# conftest.py
@pytest.fixture
async def db_session():
    """Test database session con auto-rollback"""
    engine = create_async_engine(
        "postgresql+asyncpg://test:test@localhost:5432/test_thea_ia"
    )
    
    async with AsyncSession(engine) as session:
        # Transaction para rollback
        async with session.begin():
            yield session
            await session.rollback()
    
    await engine.dispose()
🎯 Coverage Target
>80% en integration tests

Foco en:

Flujos críticos (create → read → update → delete)

Comunicación entre capas

Persistencia correcta datos

Error handling entre módulos

📊 Tests por Archivo
test_telegram_flow.py:
Telegram Update → TelegramAdapter

Adapter → CoreManager

CoreManager → Agent apropiado

Agent → Database

Response back to Telegram

test_database_flow.py:
Repository CRUD operations

Model validations

Constraints (unique, foreign keys)

Transactions

test_agent_flow.py:
Agent methods completos

Repository integration

Business logic con DB

test_adapter_agent.py:
Message normalization

Agent selection

Response formatting

test_core_agents.py:
Router logic

Multiple agents

Context management

📚 Por Implementar
H07 (27 Nov - 01 Dic)

Orden implementación:

test_database_flow.py (base)

test_agent_flow.py (agents con DB)

test_adapter_agent.py (adapters)

test_core_agents.py (routing)

test_telegram_flow.py (completo)

Implementar en: H07 (27 Nov - 01 Dic)
Última actualización: 11 Nov 2025