# Testing Documentation

**Status:** 🟢 ACTIVE (786 tests passing, 85% coverage)  
**Implementation:** H01-H08 (Complete) → H09+ (Ongoing)  
**Priority:** CRITICAL  
**Last Updated:** 06 January 2026

---

## 🎯 Current State

### ✅ Foundation Tests (H01-H08) - COMPLETE

**Total:** 786 tests passing | **Coverage:** 85%

| Component | Tests | Coverage | Status |
|-----------|-------|----------|--------|
| **Router & Orchestrator** (H01) | 10 | 60% | ✅ |
| **Database & Repositories** (H02) | 16 | 41-59% | ✅ |
| **AgentConfig & NLP** (H03) | 18 | 84-87% | ✅ |
| **FSM Core** (H04) | 196 | 63-100% | ✅ |
| **FSM Advanced** (H05) | 174 | 85%+ | ✅ |
| **FSM Integration** (H06) | 261 | 90%+ | ✅ |
| **Callbacks** (H07) | 71 | 96% | ✅ |
| **FSM Production** (H08) | 40 | 95% | ✅ |
| **TOTAL** | **786** | **85%** | ✅ |

### 🔴 Agent Tests (H09+) - IN PROGRESS

| Agent | Tests Planned | Status |
|-------|--------------|--------|
| **AgendaAgent** (H09) | 81 | 🔴 In development |
| **QueryAgent** (H10) | 40 | ⏳ Planned |
| **NoteAgent** (H10) | 40 | ⏳ Planned |
| **ReminderAgent** (H11) | 30 | ⏳ Planned |
| **TOTAL AGENTS** | **191** | **⏳** |

### ⏳ Infrastructure Tests (H12+) - PLANNED

| Component | Tests Planned | Milestone |
|-----------|--------------|-----------|
| REST API | 50 | H12 |
| WhatsApp/Slack | 40 | H13 |
| Scalability | 30 | H14 |
| Security | 20 | H15 |
| Monitoring | 30 | H16 |
| Web UI | 40 | H17 |
| **TOTAL INFRA** | **210** | **⏳** |

---

## 📊 Overall Test Plan

COMPLETED (H01-H08): 786 tests ✅
IN PROGRESS (H09): 81 tests 🔴
PLANNED (H10-H17): 310 tests ⏳
────────────────────────────────────
GRAND TOTAL: 1,177 tests

text

---

## 🧪 Test Types by Category

### Unit Tests (60%)
```python
# Test individual functions/methods
def test_date_extractor():
    result = DateExtractor.extract("mañana")
    assert result == tomorrow_date
Integration Tests (30%)
python
# Test database operations
async def test_create_appointment():
    appt = await appointment_repo.create(...)
    assert appt.id is not None
    assert await db.exists(appt.id)
E2E Tests (10%)
python
# Test complete user flows
async def test_booking_flow():
    # User sends "Quiero cita mañana 3pm"
    # System responds, asks confirmation
    # User confirms
    # Appointment created in DB
    # Google Calendar synced
    # Confirmation sent
📂 Test Structure
text
tests/
├── core/                        # H01-H08 (786 tests) ✅
│   ├── test_message_router.py
│   ├── test_orchestrator.py
│   ├── nlp/extractors/
│   └── fsm/
│       ├── test_state_machine.py
│       ├── test_callbacks.py
│       └── advanced/
├── data/                        # Repository tests ✅
│   └── repositories/
├── agents/                      # H09+ (81+ tests)
│   ├── test_agenda_agent.py     # 🔴 H09 (40 tests)
│   ├── test_query_agent.py      # ⏳ H10 (40 tests)
│   ├── test_note_agent.py       # ⏳ H10 (40 tests)
│   └── test_reminder_agent.py   # ⏳ H11 (30 tests)
├── integration/                 # Cross-component tests
│   └── test_e2e_h09.py          # 🔴 H09 (16 tests)
├── performance/                 # H08 stress tests ✅
│   └── fsm/
└── api/                         # ⏳ H12 (50 tests)
🎯 Testing Standards
Coverage Requirements
Minimum: 85% line coverage

Target: 90%+ for critical components

Exceptions: UI code, external API mocks

Test Naming Convention
python
# Pattern: test_mponent>_<scenario>_<expected>
def test_agenda_agent_book_appointment_success()
def test_agenda_agent_book_appointment_conflict()
def test_agenda_agent_book_appointment_invalid_date()
Fixtures & Mocks
python
# Use pytest fixtures
@pytest.fixture
async def db_session():
    # Setup test database
    yield session
    # Cleanup

# Mock external APIs
@pytest.fixture
def mock_google_calendar():
    with patch('google.calendar.create_event'):
        yield
📚 Future Content (H09+)
H09 (January 2026)
testing_agenda_agent.md - AgendaAgent test guide

e2e_testing_guide.md - E2E test patterns

mocking_external_apis.md - Google Calendar mocks

H12 (March 2026)
api_testing.md - REST API test strategies

integration_testing.md - API integration tests

H14 (April 2026)
load_testing.md - Performance test scenarios

stress_testing.md - 10k concurrent users

H16 (May 2026)
testing_monitoring.md - Test metrics in Grafana

🔧 Running Tests (Current)
All Foundation Tests (H01-H08)
bash
# Run all 786 tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src/theaia --cov-report=html

# Run specific component
pytest tests/core/fsm/ -v
AgendaAgent Tests (H09 - when ready)
bash
# Run AgendaAgent tests only
pytest tests/agents/test_agenda_agent.py -v

# Run E2E tests
pytest tests/integration/test_e2e_h09.py -v
📊 Test Metrics Dashboard
Current Metrics (H01-H08)
text
Total Tests:        786 ✅
Passing:            786 (100%)
Failing:            0
Coverage:           85%
Avg Duration:       0.8s per test
Total Duration:     ~10 minutes
Target Metrics (H09 completion)
text
Total Tests:        867 (786 + 81)
Passing:            867 (100%)
Coverage:           85%+
Avg Duration:       <1s per test
Total Duration:     <15 minutes
🎓 Testing Best Practices
1. Test Pyramid
text
      /\
     /E2\    10% - E2E tests (slow, high value)
    /────\
   /Integ\   30% - Integration tests (medium)
  /──────\
 / Unit   \  60% - Unit tests (fast, many)
/──────────\
2. Test Independence
python
# Each test is independent
✅ GOOD: Each test sets up its own data
❌ BAD: Tests depend on each other's state
3. Clear Assertions
python
# Clear, specific assertions
✅ GOOD: assert appointment.date == expected_date
❌ BAD: assert appointment  # What are we checking?
📖 Related Documentation
H08 Milestone - FSM testing complete

H09 Milestone - AgendaAgent tests (current)

SCHEMA.md - Testing architecture

Roadmap Master - Test distribution H01-H17

🗂️ Archived Documentation
Location: docs/archive/testing_nov2025/

Archived files (Nov 2025):

ci_cd.md, coverage_report.md, e2e_tests.md, index.md, integration_tests.md, unit_tests.md

Reason:

❌ Outdated test counts

❌ Referenced non-existent test files

❌ Not aligned with current 786 tests passing

Will update as more tests are added in H09+.

Last Updated: 06 January 2026, 19:57 CET
Next Update: Late January 2026 (H09 completion - 867 tests)
Maintained by: QA Team

🟢 786 TESTS PASSING - SOLID FOUNDATION 🟢