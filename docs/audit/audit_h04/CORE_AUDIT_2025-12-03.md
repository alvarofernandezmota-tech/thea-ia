# 🔍 AUDITORÍA CORE COMPONENTS - THEA IA

**Fecha:** 03 Diciembre 2025  
**Versión:** 1.0  
**Auditor:** Equipo THEA IA (Perplexity AI + Lead Developer)  
**Objetivo:** Analizar componentes centrales (FSM, Router, Context) para MVP

---

## 📊 RESUMEN EJECUTIVO

### Componentes Analizados: 8

| Componente | LOC | Estado | MVP? | Decisión |
|------------|-----|--------|------|----------|
| **ConversationStateMachine** | ~200 | ✅ FUNCIONAL | ✅ SÍ | 🟢 MANTENER |
| **ConversationManager** | ~350 | ⚠️ COMPLEJO | ✅ SÍ | 🟡 REFACTOR |
| **BaseStateMachine** | ~150 | ✅ BUENO | ✅ SÍ | 🟢 MANTENER |
| **CallbacksMixin** | ~100 | ✅ AVANZADO | ✅ SÍ | 🟢 MANTENER |
| **ContextMergingEngine** | ~200 | ✅ ROBUSTO | ✅ SÍ | 🟢 MANTENER |
| **TransitionConfig** | ~80 | ✅ BUENO | ✅ SÍ | 🟢 MANTENER |
| **BotFactory** | ~30 | ✅ SIMPLE | ❓ | 🟡 EVALUAR |
| **CoreRouter** | 0 | ❌ NO EXISTE | ✅ SÍ | 🔴 CREAR |

### Decisiones Tomadas: 8

- 🟢 **MANTENER:** 5 componentes (FSM sólida, callbacks avanzados, context robusto)
- 🟡 **REFACTOR:** 1 componente (ConversationManager sobrecargado)
- 🟡 **EVALUAR:** 1 componente (BotFactory sin uso claro)
- 🔴 **CREAR:** 1 componente (CoreRouter NO EXISTE - CRÍTICO MVP)

### Hallazgos Clave

- ✅ **FSM architecture excelente** - BaseStateMachine + Python transitions
- ✅ **Callbacks avanzados H03** - Pre/Post/Error callbacks con context injection
- ✅ **Context merging robusto** - 4 estrategias (overwrite, append, merge, windowing)
- ⚠️ **ConversationManager sobrecargado** - 350 LOC, responsabilidades mezcladas
- 🔴 **CoreRouter NO EXISTE** - CRÍTICO: TelegramAdapter lo necesita (H03)
- ✅ **Transition logging** - TransitionConfig con tracking completo

---

## 🎯 MATRIZ DE DECISIONES

| Componente | LOC | Framework | Tests | Coverage | MVP? | Decisión | Prioridad |
|------------|-----|-----------|-------|----------|------|----------|-----------|
| **ConversationStateMachine** | 200 | transitions | ❓ | ❓ | ✅ SÍ | 🟢 MANTENER | P0 |
| **ConversationManager** | 350 | Custom | ❓ | ❓ | ✅ SÍ | 🟡 REFACTOR | P0 |
| **BaseStateMachine** | 150 | ABC + transitions | ❓ | ❓ | ✅ SÍ | 🟢 MANTENER | P0 |
| **CallbacksMixin** | 100 | Mixin pattern | ❓ | ❓ | ✅ SÍ | 🟢 MANTENER | P1 |
| **ContextMergingEngine** | 200 | Custom | ❓ | ❓ | ✅ SÍ | 🟢 MANTENER | P1 |
| **TransitionConfig** | 80 | Logging | ❓ | ❓ | ✅ SÍ | 🟢 MANTENER | P1 |
| **BotFactory** | 30 | Factory pattern | ❓ | ❓ | ❓ | 🟡 EVALUAR | P2 |
| **CoreRouter** | 0 | NO EXISTE | 0 | 0% | ✅ SÍ | 🔴 CREAR | P0 |

**Leyenda:**
- P0 = Prioridad crítica MVP
- P1 = Prioridad alta MVP
- P2 = Prioridad baja (evaluar)

---

## 📋 ANÁLISIS DETALLADO POR COMPONENTE

### 1. ConversationStateMachine ✅ MVP

**Ubicación:** `src/theaia/core/fsm/state_machine.py`

**Estado Actual:**
- **LOC:** ~200 líneas
- **Framework:** Python transitions library
- **Herencia:** BaseStateMachine + CallbacksMixin
- **Tests:** ❓ Desconocido
- **Estado:** ✅ FUNCIONAL

**Arquitectura:**
class ConversationStateMachine(CallbacksMixin, BaseStateMachine):
"""
Máquina de estados central para manejo conversacional.

text
H03 Improvements:
- Hereda de CallbacksMixin para callbacks avanzados
- Pre/Post/Error callbacks disponibles
- Context injection en callbacks
- ContextMergingEngine para merge strategies
"""

def __init__(self, user_id: int):
    # Estados principales
    self.pending_message = None
    self.candidate_intents = []
    self.active_agent = None
    
    # Context merging
    self.context_merging_engine = ContextMergingEngine(max_history=10)
    
    super().__init__(user_id, initial_state="initial")
    self._register_h03_callbacks()
text

**Estados FSM (5 estados):**

1. **initial** - Estado inicial
2. **awaiting_disambiguation** - Esperando clarificación usuario
3. **agent_delegated** - Delegado a agente específico
4. **completed** - Conversación completada
5. **session_timeout** - Sesión expirada

**Transiciones:**

