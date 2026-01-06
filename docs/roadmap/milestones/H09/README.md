# H09: Real Ecosystem - AgendaAgent 🔴

**Period:** January 2026 (15 days, 75 hours)  
**Status:** 🔴 IN PROGRESS (Week 1)  
**Tests:** 81 planned | **Coverage Target:** 85%  
**Priority:** CRITICAL (First Functional Agent)

---

## 🎯 Objective

Build the **FIRST functional agent** (AgendaAgent) with real integrations: Telegram bot, PostgreSQL database, Google Calendar, and Groq LLM. This is the transition from infrastructure to real-world functionality.

---

## 🔴 Current Status (06 January 2026)

| Component | Status | Progress |
|-----------|--------|----------|
| **Planning** | ✅ Complete | 100% |
| **Architecture** | ✅ Complete | 100% |
| **Implementation** | 🔴 In Progress | Week 1/3 |
| **Testing** | ⏳ Planned | 0% |
| **Integration** | ⏳ Planned | 0% |

---

## 🏗️ Components (5 Total)

### 1️⃣ Telegram Bot (20 hours) 🔴

**Features:**
- Message handling (text, commands)
- Conversation state management
- User authentication
- Error handling
- Webhook support

**Files:**
src/theaia/adapters/telegram/
├── bot.py # Main bot class
├── handlers.py # Command handlers
└── middleware.py # Auth & logging

text

**Tests:** 25 planned

### 2️⃣ Database Services (15 hours) 🔴

