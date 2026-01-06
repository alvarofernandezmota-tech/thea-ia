# ⏰ ReminderAgent — THEA IA

**Version:** 2.0  
**Last Updated:** 06 January 2026  
**Status:** ⏳ Planned (H11)  
**Priority:** MEDIUM  
**Milestone:** H11 (February 2026)

---

## 🎯 Purpose

The **ReminderAgent** manages standalone reminders (not tied to events). It handles scheduling, recurring reminders, snooze functionality, and multi-channel notifications.

**This is the INDEPENDENT REMINDERS specialist** - separate from AgendaAgent's pre-event reminders.

---

## 📋 Core Responsibilities

| Responsibility | Description | Status |
|----------------|-------------|--------|
| **Create Reminders** | Schedule one-time or recurring reminders | ⏳ H11 |
| **Modify Reminders** | Change time, message, or recurrence | ⏳ H11 |
| **Delete Reminders** | Cancel active reminders | ⏳ H11 |
| **List Reminders** | View active and upcoming reminders | ⏳ H11 |
| **One-Time Reminders** | Trigger at specific date/time | ⏳ H11 |
| **Recurring Reminders** | Daily, weekly, monthly schedules | ⏳ H11 |
| **Snooze Functionality** | Postpone reminder by X minutes | ⏳ H11 |
| **Multi-Channel Delivery** | Telegram, email, push notifications | ⏳ H11 |
| **Retry Logic** | 3 attempts on delivery failure | ⏳ H11 |

---

## 🏗️ Architecture

### Technology Stack

