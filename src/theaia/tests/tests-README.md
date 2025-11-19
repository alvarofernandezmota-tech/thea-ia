# tests/ - Testing Suite

Suite completa de tests para THEA_IA - 173 tests implementados.

---

## 📋 Overview

Tests automatizados para garantizar calidad del código:

- 🧪 **Unit tests (45%)**: 77 tests - componentes aislados
- 🔗 **Integration tests (8%)**: 14 tests - módulos conectados
- 🎭 **E2E tests (29%)**: 50 tests - flujos completos
- 📱 **Adapter tests (6%)**: 10 tests - Telegram adapter
- 🎯 **Core tests (12%)**: 22 tests - FSM, router, context

**Current Stats (16 Nov 2025):**
- ✅ **173 tests total** (100% passing)
- ✅ **50% code coverage** (target reached!)
- ⚡ **~8 seconds** execution time
- 🏆 **0 failures, 0 skips**

---

## 🎯 Test Strategy

### Test Pyramid
text
    /\
   /E2E\      ← 29% (50 tests - flujos críticos)
  /------\
 /  INT  \    ← 8% (14 tests - integración)
/--------\
/ ADAPT+ \ ← 18% (32 tests - core+adapters)
/ UNIT \ ← 45% (77 tests - aislados)
/--------------\

text

**Philosophy:**
- ✅ Fast tests first (unit)
- ✅ Integration where needed
- ✅ E2E for critical paths
- ✅ >50% coverage on core modules

---

## 📁 Structure

src/theaia/tests/
│
├── conftest.py # Global fixtures
├── pytest.ini # Pytest config
│
├── unit/ # ✅ 77 tests (45%)
│ ├── test_agent_config.py # 15 tests
│ ├── test_base_agent.py # 15 tests
│ ├── test_date_parser.py # 15 tests
│ ├── test_entity_extraction.py # 18 tests
│ ├── test_fsm_specials.py # 3 tests
│ ├── test_router.py # 4 tests
│ ├── test_state_machine.py # 6 tests
│ └── test_context_persistence.py # 1 test
│
├── e2e/ # ✅ 50 tests (29%)
│ ├── test_agenda_agent_e2e.py # 17 tests
│ ├── test_note_agent_e2e.py # 14 tests
│ ├── test_reminder_agent_e2e.py # 15 tests
│ ├── test_context_flow.py # 1 test
│ ├── test_core_flow.py # 1 test
│ ├── test_fsm_disambiguation.py # 1 test
│ └── test_notas_flow.py # 1 test
│
├── integration/ # ✅ 14 tests (8%)
│ ├── test_agenda_agent_flow.py # 1 test
│ ├── test_context_persistence_between_agents.py # 1 test
│ ├── test_conversation_flow.py # 3 tests
│ ├── test_core_integration.py # 3 tests
│ ├── test_router_switches_between_agents.py # 1 test
│ └── test_telegram_database.py # 5 tests
│
├── adapters/ # ✅ 10 tests (6%)
│ └── test_telegram_adapter.py # 10 tests
│
└── core/ # ✅ 22 tests (12%)
├── test_bot_factory.py # 2 tests
├── test_callbacks.py # 9 tests
├── test_context.py # 3 tests
├── test_context_manager.py # 3 tests
├── test_router.py # 1 test
└── test_state_machine.py # 4 tests

text

---

## 🚀 Quick Start

### Run All Tests
All tests
pytest src/theaia/tests/ -v

With coverage
pytest src/theaia/tests/ --cov=src/theaia --cov-report=html

Quick summary
pytest src/theaia/tests/ -q

text

### Run by Type
Unit tests only (fast - 77 tests)
pytest src/theaia/tests/unit/ -v

E2E tests only (comprehensive - 50 tests)
pytest src/theaia/tests/e2e/ -v

Integration tests only (14 tests)
pytest src/theaia/tests/integration/ -v

Adapter tests only (10 tests)
pytest src/theaia/tests/adapters/ -v

Core tests only (22 tests)
pytest src/theaia/tests/core/ -v

text

### Run by Component
Agent tests
pytest src/theaia/tests/unit/test_agent_config.py -v
pytest src/theaia/tests/unit/test_base_agent.py -v

Entity extraction tests
pytest src/theaia/tests/unit/test_date_parser.py -v
pytest src/theaia/tests/unit/test_entity_extraction.py -v

Agent E2E tests
pytest src/theaia/tests/e2e/test_agenda_agent_e2e.py -v
pytest src/theaia/tests/e2e/test_note_agent_e2e.py -v
pytest src/theaia/tests/e2e/test_reminder_agent_e2e.py -v

text

---

## 📊 Coverage Stats (16 Nov 2025)

### Overall Coverage: 50%

| Module | Coverage | Priority |
|--------|----------|----------|
| **Agents** |
| `agent_config.py` | 100% | ⭐⭐⭐ |
| `base_agent.py` | 93% | ⭐⭐⭐ |
| **Entity Extraction** |
| `location_extractor.py` | 100% | ⭐⭐⭐ |
| `person_name_extractor.py` | 98% | ⭐⭐⭐ |
| `date_parser.py` | 91% | ⭐⭐⭐ |
| **Core** |
| `callbacks.py` | 100% | ⭐⭐ |
| `state_machine.py` | 89% | ⭐⭐⭐ |
| `router.py` | 82% | ⭐⭐ |
| **Adapters** |
| `telegram_adapter.py` | 39% | ⭐ |

