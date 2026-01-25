# H09: Real Ecosystem - AgendaAgent 🟡

**Period:** January 2026 (Started: 06-Jan, Updated: 25-Jan)  
**Status:** 🟡 **75% COMPLETADO** - En cierre  
**Tests:** 40/81 pasando | **Coverage:** 50% (target ajustado 75%)  
**Priority:** CRITICAL (First Functional Agent)

---

## 🎯 Objective

Build the **FIRST functional agent** (AgendaAgent) with real integrations: Telegram bot, PostgreSQL database, Google Calendar, and Groq LLM. This is the transition from infrastructure to real-world functionality.

---

## 🟡 Current Status (25 January 2026, 18:47 CET)

| Component | Status | Progress | Hours |
|-----------|--------|----------|-------|
| **Groq LLM** | ✅ Complete | 100% | 15h |
| **BookingAgent** | ✅ Complete | 100% | 12h |
| **Database Services** | ✅ Mostly Complete | 85% | 10h |
| **Telegram Bot Base** | ✅ Functional | 70% | 8h |
| **Google Calendar** | ❌ Missing | 0% | 0h |
| **Commands + Menu** | ❌ Missing | 0% | 0h |
| **Tests E2E** | 🟡 Partial | 50% | ~5h |
| **TOTAL** | 🟡 | **75%** | **~45h/75h** |

---

## ✅ COMPLETADO (06-24 Enero 2026)

### 1️⃣ Groq LLM Integration ✅ (100% COMPLETE)

**Status:** ✅ **PRODUCTION READY**

**Implemented:**
- ✅ LLMClient with llama-3.3-70b-versatile model
- ✅ Tool calling fully functional
- ✅ Intent extraction (book, cancel, check, list)
- ✅ Entity extraction (date, time, duration)
- ✅ Conversation context management
- ✅ Error handling robust

**Files:**
```
src/theaia/core/conversation/
├── llm_client.py         ✅ Complete
├── llm_config.py         ✅ Complete
└── conversation.py       ✅ Complete

src/theaia/services/
└── groq_tools.py         ✅ Complete (tool calling)
```

**Tests:** 16/10 planned (100% passing)  
**Coverage:** 100%  
**Hours:** 15h (as planned)

---

### 2️⃣ BookingAgent ✅ (100% COMPLETE)

**Status:** ✅ **PRODUCTION READY**

**Implemented:**
- ✅ 100% conversational AI (LLM-based)
- ✅ Tool integration (create, check, cancel, list)
- ✅ Spanish language support
- ✅ Context-aware responses
- ✅ Natural language understanding

**File:**
```
src/theaia/agents/booking_agent.py   ✅ Complete (146 lines)
```

**Architectural Decision:**
```
ORIGINAL PLAN: FSM-based with states (initial → awaiting_date → confirming)
ACTUAL IMPLEMENTATION: 100% Conversational (LLM-based, no FSM)

REASON: More flexible, better UX, natural interactions
IMPACT: ✅ Positive - Maintained for better user experience
```

**Tests:** Integrated in groq_tools tests  
**Hours:** ~12h

---

### 3️⃣ Database Services ✅ (85% COMPLETE)

**Status:** ✅ **MOSTLY COMPLETE**

**Implemented:**
- ✅ UserService (CRUD operations)
- ✅ BookingService (appointment management)
- ✅ AvailabilityEngine (slot generation, conflict detection)
- ✅ Multi-tenant architecture
- ✅ PostgreSQL async operations

**Files:**
```
src/theaia/services/
├── user_service.py           ✅ Complete
├── booking_service.py        ✅ Complete
└── availability_engine.py    ✅ Complete
```

**NOT Implemented (Planned but deferred to H10):**
```
src/theaia/data/repositories/
├── appointment_repo.py       ❌ NOT DONE (Repository Pattern)
└── availability_repo.py      ❌ NOT DONE (Repository Pattern)
```

**Reason:** Services work well without Repository Pattern. Not critical for functionality. Aplazar a H10.

**Tests:** ~15 tests passing  
**Hours:** ~10h

---

### 4️⃣ Telegram Bot Base ✅ (70% COMPLETE)

**Status:** ✅ **FUNCTIONAL** (missing commands + menu)

**Implemented:**
- ✅ 100% conversational message handling
- ✅ User auto-registration (no /start needed)
- ✅ Conversation state management
- ✅ Per-user GroqTools instances
- ✅ BookingAgent integration
- ✅ Error handling
- ✅ Long message splitting (4096 chars)
- ✅ Typing indicators

**File:**
```
src/theaia/adapters/telegram/bot.py   ✅ Complete (222 lines)
```