def setup_transitions(self):
# 1. Initial → Disambiguation
self.machine.add_transition(
trigger='request_disambiguation',
source='initial',
dest='awaiting_disambiguation',
after='_after_disambiguation'
)

text
# 2. Initial → Agent Delegated
self.machine.add_transition(
    trigger='delegate_to_agent',
    source='initial',
    dest='agent_delegated',
    after='_after_delegation'
)

# 3. Disambiguation → Agent Delegated
self.machine.add_transition(
    trigger='resolve_disambiguation',
    source='awaiting_disambiguation',
    dest='agent_delegated',
    after='_after_resolution'
)

# 4. Agent Delegated → Completed
self.machine.add_transition(
    trigger='complete_conversation',
    source='agent_delegated',
    dest='completed',
    after='_on_completion'
)

# 5. Any → Timeout
self.machine.add_transition(
    trigger='timeout_session',
    source='*',
    dest='session_timeout',
    after='_on_timeout'
)
text

**Features Implementadas:**

- ✅ **Context Merging:**
def merge_context(self, new_context: Dict, strategy: str = "merge"):
"""Merge context usando estrategia especificada."""
merged = self.context_merging_engine.merge(
self.context,
new_context,
strategy=strategy
)
self.context = merged

text

- ✅ **Pending Message Management:**
def set_pending_message(self, message: str, intents: List[str]):
self.pending_message = message
self.candidate_intents = intents

def get_pending_data(self) -> Tuple[str, List[str]]:
return self.pending_message, self.candidate_intents

def clear_pending_data(self):
self.pending_message = None
self.candidate_intents = []

text

- ✅ **H03 Callbacks Registration:**
def _register_h03_callbacks(self):
"""Registra callbacks H03 de ejemplo."""
# Pre-transition logging
self.register_universal_pre_callback(self._h03_log_before_transition)

text
# Post-transition logging
self.register_universal_post_callback(self._h03_log_after_transition)

# Error handling
self.register_universal_error_callback(self._h03_log_transition_error)
text

**Problemas Identificados:**

1. ❓ **Tests ausentes** - No hay tests específicos FSM
2. ❓ **Coverage desconocido** - Probablemente 0%
3. ⚠️ **Callbacks de ejemplo** - Registrados por defecto (logging)

**Decisión:** 🟢 **MANTENER**

**Razones:**
1. ✅ Arquitectura FSM sólida
2. ✅ Herencia limpia (BaseStateMachine + CallbacksMixin)
3. ✅ Estados bien definidos (5 estados principales)
4. ✅ Transiciones claras
5. ✅ Context merging integrado
6. ✅ H03 callbacks avanzados

**Plan FASE 3 (H06):**
- ✅ 20 tests unitarios FSM
- ✅ Tests transiciones
- ✅ Tests callbacks
- ✅ Coverage 85%+

**Target H06:** Tests 0 → 20+, Coverage → 85%+

---

### 2. ConversationManager 🟡 REFACTOR

**Ubicación:** `src/theaia/core/fsm/conversation_manager.py`

**Estado Actual:**
- **LOC:** ~350 líneas
- **Framework:** Custom
- **Tests:** ❓ Desconocido
- **Estado:** ⚠️ FUNCIONAL PERO COMPLEJO

**Arquitectura:**
class ConversationManager:
"""
Manager principal que orquesta la conversación, integra detección de intenciones
y delega a managers especializados.
"""

text
def __init__(self, user_id: int):
    self.user_id = user_id
    self.fsm = ConversationStateMachine(user_id)
    self.intent_detector = IntentDetector()
    self.transition_config = TransitionConfig()
    
    # Session management
    self.last_activity_time = time.time()
    self.session_timeout_minutes = 30
    
    # Disambiguation
    self.disambiguation_timeout_minutes = 5
    self.max_disambiguation_retries = 3
    self.disambiguation_retry_count = 0
    self.disambiguation_start_time = None
    
    # Specialized managers
    self.agenda_manager = AgendaConversationManager(user_id)
text

**Responsabilidades (DEMASIADAS):**

1. **FSM Orchestration**
2. **Intent Detection**
3. **Session Management** (timeout tracking)
4. **Disambiguation Logic** (3 retry system)
5. **Agent Delegation**
6. **Specialized Managers** (AgendaConversationManager)
7. **Error Recovery**
8. **Fallback Handling**

**Método Principal (COMPLEJO):**
async def process_input(self, message: str, candidate_intents=None) -> Tuple[str, Dict]:
"""
Procesa input usuario y retorna respuesta.

text
Maneja:
- Estados FSM (5 estados diferentes)
- Intent detection
- Disambiguation
- Timeout recovery
- Error handling
"""
try:
    # Update activity
    self.last_activity_time = time.time()
    
    # Check session timeout
    if self.fsm.state == GlobalState.COMPLETED.value:
        self.fsm.reset()
    
    # Route by state (5 handlers)
    if self.fsm.state == GlobalState.INITIAL.value:
        return await self._handle_initial_state(message, candidate_intents)
    
    elif self.fsm.state == GlobalState.AWAITING_DISAMBIGUATION.value:
        return await self._handle_disambiguation_state(message)
    
    elif self.fsm.state == GlobalState.AGENT_DELEGATED.value:
        return await self._handle_agent_delegated_state(message)
    
    elif self.fsm.state == GlobalState.SESSION_TIMEOUT.value:
        return await self._handle_timeout_recovery(message, candidate_intents)
    
    elif self.fsm.state == GlobalState.ERROR_STATE.value:
        return await self._handle_error_recovery(message, candidate_intents)
    
    else:
        return await self._handle_unknown_state(message, candidate_intents)

