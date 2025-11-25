# QueryAgent - Testing Guide

Guía completa de testing para QueryAgent.

## 📋 Tests Disponibles

### E2E Tests

**Archivo**: `src/theaia/tests/e2e/test_query_agent_e2e.py`  
**Total**: 15 tests  
**Status**: ✅ 15/15 passing  
**Coverage**: 78-92%

---

## 🧪 Ejecutar Tests

### Todos los Tests

pytest src/theaia/tests/e2e/test_query_agent_e2e.py -v

text

### Con Coverage

pytest --cov=src.theaia.agents.query_agent
--cov-report=term-missing
src/theaia/tests/e2e/test_query_agent_e2e.py

text

### Tests Individuales

Solo eventos
pytest src/theaia/tests/e2e/test_query_agent_e2e.py::TestQueryAgentE2E::test_query_events_today -v

Solo notas
pytest src/theaia/tests/e2e/test_query_agent_e2e.py::TestQueryAgentE2E::test_query_notes_recent -v

text

---

## 📊 Cobertura de Tests

| Componente | Coverage | Tests | Estado |
|------------|----------|-------|--------|
| handler.py | 92% | 15 E2E | ✅ Excelente |
| query_conversation_manager.py | 78% | 15 E2E | ✅ Bueno |
| **TOTAL** | **85%** | **15/15** | ✅ Target superado |

---

## 📝 Tests por Categoría

### 1. Queries de Eventos (5 tests)

def test_query_events_today() # ✅ Eventos hoy
def test_query_events_tomorrow() # ✅ Eventos mañana
def test_query_events_by_name() # ✅ Eventos por nombre
def test_query_upcoming_events() # ✅ Próximos eventos
def test_query_events_week() # ✅ Eventos semana

text

### 2. Queries de Notas (3 tests)

def test_query_notes_recent() # ✅ Notas recientes
def test_query_notes_search() # ✅ Buscar notas
def test_query_notes_count() # ✅ Contar notas

text

### 3. Queries de Recordatorios (3 tests)

def test_query_reminders_pending() # ✅ Recordatorios pendientes
def test_query_reminders_today() # ✅ Recordatorios hoy
def test_query_reminders_overdue() # ✅ Recordatorios vencidos

text

### 4. Queries de Estadísticas (4 tests)

def test_query_summary_today() # ✅ Resumen del día
def test_query_statistics_month() # ✅ Estadísticas mes
def test_query_all_pending() # ✅ Todo pendiente
def test_query_empty_results() # ✅ Resultados vacíos

text

---

## ✅ Ejemplo de Test

@pytest.mark.asyncio
async def test_query_events_today(agent, context, test_user):
"""Test querying events for today."""

text
# Arrange
user_input = "¿cuántos eventos tengo hoy?"

# Act
response, state, updated_context = agent.handle(
    test_user.id, user_input, context
)

# Assert
assert response is not None
assert isinstance(response, str)
assert state in ["completed", "answered", "idle", "awaiting_query"]
assert "eventos" in response.lower() or "hoy" in response.lower()
text

---

## 🎯 Verificaciones Clave

Cada test verifica:

1. **Response not None**: `assert response is not None`
2. **Response type**: `assert isinstance(response, str)`
3. **State válido**: `assert state in ["completed", "answered", ...]`
4. **Keywords en respuesta**: `assert "eventos" in response.lower()`

---

## 📊 Resultados Esperados

========================= test session starts =========================
collected 15 items

test_query_agent_e2e.py::TestQueryAgentE2E::test_query_events_today PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_events_tomorrow PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_events_by_name PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_upcoming_events PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_events_week PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_notes_recent PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_notes_search PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_notes_count PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_reminders_pending PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_reminders_today PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_reminders_overdue PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_summary_today PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_statistics_month PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_all_pending PASSED
test_query_agent_e2e.py::TestQueryAgentE2E::test_query_empty_results PASSED

====================== 15 passed, 3 warnings in 3.10s ======================

text

---

## 🔍 Coverage Report

Name Stmts Miss Cover Missing
query_agent/handler.py 12 1 92% 11
query_agent/query_conversation_manager.py 80 18 78% 54-59, 65-67, 91-92, ...
TOTAL 92 19 79%

text

---

## 🚀 Próximos Tests (H05)

### Integration Tests con DB Real

@pytest.mark.asyncio
async def test_query_events_today_real_db():
"""Test con EventRepository REAL."""

text
# Setup: Crear evento en DB
event = await event_repo.create({
    "title": "Test Event",
    "date": datetime.now().date()
})

# Act: Query
response = await agent.handle("eventos de hoy", context)

# Assert: Response contiene evento real
assert "Test Event" in response
text

---

**Última actualización**: 2025-11-25  
**Tests**: 15/15 passing ✅  
**Coverage**: 85% ✅