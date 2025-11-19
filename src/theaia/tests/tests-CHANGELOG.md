# Changelog - Testing Suite

Changes to the THEA_IA testing suite.

---

## [Unreleased]

**Planned for H07 (27 Nov - 01 Dic)**
- Complete integration test suite
- Critical E2E test scenarios
- Full CI/CD pipeline integration

---

## [0.3.0] - 2025-11-16 (H03 - Phase 3)

### 🎉 Phase 3 Complete - Agent Configuration & Entity Extraction

#### Added

**AgentConfig System**
- `test_agent_config.py`: AgentConfig class tests (15 tests, 100% coverage)
  - Config creation and management
  - Intent add/remove/check
  - Serialization (to_dict/from_dict)
  - Predefined configs for 6 agents
  - Config registry tests

**Entity Extraction Tests (48 tests total)**
- `test_date_parser.py`: DateTimeExtractor tests (15 tests, 91% coverage)
  - Relative dates: "mañana", "hoy", "en N días"
  - Weekdays: "lunes", "martes", etc.
  - Time formats: "10:30", "15h"
  - Complex expressions
  - Invalid input handling

- `test_entity_extraction.py`: Location & Person extraction (18 tests, 99% avg)
  - **LocationExtractor** (100% coverage):
    - 35+ Spanish cities recognition
    - Location types (oficina, casa, etc.)
    - Preposition patterns (en, a, desde)
    - Accent handling
  - **PersonNameExtractor** (98% coverage):
    - 35+ common Spanish names
    - Title recognition (Dr., Sr., Prof.)
    - Preposition patterns (con, de, para)
    - Complex sentences

**E2E Test Suites (46 tests total)**
- `test_agenda_agent_e2e.py`: AgendaAgent workflows (17 tests)
  - Event creation (basic, with time, location)
  - Event listing and viewing
  - Event editing and cancellation
  - Recurring events and conflict detection
  - Complete lifecycle testing

- `test_note_agent_e2e.py`: NoteAgent workflows (14 tests)
  - Note CRUD operations
  - Category and tag management
  - Search functionality
  - Pin/unpin notes
  - Full lifecycle testing

- `test_reminder_agent_e2e.py`: ReminderAgent workflows (15 tests)
  - Time-based reminders (all formats)
  - Weekday-based reminders
  - Reminder management (list, edit, complete, delete)
  - Location-based reminders
  - Recurring reminders

**Test Documentation**
- Updated `README.md` in all test directories:
  - `src/theaia/tests/README.md`: Complete overview (173 tests)
  - `unit/README.md`: Unit tests guide (77 tests)
  - `e2e/README.md`: E2E tests guide (50 tests)
  - `integration/README.md`: Integration guide (14 tests)
  - `adapters/README.md`: Adapter tests guide (10 tests)
  - `core/README.md`: Core tests guide (22 tests)

#### Stats

**Test Count:**
- Unit: 77 tests (45% of suite)
- E2E: 50 tests (29% of suite)
- Integration: 14 tests (8% of suite)
- Adapters: 10 tests (6% of suite)
- Core: 22 tests (12% of suite)
- **Total: 173 tests** (+86 new tests)

**Coverage:**
- Overall: 50% (target reached! ✅)
- AgentConfig: 100%
- LocationExtractor: 100%
- PersonNameExtractor: 98%
- DateTimeExtractor: 91%
- BaseAgent: 93%

**Performance:**
- Execution time: ~8 seconds (all 173 tests)
- Pass rate: 100% (0 failures, 0 skips)
- Warnings: 18 (deprecation warnings only)

#### Files Added
src/theaia/tests/unit/test_agent_config.py
src/theaia/tests/unit/test_date_parser.py
src/theaia/tests/unit/test_entity_extraction.py
src/theaia/tests/e2e/test_agenda_agent_e2e.py
src/theaia/tests/e2e/test_note_agent_e2e.py
src/theaia/tests/e2e/test_reminder_agent_e2e.py

text

#### Documentation Updated
src/theaia/tests/README.md
src/theaia/tests/unit/README.md
src/theaia/tests/e2e/README.md
src/theaia/tests/integration/README.md
src/theaia/tests/adapters/README.md (new)
src/theaia/tests/core/README.md
docs/testing/README.md
docs/testing/changelog.md (this file)

text

---

## [0.7.0] - 2025-12-01 (H07 Target)

### Added

**Integration Tests:**
- `test_telegram_flow.py` (Telegram → DB)
- `test_database_flow.py` (Repo → Model → DB)
- `test_agent_flow.py` (Agent CRUD completo)
- `test_adapter_agent.py` (Adapter ↔ Agent)
- `test_core_agents.py` (CoreManager routing)

**E2E Tests:**
- `test_user_journey/` (onboarding, lifecycles)
- `test_telegram_bot_complete.py`
- `test_reminder_lifecycle.py`
- `test_note_lifecycle.py`
- `test_multi_agent_flow.py`

### Coverage
- Integration: >80%
- E2E: >70%
- Total: >85%

---

## [0.2.0] - 2025-11-16 (H02 Target)

### Added

**Test Infrastructure:**
- `pytest.ini` configurado
- `conftest.py` con fixtures globales
- `fixtures/` (database, user, telegram, datetime)

**Unit Tests:**
- `test_config/` (settings, logging, constants)
- `test_database/test_connection.py`
- `test_database/test_models/` (6 models)
- `test_database/test_repositories/` (6 repositories)
- `test_models/` (Pydantic schemas - 7 módulos)
- `test_adapters/test_telegram_adapter.py`
- `test_agents/` (5 agents)
- `test_core/test_thea_manager.py`
- `test_utils/` (datetime, text, validators, formatters)

### Coverage
- Unit: >90%
- Total: >85%

### CI/CD
- GitHub Actions ejecuta tests automáticamente
- Coverage report en CI
- Fail si coverage <85%

---

## [0.1.0] - 2025-11-03 (H01)

### Added

**Estructura inicial tests/**
- Documentación:
  - `README.md`
  - `ROADMAP.md`
  - `CHANGELOG.md`
  - `STRUCTURE.md`
  - `DEPENDENCIES.md`
  - `TESTING_GUIDE.md`
- Estrategia testing (70/20/10 pirámide)

---

## Test Markers

### v0.3.0 (Current):
- `@pytest.mark.unit`
- `@pytest.mark.e2e`
- `@pytest.mark.integration`
- `@pytest.mark.database`
- `@pytest.mark.slow`

### v0.7.0 (Planned):
- `@pytest.mark.telegram`
- `@pytest.mark.ml`
- `@pytest.mark.payment`

---

**Last Updated:** 16 Nov 2025, 00:16 CET  
**Version:** 0.3.0  
**Maintainer:** Álvaro Fernández Mota
