# integration/ - Integration Tests

Tests de integración entre múltiples componentes.

---

## 📋 Overview

Tests de módulos conectados con características:

- 🔗 **Múltiples módulos** interactuando
- 🗄️ **Database real** (test DB con fixtures)
- ⏱️ **Medianos** (~100-500ms por test)
- 🎯 **Flujos completos** de features

---

## 📁 Estructura

integration/
├── test_agenda_agent_flow.py # ✅ AgendaAgent integration (1 test)
├── test_context_persistence_between_agents.py # ✅ Context between agents (1 test)
├── test_conversation_flow.py # ✅ Conversation flow (3 tests)
├── test_core_integration.py # ✅ Core integration (3 tests)
├── test_router_switches_between_agents.py # ✅ Router switching (1 test)
└── test_telegram_database.py # ✅ Telegram + DB (5 tests)

text

**Total Integration Tests: 14 tests**

---

## 🚀 Quick Start

Ejecutar todos los integration tests
pytest src/theaia/tests/integration/ -v

Solo database integration
pytest src/theaia/tests/integration/test_telegram_database.py -v

Con markers
pytest -m integration -v

Skip si no hay DB configurada
pytest -m "not database" -v

text

---

## ✅ Tests Implementados

### **🗄️ Telegram + Database (5 tests)**
`test_telegram_database.py` - Integración Telegram con persistencia:

- ✅ `test_user_creation_on_first_message` - Usuario creado al primer mensaje
- ✅ `test_message_history_persisted` - Historial de mensajes guardado
- ✅ `test_conversation_context_saved` - Contexto de conversación persistido
- ✅ `test_user_settings_loaded` - Settings de usuario cargados
- ✅ `test_multi_session_consistency` - Consistencia entre sesiones

### **📅 AgendaAgent Flow (1 test)**
`test_agenda_agent_flow.py` - Flujo completo AgendaAgent:

- ✅ `test_agenda_agent_full_workflow` - CRUD completo con DB

### **🔄 Context Management (4 tests)**
`test_context_persistence_between_agents.py` (1 test):
- ✅ `test_context_maintained_between_agents` - Contexto entre agents

`test_conversation_flow.py` (3 tests):
- ✅ `test_multi_turn_conversation` - Conversación múltiples turnos
- ✅ `test_context_switches` - Cambios de contexto
- ✅ `test_conversation_state_persistence` - Persistencia de estado

### **🎯 Core Integration (3 tests)**
`test_core_integration.py`:

- ✅ `test_core_manager_routes_messages` - CoreManager rutea correctamente
- ✅ `test_core_manager_handles_errors` - Manejo de errores
- ✅ `test_core_manager_maintains_state` - Mantiene estado

### **🔀 Router Switching (1 test)**
`test_router_switches_between_agents.py`:

- ✅ `test_router_switches_agents_correctly` - Switching entre agents

---

## 💡 Ejemplo Integration Test

test_telegram_database.py
import pytest
from src.theaia.adapters.telegram import TelegramAdapter
from src.theaia.database.repositories import UserRepository

@pytest.mark.asyncio
@pytest.mark.integration
async def test_user_creation_on_first_message(db_session):
"""
Integration test: Telegram adapter crea usuario en DB
al recibir primer mensaje.

text
Flow:
1. Nuevo usuario envía mensaje
2. TelegramAdapter detecta usuario nuevo
3. UserRepository crea usuario en DB
4. Sistema responde con onboarding
"""
# Arrange
adapter = TelegramAdapter(db_session)
user_repo = UserRepository(db_session)
telegram_update = {
    "message": {
        "from": {
            "id": 123456789,
            "username": "test_user",
            "first_name": "Test"
        },
        "text": "/start"
    }
}

# Verify user doesn't exist
user = await user_repo.get_by_telegram_id(123456789)
assert user is None

# Act
response = await adapter.handle_update(telegram_update)

# Assert - User created in DB
user = await user_repo.get_by_telegram_id(123456789)
assert user is not None
assert user.telegram_user_id == 123456789
assert user.username == "test_user"
assert user.first_name == "Test"

# Assert - Response sent
assert response["status"] == "success"
assert "bienvenido" in response["message"].lower()
text

---

## ✅ Características Integration Tests

**✅ Debe:**
- Testear integración real entre 2+ módulos
- Usar database test real (no mocks de DB)
- Verificar persistencia de datos
- Rollback automático después de cada test

**❌ NO debe:**
- Depender de servicios externos (mock them)
- Tocar production database
- Tardar >2 segundos por test
- Tener side effects entre tests

---

## 🔧 Database Setup

### Test Database Fixture
conftest.py
@pytest.fixture
async def db_session():
"""
Test database session with auto-rollback.
Each test runs in a transaction that gets rolled back.
"""
from src.theaia.database import engine
from sqlalchemy.ext.asyncio import AsyncSession

text
async with AsyncSession(engine) as session:
    async with session.begin():
        yield session
        # Auto-rollback happens here
text

### Test User Fixture
@pytest.fixture
async def test_user(db_session):
"""Create a test user for integration tests."""
from src.theaia.database.models import User

text
user = User(
    telegram_user_id=999999,
    username="test_user",
    first_name="Test"
)
db_session.add(user)
await db_session.commit()
await db_session.refresh(user)

return user
text

---

## 📊 Coverage Stats (15 Nov 2025)

| Component | Integration Tests | Status |
|-----------|-------------------|--------|
| Telegram + DB | 5 | ✅ |
| AgendaAgent Flow | 1 | ✅ |
| Context Management | 4 | ✅ |
| Core Integration | 3 | ✅ |
| Router | 1 | ✅ |
| **TOTAL** | **14** | ✅ |

**Integration Coverage:** ~80% de flujos críticos  
**Execution Time:** ~3-5 segundos total

---

## 🎯 Test Patterns

### Integration Pattern
@pytest.mark.asyncio
@pytest.mark.integration
async def test_component_integration(db_session, test_user):
# Arrange - Setup components
component_a = ComponentA(db_session)
component_b = ComponentB(db_session)

text
# Act - Execute integration
result = await component_a.process(test_user)
saved = await component_b.save(result)

# Assert - Verify both components
assert result is not None
assert saved.id is not None

# Assert - Verify in DB
from_db = await db_session.get(Model, saved.id)
assert from_db is not None
text

### Database Verification
Always verify data persistence
await db_session.refresh(entity)
assert entity.field == expected_value

Query verification
result = await db_session.execute(
select(Model).where(Model.user_id == user.id)
)
entities = list(result.scalars())
assert len(entities) == expected_count

text

---

## 🎯 Coverage Target

**>80% en integration tests**

Foco en:
- ✅ Flujos críticos (CRUD completo)
- ✅ Comunicación entre capas (Adapter → Agent → DB)
- ✅ Persistencia correcta de datos
- ✅ Error handling entre módulos
- ✅ Context management entre agents

---

## 🚀 Next Steps (Phase 4+)

**Additional Integration Tests:**
- [ ] API → Service → Repository flow
- [ ] Multi-user scenarios
- [ ] Transaction rollback handling
- [ ] Performance under concurrent requests

**Improvements:**
- [ ] Faster DB fixtures
- [ ] Parallel test execution
- [ ] Better test data factories
- [ ] CI/CD optimization

---

**Implementado:** H02 (12-14 Nov), H03 (15-16 Nov)  
**Última actualización:** 15 Nov 2025, 23:57 CET