except Exception as e:
    logger.error(f"Error processing input for user {self.user_id}: {e}", exc_info=True)
    return self._handle_error(str(e)), self.fsm.context
text

**PROBLEMA CRÍTICO:** 🔴 **350 LOC con responsabilidades mezcladas**

| Responsabilidad | LOC | Debería estar en |
|-----------------|-----|------------------|
| FSM Orchestration | ~50 | ✅ ConversationManager |
| Intent Detection | ~30 | ❌ IntentDetector (ya existe) |
| Session Timeout | ~40 | ❌ SessionManager (crear) |
| Disambiguation | ~80 | ❌ DisambiguationHandler (crear) |
| Agent Delegation | ~50 | ❌ AgentRouter (crear) |
| Error Recovery | ~40 | ❌ ErrorRecoveryHandler (crear) |
| Specialized Managers | ~60 | ❌ AgentRegistry (crear) |

**Decisión:** 🟡 **REFACTOR (H06-H07)**

**Razones:**
1. 🔴 **350 LOC demasiado grande** para un manager
2. ⚠️ **Responsabilidades mezcladas** - Viola SRP
3. ⚠️ **Difícil de testear** - Demasiados paths
4. ⚠️ **Difícil de mantener** - Cambios afectan todo

**Plan FASE 3 (H06-H07):**

Target: 150 LOC ConversationManager (vs 350 actual)
class ConversationManager:
def init(self, user_id: int):
self.user_id = user_id
self.fsm = ConversationStateMachine(user_id)

text
    # ✅ NUEVO: Componentes separados
    self.session_manager = SessionManager(timeout_minutes=30)
    self.disambiguation_handler = DisambiguationHandler(max_retries=3)
    self.agent_router = AgentRouter()
    self.error_handler = ErrorRecoveryHandler()

async def process_input(self, message: str) -> Tuple[str, Dict]:
    # 1. Check session (delegado)
    if self.session_manager.is_expired():
        return await self.error_handler.handle_timeout()
    
    # 2. Route by state (simplificado)
    if self.fsm.state == "initial":
        return await self._handle_initial(message)
    
    # ... resto simplificado
text

**Separar en 5 componentes:**
1. **ConversationManager** (150 LOC) - Orquestación FSM
2. **SessionManager** (80 LOC) - Timeout tracking
3. **DisambiguationHandler** (100 LOC) - Lógica disambiguation
4. **AgentRouter** (120 LOC) - Agent delegation
5. **ErrorRecoveryHandler** (80 LOC) - Error recovery

**Añadir:**
- ✅ 4 componentes nuevos
- ✅ 40 tests (8 por componente)
- ✅ SRP compliance
- ✅ Testabilidad mejorada

**Target H06-H07:** 350 LOC → 530 LOC (distribuidas en 5 componentes), Coverage 85%+

---

### 3. BaseStateMachine ✅ MVP

**Ubicación:** `src/theaia/core/fsm/state_machine.py`

**Estado Actual:**
- **LOC:** ~150 líneas
- **Framework:** ABC + Python transitions
- **Tests:** ❓ Desconocido
- **Estado:** ✅ BUENO

**Arquitectura:**
from abc import ABC, abstractmethod
from transitions import Machine

class BaseStateMachine(ABC):
"""
Clase base abstracta para todas las máquinas de estado en Thea IA 3.0.
"""

text
def __init__(self, user_id: int, initial_state: str):
    self.user_id = user_id
    self.context = {}
    self.machine = None
    self._setup_machine(initial_state)

@abstractmethod
def get_states(self) -> List[str]:
    """Retorna lista de estados. DEBE ser implementado por subclases."""
    pass

@abstractmethod
def setup_transitions(self):
    """Configura transiciones. DEBE ser implementado por subclases."""
    pass

def _setup_machine(self, initial_state: str):
    """Inicializa la máquina de estados."""
    states = self.get_states()
    
    self.machine = Machine(
        model=self,
        states=states,
        initial=initial_state,
        auto_transitions=False,
        send_event=True
    )
    
    self.setup_transitions()
    self._setup_universal_transitions()

def _setup_universal_transitions(self):
    """Transiciones comunes disponibles en cualquier estado."""
    # Reset transition (available from any state)
    self.machine.add_transition(
        trigger='reset',
        source='*',
        dest='initial',
        after='_on_reset'
    )
    
    # Error transition (available from any state)
    self.machine.add_transition(
        trigger='error',
        source='*',
        dest='error_state',
        after='_on_error'
    )
text

**Features Implementadas:**

- ✅ **ABC Pattern:**
@abstractmethod
def get_states(self) -> List[str]:
"""Fuerza subclases a definir estados."""
pass

@abstractmethod
def setup_transitions(self):
"""Fuerza subclases a definir transiciones."""
pass

text

- ✅ **Universal Transitions:**
Reset desde cualquier estado
self.machine.add_transition(trigger='reset', source='*', dest='initial')

Error desde cualquier estado
self.machine.add_transition(trigger='error', source='*', dest='error_state')

text

- ✅ **Context Management:**
def get_context(self, key: str = None, default=None):
"""Obtiene valor del contexto."""
if key:
return self.context.get(key, default)
return self.context

def set_context(self, **kwargs):
"""Actualiza contexto."""
self.context.update(kwargs)

def clear_context(self, keep_keys: List[str] = None):
"""Limpia contexto."""
if keep_keys:
self.context = {k: v for k, v in self.context.items() if k in keep_keys}
else:
self.context.clear()

text

- ✅ **Transition Validation:**
def can_transition(self, trigger: str) -> bool:
"""Verifica si transición es válida desde estado actual."""
try:
transitions = [t for t in self.machine.get_triggers(self.state) if t.name == trigger]
return len(transitions) > 0
except:
return False