**Current Philosophy:**
```python
# NO COMMANDS - Pure conversational AI
User: "Quiero cita mañana 3pm"
  → Bot receives
  → Groq extracts intent + entities
  → BookingAgent processes
  → Response sent
  → ✅ WORKS 100%
```

**NOT Implemented:**
```
src/theaia/adapters/telegram/
├── handlers.py              ❌ NOT DONE (command handlers)
├── commands.py              ❌ NOT DONE (command definitions)
├── keyboards.py             ❌ NOT DONE (interactive menus)
└── callbacks.py             ❌ NOT DONE (button handlers)
```

**Tests:** ~5 integration tests  
**Hours:** ~8h

---

## 🔴 PENDIENTE (26 Enero - 2 Febrero 2026)

### CRÍTICO 🔴 - Google Calendar API (12-15h)

**Priority:** **HIGHEST - Without this, H09 is NOT complete**

**To Implement:**
```
src/theaia/integrations/google_calendar/
├── __init__.py
├── calendar_client.py       # Google Calendar API client
├── sync_service.py          # Bi-directional sync
├── auth_handler.py          # OAuth2 authentication
└── models.py                # Calendar event models
```

**Features Required:**
- OAuth2 authentication flow
- Create/Update/Delete calendar events
- Bi-directional sync (Telegram ↔ Google Calendar)
- Event conflict detection
- Webhook support (optional)

**Tests:** 15 new E2E tests  
**Target:** 30 Enero  
**Hours:** 12-15h

**Flow:**
```python
# Telegram → Google Calendar
User: "Quiero cita mañana 3pm"
  → BookingAgent creates appointment
  → Database updated
  → Google Calendar event created ✨ NEW
  → Confirmation sent

# Google Calendar → Telegram
Event created in Google Calendar
  → Webhook received
  → Database updated
  → User notified in Telegram ✨ NEW
```

---

### ALTA 🟡 - Command Handlers + Interactive Menu (8-10h)

**Priority:** **HIGH - Better UX with commands + conversation**

**To Implement:**
```
src/theaia/adapters/telegram/commands/
├── __init__.py
├── handlers.py              # Command handlers (6 commands)
├── keyboards.py             # Interactive menus (5 menus)
└── callbacks.py             # Button click handlers
```

**Commands Required:**
1. `/start` → Welcome + main menu
2. `/help` → Show capabilities
3. `/mis_citas` → List user appointments
4. `/nueva_cita` → Start booking flow
5. `/cancelar` → Cancel appointment
6. `/disponibilidad` → Check available slots

**Interactive Menus:**
1. Main menu (5 options)
2. Date selection menu
3. Time slot selection
4. Appointment actions (modify/cancel)
5. Confirmation dialog

**Hybrid Architecture:**
```python
# Commands for quick navigation
/mis_citas → List appointments

# Conversation for complex interactions
"Quiero cita mañana 3pm para revisión"
  → BookingAgent processes naturally
```

**Tests:** 18 new tests (commands + callbacks)  
**Target:** 1 Febrero  
**Hours:** 8-10h

---

### MEDIA 🟢 - E2E Tests Complete (6-8h)

**Priority:** **MEDIUM - Ensure quality**

**To Implement:**
```
src/theaia/tests/integration/
├── test_google_calendar_sync.py     # 15 tests
├── test_commands.py                 # 18 tests
├── test_menu_flow.py                # 8 tests
└── test_complete_booking_flow.py    # Updated
```

**Test Scenarios:**
- ✅ Telegram message → DB → Confirmation (DONE)
- ✨ Telegram message → DB → Google Calendar → Confirmation (NEW)
- ✨ Google Calendar event → DB → Telegram notification (NEW)
- ✨ Commands work correctly (NEW)
- ✨ Interactive menus work (NEW)
- ✨ Conflict detection works (NEW)

**Target Coverage:** 75% (ajustado de 85%)  
**Target:** 2 Febrero  
**Hours:** 6-8h

---

### BAJA ⚪ - Repository Pattern (DEFERRED TO H10)

**Priority:** **LOW - Not critical for functionality**

**Original Plan:**
```
src/theaia/data/repositories/
├── appointment_repo.py      # Repository pattern
└── availability_repo.py     # Repository pattern
```

**Decision:** **APLAZAR A H10**
- Current services work well without Repository Pattern
- Not blocking functionality
- Can be refactored in H10 if needed

**Hours:** 6-8h (saved for H10)

---

## 📅 PLAN DE CIERRE H09 (26 Enero - 2 Febrero)

### Hito H09.1: Google Calendar API 🔴
**Deadline:** 30 Enero 2026  
**Hours:** 12-15h  
**Priority:** CRÍTICO

