# e2e/ - End-to-End Tests

Tests de flujos completos end-to-end de usuario.

---

## 📋 Overview

Tests de flujos completos con características:

- 🎭 **Flujos reales** de usuario completos
- 🌐 **Todo el stack** (entrada → procesamiento → salida)
- 🐌 **Lentos** (~1-5 segundos por test)
- 🎯 **Críticos** (10% del total, pero esenciales)

---

## 📁 Estructura

e2e/
├── test_agenda_agent_e2e.py # ✅ AgendaAgent (17 tests)
├── test_note_agent_e2e.py # ✅ NoteAgent (14 tests)
├── test_reminder_agent_e2e.py # ✅ ReminderAgent (15 tests)
├── test_context_flow.py # ✅ Context persistence (1 test)
├── test_core_flow.py # ✅ Core flow (1 test)
├── test_fsm_disambiguation.py # ✅ FSM disambiguation (1 test)
└── test_notas_flow.py # ✅ Notes flow (1 test)

text

**Total E2E Tests: 50 tests**

---

## 🚀 Quick Start

Ejecutar todos los E2E tests
pytest src/theaia/tests/e2e/ -v

Solo AgendaAgent
pytest src/theaia/tests/e2e/test_agenda_agent_e2e.py -v

Con markers específicos
pytest -m e2e -v

Skip E2E (son lentos)
pytest -m "not e2e" -v

text

---

## ✅ Tests Implementados

### **📅 AgendaAgent E2E (17 tests)**
`test_agenda_agent_e2e.py` - Flujos completos de eventos:

#### Creation & Listing
- ✅ `test_create_event_basic` - Crear evento simple
- ✅ `test_create_event_with_time` - Evento con hora
- ✅ `test_create_event_with_location` - Evento con ubicación
- ✅ `test_list_events_empty` - Lista vacía de eventos
- ✅ `test_list_events_with_items` - Lista con eventos

#### Complex Flows
- ✅ `test_create_multiple_events` - Crear múltiples eventos
- ✅ `test_agenda_view_flow` - Flujo completo de visualización
- ✅ `test_event_with_reminder` - Evento con recordatorio
- ✅ `test_recurring_event` - Evento recurrente

#### Edge Cases
- ✅ `test_create_event_invalid_date` - Fecha inválida
- ✅ `test_event_conflict_detection` - Detección conflictos
- ✅ `test_cancel_event` - Cancelar evento
- ✅ `test_edit_event` - Editar evento existente

#### Integration
- ✅ `test_agenda_context_persistence` - Persistencia contexto
- ✅ `test_agenda_error_recovery` - Recuperación de errores
- ✅ `test_multiple_users` - Múltiples usuarios
- ✅ `test_full_agenda_workflow` - Flujo completo inicio a fin

---

### **📝 NoteAgent E2E (14 tests)**
`test_note_agent_e2e.py` - Flujos completos de notas:

#### CRUD Operations
- ✅ `test_create_note_basic` - Crear nota simple
- ✅ `test_create_note_with_category` - Nota con categoría
- ✅ `test_create_note_with_tags` - Nota con tags
- ✅ `test_list_notes` - Listar todas las notas
- ✅ `test_view_note_detail` - Ver detalle nota
- ✅ `test_edit_note` - Editar nota existente
- ✅ `test_delete_note` - Eliminar nota

#### Advanced Features
- ✅ `test_search_notes` - Búsqueda de notas
- ✅ `test_pin_note` - Fijar nota importante
- ✅ `test_categorize_notes` - Organizar por categorías
- ✅ `test_tag_filtering` - Filtrar por tags

#### Complete Flows
- ✅ `test_note_full_lifecycle` - Ciclo vida completo
- ✅ `test_multiple_notes_management` - Gestión múltiples notas
- ✅ `test_note_context_switching` - Cambio contexto

---

### **⏰ ReminderAgent E2E (15 tests)**
`test_reminder_agent_e2e.py` - Flujos completos de recordatorios:

#### Time-based Reminders
- ✅ `test_create_reminder_basic` - Recordatorio simple
- ✅ `test_create_reminder_tomorrow` - "Mañana"
- ✅ `test_create_reminder_specific_time` - Hora específica
- ✅ `test_create_reminder_relative` - "En 3 días"
- ✅ `test_create_reminder_weekday` - "El lunes"

#### Management
- ✅ `test_list_reminders` - Listar recordatorios
- ✅ `test_edit_reminder` - Editar recordatorio
- ✅ `test_complete_reminder` - Completar recordatorio
- ✅ `test_delete_reminder` - Eliminar recordatorio
- ✅ `test_snooze_reminder` - Posponer recordatorio