text

**Decisión:** 🟢 **MANTENER**

**Razones:**
1. ✅ ABC pattern correcto
2. ✅ Herencia limpia
3. ✅ Universal transitions útiles
4. ✅ Context management robusto
5. ✅ Transition validation

**Plan FASE 3 (H06):**
- ✅ 10 tests unitarios
- ✅ Tests ABC compliance
- ✅ Tests universal transitions
- ✅ Coverage 85%+

**Target H06:** Tests 0 → 10+, Coverage → 85%+

---

### 4. CallbacksMixin ✅ MVP

**Ubicación:** `src/theaia/core/fsm/callbacks_mixin.py`

**Estado Actual:**
- **LOC:** ~100 líneas
- **Framework:** Mixin pattern
- **Tests:** ❓ Desconocido
- **Estado:** ✅ AVANZADO (H03)

**Arquitectura:**
class CallbacksMixin:
"""
Mixin que añade sistema de callbacks avanzado a FSM.

text
Features H03:
- Pre-transition callbacks (ejecutan antes de transición)
- Post-transition callbacks (ejecutan después de transición exitosa)
- Error callbacks (manejan errores en transición)
- Context injection (callbacks reciben y pueden modificar context)
- Callback registration system

Usage:
    class MyFSM(CallbacksMixin, BaseStateMachine):
        def __init__(self, user_id):
            super().__init__(user_id)
            self.register_pre_callback("my_transition", self._validate_before)
            self.register_post_callback("my_transition", self._update_after)
"""

def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    # Callback registries
    self._pre_callbacks = {}   # {transition: [callbacks]}
    self._post_callbacks = {}  # {transition: [callbacks]}
    self._error_callbacks = {} # {transition: [callbacks]}
    
    # Universal callbacks (ejecutan en TODAS las transiciones)
    self._universal_pre_callbacks = []
    self._universal_post_callbacks = []
    self._universal_error_callbacks = []
text

**Features Implementadas:**

- ✅ **Pre-Transition Callbacks:**
def register_pre_callback(self, transition: str, callback: Callable):
"""Registra callback que se ejecuta ANTES de transición."""
if transition not in self._pre_callbacks:
self._pre_callbacks[transition] = []
self._pre_callbacks[transition].append(callback)

def _execute_pre_callbacks(self, from_state, to_state, context):
"""Ejecuta todos los pre-callbacks."""
# Universal callbacks
for callback in self._universal_pre_callbacks:
result = callback(from_state, to_state, context)
if result is False:
return False # Abort transition

text
# Transition-specific callbacks
if transition in self._pre_callbacks:
    for callback in self._pre_callbacks[transition]:
        result = callback(from_state, to_state, context)
        if result is False:
            return False

return True
text

- ✅ **Post-Transition Callbacks:**
def register_post_callback(self, transition: str, callback: Callable):
"""Registra callback que se ejecuta DESPUÉS de transición exitosa."""
if transition not in self._post_callbacks:
self._post_callbacks[transition] = []
self._post_callbacks[transition].append(callback)

def _execute_post_callbacks(self, from_state, to_state, context):
"""Ejecuta todos los post-callbacks."""
for callback in self._universal_post_callbacks:
callback(from_state, to_state, context)

text
if transition in self._post_callbacks:
    for callback in self._post_callbacks[transition]:
        callback(from_state, to_state, context)
text

- ✅ **Error Callbacks:**
def register_error_callback(self, transition: str, callback: Callable):
"""Registra callback que se ejecuta si transición falla."""
if transition not in self._error_callbacks:
self._error_callbacks[transition] = []
self._error_callbacks[transition].append(callback)

def _execute_error_callbacks(self, from_state, to_state, context, error):
"""Ejecuta todos los error-callbacks."""
for callback in self._universal_error_callbacks:
callback(from_state, to_state, context, error)

text
if transition in self._error_callbacks:
    for callback in self._error_callbacks[transition]:
        callback(from_state, to_state, context, error)
text

- ✅ **Universal Callbacks:**
def register_universal_pre_callback(self, callback: Callable):
"""Registra callback que se ejecuta ANTES de CUALQUIER transición."""
self._universal_pre_callbacks.append(callback)

def register_universal_post_callback(self, callback: Callable):
"""Registra callback que se ejecuta DESPUÉS de CUALQUIER transición."""
self._universal_post_callbacks.append(callback)

def register_universal_error_callback(self, callback: Callable):
"""Registra callback que se ejecuta si CUALQUIER transición falla."""
self._universal_error_callbacks.append(callback)

text

- ✅ **Transition with Callbacks:**
def transition_with_callbacks(self, from_state, to_state, context):
"""Ejecuta transición con callbacks completos."""
try:
# 1. Pre-callbacks
if not self._execute_pre_callbacks(from_state, to_state, context):
return False # Aborted

text
    # 2. Actual transition
    trigger_method = getattr(self, to_state, None)
    if trigger_method and hasattr(trigger_method, '__call__'):
        trigger_method()
    
    # 3. Post-callbacks
    self._execute_post_callbacks(from_state, to_state, context)
    
    return True

except Exception as e:
    # 4. Error callbacks
    self._execute_error_callbacks(from_state, to_state, context, e)
    return False
text

**Decisión:** 🟢 **MANTENER**

**Razones:**
1. ✅ Feature H03 avanzado
2. ✅ Pre/Post/Error callbacks completos
3. ✅ Universal callbacks útiles
4. ✅ Context injection
5. ✅ Mixin pattern limpio

