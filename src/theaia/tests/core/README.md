# core/ - Core Tests

Tests de componentes core del sistema (router, state machine, context).

---

## 📋 Overview

Tests de la arquitectura core con características:

- 🎯 **Core logic** (FSM, Router, Context)
- 🔄 **State management** (transitions, persistence)
- 🧠 **Decision logic** (routing, intent detection)
- ⚡ **Unitarios** pero críticos

---

## 📁 Estructura

core/
├── test_bot_factory.py # ✅ Bot factory (2 tests)
├── test_callbacks.py # ✅ Callbacks (9 tests)
├── test_context.py # ✅ Context management (3 tests)
├── test_context_manager.py # ✅ Context manager (3 tests)
├── test_router.py # ✅ Router (1 test)
└── test_state_machine.py # ✅ State machine (4 tests)

text

**Total Core Tests: 22 tests**

---

## 🚀 Quick Start

Ejecutar todos los core tests
pytest src/theaia/tests/core/ -v

Solo router tests
pytest src/theaia/tests/core/test_router.py -v

Solo FSM tests
pytest src/theaia/tests/core/test_state_machine.py -v

text

---

## ✅ Tests Implementados

### **🏭 Bot Factory (2 tests)**
`test_bot_factory.py` - Factory pattern para crear bots:

- ✅ `test_create_telegram_bot` - Crea bot Telegram
- ✅ `test_bot_configuration` - Configuración correcta

**Coverage:** 64%

---

### **🔔 Callbacks (9 tests)**
`test_callbacks.py` - Sistema de callbacks:

- ✅ `test_register_callback` - Registrar callback
- ✅ `test_trigger_callback` - Disparar callback
- ✅ `test_multiple_callbacks` - Múltiples callbacks
- ✅ `test_callback_error_handling` - Manejo errores
- ✅ `test_callback_priority` - Prioridad callbacks
- ✅ `test_remove_callback` - Eliminar callback
- ✅ `test_callback_context` - Contexto en callbacks
- ✅ `test_async_callbacks` - Callbacks asíncronos
- ✅ `test_callback_chain` - Cadena callbacks

**Coverage:** 100%

---

### **📦 Context Management (6 tests)**
`test_context.py` (3 tests) + `test_context_manager.py` (3 tests):

#### Context (3 tests)
- ✅ `test_context_creation` - Crear contexto
- ✅ `test_context_update` - Actualizar contexto
- ✅ `test_context_access` - Acceder datos contexto

**Coverage:** 60%

#### Context Manager (3 tests)
- ✅ `test_context_manager_store` - Almacenar contexto
- ✅ `test_context_manager_retrieve` - Recuperar contexto
- ✅ `test_context_manager_cleanup` - Limpiar contexto

**Coverage:** 74%

---

### **🔀 Router (1 test)**
`test_router.py` - Routing de mensajes a agents:

- ✅ `test_router_basic` - Routing básico de mensajes

**Coverage:** 82%

**Note:** Router tiene más cobertura en integration tests

---

### **🔄 State Machine (4 tests)**
`test_state_machine.py` - FSM state transitions:

- ✅ `test_initial_state` - Estado inicial correcto
- ✅ `test_state_transition` - Transiciones válidas
- ✅ `test_invalid_transition` - Transiciones inválidas bloqueadas
- ✅ `test_state_callbacks` - Callbacks en transiciones

**Coverage:** 89%

---

## 💡 Ejemplo Core Test

test_state_machine.py
import pytest
from src.theaia.core.fsm import StateMachine, State

def test_state_transition():
"""
Test que la state machine permite transiciones válidas.

text
Verifica:
1. Estado inicial es correcto
2. Transición válida funciona
3. Estado final es correcto
4. Contexto se preserva
"""
# Arrange
class TestFSM(StateMachine):
    IDLE = State("idle", initial=True)
    PROCESSING = State("processing")
    DONE = State("done", final=True)
    
    transitions = [
        ("idle", "processing", "start"),
        ("processing", "done", "finish")
    ]

fsm = TestFSM()

# Act & Assert - Initial state
assert fsm.current_state == TestFSM.IDLE

# Act - Transition 1
result = fsm.transition("start")

# Assert
assert result is True
assert fsm.current_state == TestFSM.PROCESSING

# Act - Transition 2
result = fsm.transition("finish")

# Assert
assert result is True
assert fsm.current_state == TestFSM.DONE
assert fsm.is_final is True
text

---

## ✅ Características Core Tests

**✅ Debe:**
- Testear lógica core aislada
- Verificar transiciones de estado
- Validar routing correcto
- Testear context management

**❌ NO debe:**
- Depender de database
- Hacer network calls
- Testear UI/UX
- Duplicar tests de agents

---

## 📊 Coverage Stats (15 Nov 2025)

| Component | Tests | Coverage | Status |
|-----------|-------|----------|--------|
| BotFactory | 2 | 64% | ✅ |
| Callbacks | 9 | 100% | ✅ |
| Context | 3 | 60% | ✅ |
| ContextManager | 3 | 74% | ✅ |
| Router | 1 | 82% | ✅ |
| StateMachine | 4 | 89% | ✅ |
| **TOTAL** | **22** | **~78%** | ✅ |

---

## 🎯 Test Patterns

### State Machine Pattern
def test_fsm_behavior():
# Arrange
fsm = MyFSM()

text
# Act
fsm.transition("event")

# Assert
assert fsm.current_state == ExpectedState
assert fsm.context["key"] == "value"
text

### Router Pattern
def test_router_selects_agent():
# Arrange
router = Router()
message = "crear recordatorio"

text
# Act
agent = router.route(message)

# Assert
assert isinstance(agent, ReminderAgent)
text

### Context Pattern
def test_context_persistence():
# Arrange
ctx_manager = ContextManager()
context = {"user_id": 123, "state": "active"}

text
# Act
ctx_manager.save("session_1", context)
retrieved = ctx_manager.get("session_1")

# Assert
assert retrieved == context
text

---

## 🎯 Future Tests (Phase 4+)

**Additional Core Tests:**
- [ ] Complex FSM scenarios
- [ ] Multi-agent routing
- [ ] Context serialization
- [ ] Error recovery in FSM
- [ ] Performance tests (routing speed)

---

## 📚 Convenciones

### Test Naming
def test_component_behavior_expected():
"""Test that component behavior results in expected."""

text

### State Machine Tests
def test_fsm_<scenario>():
"""Test FSM handles <scenario> correctly."""
fsm = create_fsm()
# ... test scenario

text

---

**Implementado:** H02 (12-14 Nov 2025)  
**Última actualización:** 16 Nov 2025, 00:01 CET