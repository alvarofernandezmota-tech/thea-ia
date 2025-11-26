# EventAgent - Testing Documentation

Documentación completa de testing para EventAgent.

**Última actualización:** 25 Noviembre 2025  
**Versión:** 1.0.0  
**Status:** ⏳ Tests pendientes (implementación H04)

---

## 📊 Test Suite Overview

### Estado Actual

╔════════════════════════════════════════════════════════╗
║ EVENT AGENT TEST SUITE - STATUS ║
╠════════════════════════════════════════════════════════╣
║ Código: ✅ 100% Implementado ║
║ - Handler: 13 LOC ║
║ - Manager: 112 LOC ║
║ - FSM: 91 LOC ║
║ ║
║ Tests: ⏳ PENDIENTE H04 ║
║ - Unit Tests: 0/TBD ║
║ - E2E Tests: 0/TBD ║
║ - Integration: 0/TBD ║
║ ║
║ Coverage Target: ≥70% ║
║ Coverage Actual: 0% (no tests ejecutados) ║
╠════════════════════════════════════════════════════════╣
║ PRÓXIMO: Implementar suite completa en H04 ║
╚════════════════════════════════════════════════════════╝

text

---

## 🎯 Test Strategy (Planificado H04)

### Test Pyramid

text
                ┌─────────────┐
                │   E2E (15)  │  ← Flujos completos
                └─────────────┘
              ┌─────────────────┐
              │ Integration (8)  │  ← FSM + ML
              └─────────────────┘
          ┌───────────────────────┐
          │    Unit Tests (25)     │  ← Componentes
          └───────────────────────┘
TOTAL ESTIMADO: ~48 tests
TARGET COVERAGE: ≥70%
EXECUTION TIME: <15 seconds

text

---

## 🧪 Test Categories (Planificadas)

### 1. Unit Tests (25 tests estimados)

#### 1.1 Handler Tests (8 tests)

**Archivo:** `src/theaia/agents/event_agent_new/tests/test_handler.py`

Tests planificados:
class TestEventAgentHandler:
"""Test suite para EventAgent handler."""

text
def test_handler_initialization(self):
    """Verifica inicialización correcta."""
    agent = EventAgent(user_id="test_user_123")
    assert agent.user_id == "test_user_123"
    assert agent.conversation_manager is not None

def test_get_supported_intents(self):
    """Verifica lista de intents."""
    agent = EventAgent(user_id="test_user")
    intents = agent.get_supported_intents()
    assert "crear_evento" in intents
    assert "listar_eventos" in intents
    assert len(intents) == 9

def test_can_handle_valid_intents(self):
    """Verifica reconocimiento de intents válidos."""
    agent = EventAgent(user_id="test_user")
    assert agent.can_handle("crear_evento")
    assert agent.can_handle("evento")
    assert agent.can_handle("agendar")

def test_can_handle_invalid_intents(self):
    """Verifica rechazo de intents inválidos."""
    agent = EventAgent(user_id="test_user")
    assert not agent.can_handle("crear_recordatorio")
    assert not agent.can_handle("unknown_intent")

async def test_handle_message_basic(self):
    """Verifica manejo básico de mensajes."""
    agent = EventAgent(user_id="test_user")
    response, state, context = await agent.handle(
        user_id="test_user",
        message="Quiero crear un evento",
        context={}
    )
    assert response is not None
    assert state == "awaiting_event_title"
    assert isinstance(context, dict)

async def test_handle_message_with_context(self):
    """Verifica preservación de contexto."""
    agent = EventAgent(user_id="test_user")
    initial_context = {"previous_data": "test"}
    response, state, context = await agent.handle(
        user_id="test_user",
        message="Reunión",
        context=initial_context
    )
    assert "previous_data" in context

def test_multi_user_isolation(self):
    """Verifica aislamiento entre usuarios."""
    agent1 = EventAgent(user_id="user_1")
    agent2 = EventAgent(user_id="user_2")
    assert agent1.user_id != agent2.user_id
    assert agent1.conversation_manager != agent2.conversation_manager