**Plan FASE 3 (H06):**
- ✅ 15 tests callbacks
- ✅ Tests pre/post/error
- ✅ Tests universal callbacks
- ✅ Coverage 85%+

**Target H06:** Tests 0 → 15+, Coverage → 85%+

---

### 5. ContextMergingEngine ✅ MVP

**Ubicación:** `src/theaia/core/fsm/context_merging.py`

**Estado Actual:**
- **LOC:** ~200 líneas
- **Framework:** Custom
- **Tests:** ❓ Desconocido
- **Estado:** ✅ ROBUSTO (H03)

**Arquitectura:**
from enum import Enum

class MergeStrategy(Enum):
"""Estrategias de merge para context."""
OVERWRITE = "overwrite"
APPEND = "append"
MERGE = "merge"
WINDOWING = "windowing"

class ContextMergingEngine:
"""
Motor de merge context con múltiples estrategias.

text
Características H03:
- Merge strategies (overwrite, append, merge, windowing)
- Context windowing (últimos N mensajes)
- Session isolation (contexto por usuario)
- Smart merge para structures profundas
- Timestamp tracking

Usage:
    engine = ContextMergingEngine(max_history=10)
    merged = engine.merge(old_context, new_context, strategy="merge")
"""

def __init__(self, max_history: int = 10):
    self.max_history = max_history
text

**4 Estrategias Implementadas:**

**1. OVERWRITE:**
def _merge_overwrite(self, old_context: Dict, new_context: Dict) -> Dict:
"""
OVERWRITE: Sobrescribe completamente old_context con new_context.

text
Simple y directo: old context se pierde.
"""
result = dict(old_context)
result.update(new_context)
return result
text

**2. APPEND:**
def _merge_append(self, old_context: Dict, new_context: Dict) -> Dict:
"""
APPEND: Añade valores nuevos a listas existentes.

text
Para listas: old_list + new_list
Para otros: sobrescribe
"""
result = dict(old_context)

for key, new_value in new_context.items():
    if key in result:
        old_value = result[key]
        
        # Si ambos son listas, append
        if isinstance(old_value, list) and isinstance(new_value, list):
            result[key] = list(set(old_value + new_value))  # Unique
        else:
            result[key] = new_value
    else:
        result[key] = new_value

return result
text

**3. MERGE (Recursivo):**
def _merge_recursive(self, old_context: Dict, new_context: Dict) -> Dict:
"""
MERGE: Merge recursivo profundo.

text
Dicts se mergen recursivamente.
Listas se combinan.
Otros valores sobrescriben.
"""
result = dict(old_context)

for key, new_value in new_context.items():
    if key in result:
        old_value = result[key]
        
        # Ambos dicts → merge recursivo
        if isinstance(old_value, dict) and isinstance(new_value, dict):
            result[key] = self._merge_recursive(old_value, new_value)
        
        # Ambos listas → append unique
        elif isinstance(old_value, list) and isinstance(new_value, list):
            result[key] = old_value + new_value
        
        # Otros → sobrescribe
        else:
            result[key] = new_value
    else:
        result[key] = new_value

return result
text

**4. WINDOWING:**
def _merge_windowing(self, old_context: Dict, new_context: Dict) -> Dict:
"""
WINDOWING: Mantiene solo últimos N mensajes.

text
Útil para limitar memoria conversacional.
"""
# Merge primero
result = self._merge_recursive(old_context, new_context)

# Apply windowing
result = self.apply_windowing(result)

return result
def apply_windowing(self, context: Dict) -> Dict:
"""Aplica windowing a contexto."""
for key, value in list(context.items()):
if isinstance(value, list):
# Keep only last N items
if len(value) > self.max_history:
context[key] = value[-self.max_history:]

text
return context
text

**Features Adicionales:**

- ✅ **Session Isolation:**
def create_isolated_context(self, user_id: int, session_id: str, context: Dict) -> Dict:
"""Crea contexto aislado con metadata de sesión."""
return {
"user_id": user_id,
"session_id": session_id,
"timestamp": datetime.now(timezone.utc).isoformat(),
"data": context
}

text

- ✅ **Context Stats:**
def get_context_stats(self, context: Dict) -> Dict:
"""Retorna estadísticas del context."""
return {
"total_keys": len(context),
"lists": sum(1 for v in context.values() if isinstance(v, list)),
"dicts": sum(1 for v in context.values() if isinstance(v, dict)),
"total_list_items": sum(len(v) for v in context.values() if isinstance(v, list))
}

text

**Decisión:** 🟢 **MANTENER**

**Razones:**
1. ✅ 4 estrategias robustas
2. ✅ Merge recursivo profundo
3. ✅ Windowing para memoria limitada
4. ✅ Session isolation
5. ✅ Context stats útiles

**Plan FASE 3 (H06):**
- ✅ 20 tests (5 por estrategia)
- ✅ Tests merge recursivo
- ✅ Tests windowing
- ✅ Coverage 85%+

**Target H06:** Tests 0 → 20+, Coverage → 85%+

---

### 6. TransitionConfig ✅ MVP

**Ubicación:** `src/theaia/core/fsm/transitions.py`

**Estado Actual:**
- **LOC:** ~80 líneas
- **Framework:** Logging
- **Tests:** ❓ Desconocido
- **Estado:** ✅ BUENO

**Arquitectura:**
class TransitionConfig:
"""
Configuración y logging de transiciones FSM.

text
Features:
- Transition logging
- Callback registration helpers
- Transition tracking
- Error logging
"""

def __init__(self):
    self.transition_history = []
    self.error_count = 0
text

**Features Implementadas:**

