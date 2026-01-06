# 🗺️ THEA IA - Master Roadmap (H01-H17)

**Version:** v3.0.0  
**Last Updated:** 06 January 2026  
**Timeline:** November 2024 - June 2026 (8 months)  
**Current Sprint:** H09 (January 2026)

---

## 📊 Executive Summary

| Status | Milestones | Tests | Coverage | Period |
|--------|------------|-------|----------|--------|
| ✅ **Completed** | H01-H08 (8) | 786 | 85% | Nov 2024 - Dec 2025 |
| 🔴 **In Progress** | H09 (1) | 81 planned | 85% | Jan 2026 |
| ⏳ **Planned** | H10-H17 (8) | 200+ planned | 85%+ | Feb-Jun 2026 |

**Total LOC:** 12,300+ | **Tech Debt:** ZERO | **Quality Score:** 95%

---

## 🎯 Roadmap Overview

┌──────────────────────────────────────────────────────────┐
│ PHASE 1: FOUNDATION (H01-H08) ✅ COMPLETED │
│ Nov 2024 - Dec 2025 | 786 tests | 85% coverage │
└──────────────────────────────────────────────────────────┘
↓
┌──────────────────────────────────────────────────────────┐
│ PHASE 2: REAL ECOSYSTEM (H09) 🔴 IN PROGRESS │
│ Jan 2026 | AgendaAgent | 81 tests │
└──────────────────────────────────────────────────────────┘
↓
┌──────────────────────────────────────────────────────────┐
│ PHASE 3: INTELLIGENT AGENTS (H10-H11) ⏳ PLANNED │
│ Feb 2026 | QueryAgent + NoteAgent + ReminderAgent │
└──────────────────────────────────────────────────────────┘
↓
┌──────────────────────────────────────────────────────────┐
│ PHASE 4: SCALE & INTEGRATIONS (H12-H14) ⏳ PLANNED │
│ Mar-Apr 2026 | REST API + Integrations + Scalability │
└──────────────────────────────────────────────────────────┘
↓
┌──────────────────────────────────────────────────────────┐
│ PHASE 5: ENTERPRISE READY (H15-H17) ⏳ PLANNED │
│ May-Jun 2026 | Security + Monitoring + Web UI │
└──────────────────────────────────────────────────────────┘

text

---

## ✅ PHASE 1: FOUNDATION (H01-H08) — COMPLETED

### H01: Router & Orchestrator ✅
**Period:** November 2024 (2 weeks)  
**Status:** ✅ COMPLETED  
**Tests:** 10 | **Coverage:** 60%

#### Deliverables
- ✅ MessageRouter with intent classification
- ✅ Orchestrator for agent coordination
- ✅ Basic routing logic
- ✅ 10 tests passing

#### Files
- `src/theaia/core/message_router.py` (145 LOC)
- `src/theaia/core/orchestrator.py` (180 LOC)
- `tests/core/test_message_router.py`
- `tests/core/test_orchestrator.py`

#### Key Decisions
- Router handles intent classification
- Orchestrator coordinates agent lifecycle
- Simple priority-based routing

---

### H02: Multi-tenancy & Database ✅
**Period:** November 2024 (3 weeks)  
**Status:** ✅ COMPLETED  
**Tests:** 16 | **Coverage:** 41-59%

#### Deliverables
- ✅ PostgreSQL 14+ schema (7 core tables)
- ✅ Repository pattern (6 repositories + base)
- ✅ TelegramAdapter (basic)
- ✅ Multi-tenant isolation
- ✅ SQLAlchemy 2.0 async