async def test_error_handling(self):
    """Verifica manejo de errores."""
    agent = EventAgent(user_id="test_user")
    # Test con input inválido
    response, state, context = await agent.handle(
        user_id="test_user",
        message="",
        context={}
    )
    assert "error" in response.lower() or state == "idle"
text

#### 1.2 ConversationManager Tests (12 tests)

**Archivo:** `src/theaia/agents/event_agent_new/tests/test_conversation_manager.py`

Tests planificados:
class TestEventConversationManager:
"""Test suite para EventConversationManager."""

text
def test_manager_initialization(self):
    """Verifica inicialización del manager."""
    manager = EventConversationManager(user_id="test_user")
    assert manager.user_id == "test_user"
    assert manager.fsm is not None
    assert manager.context == {}

async def test_extract_entities_datetime(self):
    """Verifica extracción de fecha/hora."""
    manager = EventConversationManager(user_id="test_user")
    entities = await manager._extract_entities("mañana a las 15:00")
    assert "datetime" in entities
    # Verificar que datetime es correcto

async def test_extract_entities_location(self):
    """Verifica extracción de ubicación."""
    manager = EventConversationManager(user_id="test_user")
    entities = await manager._extract_entities("en la oficina")
    assert "location" in entities
    assert entities["location"] == "oficina"

async def test_handle_idle_state(self):
    """Verifica manejo del estado idle."""
    manager = EventConversationManager(user_id="test_user")
    response, state, context = await manager._handle_idle_state(
        "crear evento"
    )
    assert state == "awaiting_event_title"
    assert "título" in response.lower()

async def test_handle_awaiting_title(self):
    """Verifica captura de título."""
    manager = EventConversationManager(user_id="test_user")
    response, state, context = await manager._handle_awaiting_title(
        "Reunión de equipo"
    )
    assert state == "awaiting_event_datetime"
    assert context["event_title"] == "Reunión de equipo"

async def test_handle_awaiting_datetime(self):
    """Verifica captura de fecha/hora."""
    manager = EventConversationManager(user_id="test_user")
    manager.context = {"event_title": "Test"}
    entities = {"datetime": "2025-11-26 15:00"}
    response, state, context = await manager._handle_awaiting_datetime(
        "mañana a las 15:00",
        entities
    )
    assert state == "awaiting_event_location"
    assert "event_datetime" in context

async def test_handle_awaiting_location(self):
    """Verifica captura de ubicación."""
    manager = EventConversationManager(user_id="test_user")
    entities = {"location": "Sala A"}
    response, state, context = await manager._handle_awaiting_location(
        "en la sala A",
        entities
    )
    assert state == "awaiting_event_description"
    assert context["event_location"] == "Sala A"

async def test_handle_awaiting_description(self):
    """Verifica captura de descripción."""
    manager = EventConversationManager(user_id="test_user")
    response, state, context = await manager._handle_awaiting_description(
        "Discutir roadmap Q1"
    )
    assert state == "awaiting_confirmation"
    assert context["event_description"] == "Discutir roadmap Q1"

async def test_handle_confirmation_yes(self):
    """Verifica confirmación positiva."""
    manager = EventConversationManager(user_id="test_user")
    manager.context = {
        "event_title": "Test",
        "event_datetime": "2025-11-26 15:00"
    }
    response, state, context = await manager._handle_confirmation("sí")
    assert state == "event_confirmed"
    assert context["event_confirmed"] == True

async def test_handle_confirmation_no(self):
    """Verifica cancelación."""
    manager = EventConversationManager(user_id="test_user")
    response, state, context = await manager._handle_confirmation("no")
    assert state == "idle"
    assert len(context) == 1  # Solo state

