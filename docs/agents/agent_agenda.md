# 📅 AgendaAgent — THEA IA

**Version:** 2.0  
**Last Updated:** 06 January 2026  
**Status:** 🔴 In Development (H09)  
**Priority:** CRITICAL  
**Milestone:** H09 (January 2026)

---

## 🎯 Purpose

The **AgendaAgent** manages appointments, events, and calendar operations. It handles booking, scheduling, availability checks, conflict detection, and integration with external calendar services (Google Calendar).

**This is the FIRST functional agent** being implemented in H09 as the foundation for THEA IA's real-world functionality.

---

## 📋 Core Responsibilities

| Responsibility | Description | Status |
|----------------|-------------|--------|
| **Create Appointments** | Book new appointments with date, time, notes | 🔴 H09 |
| **Check Availability** | Generate available time slots (9am-6pm, 30min intervals) | 🔴 H09 |
| **Conflict Detection** | Prevent overbooking by checking existing appointments | 🔴 H09 |
| **Modify Appointments** | Reschedule or update appointment details | 🔴 H09 |
| **Cancel Appointments** | Delete appointments with proper cleanup | 🔴 H09 |
| **List Appointments** | Retrieve appointments by date range | 🔴 H09 |
| **Pre-Event Reminders** | Send reminders 15min/1h before appointment | 🔴 H09 |
| **Google Calendar Sync** | Bi-directional sync with Google Calendar API | 🔴 H09 |

---

## 🏗️ Architecture

### Technology Stack

```yaml
# Database Tables
appointments:
  - id, user_id, date, start_time, end_time
  - notes, status (booked/cancelled/completed)
  - reminder_minutes, created_at, updated_at

availability:
  - id, date, time_slot, available
  - updated_at

# Services
- CalendarEngine: Slot generation, conflict detection
- BookingService: CRUD operations
- GoogleCalendarSync: External calendar integration
- GroqLLM: Natural language understanding

# Technology
- Database: PostgreSQL 14+
- NLP: Groq LLM (llama-3.1-70b-versatile)
- External API: Google Calendar API v3
- Timezone: UTC ↔ Local conversion
Natural Language Processing
AgendaAgent uses Groq LLM to understand user requests:

python
# Example interpretations:
"Quiero una cita mañana a las 3pm"
  → intent: BOOK_APPOINTMENT
  → date: tomorrow
  → time: 15:00
  → duration: 30 (default)

"¿Tienes disponibilidad el viernes?"
  → intent: CHECK_AVAILABILITY
  → date: next_friday
  → time: any
🔧 Implementation Status (H09)
Phase 1: Database & Core Services ✅
✅ PostgreSQL schema design

✅ Repository pattern implementation

✅ CalendarEngine with slot generation

Phase 2: Booking Logic 🔴 In Progress
🔴 Create appointment workflow

🔴 Conflict detection algorithm

🔴 Availability checking

Phase 3: External Integration ⏳ Planned
⏳ Google Calendar OAuth2 flow

⏳ Bi-directional sync

⏳ Timezone handling

Phase 4: Reminders ⏳ Planned
⏳ Pre-event reminder system

⏳ Telegram notification delivery

⏳ Email notification (secondary)

📊 Testing Strategy
Test Coverage Target: 85%+
Test Type	Count	Status
Unit Tests	40	🔴 H09
Integration Tests	25	🔴 H09
E2E Tests	16	🔴 H09
Total	81	🔴 H09
🌐 API Examples
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
Cancel Appointment
text
DELETE /api/v1/appointments/456
🔄 Differences from Other Agents
Feature	AgendaAgent	ReminderAgent
Purpose	Manage appointments	Standalone reminders
Reminders	PRE-event (15 min before)	INDEPENDENT (not tied to events)
Example	"Reminder: Meeting in 15 min"	"Buy milk tomorrow at 10am"
Data	Linked to appointment	Self-contained message
📂 File Locations
text
src/theaia/agents/agenda_agent/
├── agent.py                    # Main AgendaAgent class
├── handler.py                  # Command handler
├── fsm_machine.py              # State machine
├── context_manager.py          # Context handling
├── conversation_manager.py     # Conversation flow
├── datetime_parser.py          # Date/time parsing
├── intent_parser.py            # Intent extraction
├── nlp_engine.py               # NLP processing
├── orchestrator.py             # Agent orchestration
├── model/                      # Data models
├── schemas/                    # Pydantic schemas
├── services/                   # Business logic
├── tests/                      # Test suite
└── tools/                      # Utility functions
🚀 Roadmap
H09 (January 2026) - 🔴 Current
Implement full booking workflow

81 tests passing

Google Calendar basic sync

Telegram bot integration

H10 (February 2026) - ⏳ Next
Advanced conflict resolution

Recurring appointments

Multi-calendar support

H11+ - ⏳ Future
AI-powered scheduling suggestions

Calendar sharing

Advanced timezone handling

📖 Related Documentation
Agents Overview - All 4 agents comparison

SCHEMA.md - Project architecture

Roadmap Master - H01-H17 timeline

H09 Milestone - Current sprint details

Last Updated: 06 January 2026, 17:45 CET
Next Review: 15 January 2026 (H09 completion)
Maintained by: Agents Team