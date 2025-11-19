Testing Suite – THEA-IA Complete (H02 Database + Full Stack)
Visión General
THEA-IA tiene una suite de testing multinivel: desde tests unitarios de componentes aislados hasta E2E completos, pasando por tests exhaustivos de persistencia.

Status Actual (19 Nov 2025):

✅ 173 tests total (100% passing)

✅ 50% code coverage (target reached)

✅ H02 Database tests: 13/13 PASAN (UserRepository 100%)

⚡ ~8 seconds execution time

🏆 0 failures, 0 skips

📊 Test Distribution
text
THEA-IA Testing Pyramid (173 tests total)

         /\
        /E2E\         ← 50 tests (29%)
       /------\
      / INT   \       ← 14 tests (8%)
     /--------\
    / CORE    \       ← 22 tests (12%)
   /-----------\
  / ADAPTER    \      ← 10 tests (6%)
 /             \
/ UNIT (CORE)  \      ← 77 tests (45%)
/_______________\

NEW LAYER (H02):
┌─────────────────────────────────────┐
│ DATABASE REPOSITORY TESTS           │
│ ✅ UserRepository:      13 tests    │
│ ⏳ EventRepository:      ~ 10 tests │
│ ⏳ NoteRepository:       ~ 10 tests │
│ ⏳ ConversationRepository: ~ 10 tests│
│ ⏳ MessageHistoryRepository: ~ 12 tests│
│ ────────────────────────────────────│
│ Subtotal H02:          ~55 tests    │
│ (En progreso)                       │
└─────────────────────────────────────┘
📁 Estructura Completa de Tests
text
src/theaia/tests/
│
├── conftest.py                  # Global fixtures (todos los tests)
├── pytest.ini                   # Pytest config
│
├── database/                    # 🆕 H02 - Advanced Persistence
│ └── repositories/
│     ├── conftest.py            # Fixtures DB (engine por test, timezone-aware)
│     ├── test_user_repository.py # 13 tests ✅ PASAN
│     ├── test_event_repository.py # (planned)
│     ├── test_note_repository.py  # (planned)
│     ├── test_conversation_repository.py # (planned)
│     └── test_message_history_repository.py # (planned)
│
├── unit/                        # 77 tests (45%) - Componentes aislados
│ ├── test_agent_config.py       # 15 tests - AgentConfig
│ ├── test_base_agent.py         # 15 tests - BaseAgent
│ ├── test_date_parser.py        # 15 tests - DateTime parsing
│ ├── test_entity_extraction.py  # 18 tests - Entity extractors
│ ├── test_fsm_specials.py       # 3 tests - FSM edge cases
│ ├── test_router.py             # 4 tests - Router logic
│ ├── test_state_machine.py      # 6 tests - State machine
│ └── test_context_persistence.py # 1 test - Context storage
│
├── e2e/                         # 50 tests (29%) - Flujos completos
│ ├── test_agenda_agent_e2e.py   # 17 tests - Agenda agent flow
│ ├── test_note_agent_e2e.py     # 14 tests - Note agent flow
│ ├── test_reminder_agent_e2e.py # 15 tests - Reminder agent flow
│ ├── test_context_flow.py       # 1 test - Context persistence
│ ├── test_core_flow.py          # 1 test - Core flow
│ ├── test_fsm_disambiguation.py # 1 test - Disambiguation
│ └── test_notas_flow.py         # 1 test - Notes flow
│
├── integration/                 # 14 tests (8%) - Módulos conectados
│ ├── test_agenda_agent_flow.py  # 1 test
│ ├── test_context_persistence_between_agents.py # 1 test
│ ├── test_conversation_flow.py  # 3 tests
│ ├── test_core_integration.py   # 3 tests
│ ├── test_router_switches_between_agents.py # 1 test
│ └── test_telegram_database.py  # 5 tests - Database integration
│
├── adapters/                    # 10 tests (6%) - External integrations
│ └── test_telegram_adapter.py   # 10 tests - Telegram adapter
│
└── core/                        # 22 tests (12%) - Core infrastructure
    ├── test_bot_factory.py      # 2 tests
    ├── test_callbacks.py        # 9 tests
    ├── test_context.py          # 3 tests
    ├── test_context_manager.py  # 3 tests
    ├── test_router.py           # 1 test
    └── test_state_machine.py    # 4 tests
🚀 Quick Start – Ejecutar Tests
Todos los tests
bash
# Todos los tests con output verbose
pytest src/theaia/tests/ -v

# Con coverage report
pytest src/theaia/tests/ --cov=src/theaia --cov-report=html