**Tasks:**
1. Google Cloud Project setup (OAuth2 credentials)
2. Implement `calendar_client.py`
3. Implement `sync_service.py`
4. Implement `auth_handler.py`
5. Integration with BookingAgent
6. Basic tests (15 tests)

**Success Criteria:**
- ✅ Events created in Google Calendar
- ✅ Bi-directional sync working
- ✅ Tests passing

---

### Hito H09.2: Commands + Menu 🟡
**Deadline:** 1 Febrero 2026  
**Hours:** 8-10h  
**Priority:** ALTA

**Tasks:**
1. Implement `handlers.py` (6 commands)
2. Implement `keyboards.py` (5 menus)
3. Implement `callbacks.py`
4. Update `bot.py` with hybrid mode
5. Tests (18 tests)

**Success Criteria:**
- ✅ 6 commands working
- ✅ Interactive menus functional
- ✅ Hybrid mode (commands + conversation)

---

### Hito H09.3: Tests E2E + Documentation 🟢
**Deadline:** 2 Febrero 2026  
**Hours:** 6-8h  
**Priority:** MEDIA

**Tasks:**
1. E2E tests with Google Calendar (15 tests)
2. Command tests (18 tests)
3. Update documentation
4. Final verification
5. **✅ CIERRE H09**

**Success Criteria:**
- ✅ 75+ tests passing
- ✅ Coverage ≥ 75%
- ✅ Documentation updated
- ✅ H09 COMPLETE

---

## 🎯 CRITERIOS DE CIERRE H09 (Actualizados)

### Must Have ✅
- ✅ Bot conversacional funcional (DONE)
- ✅ Groq LLM integration (DONE)
- ✅ Database services (DONE)
- 🔴 Google Calendar sync bi-direccional (PENDING)
- 🔴 Commands + Interactive menu (PENDING)
- 🔴 Tests ≥ 75 passing (40/75 DONE)
- 🔴 Coverage ≥ 75% (50% DONE)

### Should Have 🟡
- Webhook mode (optional - polling works)
- Advanced error handling
- Performance optimization

### Won't Have ⚪
- Repository Pattern (deferred to H10)
- Advanced analytics
- Multi-language support

---

## 📊 MÉTRICAS FINALES (Actualizadas 25 Enero)

| Métrica | Plan Original | Estado Actual | Target Ajustado |
|---------|---------------|---------------|-----------------|
| **Horas totales** | 75h | ~45h (60%) | 71-78h |
| **Tests** | 81 | 40 (49%) | 75 mínimo |
| **Coverage** | 85% | 50% | 75% |
| **Componentes** | 5 | 4/5 (80%) | 5/5 |
| **Google Calendar** | ✅ Planned | ❌ 0% | ✅ CRÍTICO |
| **Commands** | ✅ Planned | ❌ 0% | ✅ ALTA |
| **Production Ready** | ✅ | 🟡 75% | ✅ 100% |

---

## 🔄 CAMBIOS ARQUITECTÓNICOS REALIZADOS

### Decisión 1: Conversacional > FSM ✅
**Original Plan:** AgendaAgent with FSM states (initial → awaiting_date → confirming)  
**Actual Implementation:** 100% Conversational (LLM-based, no FSM)  
**Reason:** More flexible, better UX, natural language interactions  
**Impact:** ✅ **POSITIVE** - Better user experience, maintained

**Trade-offs:**
- ✅ More natural conversations
- ✅ Flexible interactions
- ❌ Requires LLM always active (cost)
- ❌ Less predictable flows

**Decision:** **KEEP** conversational approach

---

### Decisión 2: Repository Pattern → Deferred to H10 ⏸️
**Original Plan:** Implement Repository Pattern in H09  
**Actual Implementation:** Direct services (UserService, BookingService)  
**Reason:** Not critical for functionality, services work well  
**Impact:** ⚪ **NEUTRAL** - Can refactor later if needed

**Trade-offs:**
- ✅ Faster implementation
- ✅ Services work well
- ⚪ Less abstraction (acceptable for MVP)

**Decision:** **DEFER** to H10 (not blocking)

---

### Decisión 3: Hybrid Commands + Conversation ✅
**Original Plan:** Commands only  
**Actual Implementation:** Commands + Conversational AI (hybrid)  
**Reason:** Better UX - quick commands + flexible conversation  
**Impact:** ✅ **POSITIVE** - Best of both worlds

**Architecture:**
```python
# Quick navigation with commands
/mis_citas → Instant list

# Complex interactions with conversation
"Quiero cita mañana 3pm para revisión médica"
  → Natural language processing
```