def test_build_event_summary(self):
    """Verifica generación de resumen."""
    manager = EventConversationManager(user_id="test_user")
    manager.context = {
        "event_title": "Test Event",
        "event_datetime": "2025-11-26 15:00",
        "event_location": "Sala A",
        "event_description": "Test description"
    }
    summary = manager._build_event_summary()
    assert "Test Event" in summary
    assert "Sala A" in summary
    assert "Test description" in summary

def test_reset_context(self):
    """Verifica reset de contexto."""
    manager = EventConversationManager(user_id="test_user")
    manager.context = {"data": "test"}
    manager.reset()
    assert manager.context == {"state": "idle"}
text

#### 1.3 FSM Tests (5 tests)

**Archivo:** `src/theaia/agents/event_agent_new/tests/test_event_fsm.py`

Tests planificados:
class TestEventFSM:
"""Test suite para EventFSM."""

text
def test_fsm_initialization(self):
    """Verifica inicialización del FSM."""
    fsm = EventFSM()
    assert fsm.current_state == "idle"
    assert len(fsm.states) == 7

def test_valid_transitions(self):
    """Verifica transiciones válidas."""
    fsm = EventFSM()
    assert fsm.can_transition("idle", "awaiting_event_title")
    assert fsm.can_transition("awaiting_event_title", "awaiting_event_datetime")
    assert fsm.can_transition("awaiting_confirmation", "event_confirmed")

def test_invalid_transitions(self):
    """Verifica que transiciones inválidas se rechacen."""
    fsm = EventFSM()
    assert not fsm.can_transition("idle", "event_confirmed")
    assert not fsm.can_transition("awaiting_event_title", "idle")

def test_get_available_transitions(self):
    """Verifica obtención de transiciones disponibles."""
    fsm = EventFSM()
    transitions = fsm.get_available_transitions("idle")
    assert "awaiting_event_title" in transitions

def test_state_history(self):
    """Verifica historial de estados."""
    fsm = EventFSM()
    fsm.transition("awaiting_event_title")
    fsm.transition("awaiting_event_datetime")
    assert len(fsm.history) == 2
    assert fsm.history == "idle"
text

---

### 2. E2E Tests (15 tests estimados)

**Archivo:** `src/theaia/agents/tests/test_event_agent_e2e.py`

Tests E2E planificados:
class TestEventAgentE2E:
"""End-to-end tests para flujos completos."""

text
async def test_create_event_complete_flow(self):
    """Test: Crear evento completo paso a paso."""
    # Flujo completo desde inicio hasta confirmación

async def test_create_event_minimal(self):
    """Test: Crear evento solo con título y fecha."""
    # Sin ubicación ni descripción

async def test_create_event_online(self):
    """Test: Crear evento online."""
    # Ubicación = "online" o "virtual"

async def test_create_event_with_location(self):
    """Test: Crear evento con ubicación específica."""
    # Extracción de ubicación compleja

async def test_create_event_with_description(self):
    """Test: Crear evento con descripción detallada."""
    # Descripción larga y compleja

async def test_cancel_event_creation(self):
    """Test: Cancelar creación en confirmación."""
    # Usuario dice "no" en confirmación

async def test_list_events(self):
    """Test: Listar eventos próximos."""
    # Pre: 3 eventos creados
    # Acción: Listar

async def test_edit_event(self):
    """Test: Editar evento existente."""
    # Cambiar fecha, hora o ubicación

async def test_cancel_event(self):
    """Test: Cancelar evento."""
    # Eliminar evento creado

async def test_view_event_details(self):
    """Test: Ver detalles de evento."""
    # Mostrar toda la información

async def test_multiple_events_same_day(self):
    """Test: Crear múltiples eventos mismo día."""
    # Verificar sin conflictos

async def test_event_past_date_error(self):
    """Test: Error al crear evento en fecha pasada."""
    # Validación de fecha futura

async def test_multi_user_event_isolation(self):
    """Test: Aislamiento de eventos entre usuarios."""
    # User A no ve eventos de User B