# Resumen rápido
pytest src/theaia/tests/ -q
H02 Database Tests específicamente
bash
# TODOS los repository tests
pytest src/theaia/tests/database/repositories/ -v

# UserRepository solo (13 tests)
pytest src/theaia/tests/database/repositories/test_user_repository.py -v

# Con coverage
pytest src/theaia/tests/database/repositories/test_user_repository.py -v --cov=src/theaia/database/repositories --cov-report=term-missing
Por categoría (legacy tests)
bash
# Unit tests (77 tests - rápidos)
pytest src/theaia/tests/unit/ -v

# E2E tests (50 tests - comprensivos)
pytest src/theaia/tests/e2e/ -v

# Integration tests (14 tests)
pytest src/theaia/tests/integration/ -v

# Adapter tests (10 tests)
pytest src/theaia/tests/adapters/ -v

# Core tests (22 tests)
pytest src/theaia/tests/core/ -v
Por componente específico
bash
# Agent tests
pytest src/theaia/tests/unit/test_agent_config.py -v
pytest src/theaia/tests/unit/test_base_agent.py -v

# Entity extraction
pytest src/theaia/tests/unit/test_date_parser.py -v
pytest src/theaia/tests/unit/test_entity_extraction.py -v

# Database + integration
pytest src/theaia/tests/database/ -v
pytest src/theaia/tests/integration/test_telegram_database.py -v
📊 Coverage Stats
Overall Coverage: 50% (Target Reached)
Module	Coverage	Status	Priority
H02 Database			
UserRepository	71%	✅ TESTEADO	⭐⭐⭐
BaseRepository	76%	✅ TESTEADO	⭐⭐⭐
Agents			
agent_config.py	100%	✅	⭐⭐⭐
base_agent.py	93%	✅	⭐⭐⭐
Entity Extraction			
location_extractor.py	100%	✅	⭐⭐⭐
person_name_extractor.py	98%	✅	⭐⭐⭐
date_parser.py	91%	✅	⭐⭐⭐
Core			
callbacks.py	100%	✅	⭐⭐
state_machine.py	89%	✅	⭐⭐⭐
router.py	82%	✅	⭐⭐
Adapters			
telegram_adapter.py	39%	⏳	⭐
Test Distribution
Database (H02): 13 tests (8% del total nuevo)

Unit: 77 tests (45%)

E2E: 50 tests (29%)

Core: 22 tests (12%)

Integration: 14 tests (8%)

Adapters: 10 tests (6%)

🧪 Test Examples
H02: Unit Test – Repository
python
# src/theaia/tests/database/repositories/test_user_repository.py

@pytest.mark.asyncio
async def test_create_user_basic(self, db_session, test_user_data):
    """Crear usuario básico con todos los campos."""
    repo = UserRepository(db_session)
    
    user = await repo.create(**test_user_data)
    
    # Validaciones
    assert user.id is not None
    assert user.telegram_id == test_user_data["telegram_id"]
    assert user.tenant_id == test_user_data["tenant_id"]
    assert user.created_at is not None
    assert user.created_at.tzinfo is not None  # ✅ Timezone-aware
H02: Multi-tenant Isolation Test
python
@pytest.mark.asyncio
async def test_users_isolated_by_tenant(self, db_session, test_user_data):
    """Usuarios de diferentes tenants NO se cruzan."""
    repo = UserRepository(db_session)
    
    # Crear usuario en tenant_1
    user_1 = await repo.create(**{
        **test_user_data, 
        "tenant_id": "tenant_1"
    })
    
    # Crear usuario en tenant_2 (MISMO telegram_id)
    user_2 = await repo.create(**{
        **test_user_data, 
        "tenant_id": "tenant_2"
    })
    
    # Validar aislamiento
    assert user_1.id != user_2.id  # Usuarios diferentes
    assert user_1.tenant_id == "tenant_1"
    assert user_2.tenant_id == "tenant_2"
    
    # Verificar que queries respetan tenant_id
    retrieved_1 = await repo.get_by_telegram_id(
        test_user_data["telegram_id"],
        "tenant_1"
    )
    assert retrieved_1.id == user_1.id  # Solo retorna user_1
H02: Timezone-aware Test
python
@pytest.mark.asyncio
async def test_update_last_activity(self, db_session, test_user_data):
    """Última actividad con timezone-aware timestamps."""
    repo = UserRepository(db_session)
    user = await repo.create(**test_user_data)
    
    # Actualizar última actividad
    updated = await repo.update_last_activity(user.id)
    
    # Validaciones
    assert updated.last_activity is not None
    assert updated.last_activity > user.created_at  # ✅ Comparación funciona
    assert updated.last_activity.tzinfo is not None  # ✅ Timezone-aware
    assert str(updated.last_activity.tzinfo) == "UTC"  # UTC explícito
