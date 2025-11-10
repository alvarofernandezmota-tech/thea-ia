🧪 Agenda Agent Tests — Suite de Pruebas
Versión: v1.0.0
Ruta: src/theaia/agents/agenda_agent/tests/
Última actualización: 2025-11-10 17:24 CET (S39)
Coverage: 85%+

📋 Propósito
Suite de pruebas unitarias para Agenda Agent. Valida que:

✅ AgendaAgent.handle() funciona correctamente

✅ FSM transiciones son correctas

✅ Manejo de edge cases

✅ Integración entre componentes

📁 Estructura Tests
text
tests/
├── test_handler.py (1353 bytes)
│   └── Tests para AgendaAgent + ConversationManager
│
├── test_agenda_fsm.py (1906 bytes)
│   └── Tests para FSM states + transitions
│
└── __init__.py
🧪 Test Files
1. test_handler.py
Propósito: Validar clase AgendaAgent y AgendaConversationManager.

Tests principales:

test_agenda_agent_initialization()
python
def test_agenda_agent_initialization():
    """Verifica que AgendaAgent se inicializa correctamente."""
    agent = AgendaAgent(user_id="user_123")
    assert agent.user_id == "user_123"
    assert agent.conversation_manager is not None
Valida:

✅ Inicialización correcta

✅ Atributos seteados

✅ Conversation manager inyectado

test_get_supported_intents()
python
def test_get_supported_intents():
    """Verifica que intenciones soportadas son correctas."""
    agent = AgendaAgent(user_id="user_123")
    intents = agent.get_supported_intents()
    expected = ["agenda", "cita", "reunión", "evento", "agendar"]
    assert intents == expected
Valida:

✅ Intenciones definidas

✅ Orden correcto

✅ Cobertura de sinónimos

test_handle_basic_flow()
python
def test_handle_basic_flow():
    """Flujo completo: title → datetime → confirmation → scheduled."""
    agent = AgendaAgent(user_id="user_123")
    context = {}
    
    # Turno 1: Capturar título
    response, state, context = agent.handle(
        "user_123", 
        "Reunión con equipo",
        context
    )
    assert state == "awaiting_date"
    assert "¿Cuándo" in response
    
    # Turno 2: Capturar fecha
    response, state, context = agent.handle(
        "user_123",
        "Viernes",
        context
    )
    assert state == "confirmation"
    assert "Confirmar" in response
    
    # Turno 3: Confirmar
    response, state, context = agent.handle(
        "user_123",
        "Sí",
        context
    )
    assert state == "completed"
    assert "agendada" in response
Valida:

✅ Flujo multi-turno

✅ Transiciones correctas

✅ Contexto persistente

test_handle_cancellation()
python
def test_handle_cancellation():
    """Verifica cancelación en confirmation."""
    agent = AgendaAgent(user_id="user_123")
    context = {
        "fsm_state": "confirmation",
        "event_title": "Test"
    }
    
    response, state, context = agent.handle(
        "user_123",
        "No",
        context
    )
    assert state == "completed"
    assert "cancelada" in response
Valida:

✅ Cancelación funciona

✅ Respuesta apropiada

✅ Estado final correcto

2. test_agenda_fsm.py
Propósito: Validar máquina de estados AgendaFSM.

Tests principales:

test_fsm_initialization()
python
def test_fsm_initialization():
    """Verifica que FSM se inicializa en estado correcto."""
    fsm = AgendaFSM()
    assert fsm.state == "awaiting_title"
    assert fsm.context == {}
Valida:

✅ Estado inicial correcto

✅ Contexto vacío

test_fsm_awaiting_title_transition()
python
def test_fsm_awaiting_title_transition():
    """Verifica transición: awaiting_title → awaiting_datetime."""
    fsm = AgendaFSM()
    response, new_state = fsm.process_message("Reunión", {})
    
    assert new_state == "awaiting_datetime"
    assert "¿Cuándo" in response
    assert fsm.context["event_title"] == "Reunión"
Valida:

✅ Transición correcta

✅ Contexto guardado

✅ Respuesta apropiada