async def test_complex_datetime_extraction(self):
    """Test: Extracción de fechas complejas."""
    # "el próximo viernes 18 a las 15:30"

async def test_location_extraction_cities(self):
    """Test: Extracción de ciudades españolas."""
    # "en Madrid", "en Barcelona"
text

---

### 3. Integration Tests (8 tests estimados)

**Archivo:** `src/theaia/agents/tests/test_event_agent_integration.py`

Tests de integración planificados:
class TestEventAgentIntegration:
"""Tests de integración FSM + ML + Handler."""

text
async def test_fsm_with_entity_extraction(self):
    """Integración FSM + DateTimeExtractor."""
    # Verificar flujo completo con extracción real

async def test_fsm_with_location_extraction(self):
    """Integración FSM + LocationExtractor."""
    # Verificar extracción de ubicaciones

async def test_context_preservation_across_states(self):
    """Verificar preservación de contexto."""
    # Context se mantiene entre transiciones

async def test_error_recovery(self):
    """Verificar recuperación de errores."""
    # FSM se recupera de estados inválidos

async def test_concurrent_conversations(self):
    """Verificar conversaciones concurrentes."""
    # Múltiples usuarios simultáneos

async def test_state_timeout_handling(self):
    """Verificar timeout de estados."""
    # Estados expiran después de N minutos

async def test_database_integration(self):
    """Integración con EventRepository (H05)."""
    # CRUD completo

async def test_notification_integration(self):
    """Integración con sistema de notificaciones (H05)."""
    # Envío de recordatorios
text

---

## 🚀 Running Tests (Comandos Planificados)

### Comandos Básicos

Todos los tests de EventAgent
pytest src/theaia/agents/event_agent_new/tests/ -v

Solo unit tests
pytest src/theaia/agents/event_agent_new/tests/test_handler.py -v

Solo E2E tests
pytest src/theaia/agents/tests/test_event_agent_e2e.py -v

Con coverage
pytest src/theaia/agents/event_agent_new/
--cov=src/theaia/agents/event_agent_new
--cov-report=term-missing
--cov-report=html

Tests específicos
pytest src/theaia/agents/event_agent_new/tests/test_handler.py::test_handler_initialization -v

text

### Opciones Avanzadas

Con output detallado
pytest -v -s

Stop on first failure
pytest -x

Parallel execution
pytest -n auto

Con timing
pytest --durations=10

Solo tests marcados
pytest -m "unit" # Requiere markers en tests

text

---

## 📈 Coverage Targets (H04)

### Por Componente

Component Target Actual Status
─────────────────────────────────────────────
Handler 70% 0% ⏳ Pendiente
ConversationManager 70% 0% ⏳ Pendiente
FSM 70% 0% ⏳ Pendiente
Overall 70% 0% ⏳ Pendiente

text

### Por Tipo de Test

Type Count Coverage Status
────────────────────────────────────────────
Unit 25 80% ⏳ H04
Integration 8 60% ⏳ H04
E2E 15 50% ⏳ H04
────────────────────────────────────────────
TOTAL 48 ≥70% ⏳ H04

text

---

## 🎯 Test Implementation Plan (H04)

### Week 1: Unit Tests (8 horas)

Day 1 (3h): Handler Tests (8 tests)
Day 2 (4h): ConversationManager Tests (12 tests)
Day 3 (1h): FSM Tests (5 tests)

text

### Week 2: E2E Tests (10 horas)

Day 1 (4h): Basic E2E (tests 1-7)
Day 2 (4h): Advanced E2E (tests 8-15)
Day 3 (2h): Integration Tests (8 tests)

text

### Week 3: Coverage & Polish (4 horas)

Day 1 (2h): Alcanzar coverage ≥70%
Day 2 (1h): Fix failing tests
Day 3 (1h): Documentation update

text

**TOTAL: 22 horas estimadas (H04)**

---

## 🐛 Known Issues & Limitations

### Limitaciones Actuales

