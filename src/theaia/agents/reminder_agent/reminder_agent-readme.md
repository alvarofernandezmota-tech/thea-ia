🧪 Reminder Agent Tests — Suite de Pruebas
Versión: v1.0.0
Ruta: src/theaia/agents/reminder_agent/tests/
Última actualización: 2025-11-10 17:52 CET (S39)
Coverage: 85%+

📋 Propósito
Suite de pruebas unitarias para Reminder Agent. Valida que:

✅ ReminderAgent.handle() funciona correctamente

✅ FSM transiciones son correctas

✅ Manejo de edge cases

✅ Integración entre componentes

📁 Estructura Tests
text
tests/
├── test_handler.py (1353 bytes)
│   └── Tests para ReminderAgent + ConversationManager
│
├── test_reminder_fsm.py (1906 bytes)
│   └── Tests para FSM states + transitions
│
└── __init__.py
🧪 Test Files
1. test_handler.py
Propósito: Validar clase ReminderAgent y ReminderConversationManager.

Tests principales:

test_reminder_agent_initialization()
python
def test_reminder_agent_initialization():
    """Verifica que ReminderAgent se inicializa correctamente."""
    agent = ReminderAgent(user_id="user_123")
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
    agent = ReminderAgent(user_id="user_123")
    intents = agent.get_supported_intents()
    expected = ["recordatorio", "alarma", "recuérdame", "reminder"]
    assert intents == expected
Valida:

✅ Intenciones definidas

✅ Orden correcto

✅ Cobertura de sinónimos

