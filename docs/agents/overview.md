# 🤖 Agents Overview — THEA IA

**Version:** v3.0.0  
**Last Updated:** 06 January 2026  
**Status:** 1/4 Implemented (AgendaAgent)

---

## 🎯 Agent Architecture Philosophy

THEA IA uses a **specialized agent architecture** where each agent has:
- ✅ **Clear boundaries** - No functional overlap
- ✅ **Single responsibility** - One domain per agent
- ✅ **Independent operation** - Agents don't depend on each other
- ✅ **Composable** - Can be combined via orchestrator

---

## 📊 The 4 Core Agents

| Agent | Status | Milestone | Purpose | Priority |
|-------|--------|-----------|---------|----------|
| **AgendaAgent** | 🔴 Implementing | H09 (Jan 2026) | Booking & scheduling | CRITICAL |
| **QueryAgent** | ⏳ Planned | H10 (Feb 2026) | Semantic search & QA | HIGH |
| **NoteAgent** | ⏳ Planned | H10 (Feb 2026) | Note management | HIGH |
| **ReminderAgent** | ⏳ Planned | H11 (Feb 2026) | Independent reminders | MEDIUM |

---

## 1️⃣ AgendaAgent (Booking) 📅

### Status
- **Milestone:** H09 (January 2026)
- **Implementation:** 🔴 In Progress
- **Priority:** CRITICAL
- **Tests:** 81 planned
- **LOC:** ~3,000

### Purpose
Manages events, appointments, and calendar operations. Handles all booking-related functionality with conflict detection and external calendar sync.

### Core Responsibilities

#### ✅ Event Management
- **Create appointments** with date, time, attendees
- **Modify appointments** (reschedule, update attendees)
- **Cancel appointments** with proper cleanup
- **List appointments** by date range

#### ✅ Availability Management
- **Generate time slots** (9am-6pm, 30min intervals)
- **Check availability** for specific date/time
- **Detect conflicts** (prevent overbooking)
- **Business hours** configuration

#### ✅ Calendar Integration
- **Google Calendar sync** (primary integration)
- **Timezone support** (UTC ↔ local conversion)
- **Recurring appointments** (future)

#### ✅ Reminders
- **Pre-event reminders** (15 min before, 1 hour before)
- **Configurable reminder times**
- **Multi-channel delivery** (Telegram, email)

### Technology Stack