Legacy: Unit Test – Agent Config
python
def test_create_config():
    """Test creating agent config."""
    config = AgentConfig(
        name="TestAgent",
        supported_intents=["test"],
        requires_database=True
    )
    
    assert config.name == "TestAgent"
    assert "test" in config.supported_intents
    assert config.requires_database is True
Legacy: E2E Test – Agenda Agent
python
@pytest.mark.asyncio
async def test_create_event_with_time(db_session, mock_user):
    """E2E: Usuario crea evento con fecha y hora."""
    handler = AgendaAgentHandler(db_session)
    
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
Legacy: Integration Test – Telegram Database
python
@pytest.mark.asyncio
async def test_user_creation_on_first_message(db_session):
    """Integration: Telegram adapter crea usuario en DB."""
    adapter = TelegramAdapter(db_session)
    telegram_update = create_mock_update("/start", user_id=123)
    
    response = await adapter.handle_update(telegram_update)
    
    # Verify user created in database
    user = await user_repo.get_by_telegram_id(123, "default")
    assert user is not None
    assert user.telegram_id == "123"
🔧 Fixtures Clave
H02: Database Session Fixture (Engine per test)
python
# src/theaia/tests/database/repositories/conftest.py

@pytest_asyncio.fixture
async def db_session():
    """
    Fixture que proporciona sesión limpia por test.
    
    WINDOWS FIX CRÍTICO:
    - Crea engine NUEVO por test
    - Cada test obtiene su propio pool
    - Evita event loop mismatch en asyncpg
    """
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    
    test_engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        pool_pre_ping=False,  # Deshabilitado en tests (Windows compatibility)
        pool_size=1,
        max_overflow=0,
    )
    
    TestSessionLocal = async_sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()
    
    await test_engine.dispose()
Global Database Fixture (Legacy)
python
@pytest.fixture
async def db_session():
    """Test database session with auto-rollback."""
    async with AsyncSession(engine) as session:
        async with session.begin():
            yield session
Mock User Fixture
python
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
Test Data Fixtures (H02)
python
@pytest.fixture
def test_tenant_id() -> str:
    return "test_tenant_001"

@pytest.fixture
def test_user_data(test_tenant_id: str) -> dict:
    return {
        "tenant_id": test_tenant_id,
        "telegram_id": 123456789,
        "username": "test_user",
        "first_name": "Test",
        "last_name": "User",
        "language_code": "es",
    }
🎯 Test Markers
bash
# Run specific markers
pytest -m unit                  # Unit tests
pytest -m e2e                   # E2E tests
pytest -m integration           # Integration tests
pytest -m slow                  # Slow tests
pytest -m database              # Database tests

# Exclude markers
pytest -m "not slow"            # Skip slow tests
pytest -m "not database"        # Skip DB tests
📋 pytest.ini Configuration
text
[pytest]
testpaths = src/theaia/tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Asyncio mode for pytest-asyncio
asyncio_mode = strict

# Markers
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
    database: Database tests
    asyncio: Asyncio tests

# Coverage
addopts =
    -ra -q --strict-markers
    --cov=src/theaia
    --cov-report=term-missing

# Logging
log_cli = false
log_cli_level = INFO
📊 H02 Testing Strategy – Database Layer
Test Pyramid for Repositories
text
       /\
      /E2E\         ← API endpoint tests (future)
     /------\
    / INT   \       ← Cross-repo integration tests
   /--------\
  / UNIT    \       ← Individual repository CRUD tests
 /___________\

CURRENT H02 STATUS:
- ✅ UserRepository: 13/13 tests PASAN (UNIT + basic INT)
- ⏳ EventRepository: Pending (template ready)
- ⏳ NoteRepository: Pending
- ⏳ ConversationRepository: Pending
- ⏳ MessageHistoryRepository: Pending
Coverage Targets for H02
Repository	Tests	Coverage Target	Status
BaseRepository	8	75%	✅ 76%
UserRepository	13	70%	✅ 71%
EventRepository	10	70%	⏳ Pending
NoteRepository	10	70%	⏳ Pending
ConversationRepository	10	70%	⏳ Pending
MessageHistoryRepository	12	70%	⏳ Pending
🎯 Phase Achievements
Phase 3 (15-16 Nov 2025) – Full Stack Testing
✅ AgentConfig tests (15 tests, 100% coverage)

✅ BaseAgent tests (15 tests, 93% coverage)

✅ Entity extraction tests (48 tests, 96% avg)

✅ E2E agent flows (46 tests)

✅ Total: 173 tests, 50% coverage