No hay tests implementados aún
→ Planificado para H04
→ Código está preparado para testing

Coverage 0%
→ Normal sin tests
→ Target H04: ≥70%

Sin validación automática
→ Requiere tests E2E
→ Implementar en H04

text

### Deuda Técnica

□ Implementar test fixtures
□ Crear mocks para entity extractors
□ Setup test database
□ Configurar CI/CD pipeline
□ Añadir property-based testing

text

---

## 📊 Test Metrics (Estimadas H04)

Metric Estimated
─────────────────────────────────
Total Tests 48
Unit Tests 25 (52%)
Integration Tests 8 (17%)
E2E Tests 15 (31%)
Execution Time ~12 seconds
Coverage ≥70%
Pass Rate 100%

text

---

## 🔄 CI/CD Integration (Planificado H09)

### GitHub Actions Workflow

name: EventAgent Tests

on: [push, pull_request]

jobs:
test:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v2
- name: Set up Python
uses: actions/setup-python@v2
with:
python-version: '3.11'
- name: Install dependencies
run: pip install -r requirements.txt
- name: Run tests
run: |
pytest src/theaia/agents/event_agent_new/tests/ -v --cov
pytest src/theaia/agents/tests/test_event_agent_e2e.py -v
- name: Check coverage
run: |
coverage report --fail-under=70

text

---

## 📚 Testing Best Practices

### Para Implementar en H04

Test Isolation
✓ Cada test independiente
✓ No compartir estado entre tests
✓ Cleanup después de cada test

Realistic Data
✓ Usar fechas/horas reales
✓ Datos representativos
✓ Edge cases incluidos

Clear Assertions
✓ Assertions específicas
✓ Mensajes de error claros
✓ Verificar múltiples condiciones

Fast Execution
✓ Tests rápidos (<1s cada uno)
✓ Mocks para dependencias lentas
✓ Parallel execution cuando sea posible

Comprehensive Coverage
✓ Happy paths
✓ Error paths
✓ Edge cases
✓ Multi-user scenarios

text

---

## 🎓 Testing Guidelines

### Naming Conventions

Tests descriptivos
def test_create_event_with_valid_datetime(): # ✅ Claro
def test_handler(): # ❌ Vago

Classes organizadas
class TestEventAgentHandler: # ✅ Por componente
class TestCreateEvent: # ✅ Por feature
class Tests: # ❌ Genérico

text

### Assert Patterns

Assertions específicas
assert response == "✅ Evento creado" # ✅
assert response # ❌

Múltiples verificaciones
assert event.title == "Test"
assert event.datetime is not None
assert event.location == "Sala A" # ✅

assert event # ❌

text

---

## 📝 Next Steps (H04)

### Implementación Inmediata

Crear archivos de tests
□ test_handler.py
□ test_conversation_manager.py
□ test_event_fsm.py
□ test_event_agent_e2e.py

Implementar fixtures
□ Mock user_id
□ Mock datetime
□ Mock entity extractors

Escribir unit tests (25)
□ Handler (8 tests)
□ ConversationManager (12 tests)
□ FSM (5 tests)

Escribir E2E tests (15)
□ Happy paths
□ Error scenarios
□ Multi-user

Alcanzar coverage ≥70%

Configurar CI/CD

Actualizar esta documentación

text

---

## 📚 Referencias

- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [FSM Testing Patterns](https://martinfowler.com/articles/mocksArentStubs.html)

---

## 🎯 Success Criteria (H04)

✓ 48+ tests implementados
✓ 100% tests passing
✓ ≥70% code coverage
✓ <15s execution time
✓ CI/CD pipeline configurado
✓ Documentation actualizada

text

---

**Última actualización:** 25 Noviembre 2025  
**Mantenido por:** Álvaro Fernández Mota (CEO THEA-IA)  
**Status:** ⏳ PLANIFICADO - Implementación H04  
**Estimación:** 22 horas de desarrollo