- ✅ **Transition Logging:**
def log_transition(self, from_state: str, to_state: str, trigger: str, context: Dict):
"""Registra transición en history."""
entry = {
"from": from_state,
"to": to_state,
"trigger": trigger,
"timestamp": datetime.now().isoformat(),
"context_snapshot": context.copy()
}

text
self.transition_history.append(entry)

logger.info(f"[TransitionConfig] {from_state} -> {to_state} via '{trigger}'")
text

- ✅ **Error Logging:**
def log_error(self, from_state: str, to_state: str, error: Exception):
"""Registra error de transición."""
self.error_count += 1

text
logger.error(
    f"[TransitionConfig] ERROR: {from_state} -> {to_state} failed: {error}",
    exc_info=True
)
text

- ✅ **Transition History:**
def get_history(self, last_n: int = 10) -> List[Dict]:
"""Retorna últimas N transiciones."""
return self.transition_history[-last_n:]

def clear_history(self):
"""Limpia historial."""
self.transition_history = []
self.error_count = 0

text

**Decisión:** 🟢 **MANTENER**

**Razones:**
1. ✅ Logging útil
2. ✅ Transition history tracking
3. ✅ Error counting
4. ✅ Simple y efectivo

**Plan FASE 3 (H06):**
- ✅ 8 tests logging
- ✅ Tests history
- ✅ Coverage 85%+

**Target H06:** Tests 0 → 8+, Coverage → 85%+

---

### 7. BotFactory 🟡 EVALUAR

**Ubicación:** `src/theaia/core/bot_factory.py`

**Estado Actual:**
- **LOC:** ~30 líneas
- **Framework:** Factory pattern
- **Tests:** ❓ Desconocido
- **Estado:** ✅ SIMPLE
- **Uso:** ❓ NO USADO EN CÓDIGO ACTUAL

**Arquitectura:**
from typing import Dict, Type, Any

class BotFactory:
"""Registro e instanciación dinámica de agentes/bots para Thea IA 2.0."""

text
def __init__(self):
    self._registry = {}

def register_agent(self, name: str, agent_cls: Type):
    """Registra la clase del agente bajo un nombre clave."""
    self._registry[name] = agent_cls

def create_agent(self, name: str, **kwargs) -> Any:
    """Instancia agente registrado."""
    if name not in self._registry:
        raise ValueError(f"Agent '{name}' not registered")
    
    agent_cls = self._registry[name]
    return agent_cls(**kwargs)

def list_agents(self) -> list:
    """Lista nombres de agentes registrados."""
    return list(self._registry.keys())
text

**Uso Esperado (NO implementado):**
Setup
factory = BotFactory()
factory.register_agent("agenda", AgendaAgent)
factory.register_agent("note", NoteAgent)
factory.register_agent("reminder", ReminderAgent)

Runtime
agent = factory.create_agent("agenda", user_id=123)
response = await agent.handle(message, context)

text

**PROBLEMA:** ❓ **NO USADO EN CÓDIGO ACTUAL**

- TelegramAdapter NO usa BotFactory
- ConversationManager NO usa BotFactory
- AgendaConversationManager NO usa BotFactory

**Decisión:** 🟡 **EVALUAR (H06)**

**Opciones:**

**A) MANTENER Y USAR:**
CoreRouter debería usar BotFactory
class CoreRouter:
def init(self):
self.factory = BotFactory()

text
    # Register agents
    self.factory.register_agent("agenda", AgendaAgent)
    self.factory.register_agent("note", NoteAgent)
    # ...

async def route_to_agent(self, intent: str, **kwargs):
    agent = self.factory.create_agent(intent, **kwargs)
    return await agent.handle(...)
text

**B) DELETE:**
- Si CoreRouter usa otro patrón
- Si no se necesita dynamic registration

**Plan FASE 3 (H06):**
- ☐ Evaluar uso en CoreRouter
- ☐ Si NO → DELETE
- ☐ Si SÍ → Integrar + 5 tests

**Target H06:** Decisión final + implementación

---

### 8. CoreRouter 🔴 CREAR MVP

**Ubicación:** ❌ **NO EXISTE**

**Estado Actual:**
- **LOC:** 0
- **Framework:** NO EXISTE
- **Tests:** 0
- **Estado:** ❌ NO EXISTE

**PROBLEMA CRÍTICO:**

TelegramAdapter.py
class TelegramAdapter:
def init(self, token: str):
self.router = CoreRouter() # ❌ ImportError: CoreRouter no existe

text
async def handle_message(self, update, context):
    # Procesar con CoreRouter (placeholder)
    # TODO H03: Implementar CoreRouter.process() completo
    bot_response = "🤖 Recibí: '{user_message}'"
text

**CoreRouter ESPERADO (H03):**

src/theaia/core/router.py
from src.theaia.ml.intent_detector.router_integration import NLPPipeline
from src.theaia.agents.base_agent import BaseAgent

class CoreRouter:
"""
Router central que:
1. Procesa mensaje con NLP (Intent + Entities)
2. Rutea a agente apropiado
3. Gestiona FSM conversacional
4. Retorna respuesta

text
H03 MVP Requirements:
- NLP integration (IntentDetector + EntityExtractor)
- Agent routing (AgendaAgent, NoteAgent, ReminderAgent, QueryAgent, HelpFallbackAgent)
- FSM orchestration (ConversationStateMachine)
- Error handling
"""

def __init__(self):
    # NLP Pipeline
    self.nlp_pipeline = NLPPipeline(confidence_threshold=0.5)
    
    # Agent registry
    self.agents = {
        "create_event": AgendaAgent(),
        "create_note": NoteAgent(),
        "create_reminder": ReminderAgent(),
        "query_agenda": QueryAgent(),
        "help": HelpFallbackAgent(),
        "fallback": HelpFallbackAgent(),
    }
    
    # FSM per user
    self.fsm_instances = {}  # {user_id: ConversationStateMachine}