#### Database Tables
```sql
-- Core Tables
tenants          -- Multi-tenant isolation
users            -- User accounts
conversations    -- Chat sessions
messages         -- Message history
agent_configs    -- Agent configurations
user_preferences -- User settings
api_keys         -- API key management
Files
src/theaia/data/models/ (7 SQLAlchemy models)

src/theaia/data/repositories/ (6 repositories)

src/theaia/adapters/telegram_adapter.py

tests/data/repositories/

Key Decisions
Repository pattern for data access

tenant_id mandatory in all queries

Async/await throughout

H03: AgentConfig & NLP Extractors ✅
Period: Early December 2024 (2 weeks)
Status: ✅ COMPLETED
Tests: 18 | Coverage: 84-87%

Deliverables
✅ AgentConfig system (YAML-based)

✅ 5 NLP Extractors (date, time, name, email, phone)

✅ Config validation

✅ Extractor pipeline

Extractors
python
- DateExtractor      # "mañana", "15 de enero"
- TimeExtractor      # "3pm", "15:30"
- NameExtractor      # "Juan Pérez"
- EmailExtractor     # "user@example.com"
- PhoneExtractor     # "+34 600 123 456"
Files
src/theaia/core/agent_config.py

src/theaia/core/nlp/extractors/

tests/core/nlp/extractors/

Key Decisions
YAML for human-readable configs

Pydantic for validation

Extractor composition pattern

H04: FSM Core System ✅
Period: Mid-Late December 2024 (3 weeks)
Status: ✅ COMPLETED
Tests: 196 | Coverage: 63-100%

Deliverables
✅ StateMachine core (732 LOC)

✅ State & Transition models

✅ Context management

✅ Lifecycle (init → transitions → terminal)

✅ 196 tests passing

Architecture
python
StateMachine:
  - states: Dict[str, State]
  - transitions: List[Transition]
  - context: Context
  - current_state: State
  
  Methods:
  - start() → initial_state
  - process_input(input) → next_state
  - can_transition(from, to) → bool
Files
src/theaia/core/state_machine.py (732 LOC)

src/theaia/core/state.py (280 LOC)

src/theaia/core/transition.py (195 LOC)

tests/core/fsm/ (196 tests)

Key Decisions
Explicit state transitions

Context carries conversation data

Guard conditions for validation

H05: FSM Advanced Patterns ✅
Period: January 2025 (3 weeks)
Status: ✅ COMPLETED
Tests: 174 | Coverage: 85%+

Deliverables
✅ Hierarchical states (parent/child)

✅ Parallel states (concurrent execution)

✅ History states (resume previous state)

✅ Composite states

✅ 174 advanced tests

Patterns
python
# Hierarchical
BookingFlow (parent)
  ├─ DateSelection (child)
  ├─ TimeSelection (child)
  └─ Confirmation (child)

# Parallel
PaymentProcess
  ├─ AuthCheck (parallel)
  └─ InventoryCheck (parallel)

# History
WizardFlow with history_state
  → Can resume at last step
Files
src/theaia/core/fsm/hierarchical.py

src/theaia/core/fsm/parallel.py

src/theaia/core/fsm/history.py

tests/core/fsm/advanced/ (174 tests)

Key Decisions
Hierarchical for complex flows

Parallel for independent processes

History for wizard-like UX

H06: FSM Integration & Polish ✅
Period: February-March 2025 (4 weeks)
Status: ✅ COMPLETED
Tests: 261 | Coverage: 90%+

Deliverables
✅ FSM + Repository integration

✅ FSM + Adapter integration

✅ Error recovery patterns

✅ State persistence

✅ 261 integration tests

Features
python
# State Persistence
- Save FSM state to database
- Resume conversation from DB
- Context serialization

# Error Recovery
- Retry failed transitions
- Fallback states
- Error state handlers
Files
src/theaia/core/fsm/persistence.py

src/theaia/core/fsm/error_recovery.py

tests/integration/fsm/ (261 tests)

Key Decisions
Persist only essential state

Automatic error recovery

Graceful degradation

H07: Callbacks Manager ✅
Period: April 2025 (2 weeks)
Status: ✅ COMPLETED
Tests: 71 | Coverage: 96%

Deliverables
✅ Callback registration system

✅ Lifecycle hooks (on_enter, on_exit, on_transition)

✅ Async callback execution

✅ Priority-based ordering

✅ 71 tests passing

Callback Types
python
# State Callbacks
- on_enter(state, context)    # Before entering
- on_exit(state, context)     # Before leaving

# Transition Callbacks
- before_transition(from, to, context)
- after_transition(from, to, context)

# Global Callbacks
- on_error(error, context)
- on_complete(final_state, context)
Files
src/theaia/core/callbacks.py (300 LOC, 96% coverage)

tests/core/test_callbacks.py (71 tests)

Key Decisions
Observer pattern for callbacks

Priority queue for ordering

Async/await for non-blocking

H08: FSM Production Ready ✅
Period: May-December 2025 (6 months)
Status: ✅ COMPLETED
Tests: 40 | Coverage: 95%

Deliverables
✅ Performance optimization

✅ Memory management

✅ Load testing (100 concurrent FSMs)

✅ Documentation complete

✅ 40 stress tests

Optimizations
python
# Performance
- Lazy state loading
- Callback caching
- Transition indexing

# Memory
- Context cleanup
- State object pooling
- Weak references

# Reliability
- Graceful shutdown
- State recovery
- Transaction safety
Metrics
Throughput: 100 FSMs/sec

Latency: <50ms per transition

Memory: <10MB per FSM

Uptime: 99.9%

Files
src/theaia/core/fsm/optimization.py

tests/performance/fsm/ (40 tests)

docs/architecture/fsmengine.md

🔴 PHASE 2: REAL ECOSYSTEM (H09) — IN PROGRESS
H09: Real Ecosystem ✅🔴
Period: January 2026 (15 days, 75 hours)
Status: 🔴 IN PROGRESS (Week 1)
Tests: 81 planned | Coverage: 85% target

Objective
Build first functional agent (AgendaAgent) with real integrations: Telegram bot, PostgreSQL database, Google Calendar, and Groq LLM.

Components (5)
1️⃣ Telegram Bot (20h) 🔴
python
# Features
- Message handling (text, commands)
- Conversation state management
- User authentication
- Error handling
- Webhook support

# Files
- src/theaia/adapters/telegram/
  ├─ bot.py
  ├─ handlers.py
  └─ middleware.py
2️⃣ Database Services (15h) 🔴
python
# Tables
appointments:
  - id, user_id, date, start_time, end_time
  - notes, status, reminder_minutes

availability:
  - id, date, time_slot, available

# Repositories
- AppointmentRepository (CRUD)
- AvailabilityRepository (CRUD)
3️⃣ Calendar Engine (18h) 🔴
python
# Services
- CalendarEngine: slot generation, conflict detection
- BookingService: appointment management
- AvailabilityService: free/busy logic

# Features
- Generate slots (9am-6pm, 30min intervals)
- Detect conflicts (prevent overbooking)
- Business hours configuration
4️⃣ Groq LLM Integration (15h) 🔴
python
# NLU Pipeline
User: "Quiero una cita mañana a las 3pm"
  ↓
GroqLLM: Intent extraction
  → intent: BOOK_APPOINTMENT
  → date: tomorrow
  → time: 15:00
  ↓
AgendaAgent: Create appointment
5️⃣ E2E Integration (7h) 🔴
python
# Full Flow
1. User sends Telegram message
2. Bot receives + authenticates
3. Groq extracts intent + entities
4. AgendaAgent processes request
5. Database updated
6. Google Calendar synced
7. Confirmation sent to user

# Tests: 81 E2E scenarios
Current Status (06 Jan 2026)
✅ Planning complete

✅ Architecture defined

🔴 Implementation: Week 1

⏳ Testing: Week 2

⏳ Integration: Week 3

Files (Planned)
text
src/theaia/
├─ adapters/telegram/         # Telegram bot
├─ agents/agenda_agent.py     # AgendaAgent
├─ services/
│  ├─ calendar_engine.py      # Calendar logic
│  ├─ booking_service.py      # Booking CRUD
│  └─ groq_service.py         # LLM integration
└─ data/repositories/
   ├─ appointment_repo.py     # DB access
   └─ availability_repo.py    # Availability

tests/
├─ agents/test_agenda_agent.py       # 40 tests
├─ services/test_calendar_engine.py  # 25 tests
└─ integration/test_e2e_h09.py       # 16 tests
⏳ PHASE 3: INTELLIGENT AGENTS (H10-H11) — PLANNED
H10: QueryAgent + NoteAgent ⏳
Period: February 2026 (20 days, 100 hours)
Status: ⏳ PLANNED
Tests: 80 planned | Coverage: 85%+

QueryAgent (Search & QA) 🔍
Duration: 10 days, 50 hours

Features
✅ Semantic search (vector embeddings)

✅ Question answering (extract answers from context)

✅ Multi-source search (notes + events + docs)

✅ Entity extraction (NER)

Technology
python
# NLP Models
- Embeddings: sentence-transformers/all-MiniLM-L6-v2
- QA Model: deepset/roberta-base-squad2
- Search: PostgreSQL + pgvector

# Services
- SemanticSearchService
- QuestionAnsweringService
- EntityExtractor
Tests: 40
NoteAgent (Note Management) 📝
Duration: 10 days, 50 hours

Features
✅ Create/edit/delete notes (markdown)

✅ Full-text search (PostgreSQL ts_vector)

✅ Tagging system (manual + auto)

✅ Duplicate detection

✅ Archive system

Database
sql
notes:
  - id, user_id, title, content
  - tags (array), created_at, updated_at
  - archived, embedding (vector)

Indexes:
  - Full-text: to_tsvector('spanish', content)
  - Tags: GIN index
  - Vector: similarity search
Tests: 40
H11: ReminderAgent ⏳
Period: Late February 2026 (10 days, 50 hours)
Status: ⏳ PLANNED
Tests: 30 planned | Coverage: 85%+

Features
✅ Create/modify/delete reminders

✅ One-time + recurring reminders

✅ Multi-channel notifications (Telegram, email)

✅ Snooze functionality

✅ Retry logic (3 attempts)

Technology
python
# Scheduler
- APScheduler or Celery
- Cron-like scheduling
- Background task queue

# Database
reminders:
  - id, user_id, message, trigger_at
  - recurrence (daily/weekly/monthly)
  - channels (array), status
Tests: 30
⏳ PHASE 4: SCALE & INTEGRATIONS (H12-H14) — PLANNED
H12: REST API & OAuth ⏳
Period: March 2026 (15 days)
Status: ⏳ PLANNED
Tests: 50 planned

Features
REST API (FastAPI)

OAuth2 + JWT authentication

Rate limiting

API documentation (OpenAPI)

Webhooks

Endpoints
text
POST /api/v1/appointments
GET  /api/v1/appointments/availability
POST /api/v1/notes
GET  /api/v1/notes/search
POST /api/v1/reminders
POST /api/v1/query/search
POST /api/v1/query/ask
H13: WhatsApp + Slack ⏳
Period: March 2026 (10 days)
Status: ⏳ PLANNED
Tests: 40 planned

Adapters
WhatsAppAdapter (Twilio/Meta Cloud API)

SlackAdapter (Bolt SDK)

Unified message format

H14: Scalability & Performance ⏳
Period: April 2026 (15 days)
Status: ⏳ PLANNED
Tests: 30 planned

Features
Horizontal scaling (Redis session)

Database connection pooling

Caching layer (Redis)

Load balancing

CDN for static assets

Targets
10,000 concurrent users

<100ms API latency

99.9% uptime

⏳ PHASE 5: ENTERPRISE READY (H15-H17) — PLANNED
H15: Advanced Security ⏳
Period: May 2026 (10 days)
Status: ⏳ PLANNED

Features
Row-level security (RLS)

Encryption at rest

Audit logging

GDPR compliance

Penetration testing

H16: Monitoring & Observability ⏳
Period: May 2026 (10 days)
Status: ⏳ PLANNED

Features
Prometheus metrics

Grafana dashboards

Distributed tracing (Jaeger)

Log aggregation (ELK)

Alerting (PagerDuty)

H17: Web Dashboard ⏳
Period: June 2026 (20 days)
Status: ⏳ PLANNED

Features
React + TypeScript frontend

Admin panel

Analytics dashboard

User management

Real-time updates (WebSockets)

📊 Overall Progress Tracking
Tests Distribution
Phase	Milestones	Tests Completed	Tests Planned	Total
Phase 1	H01-H08	786	0	786
Phase 2	H09	0	81	81
Phase 3	H10-H11	0	110	110
Phase 4	H12-H14	0	120	120
Phase 5	H15-H17	0	80	80
TOTAL	H01-H17	786	391	1,177
Timeline Summary
text
2024 Nov-Dec: H01-H04 (Foundation)         ✅ 4 months
2025 Jan-Dec: H05-H08 (FSM Production)     ✅ 8 months
───────────────────────────────────────────────────────
2026 Jan:     H09 (Real Ecosystem)         🔴 15 days
2026 Feb:     H10-H11 (Agents)             ⏳ 30 days
2026 Mar-Apr: H12-H14 (Scale)              ⏳ 40 days
2026 May-Jun: H15-H17 (Enterprise)         ⏳ 40 days
Quality Metrics
Metric	Current	Target	Status
Tests	786	1,177	🟢 67%
Coverage	85%	85%+	🟢 Met
Tech Debt	0	0	🟢 Zero
Documentation	10/10	10/10	🟢 Complete
🎯 Success Criteria
Phase 1 (H01-H08) ✅
✅ 786 tests passing

✅ 85% code coverage

✅ FSM production-ready

✅ Zero technical debt

Phase 2 (H09) 🔴
🔴 AgendaAgent functional

🔴 Telegram bot working

🔴 Google Calendar synced

🔴 81 E2E tests passing

Phase 3 (H10-H11) ⏳
⏳ 4 agents operational

⏳ 110 tests passing

⏳ NLP pipeline working

⏳ Multi-agent coordination

Phase 4 (H12-H14) ⏳
⏳ REST API live

⏳ 3 adapters (Telegram, WhatsApp, Slack)

⏳ 10k concurrent users

⏳ 120 tests passing

Phase 5 (H15-H17) ⏳
⏳ Enterprise security

⏳ Monitoring dashboards

⏳ Web UI deployed

⏳ Production release

📖 Related Documentation
SCHEMA.md - Complete project state

README.md - Project overview

Agents Overview - Agent architecture

Architecture - System design

Testing Guide - Testing strategy

Last Updated: 06 January 2026, 16:40 CET
Version: v3.0.0
Current Sprint: H09 (Week 1 of 3)
Next Milestone: H10 (February 2026)

text