#### Advanced
- ✅ `test_reminder_with_location` - Con ubicación
- ✅ `test_recurring_reminder` - Recordatorio recurrente
- ✅ `test_priority_reminders` - Prioridades

#### Complete Flows
- ✅ `test_reminder_full_lifecycle` - Ciclo completo
- ✅ `test_multiple_reminders_workflow` - Múltiples recordatorios

---

### **🔄 Context & FSM Flows (4 tests)**
- ✅ `test_context_flow.py` - Persistencia de contexto
- ✅ `test_core_flow.py` - Flujo core del sistema
- ✅ `test_fsm_disambiguation.py` - Desambiguación FSM
- ✅ `test_notas_flow.py` - Flujo completo notas

---

## 💡 Ejemplo E2E Test

test_agenda_agent_e2e.py
import pytest
from src.theaia.agents.agenda_agent.handler import AgendaAgentHandler

@pytest.mark.asyncio
async def test_create_event_with_time(db_session, mock_user):
"""
E2E: Usuario crea evento con fecha y hora específica.

text
Flow:
1. Usuario dice "Reunión con cliente mañana 15:00"
2. Sistema extrae: fecha (mañana), hora (15:00), título (Reunión con cliente)
3. Sistema crea evento en DB
4. Sistema confirma al usuario
"""
# Arrange
handler = AgendaAgentHandler(db_session)
user_message = "Reunión con cliente mañana 15:00"

# Act
response = await handler.handle_message(
    user_id=mock_user.id,
    message=user_message
)

# Assert - Response
assert response["status"] == "success"
assert "evento creado" in response["message"].lower()
assert "Reunión con cliente" in response["message"]
assert "mañana" in response["message"].lower()
assert "15:00" in response["message"]

# Assert - Database
from src.theaia.database.models import Event
events = await db_session.execute(
    select(Event).where(Event.user_id == mock_user.id)
)
events = list(events.scalars())

assert len(events) == 1
event = events
assert "cliente" in event.title.lower()
assert event.datetime.hour == 15
assert event.datetime.minute == 0
text

---

## ✅ Características E2E

**✅ Debe:**
- Simular flujo de usuario real completo
- Testear happy paths críticos
- Verificar DB + lógica + respuesta
- Cubrir journey completo (start → finish)

**❌ NO debe:**
- Testear todos los edge cases (→ unit tests)
- Depender de servicios externos reales
- Tardar >10 segundos por test
- Duplicar cobertura de unit tests

---

## 📊 Coverage Stats (15 Nov 2025)

| Agent/Component | E2E Tests | Status |
|-----------------|-----------|--------|
| AgendaAgent | 17 | ✅ Complete |
| NoteAgent | 14 | ✅ Complete |
| ReminderAgent | 15 | ✅ Complete |
| Context/FSM | 4 | ✅ Complete |
| **TOTAL E2E** | **50** | ✅ |

**E2E Coverage:** ~30% de casos de uso críticos  
**Execution Time:** ~15-20 segundos total

---

## 🎯 Test Patterns

### AAA Pattern
async def test_example():
# Arrange - Setup
handler = AgentHandler(db_session)
user_message = "crear nota importante"

text
# Act - Execute
response = await handler.handle(user_id, user_message)

# Assert - Verify
assert response["status"] == "success"
# ... verify DB, response, etc.
text

### Database Verification
Always verify DB consistency
notes = await db_session.execute(
select(Note).where(Note.user_id == user.id)
)
notes = list(notes.scalars())
assert len(notes) == 1
assert notes.title == "importante"

text

### Context Verification
Verify context is maintained
assert "context" in response
assert response["context"]["state"] == "awaiting_confirmation"

text

---

## 🐌 Performance

E2E tests son inherentemente más lentos:

- **Target:** <5 segundos por test
- **Total suite:** <30 segundos
- **Optimizations:**
  - Mock external services
  - Database fixtures rápidos
  - Parallel execution donde posible

---

## 🎯 Next Steps (Phase 4+)

**Additional E2E Tests:**
- [ ] Multi-agent workflows
- [ ] Error recovery scenarios
- [ ] Performance under load
- [ ] Telegram integration tests (con mock)

**Improvements:**
- [ ] Faster DB fixtures
- [ ] Better test data factories
- [ ] Parallel test execution
- [ ] CI/CD integration optimizations

---

**Implementado:** H03 (15-16 Nov 2025)  
**Última actualización:** 15 Nov 2025, 23:56 CET