```python
# Database Tables
appointments:
  - id, user_id, date, start_time, end_time
  - notes, status (booked/cancelled/completed)
  - reminder_minutes, created_at, updated_at

availability:
  - id, date, time_slot, available
  - updated_at

# Services
- CalendarEngine: slot generation, conflict detection
- BookingService: CRUD operations
- GoogleCalendarSync: external integration
- GroqLLM: natural language understanding
Natural Language Understanding
python
# Groq LLM interprets user requests:
"Quiero una cita mañana a las 3pm"
  → intent: BOOK_APPOINTMENT
  → date: tomorrow
  → time: 15:00

"¿Tienes disponibilidad el viernes?"
  → intent: CHECK_AVAILABILITY
  → date: next_friday
  → time: any
API Examples
python
# Create appointment
POST /api/v1/appointments
{
  "user_id": 123,
  "date": "2026-01-07",
  "time": "15:00",
  "duration": 30,
  "notes": "Consulta médica"
}

# Check availability
GET /api/v1/appointments/availability?date=2026-01-07

# Cancel appointment
DELETE /api/v1/appointments/456
File Location
Spec: docs/agents/agent_agenda.md

Code: src/theaia/agents/agenda_agent.py (H09)

Tests: tests/agents/test_agenda_agent.py (H09)

2️⃣ QueryAgent (Search) 🔍
Status
Milestone: H10 (February 2026)

Implementation: ⏳ Planned

Priority: HIGH

Tests: 40 planned

LOC: ~2,000

Purpose
Performs intelligent searches using semantic understanding. Answers questions by searching across multiple data sources (notes, events, documents).

Core Responsibilities
✅ Semantic Search
Meaning-based search (not just keywords)

Vector embeddings for content similarity

Contextual understanding

Multi-language support (Spanish, English)

✅ Question Answering
Direct answers to user questions

"When is my next appointment?" → "Tomorrow at 3pm"

"What did I note about roadmap?" → Extract relevant info

Citation support (show sources)

✅ Multi-Source Search
Search across notes

Search across events/appointments

Search across documents

Unified results with relevance ranking

✅ Entity Extraction
Extract dates from text

Extract names (people, places)

Extract key concepts

Relationship detection

Technology Stack
python
# NLP Models
- Embedding: sentence-transformers/all-MiniLM-L6-v2
- QA Model: deepset/roberta-base-squad2
- Search Engine: PostgreSQL full-text + vector search

# Database
- Vector embeddings table
- Full-text search indexes
- Relevance scoring cache

# Services
- SemanticSearchService: vector similarity search
- QuestionAnsweringService: extract answers from context
- EntityExtractor: NER and entity linking
Difference from Other Agents
Agent	Responsibility
AgendaAgent	Creates/modifies appointments
QueryAgent	Searches/answers questions about appointments
NoteAgent	Creates/modifies notes
QueryAgent	Searches within notes with NLP
API Examples
python
# Semantic search
POST /api/v1/query/search
{
  "query": "roadmap planning meetings",
  "sources": ["notes", "events"],
  "limit": 10
}

# Question answering
POST /api/v1/query/ask
{
  "question": "¿Cuándo es mi próxima reunión?",
  "context": ["events"]
}
File Location
Spec: docs/agents/agent_query.md

Code: src/theaia/agents/query_agent.py (H10)

Tests: tests/agents/test_query_agent.py (H10)

3️⃣ NoteAgent (Notes) 📝
Status
Milestone: H10 (February 2026)

Implementation: ⏳ Planned

Priority: HIGH

Tests: 40 planned

LOC: ~2,000

Purpose
Manages user notes with full-text search, tagging, and organization capabilities. Handles creation, modification, and organization of markdown notes.

Core Responsibilities
✅ Note Management
Create notes with title and markdown content

Edit notes (modify title/content)

Delete notes (soft delete to archive)

List notes with filtering

✅ Search & Organization
Full-text search (PostgreSQL ts_vector)

Tag-based filtering

Date range filtering

Relevance ranking

✅ Tagging System
Manual tags (user-defined)

Auto-tagging with NLP (topic extraction)

Tag suggestions based on content

Tag hierarchies (future)

✅ Smart Features
Duplicate detection (similarity > 0.9)

Related notes suggestions

Archive old notes

Version history (future)

Technology Stack
python
# Database
notes:
  - id, user_id, title, content (markdown)
  - tags (array), created_at, updated_at
  - archived (bool), embedding (vector)

# Indexes
- Full-text: to_tsvector('spanish', content)
- Tags: GIN index on tags array
- Vector: similarity search index

# Services
- NoteService: CRUD operations
- FullTextSearchService: PostgreSQL search
- AutoTaggerService: NLP-based topic extraction
- DuplicateDetector: embedding similarity
Difference from Other Agents
Agent	Responsibility
NoteAgent	Manages notes (create/edit/organize)
QueryAgent	Searches within notes (doesn't modify)
API Examples
python
# Create note
POST /api/v1/notes
{
  "title": "Roadmap Q1",
  "content": "# Q1 Goals\n- Feature A\n- Feature B",
  "tags": ["planning", "roadmap"]
}

# Search notes
GET /api/v1/notes/search?q=roadmap&tags=planning

# Auto-tag
POST /api/v1/notes/123/auto-tag
→ Returns: ["planning", "product", "quarterly"]
File Location
Spec: docs/agents/agent_note.md

Code: src/theaia/agents/note_agent.py (H10)

Tests: tests/agents/test_note_agent.py (H10)

4️⃣ ReminderAgent (Reminders) ⏰
Status
Milestone: H11 (February 2026)

Implementation: ⏳ Planned

Priority: MEDIUM

Tests: 30 planned

LOC: ~1,500

Purpose
Manages standalone reminders (not tied to events). Handles scheduling, recurring reminders, and multi-channel notifications.

Core Responsibilities
✅ Reminder Management
Create reminders with message and trigger time

Modify reminders (change time/message)

Delete reminders

List active reminders

✅ Scheduling
One-time reminders (specific date/time)

Recurring reminders (daily, weekly, monthly)

Relative reminders ("in 2 hours", "tomorrow at 9am")

Snooze functionality (postpone reminder)

✅ Multi-Channel Notifications
Telegram (primary channel)

Email (secondary)

Push notifications (future)

SMS (future, optional)

✅ Reliability
Retry logic (3 attempts)

Delivery confirmation

Failure notifications

Queue management

Technology Stack
python
# Database
reminders:
  - id, user_id, message, trigger_at
  - recurrence (null/daily/weekly/monthly)
  - channels (array: telegram/email/push)
  - status (active/triggered/snoozed/cancelled)
  - retry_count, last_attempt, created_at

# Scheduler
- Celery or APScheduler
- Cron-like scheduling
- Background task queue

# Services
- ReminderService: CRUD operations
- SchedulerService: trigger management
- NotificationService: multi-channel delivery
- RetryService: failed delivery handling
Difference from AgendaAgent
Feature	AgendaAgent	ReminderAgent
Purpose	Manage appointments	Standalone reminders
Reminders	PRE-event (15 min before appointment)	INDEPENDENT (not tied to events)
Example	"Reminder: Meeting in 15 min"	"Buy milk tomorrow at 10am"
Data	Linked to appointment	Self-contained message
API Examples
python
# Create reminder
POST /api/v1/reminders
{
  "message": "Comprar leche",
  "trigger_at": "2026-01-07T10:00:00Z",
  "channels": ["telegram"],
  "recurrence": null
}

# Create recurring reminder
POST /api/v1/reminders
{
  "message": "Tomar agua",
  "trigger_at": "2026-01-07T08:00:00Z",
  "recurrence": "daily",
  "channels": ["telegram", "email"]
}

# Snooze reminder
POST /api/v1/reminders/123/snooze
{
  "minutes": 30
}
File Location
Spec: docs/agents/agent-reminder.md

Code: src/theaia/agents/reminder_agent.py (H11)

Tests: tests/agents/test_reminder_agent.py (H11)

🔄 Agent Interaction Patterns
Pattern 1: AgendaAgent + ReminderAgent
text
User: "Agenda cita mañana 3pm con recordatorio 1 hora antes"

1. AgendaAgent:
   - Creates appointment for tomorrow 15:00
   - Returns appointment_id: 456

2. AgendaAgent (internal):
   - Creates PRE-EVENT reminder automatically
   - "Tienes cita en 1 hora" at 14:00
   - Linked to appointment_id: 456
Pattern 2: QueryAgent + NoteAgent
text
User: "¿Qué notas tengo sobre roadmap?"

1. QueryAgent:
   - Performs semantic search in notes
   - Finds: "Roadmap Q1", "H09 Planning", "Feature Roadmap"
   - Returns results with relevance scores

2. User: "Edita la nota de Q1"

3. NoteAgent:
   - Opens note "Roadmap Q1"
   - Allows editing
   - Saves changes
Pattern 3: AgendaAgent + QueryAgent
text
User: "¿Cuándo es mi próxima reunión?"

1. QueryAgent:
   - Question answering mode
   - Searches in appointments table
   - Returns: "Mañana a las 15:00"

User: "Cancélala"

2. AgendaAgent:
   - Identifies appointment_id from context
   - Cancels appointment
   - Confirms: "Cita cancelada"
📊 Agent Comparison Table
Feature	AgendaAgent	QueryAgent	NoteAgent	ReminderAgent
Domain	Appointments	Search & QA	Notes	Reminders
Primary Action	Create/Modify	Search/Answer	Create/Edit	Schedule
Data Source	appointments	All sources	notes	reminders
NLP	Date parsing	Semantic search	Auto-tagging	Time parsing
External API	Google Calendar	-	-	-
Notifications	Pre-event	-	-	Multi-channel
Milestone	H09	H10	H10	H11
Status	🔴 Implementing	⏳ Planned	⏳ Planned	⏳ Planned
🧪 Testing Strategy
Agent-Specific Tests
Each agent has:

Unit tests - Individual methods

Integration tests - Database operations

E2E tests - Full user flows

Cross-Agent Tests (H12+)
AgendaAgent + ReminderAgent integration

QueryAgent searching across all agents

Orchestrator coordinating multiple agents

🎯 Development Roadmap
text
H09 (Jan 2026) - AgendaAgent
├─ Bot Telegram
├─ Calendar Engine
├─ Google Calendar sync
└─ 81 tests

H10 (Feb 2026) - QueryAgent + NoteAgent
├─ Semantic search
├─ Note management
├─ Auto-tagging
└─ 80 tests

H11 (Feb 2026) - ReminderAgent
├─ Scheduling system
├─ Multi-channel notifications
├─ Recurring reminders
└─ 30 tests

H12+ (Mar 2026+) - Integration
├─ Cross-agent workflows
├─ Orchestrator improvements
└─ Advanced features
📖 Related Documentation
SCHEMA.md - Complete project overview

Roadmap Master - H01-H17 timeline

Architecture Overview - System design

Individual Agent Specs:

AgendaAgent

QueryAgent

NoteAgent

ReminderAgent

Last Updated: 06 January 2026, 16:38 CET
Version: v3.0.0
Next Review: February 2026 (H10 completion)