async def process(
    self,
    user_id: int,
    message: str,
    context: Dict[str, Any]
) -> Tuple[str, str, Dict[str, Any]]:
    """
    Procesa mensaje y retorna respuesta.
    
    Args:
        user_id: ID usuario
        message: Mensaje usuario
        context: Contexto conversación
    
    Returns:
        (bot_response, new_state, updated_context)
    """
    # 1. NLP Processing
    nlp_result = self.nlp_pipeline.process(message)
    intent = nlp_result['intent']
    confidence = nlp_result['confidence']
    entities = nlp_result['entities']
    
    # 2. Get/Create FSM
    if user_id not in self.fsm_instances:
        self.fsm_instances[user_id] = ConversationStateMachine(user_id)
    
    fsm = self.fsm_instances[user_id]
    
    # 3. Route to Agent
    if intent in self.agents:
        agent = self.agents[intent]
        
        # Agent handles message
        bot_response, agent_state, agent_context = await agent.handle(
            user_id=user_id,
            message=message,
            context=context,
            entities=entities
        )
        
        # 4. Update FSM
        fsm.merge_context(agent_context, strategy="merge")
        
        # 5. Return
        return bot_response, agent_state, fsm.context
    
    else:
        # Fallback
        return "No entiendo tu solicitud. ¿Puedes reformular?", "idle", context

def clear_session(self, user_id: int):
    """Limpia sesión usuario."""
    if user_id in self.fsm_instances:
        del self.fsm_instances[user_id]
text

**Arquitectura CoreRouter MVP:**

CoreRouter
│
├── NLPPipeline (IntentDetector + EntityExtractor)
│ ├── predict intent
│ ├── extract entities
│ └── return confidence
│
├── Agent Registry
│ ├── AgendaAgent (create_event)
│ ├── NoteAgent (create_note)
│ ├── ReminderAgent (create_reminder)
│ ├── QueryAgent (query_agenda)
│ └── HelpFallbackAgent (help, fallback)
│
├── FSM Orchestration
│ ├── ConversationStateMachine per user
│ ├── Context merging
│ └── State management
│
└── Error Handling
├── Intent confidence threshold
├── Agent exceptions
└── Fallback handling

text

**Decisión:** 🔴 **CREAR EN H03 (CRÍTICO MVP)**

**Razones:**
1. 🔴 **TelegramAdapter lo necesita** - Actualmente placeholder
2. 🔴 **MVP no funciona sin CoreRouter** - Central architecture
3. 🔴 **NLP integration depende de CoreRouter** - Único punto integración
4. 🔴 **Agent routing depende de CoreRouter** - Orquestación central

**Plan FASE 2 (H03):**

Target: 250-300 LOC CoreRouter
Tests: 25+ (routing + NLP + FSM + errors)
Integration: TelegramAdapter + WebAdapter
class CoreRouter:
# Core functionality
async def process(...) # Main entry point
async def route_to_agent(...) # Agent delegation
def get_fsm(...) # FSM per user
def clear_session(...) # Session cleanup

text
# Error handling
def handle_low_confidence(...)   # Confidence < threshold
def handle_agent_error(...)      # Agent exception
def handle_fallback(...)         # Unknown intent
text

**Añadir:**
- ✅ CoreRouter class (250-300 LOC)
- ✅ NLPPipeline integration
- ✅ Agent registry (5 agents MVP)
- ✅ FSM orchestration per user
- ✅ Error handling completo
- ✅ 25 tests (routing + integration)

**Target H03:** CoreRouter funcional al 100%, integrado en TelegramAdapter

---

## 📊 HALLAZGOS GENERALES

### Fortalezas ✅

1. **FSM architecture excelente** - BaseStateMachine + transitions library
2. **Callbacks avanzados H03** - Pre/Post/Error con context injection
3. **Context merging robusto** - 4 estrategias bien implementadas
4. **Estados bien definidos** - 5 estados principales claros
5. **Transiciones logging** - TransitionConfig completo
6. **Herencia limpia** - ABC + Mixin pattern correctos

### Debilidades ⚠️

1. **ConversationManager sobrecargado** - 350 LOC, demasiadas responsabilidades
2. **CoreRouter NO EXISTE** - CRÍTICO para MVP
3. **BotFactory sin uso** - 30 LOC no usadas en código
4. **Tests ausentes** - Coverage probablemente 0% todo Core
5. **Documentación parcial** - Docstrings incompletos

### Riesgos 🔴

1. **MVP bloqueado sin CoreRouter** - TelegramAdapter placeholder
2. **Refactor ConversationManager** - Afecta toda la aplicación
3. **Sin tests Core** - Riesgo alto en cambios
4. **Complejidad ConversationManager** - Difícil de mantener

---

## 🎯 ROADMAP MVP - CORE COMPONENTS

### FASE 2 (H03) - CoreRouter

**H03 — CoreRouter Creation (CRÍTICO)**
- 🔴 Crear CoreRouter class (250-300 LOC)
- 🔴 NLPPipeline integration
- 🔴 Agent registry (5 agents MVP)
- 🔴 FSM orchestration per user
- 🔴 Error handling
- 🔴 25 tests CoreRouter

**Duración:** 8-10h (parte de las 66h H03)

---

### FASE 3 (H06-H07) - Refactor + Tests

**H06 — Tests Core Components**
- 🟢 20 tests ConversationStateMachine
- 🟢 10 tests BaseStateMachine
- 🟢 15 tests CallbacksMixin
- 🟢 20 tests ContextMergingEngine
- 🟢 8 tests TransitionConfig
- Target: 73 tests, Coverage 85%+