```yaml
# Database
reminders:
  - id, user_id, message, trigger_at
  - recurrence (null/daily/weekly/monthly)
  - channels (array: telegram/email/push)
  - status (active/triggered/snoozed/cancelled)
  - retry_count, last_attempt, created_at

# Scheduler
- APScheduler or Celery
- Cron-like scheduling
- Background task queue

# Services
- ReminderService: CRUD operations
- SchedulerService: Trigger management
- NotificationService: Multi-channel delivery
- RetryService: Failed delivery handling
Reminder Lifecycle
text
1. CREATE
   User: "Recuérdame comprar leche mañana a las 10am"
   → reminder_id: 123
   → trigger_at: 2026-01-07 10:00:00
   → status: active

2. SCHEDULE
   → Scheduler adds to queue
   → Waits until trigger_at

3. TRIGGER
   → Time reached: 2026-01-07 10:00:00
   → Send notification via Telegram
   → status: triggered

4. DELIVERY
   → Success: Mark as delivered
   → Failure: Retry (3 attempts)
   → status: delivered or failed

5. RECURRING (if applicable)
   → Calculate next trigger_at
   → Reschedule
   → status: active (for next occurrence)
🔧 Implementation Plan (H11)
Phase 1: Core Reminders ⏳
⏳ Create one-time reminder

⏳ Trigger at specific time

⏳ Delete/cancel reminder

⏳ List active reminders

Phase 2: Scheduling ⏳
⏳ APScheduler integration

⏳ Cron-like scheduling

⏳ Background task queue

⏳ Timezone handling

Phase 3: Recurring ⏳
⏳ Daily reminders

⏳ Weekly reminders

⏳ Monthly reminders

⏳ Custom intervals

Phase 4: Reliability ⏳
⏳ Multi-channel delivery

⏳ Retry logic (3 attempts)

⏳ Failure notifications

⏳ Delivery confirmation

📊 Testing Strategy
Test Coverage Target: 85%+
Test Type	Count	Status
Unit Tests	20	⏳ H11
Integration Tests	8	⏳ H11
E2E Tests	2	⏳ H11
Total	30	⏳ H11
🌐 API Examples
Create One-Time Reminder
text
POST /api/v1/reminders
Content-Type: application/json

{
  "message": "Comprar leche",
  "trigger_at": "2026-01-07T10:00:00Z",
  "channels": ["telegram"],
  "recurrence": null
}

Response:
{
  "id": "reminder_123",
  "message": "Comprar leche",
  "trigger_at": "2026-01-07T10:00:00Z",
  "status": "active",
  "created_at": "2026-01-06T17:00:00Z"
}
Create Recurring Reminder
text
POST /api/v1/reminders
Content-Type: application/json

{
  "message": "Tomar agua",
  "trigger_at": "2026-01-07T08:00:00Z",
  "recurrence": "daily",
  "channels": ["telegram", "email"]
}

Response:
{
  "id": "reminder_456",
  "message": "Tomar agua",
  "trigger_at": "2026-01-07T08:00:00Z",
  "recurrence": "daily",
  "next_trigger": "2026-01-08T08:00:00Z",
  "status": "active"
}
Snooze Reminder
text
POST /api/v1/reminders/123/snooze
Content-Type: application/json

{
  "minutes": 30
}

Response:
{
  "id": "reminder_123",
  "message": "Comprar leche",
  "trigger_at": "2026-01-07T10:30:00Z",
  "status": "snoozed",
  "snoozed_from": "2026-01-07T10:00:00Z"
}
List Active Reminders
text
GET /api/v1/reminders?status=active

Response:
{
  "reminders": [
    {
      "id": "reminder_123",
      "message": "Comprar leche",
      "trigger_at": "2026-01-07T10:00:00Z",
      "recurrence": null
    },
    {
      "id": "reminder_456",
      "message": "Tomar agua",
      "trigger_at": "2026-01-07T08:00:00Z",
      "recurrence": "daily"
    }
  ],
  "total": 2
}
🔄 Differences from AgendaAgent
Feature	AgendaAgent	ReminderAgent
Purpose	Manage appointments	Standalone reminders
Reminders	PRE-event (15 min before appointment)	INDEPENDENT (not tied to events)
Example	"Reminder: Meeting in 15 min"	"Buy milk tomorrow at 10am"
Data	Linked to appointment	Self-contained message
Recurring	Events can be recurring	Reminders can be recurring
Calendar	Syncs with Google Calendar	No calendar integration
Key Principle: ReminderAgent reminders are INDEPENDENT and NOT tied to appointments or events.

💡 Recurrence Patterns
text
# Daily
recurrence: "daily"
trigger_at: "2026-01-07 08:00:00"
next_triggers:
  - "2026-01-08 08:00:00"
  - "2026-01-09 08:00:00"
  - ...

# Weekly
recurrence: "weekly"
trigger_at: "2026-01-07 08:00:00"  # Tuesday
next_triggers:
  - "2026-01-14 08:00:00"  # Next Tuesday
  - "2026-01-21 08:00:00"
  - ...

# Monthly
recurrence: "monthly"
trigger_at: "2026-01-07 08:00:00"  # Day 7
next_triggers:
  - "2026-02-07 08:00:00"
  - "2026-03-07 08:00:00"
  - ...
🔔 Multi-Channel Delivery
Priority Order
Telegram (Primary) - Instant, reliable

Email (Secondary) - Backup if Telegram fails

Push Notifications (Future) - Mobile app

Retry Logic
text
Attempt 1: Send via Telegram
  → Failure: Wait 5 minutes
  
Attempt 2: Retry Telegram
  → Failure: Wait 10 minutes
  
Attempt 3: Send via Email (fallback)
  → Failure: Mark as failed, notify user
📂 File Locations
text
src/theaia/agents/reminder_agent/       # (H11 - to be created)
├── agent.py                             # Main ReminderAgent class
├── reminder_service.py                  # CRUD operations
├── scheduler_service.py                 # APScheduler integration
├── notification_service.py              # Multi-channel delivery
├── retry_service.py                     # Failure handling
├── recurrence.py                        # Recurrence logic
├── models/                              # Data models
├── tests/                               # Test suite
└── tools/                               # Utilities
🚀 Roadmap
H11 (February 2026) - ⏳ Planned
Implement core reminders

One-time + recurring

Multi-channel delivery

Retry logic

30 tests passing

H12 (March 2026) - ⏳ Future
Location-based reminders

Smart snooze suggestions

Reminder templates

H13+ - ⏳ Future
AI-powered reminder suggestions

Context-aware reminders

Integration with other agents

💡 Example Use Cases
text
User: "Recuérdame comprar leche mañana a las 10am"
ReminderAgent:
  → Creates one-time reminder
  → trigger_at: 2026-01-07 10:00:00
  → channels: [telegram]
  → Returns reminder_id

User: "Recuérdame tomar agua cada día a las 8am"
ReminderAgent:
  → Creates recurring reminder
  → recurrence: daily
  → trigger_at: 08:00 every day
  → Returns reminder_id

User: "Pospón el recordatorio 30 minutos"
ReminderAgent:
  → Snoozes active reminder
  → new_trigger_at: +30 minutes
  → status: snoozed

User: "Cancela todos mis recordatorios"
ReminderAgent:
  → Lists active reminders
  → Marks all as cancelled
  → Removes from scheduler
📖 Related Documentation
Agents Overview - All 4 agents comparison

SCHEMA.md - Project architecture

Roadmap Master - H01-H17 timeline

H11 Milestone - Future sprint

Last Updated: 06 January 2026, 17:54 CET
Next Review: February 2026 (H11 start)
Maintained by: Agents Team