**Tables:**
```sql
appointments:
  - id, user_id, date, start_time, end_time
  - notes, status (booked/cancelled/completed)
  - reminder_minutes, created_at, updated_at

availability:
  - id, date, time_slot, available
  - updated_at
Repositories:

AppointmentRepository (CRUD)

AvailabilityRepository (CRUD)

Tests: 20 planned

3️⃣ Calendar Engine (18 hours) 🔴
Services:

CalendarEngine: Slot generation, conflict detection

BookingService: Appointment management

AvailabilityService: Free/busy logic

Features:

Generate slots (9am-6pm, 30min intervals)

Detect conflicts (prevent overbooking)

Business hours configuration

Tests: 20 planned

4️⃣ Groq LLM Integration (15 hours) 🔴
NLU Pipeline:

text
User: "Quiero una cita mañana a las 3pm"
  ↓
GroqLLM: Intent extraction
  → intent: BOOK_APPOINTMENT
  → date: tomorrow
  → time: 15:00
  ↓
AgendaAgent: Create appointment
Model: llama-3.1-70b-versatile

Tests: 10 planned

5️⃣ E2E Integration (7 hours) 🔴
Full Flow:

text
1. User sends Telegram message
2. Bot receives + authenticates
3. Groq extracts intent + entities
4. AgendaAgent processes request
5. Database updated
6. Google Calendar synced
7. Confirmation sent to user
Tests: 16 E2E scenarios planned

📊 Test Plan (81 Total)
Test Type	Count	Coverage Target	Status
Unit Tests	40	85%+	⏳ Planned
Integration Tests	25	85%+	⏳ Planned
E2E Tests	16	100% flows	⏳ Planned
TOTAL	81	85%	⏳ Planned
🔧 Technology Stack
text
# Backend
Database: PostgreSQL 14+
ORM: SQLAlchemy 2.0 (async)
Migration: Alembic

# NLP
LLM: Groq (llama-3.1-70b-versatile)
Extractors: Custom (from H03)

# External APIs
Messaging: Telegram Bot API
Calendar: Google Calendar API v3

# Infrastructure
Framework: FastAPI (async)
Task Queue: Celery (for reminders)
Cache: Redis (session management)
📅 Implementation Timeline
Week 1 (06-10 Jan) - 🔴 Current
🔴 Telegram bot basic setup

🔴 Database schema creation

🔴 AppointmentRepository implementation

🔴 Basic CRUD operations

Week 2 (13-17 Jan) - ⏳ Next
⏳ Calendar engine (slots, conflicts)

⏳ Groq LLM integration

⏳ AgendaAgent FSM flows

⏳ Unit + integration tests

Week 3 (20-24 Jan) - ⏳ Future
⏳ Google Calendar sync

⏳ E2E testing (81 tests)

⏳ Performance tuning

⏳ Production deployment

🌐 API Endpoints (Planned)
Create Appointment
text
POST /api/v1/appointments
Content-Type: application/json

{
  "user_id": 123,
  "date": "2026-01-07",
  "time": "15:00",
  "duration": 30,
  "notes": "Consulta médica"
}
Check Availability
text
GET /api/v1/appointments/availability?date=2026-01-07

Response:
{
  "date": "2026-01-07",
  "slots": [
    {"time": "09:00", "available": true},
    {"time": "09:30", "available": true},
    {"time": "10:00", "available": false},
    ...
  ]
}
Cancel Appointment
text
DELETE /api/v1/appointments/456

Response:
{
  "success": true,
  "message": "Appointment cancelled",
  "appointment_id": 456
}
🔄 AgendaAgent FSM Flow
text
States:
  initial
    ↓
  awaiting_date (FSM asks: "¿Qué día?")
    ↓
  awaiting_time (FSM asks: "¿A qué hora?")
    ↓
  confirming (FSM shows: "Cita 07-Jan 15:00, ¿confirmar?")
    ↓
  booked (FSM: "✅ Cita confirmada")

Callbacks:
  on_enter("awaiting_date"): Show date picker
  on_enter("awaiting_time"): Show available slots
  on_enter("confirming"): Generate summary
  after_transition("booked"): Create in DB + Sync Google Calendar
📂 File Structure (Planned)
text
src/theaia/
├── adapters/
│   └── telegram/
│       ├── bot.py                   # Telegram bot
│       ├── handlers.py              # Message handlers
│       └── middleware.py            # Auth/logging
├── agents/
│   └── agenda_agent/
│       ├── agent.py                 # AgendaAgent main
│       ├── handler.py               # Command handler
│       ├── fsm_machine.py          # FSM definition
│       └── services/
│           ├── calendar_engine.py   # Slot generation
│           └── booking_service.py   # CRUD
├── data/
│   └── repositories/
│       ├── appointment_repo.py      # Appointments
│       └── availability_repo.py     # Availability
└── services/
    └── groq_service.py              # LLM integration

tests/
├── agents/
│   └── test_agenda_agent.py         # 40 tests
├── services/
│   └── test_calendar_engine.py      # 25 tests
└── integration/
    └── test_e2e_h09.py              # 16 tests
🎯 Success Criteria
✅ AgendaAgent functional end-to-end

✅ Telegram bot working in production

✅ Google Calendar synced bi-directionally

✅ 81 tests passing (85%+ coverage)

✅ <200ms response time

✅ Handles 50+ concurrent users

✅ Zero data loss

🚨 Risks & Mitigations
Risk	Mitigation
Google Calendar API rate limits	Implement caching + batch operations
Groq LLM accuracy < 90%	Fallback to rule-based extraction
Telegram webhook reliability	Implement retry logic + polling fallback
Database conflicts	Optimistic locking + conflict detection
📖 Detailed Documentation
Planning Docs (in this folder)
CHECKLIST-EJECUTIVO-FINAL.md - Executive checklist

H09-ECOSISTEMA-REAL-PRIORIDAD.md - Priority breakdown

H09-ECOSYSTEM.md - Complete ecosystem design

H09-E2E-TESTING.md - E2E test scenarios

PLAN-ATAQUE-H09-EJECUCION.md - Execution plan

🔄 Dependencies
From Previous Milestones
✅ H01: Router & Orchestrator

✅ H02: Database & Multi-tenancy

✅ H03: NLP Extractors (date, time)

✅ H04-H05: FSM Core & Advanced

✅ H06-H07: FSM Integration & Callbacks

✅ H08: FSM Production Ready

All infrastructure ready - H09 builds on solid foundation ✅

🎬 What's Next After H09?
H10 (February 2026) - ⏳ Next
QueryAgent (semantic search)

NoteAgent (note management)

80 tests planned

H11 (February 2026) - ⏳ Future
ReminderAgent (standalone reminders)

30 tests planned

📖 Related Documentation
Master Roadmap - Full H01-H17 timeline

SCHEMA.md - Current project state

AgendaAgent Spec - Agent details

Previous: H08 - FSM Production

Next: H10-H17 - Future agents

Started: 06 January 2026
Expected Completion: 24 January 2026
Status: 🔴 Week 1 of 3 in progress
Impact: FIRST real agent - proves entire architecture works

🚨 CURRENT MILESTONE - Active Development 🚨