Phase 2 (Today – 19 Nov 2025) – H02 Database Layer
✅ BaseModel design (timezone-aware, multi-tenant)

✅ BaseRepository pattern (generic async CRUD)

✅ UserRepository implementation (Telegram integration)

✅ conftest.py Windows fix (engine per test)

✅ 13 UserRepository tests: 13/13 PASAN

✅ Total: 173 + 13 = 186 tests

Phase 4+ (Roadmap)
 EventRepository tests (10 tests, ≥70% coverage)

 NoteRepository tests (10 tests, ≥70% coverage)

 ConversationRepository tests (10 tests, ≥70% coverage)

 MessageHistoryRepository tests (12 tests, ≥70% coverage)

 Cross-repo integration tests

 API endpoint tests (FastAPI integration)

 Performance/load tests

 Target: 60%+ coverage overall

🛠️ Troubleshooting
Tests fail with DB errors
bash
# Check PostgreSQL running
docker ps | grep postgres

# Verify test DB exists
docker exec -it postgres psql -U postgres -c "\l"

# Create test DB if missing
docker exec -it postgres psql -U postgres -c "CREATE DATABASE thea_ia_test;"
Import errors
bash
# Install in editable mode
pip install -e .

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
Slow tests
bash
# Run in parallel (requires pytest-xdist)
pytest -n auto

# Skip slow tests
pytest -m "not slow"
Windows asyncpg event loop errors
bash
# ✅ Already fixed in conftest.py (engine per test)
# If you see: RuntimeError: Task got Future attached to a different loop
# → Check that db_session fixture uses new engine (not global pool)
📚 Documentation Hierarchy
text
tests/README.md (este archivo)
├── database/repositories/README.md (H02 database testing)
├── unit/README.md (unit testing guide)
├── e2e/README.md (E2E testing guide)
├── integration/README.md (integration testing guide)
├── adapters/README.md (adapter testing guide)
└── core/README.md (core infrastructure testing)

+ Top-level docs:
├── src/theaia/database/migrations/README.md (migration justification)
├── src/theaia/database/models/README.md (model design decisions)
├── src/theaia/database/repositories/README.md (repository pattern)
└── src/theaia/tests/database/repositories/README.md (test strategy)
🆘 How to Add New Tests
For H02 Repositories (Database Layer)
Copy template from UserRepository tests

python
# src/theaia/tests/database/repositories/test_event_repository.py

class TestEventRepositoryBasic:
    """CRUD básico"""
    @pytest.mark.asyncio
    async def test_create_event(self, db_session, test_event_data):
        repo = EventRepository(db_session)
        event = await repo.create(**test_event_data)
        assert event.id is not None
Add multi-tenant test

python
@pytest.mark.asyncio
async def test_event_isolation_by_tenant(self, ...):
    """Eventos de diferentes tenants NO se cruzan"""
    # Similar a TestUserRepositoryMultiTenant
Add timezone-aware test

python
@pytest.mark.asyncio
async def test_event_date_timezone_aware(self, ...):
    """event_date es timezone-aware"""
    assert event.event_date.tzinfo is not None
Target: ≥70% coverage

bash
pytest src/theaia/tests/database/repositories/test_event_repository.py \
    --cov=src/theaia/database/repositories/event_repository \
    --cov-report=term-missing
For Legacy Tests (Agents, FSM, etc.)
Follow existing patterns in:

tests/unit/test_agent_config.py

tests/e2e/test_agenda_agent_e2e.py

tests/integration/test_core_integration.py

📈 Metrics & KPIs
Current (19 Nov 2025)
Total tests: 186 (173 legacy + 13 H02)

Pass rate: 100%

Overall coverage: 50%

H02 coverage: 71% (UserRepository), 76% (BaseRepository)

Execution time: ~8 seconds

Target (End of H02)
Total tests: 230+ (186 + 5 repos × 10 tests)

Pass rate: 100%

Overall coverage: 55%+

H02 coverage: ≥70% per repository

Execution time: ~15 seconds (acceptable)

📞 Support & Questions
Database tests stuck? → Check conftest.py fixture (engine per test)

Timezone errors? → Verify DateTime(timezone=True) in models

Multi-tenant leak? → Grep for queries sin tenant_id filter

Windows async error? → Que no sea pool_pre_ping global (solo tests)

Version: 0.3.0 (H02 Integration)
Status: ✅ H02 Phase 1 Complete + Legacy Tests Active
Next: Phase 4 - Complete H02 Repositories
Last Updated: 19 Nov 2025, 16:49 CET
Maintainer: JARVIS + Álvaro Fernández Mota (THEA-IA)