**Decision:** **IMPLEMENT** hybrid approach in H09.2

---

## 🚨 RISKS & MITIGATIONS

### Risk 1: Google Calendar API Complexity
**Risk Level:** 🔴 HIGH  
**Mitigation:**
- Start with basic OAuth2 flow
- Use official Python library
- Implement retry logic
- Fallback to local-only mode if API fails

### Risk 2: Time Constraints (30h remaining)
**Risk Level:** 🟡 MEDIUM  
**Mitigation:**
- Focus on critical features (Google Calendar)
- Commands can be simplified (fewer menus)
- Tests can be 75 instead of 81

### Risk 3: WSL2 Environment Issues
**Risk Level:** 🟢 LOW  
**Mitigation:**
- WSL2 + PostgreSQL already working
- 64 tests passing on Linux
- Production-ready environment

---

## 📂 File Structure (Current State)

```
src/theaia/
├── adapters/
│   └── telegram/
│       ├── bot.py                   ✅ Complete
│       └── commands/                ❌ TO CREATE
│           ├── handlers.py          ❌ Pending
│           ├── keyboards.py         ❌ Pending
│           └── callbacks.py         ❌ Pending
├── agents/
│   └── booking_agent.py             ✅ Complete
├── core/
│   └── conversation/
│       ├── llm_client.py            ✅ Complete
│       └── llm_config.py            ✅ Complete
├── services/
│   ├── user_service.py              ✅ Complete
│   ├── booking_service.py           ✅ Complete
│   ├── availability_engine.py       ✅ Complete
│   └── groq_tools.py                ✅ Complete
├── integrations/                    ❌ TO CREATE
│   └── google_calendar/             ❌ Pending
│       ├── calendar_client.py       ❌ Pending
│       ├── sync_service.py          ❌ Pending
│       ├── auth_handler.py          ❌ Pending
│       └── models.py                ❌ Pending
└── tests/
    ├── unit/                        ✅ 40 tests passing
    └── integration/                 🟡 Partial (need +41 tests)
```

---

## 🎬 What's Next After H09?

### H10 (February 2026) - ⏳ Next
**Focus:** QueryAgent + Advanced Features
- QueryAgent (semantic search)
- NoteAgent improvements
- Repository Pattern (if needed)
- 80 tests planned

**Dependencies from H09:**
- ✅ Groq LLM infrastructure (ready)
- ✅ Database services (ready)
- ✅ Telegram bot (ready)

### H11 (February 2026) - ⏳ Future
**Focus:** ReminderAgent
- Standalone reminders
- Location-based reminders
- Time-based reminders
- 30 tests planned

---

## 📖 Related Documentation

- [Master Roadmap](../../ROADMAP.md) - Full H01-H17 timeline
- [SCHEMA.md](../../../docs/SCHEMA.md) - Current project state
- [H09 Planning Docs](.) - Detailed planning (this folder)
- [Previous: H08](../H08/) - FSM Production
- [Next: H10-H17](../../ROADMAP.md) - Future agents
- [Auditoría 24-Ene](../../../docs/diary/2026/enero/2026-01-24-AUDITORIA-H09.md) - Latest audit

---

## 📞 Contact & Updates

**Responsible:** Álvaro Fernández Mota (CEO THEA IA)  
**Email:** alvarofernandezmota@gmail.com  
**Started:** 06 January 2026  
**Updated:** 25 January 2026, 18:47 CET  
**Expected Completion:** 02 February 2026  
**Status:** 🟡 **75% Complete - In Closure**  
**Impact:** FIRST real functional agent - proves architecture works

---

## ✅ Quick Action Items (This Week)

### Monday 27 Jan - Tuesday 28 Jan
🔴 **Google Calendar API** (Day 1-2)
- Setup Google Cloud Project
- Implement calendar_client.py
- Basic OAuth2 flow working

### Wednesday 29 Jan - Thursday 30 Jan
🔴 **Google Calendar API** (Day 3-4)
- Implement sync_service.py
- Bi-directional sync
- Tests (15 tests)

### Friday 31 Jan - Saturday 1 Feb
🟡 **Commands + Menu** (Day 5-6)
- Implement handlers.py (6 commands)
- Implement keyboards.py (5 menus)
- Implement callbacks.py
- Tests (18 tests)

### Sunday 2 Feb
🟢 **Final Testing + Closure**
- E2E tests complete
- Documentation update
- ✅ **H09 COMPLETE**

---

**🚨 CURRENT MILESTONE - 75% COMPLETE - ACTIVE CLOSURE 🚨**
**Next Deadline: Google Calendar API - 30 January 2026**