### Test Distribution
- Unit: 77 tests (45%)
- E2E: 50 tests (29%)
- Core: 22 tests (12%)
- Integration: 14 tests (8%)
- Adapters: 10 tests (6%)

---

## 🧪 Test Examples

### Unit Test
test_agent_config.py
def test_create_config():
"""Test creating agent config."""
config = AgentConfig(
name="TestAgent",
supported_intents=["test"],
requires_database=True
)

text
assert config.name == "TestAgent"
assert "test" in config.supported_intents
assert config.requires_database is True
text

### E2E Test
test_agenda_agent_e2e.py
@pytest.mark.asyncio
async def test_create_event_with_time(db_session, mock_user):
"""E2E: Usuario crea evento con fecha y hora."""
handler = AgendaAgentHandler(db_session)

text
response = await handler.handle_message(
    user_id=mock_user.id,
    message="Reunión con cliente mañana 15:00"
)

assert response["status"] == "success"
assert "evento creado" in response["message"].lower()

# Verify in database
events = await db_session.execute(
    select(Event).where(Event.user_id == mock_user.id)
)
assert len(list(events.scalars())) == 1
text

### Integration Test
test_telegram_database.py
@pytest.mark.asyncio
async def test_user_creation_on_first_message(db_session):
"""Integration: Telegram adapter crea usuario en DB."""
adapter = TelegramAdapter(db_session)
telegram_update = create_mock_update("/start", user_id=123)

text
response = await adapter.handle_update(telegram_update)

# Verify user created
user = await user_repo.get_by_telegram_id(123)
assert user is not None
assert user.telegram_user_id == 123
text

---

## 🎯 Test Markers

Run specific markers
pytest -m unit # Unit tests
pytest -m e2e # E2E tests
pytest -m integration # Integration tests
pytest -m slow # Slow tests
pytest -m database # Database tests

Exclude markers
pytest -m "not slow" # Skip slow tests
pytest -m "not database" # Skip DB tests

text

---

## 🔧 Configuration

### pytest.ini
[pytest]
testpaths = src/theaia/tests
python_files = test_.py
python_classes = Test
python_functions = test_*

markers =
unit: Unit tests
integration: Integration tests
e2e: End-to-end tests
slow: Slow tests
database: Database tests

addopts =
-v
--strict-markers
--cov=src/theaia
--cov-report=term-missing

text

---

## 📦 Key Fixtures

### Database
@pytest.fixture
async def db_session():
"""Test database session with auto-rollback."""
async with AsyncSession(engine) as session:
async with session.begin():
yield session

text

### Mock User
@pytest.fixture
async def mock_user(db_session):
"""Create test user."""
user = User(
telegram_user_id=999999,
username="test_user"
)
db_session.add(user)
await db_session.commit()
return user

text

---

## 🎯 Phase 3 Achievements

**Completed (15-16 Nov 2025):**
- ✅ AgentConfig tests (15 tests, 100% coverage)
- ✅ BaseAgent tests (15 tests, 93% coverage)
- ✅ Entity extraction tests (48 tests, 96% avg coverage)
  - DateTimeExtractor (15 tests, 91%)
  - LocationExtractor (18 tests, 100%)
  - PersonNameExtractor (18 tests, 98%)
- ✅ AgendaAgent E2E (17 tests)
- ✅ NoteAgent E2E (14 tests)
- ✅ ReminderAgent E2E (15 tests)

**Results:**
- 173 tests total (+86 since Phase 2)
- 50% coverage (target reached!)
- 0 failures, 0 skips
- ~8 seconds execution time

---

## 📚 Documentation

- `unit/README.md` - Unit tests guide
- `e2e/README.md` - E2E tests guide
- `integration/README.md` - Integration tests guide
- `adapters/README.md` - Adapter tests guide
- `core/README.md` - Core tests guide
- `docs/testing/` - Complete testing documentation

---

## 🆘 Troubleshooting

### Tests fail with DB errors
Check PostgreSQL running
docker ps | grep postgres

Verify test DB exists
docker exec -it postgres psql -U postgres -c "\l"

text

### Import errors
Install in editable mode
pip install -e .

Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

text

### Slow tests
Run in parallel
pytest -n auto # requires pytest-xdist

Skip slow tests
pytest -m "not slow"

text

---

## 🎯 Next Steps (Phase 4+)

**Additional Tests:**
- [ ] API endpoint tests
- [ ] Service layer tests
- [ ] Performance tests
- [ ] Load tests
- [ ] Security tests

**Improvements:**
- [ ] Increase coverage to 60%+
- [ ] Add mutation testing
- [ ] Performance benchmarks
- [ ] Visual regression tests

---

**Version:** 0.2.0  
**Status:** ✅ Phase 3 Complete (16 Nov 2025)  
**Next Phase:** Phase 4 - Deployment & Production  
**Last Updated:** 16 Nov 2025, 00:07 CET  
**Maintainer:** Álvaro Fernández Mota