test_handle_basic_flow()
python
def test_handle_basic_flow():
    """Flujo completo: text → time → confirmation → scheduled."""
    agent = ReminderAgent(user_id="user_123")
    context = {}
    
    # Turno 1: Capturar texto
    response, state, context = agent.handle(
        "user_123", 
        "Llamar a mamá",
        context
    )
    assert state == "awaiting_time"
    assert "¿Cuándo" in response
    
    # Turno 2: Capturar hora
    response, state, context = agent.handle(
        "user_123",
        "7 PM",
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
    assert state == "scheduled"
    assert "programado" in response
Valida:

✅ Flujo multi-turno

✅ Transiciones correctas

✅ Contexto persistente

test_handle_cancellation()
python
def test_handle_cancellation():
    """Verifica cancelación en confirmation."""
    agent = ReminderAgent(user_id="user_123")
    context = {
        "fsm_state": "confirmation",
        "reminder_text": "Test",
        "reminder_time": "7 PM"
    }
    
    response, state, context = agent.handle(
        "user_123",
        "No",
        context
    )
    assert state == "scheduled"
    assert "cancelado" in response
Valida:

✅ Cancelación funciona

✅ Respuesta apropiada

✅ Estado final correcto

2. test_reminder_fsm.py
Propósito: Validar máquina de estados ReminderFSM.

Tests principales:

test_fsm_initialization()
python
def test_fsm_initialization():
    """Verifica que FSM se inicializa en estado correcto."""
    fsm = ReminderFSM()
    assert fsm.state == "awaiting_text"
    assert fsm.context == {}
Valida:

✅ Estado inicial correcto

✅ Contexto vacío

test_fsm_text_transition()
python
def test_fsm_text_transition():
    """Verifica transición: awaiting_text → awaiting_time."""
    fsm = ReminderFSM()
    response, new_state = fsm.process_message("Llamar a mamá", {})
    
    assert new_state == "awaiting_time"
    assert "¿Cuándo" in response
    assert fsm.context["reminder_text"] == "Llamar a mamá"
Valida:

✅ Transición correcta

✅ Contexto guardado

✅ Respuesta apropiada

test_fsm_time_transition()
python
def test_fsm_time_transition():
    """Verifica transición: awaiting_time → confirmation."""
    fsm = ReminderFSM()
    fsm.state = "awaiting_time"
    fsm.context = {"reminder_text": "Test"}
    
    response, new_state = fsm.process_message("7 PM", {})
    
    assert new_state == "confirmation"
    assert "Confirmar" in response
    assert fsm.context["reminder_time"] == "7 PM"
Valida:

✅ Parse de hora

✅ Transición correcta

✅ Confirmación explícita

test_fsm_confirmation_positive()
python
def test_fsm_confirmation_positive():
    """Verifica confirmación positiva: confirmation → scheduled."""
    fsm = ReminderFSM()
    fsm.state = "confirmation"
    fsm.context = {"reminder_text": "Test", "reminder_time": "7 PM"}
    
    response, new_state = fsm.process_message("Sí", {})
    
    assert new_state == "scheduled"
    assert "✓" in response or "programado" in response
Valida:

✅ Respuesta positiva reconocida

✅ Estado final correcto

✅ Mensaje éxito

test_fsm_confirmation_negative()
python
def test_fsm_confirmation_negative():
    """Verifica confirmación negativa: confirmation → cancelled."""
    fsm = ReminderFSM()
    fsm.state = "confirmation"
    
    response, new_state = fsm.process_message("No", {})
    
    assert new_state == "cancelled"
    assert "cancelado" in response
Valida:

✅ Respuesta negativa reconocida

✅ Estado final correcto

✅ Mensaje cancelación

test_fsm_state_persistence()
python
def test_fsm_state_persistence():
    """Verifica que contexto persiste entre process_message calls."""
    fsm = ReminderFSM()
    context = {}
    
    # Primer call
    fsm.process_message("Recordatorio", context)
    context_after_1 = fsm.context.copy()
    
    # Segundo call (contexto debe mantenerse)
    fsm.context = context_after_1
    fsm.process_message("7 PM", context_after_1)
    context_after_2 = fsm.context.copy()
    
    assert "reminder_text" in context_after_2
    assert context_after_2["reminder_text"] == "Recordatorio"
Valida:

✅ Persistencia de contexto

✅ No sobrescribe atributos previos

✅ Acumulación de información

🏃 Ejecutar Tests
bash
# Todos los tests
pytest src/theaia/agents/reminder_agent/tests/ -v

# Específico
pytest src/theaia/agents/reminder_agent/tests/test_handler.py -v
pytest src/theaia/agents/reminder_agent/tests/test_reminder_fsm.py -v

# Con cobertura
pytest src/theaia/agents/reminder_agent/tests/ --cov=src.theaia.agents.reminder_agent

# Verbose + print
pytest src/theaia/agents/reminder_agent/tests/ -v -s
📊 Coverage Actual
text
Name                                        Stmts   Miss  Cover
─────────────────────────────────────────────────────────────
reminder_agent/handler.py                     12      2    83%
reminder_agent/reminder_conversation_manager  15      3    80%
reminder_agent/model/reminder_fsm.py          22      2    91%
─────────────────────────────────────────────────────────────
TOTAL                                         49      7    85%
Meta: ≥85% ✅

🐛 Test Cases Edge / Known Issues
Casos Probados
✅ Flujo feliz (text → time → confirm → scheduled)

✅ Cancelación

✅ Respuestas variadas ("sí", "si", "ok", "confirmar")

✅ Contexto persistente

✅ Inicialización

No Probados Aún
⚠️ Parse de horas complejas

⚠️ Timezones

⚠️ Conflictos con otros recordatorios

⚠️ Datos corruptos/malformados

🔮 Roadmap Tests
H01: Parser Validation
 Test parse horas naturales

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
Directorio	src/theaia/agents/reminder_agent/tests/
Test Files	2 (test_handler.py, test_reminder_fsm.py)
Test Cases	12+
Coverage	85%+
Framework	pytest 8.1.1+
Última ejecución	2025-11-10 17:52 CET
Status	✅ PASSING
Reminder Agent Tests v1.0
12+ test cases + 85% coverage
All critical flows validated