**H07 — Refactor ConversationManager**
- 🟡 Separar en 5 componentes:
  - ConversationManager (150 LOC)
  - SessionManager (80 LOC)
  - DisambiguationHandler (100 LOC)
  - AgentRouter (120 LOC)
  - ErrorRecoveryHandler (80 LOC)
- 🟡 40 tests nuevos (8 por componente)
- Target: 350 LOC → 530 LOC (distribuidas), Coverage 85%+

**Duración:** 15h (H06: 8h, H07: 7h)

---

### FASE 4 (H10) - BotFactory Decision

**H10 — Evaluar BotFactory**
- 🟡 Opción A: Integrar en CoreRouter + 5 tests
- 🟡 Opción B: DELETE si no se usa

**Duración:** 2h

---

## 📈 MÉTRICAS ÉXITO MVP

### Coverage Targets

| Componente | Actual | Target MVP |
|------------|--------|------------|
| **ConversationStateMachine** | ❓ 0%? | 85%+ |
| **ConversationManager** | ❓ 0%? | 85%+ |
| **BaseStateMachine** | ❓ 0%? | 85%+ |
| **CallbacksMixin** | ❓ 0%? | 85%+ |
| **ContextMergingEngine** | ❓ 0%? | 85%+ |
| **TransitionConfig** | ❓ 0%? | 85%+ |
| **CoreRouter** | 0% | 85%+ |

### Tests Targets

| Componente | Tests Actual | Target MVP |
|------------|--------------|------------|
| **ConversationStateMachine** | 0 | 20+ |
| **ConversationManager** | 0 | 40+ (después refactor) |
| **BaseStateMachine** | 0 | 10+ |
| **CallbacksMixin** | 0 | 15+ |
| **ContextMergingEngine** | 0 | 20+ |
| **TransitionConfig** | 0 | 8+ |
| **CoreRouter** | 0 | 25+ |
| **TOTAL** | 0 | 138+ |

### Quality Targets

| Aspecto | Actual | Target MVP |
|---------|--------|------------|
| **Componentes Core** | 7 | 12 (+ 5 nuevos) |
| **LOC Total** | ~1,110 | ~1,600 |
| **Tests Total** | 0 | 138+ |
| **Coverage Promedio** | 0% | 85%+ |
| **Documentación** | ⚠️ Parcial | ✅ Completa |

---

## 💡 CONCLUSIONES

### Estado General: 🟡 **BUENO CON GAP CRÍTICO**

**Core components tienen arquitectura sólida**, pero:
1. 🔴 **CoreRouter NO EXISTE** - Bloquea MVP completo
2. ⚠️ **ConversationManager sobrecargado** - Necesita refactor
3. ❓ **Tests ausentes** - Coverage 0% (probablemente)
4. ✅ **FSM architecture excelente** - Base muy sólida

### Prioridades Inmediatas

1. **P0 - Crear CoreRouter** (H03) - CRÍTICO MVP, bloquea TelegramAdapter
2. **P0 - Tests Core** (H06) - Coverage 0% → 85%+
3. **P1 - Refactor ConversationManager** (H07) - 350 LOC → 530 LOC (5 componentes)
4. **P2 - Evaluar BotFactory** (H10) - Usar o eliminar

### Micro-recompensas Completadas

- ✅ **BLOQUE 1.4 completado** (+2 puntos)
- ✅ **8 componentes auditados**
- ✅ **CoreRouter gap detectado**
- ✅ **Roadmap Core definido**

---

## 🎉 FASE 1 COMPLETADA AL 100%

✅✅✅ FASE 1 AUDITORÍA COMPLETA ✅✅✅

BLOQUES COMPLETADOS: 4/4 (100%)

✅ Bloque 1.1: Agentes (8 puntos)

✅ Bloque 1.2: ML Components (3 puntos)

✅ Bloque 1.3: Adapters (2 puntos)

✅ Bloque 1.4: Core Components (2 puntos)

TOTAL: 15/15 puntos (100%)

COMPONENTES AUDITADOS: 26

8 Agentes

4 ML Components

1 Adapter (+ 3 faltantes identificados)

8 Core Components (+ 1 faltante identificado)

LOC ANALIZADAS: ~5,000

DOCUMENTOS GENERADOS: 4

docs/audit/AGENTS_AUDIT_2025-12-03.md

docs/audit/ML_COMPONENTS_AUDIT_2025-12-03.md

docs/audit/ADAPTERS_AUDIT_2025-12-03.md

docs/audit/CORE_AUDIT_2025-12-03.md

text

---

## 📝 PRÓXIMOS PASOS

**FASE 2 (H04-H05):**
- [ ] H04: Crear modelos SQLAlchemy (Event, Note, Reminder, QueryCache)
- [ ] H04: Implementar repositories completos
- [ ] H04: WebAdapter (REST API)
- [ ] H05: Tests E2E database + adapters

**FASE 3 (H03, H06-H10):**
- [ ] H03: **CREAR CoreRouter** (CRÍTICO)
- [ ] H06: Tests Core Components (138+ tests)
- [ ] H06-H10: Refactor 5 agentes MVP
- [ ] H07: Refactor ConversationManager (5 componentes)
- [ ] H10: Evaluar BotFactory

---

**Auditoría Core completada. CoreRouter NO EXISTE - CRÍTICO para H03.** 🎯

**¡FASE 1 COMPLETA! 🎉 Auditoría total sistema finalizada exitosamente.**

---

**Progreso Global:** 15/15 puntos FASE 1 (100%) ✅✅✅