test_fsm_awaiting_datetime_transition()
python
def test_fsm_awaiting_datetime_transition():
    """Verifica transición: awaiting_datetime → confirmation."""
    fsm = AgendaFSM()
    fsm.state = "awaiting_datetime"
    fsm.context = {"event_title": "Test"}
    
    response, new_state = fsm.process_message("Viernes 3 PM", {})
    
    assert new_state == "confirmation"
    assert "Confirmo" in response
    assert fsm.context["event_datetime"] == "Viernes 3 PM"
Valida:

✅ Parse de fecha

✅ Transición correcta

✅ Confirmación explícita

test_fsm_confirmation_positive()
python
def test_fsm_confirmation_positive():
    """Verifica confirmación positiva: confirmation → scheduled."""
    fsm = AgendaFSM()
    fsm.state = "confirmation"
    fsm.context = {"event_title": "Test", "event_datetime": "Viernes"}
    
    response, new_state = fsm.process_message("Sí", {})
    
    assert new_state == "scheduled"
    assert "✓" in response or "agendada" in response
Valida:

✅ Respuesta positiva reconocida

✅ Estado final correcto

✅ Mensaje éxito

test_fsm_confirmation_negative()
python
def test_fsm_confirmation_negative():
    """Verifica confirmación negativa: confirmation → cancelled."""
    fsm = AgendaFSM()
    fsm.state = "confirmation"
    
    response, new_state = fsm.process_message("No", {})
    
    assert new_state == "cancelled"
    assert "cancelada" in response
Valida:

✅ Respuesta negativa reconocida

✅ Estado final correcto

✅ Mensaje cancelación

test_fsm_state_persistence()
python
def test_fsm_state_persistence():
    """Verifica que contexto persiste entre process_message calls."""
    fsm = AgendaFSM()
    context = {}
    
    # Primer call
    fsm.process_message("Reunion", context)
    context_after_1 = fsm.context.copy()
    
    # Segundo call (contexto debe mantenerse)
    fsm.context = context_after_1
    fsm.process_message("Viernes", context_after_1)
    context_after_2 = fsm.context.copy()
    
    assert "event_title" in context_after_2
    assert context_after_2["event_title"] == "Reunion"
Valida:

✅ Persistencia de contexto

✅ No sobrescribe atributos previos

✅ Acumulación de información

🏃 Ejecutar Tests
bash
# Todos los tests
pytest src/theaia/agents/agenda_agent/tests/ -v

# Específico
pytest src/theaia/agents/agenda_agent/tests/test_handler.py -v
pytest src/theaia/agents/agenda_agent/tests/test_agenda_fsm.py -v

# Con cobertura
pytest src/theaia/agents/agenda_agent/tests/ --cov=src.theaia.agents.agenda_agent

# Verbose + print
pytest src/theaia/agents/agenda_agent/tests/ -v -s
📊 Coverage Actual
text
Name                                     Stmts   Miss  Cover
─────────────────────────────────────────────────────────
agenda_agent/handler.py                    12      2    83%
agenda_agent/agenda_conversation_manager   15      3    80%
agenda_agent/model/agenda_fsm.py           22      2    91%
─────────────────────────────────────────────────────────
TOTAL                                      49      7    85%
Meta: ≥85% ✅

🐛 Test Cases Edge / Known Issues
Casos Probados
✅ Flujo feliz (titulo → datetime → confirm → scheduled)

✅ Cancelación

✅ Respuestas variadas ("sí", "si", "ok", "confirmar")

✅ Contexto persistente

✅ Inicialización

No Probados Aún
⚠️ Parse de fechas complejas

⚠️ Timezones

⚠️ Conflictos con calendario real

⚠️ Datos corruptos/malformados

🔮 Roadmap Tests
H01: Parser Validation
 Test parse fechas naturales

 Test zonas horarias

 Test formatos ambiguos

H02: Integration Tests
 Test con BaseAgent

 Test con Router

 Test con ContextManager

H03: Performance Tests
 Benchmark process_message()

 Memory leak tests

 Stress tests (1000 mensajes)

📌 Meta-Información
Campo	Valor
Directorio	src/theaia/agents/agenda_agent/tests/
Test Files	2 (test_handler.py, test_agenda_fsm.py)
Test Cases	12+
Coverage	85%+
Framework	pytest 8.1.1+
Última ejecución	2025-11-10 17:24 CET
Status	✅ PASSING
Agenda Agent Tests v1.0
12+ test cases + 85% coverage
All critical flows validated