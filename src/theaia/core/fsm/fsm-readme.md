FSM — Finite State Machine Engine
Versión: v1.0
Ubicación: src/theaia/core/fsm/
Última actualización: 2025-11-10 15:20 CET (S38 Final)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Production Ready

📖 Overview
El módulo fsm/ implementa el motor de máquina de estados que orquesta toda la conversación en THEA IA 2.0.

Responsabilidad: Gestionar flujo conversacional global (routing, desambiguación, delegación a agentes).

text
fsm/ (orquestador)
   ├─ Router de intents
   ├─ Gestión de contexto
   ├─ Desambiguación
   ├─ Delegación a agentes
   └─ Recuperación de sesiones
🏗️ Estructura Física
text
src/theaia/core/fsm/
├── __init__.py                          # Exporta público
├── state_machine.py                     # BaseStateMachine + ConversationStateMachine
├── conversation_manager.py              # Orquestador central
├── transitions.py                       # Configuración transiciones
├── agenda_conversation_manager.py       # Especializado Agenda
└── states/                              # Estados (ver states-README.md)
    ├── __init__.py
    ├── base_states.py
    ├── global_states.py
    ├── agent_states.py
    ├── agenda_states.py
    └── disambiguation_state.py
🔑 Componentes Clave
1. BaseStateMachine (state_machine.py)
Clase abstracta base para todas las FSM:

python
class BaseStateMachine(ABC):
    def __init__(self, user_id: str, initial_state: str = "initial")
    
    @abstractmethod
    def get_states(self) -> List[str]
    
    @abstractmethod
    def setup_transitions(self)
    
    def can_transition(self, trigger: str) -> bool
    def get_valid_transitions(self) -> List[str]
    def update_context(self, **kwargs)
    def clear_context()
    def get_context(self, key: Optional[str] = None) -> Dict
Métodos públicos:

can_transition(trigger) — ¿Es válido este trigger en estado actual?

get_valid_transitions() — Lista triggers disponibles

update_context(**kwargs) — Agrega datos al contexto conversacional

clear_context() — Limpia (mantiene essentials: user_id, session_id)

get_context(key) — Recupera contexto (todo o específico)

Transiciones universales:

reset — Retorna a initial desde cualquier estado

error — Transiciona a error_state desde cualquier estado

Ejemplo de uso:

python
fsm = ConversationStateMachine(user_id="alvaro_123")

# Verificar transición
if fsm.can_transition("request_disambiguation"):
    fsm.request_disambiguation()

# Ver contexto
print(fsm.get_context())  # {'user_id': 'alvaro_123', ...}

# Actualizar
fsm.update_context(pending_message="Agendar reunión", candidate_intents=["agenda"])
2. ConversationStateMachine (state_machine.py)
FSM especializado para orquestación conversacional THEA IA:

Estados (6 totales):

text
INITIAL
  ├─ on_enter: Esperando primer mensaje
  └─ on_message: [User sends message]
      ├─ Si 1 intent → delegate_to_agent()
      ├─ Si 2+ intents → request_disambiguation()
      └─ Si 0 intents → fallback

AWAITING_DISAMBIGUATION
  ├─ on_enter: Esperando aclaración
  └─ on_message: [User chooses]
      ├─ Si válido → resolve_disambiguation()
      ├─ Si inválido → retry (max 3)
      └─ Si timeout (5 min) → session_timeout

AGENT_DELEGATED
  ├─ on_enter: Agente activo
  └─ on_message: [Agente procesa]
      ├─ Si completa → complete_conversation()
      ├─ Si error → error_state
      └─ Si timeout (30 min) → session_timeout

COMPLETED
  ├─ on_enter: Conversación finalizada
  └─ on_message: [Esperando nuevo request o reset]

SESSION_TIMEOUT
  ├─ on_enter: Sesión expirada
  └─ on_message: [User retoma]
      └─ Volver a INITIAL

ERROR_STATE
  ├─ on_enter: Error recuperable
  └─ on_message: [User retoma o reset]
      └─ Volver a INITIAL
Métodos especializados:

python
# Desambiguación
set_pending_message(message: str, intents: List[str])
get_pending_data() -> Tuple[Optional[str], List[str]]
clear_pending_data()

# Triggers
request_disambiguation()      # initial → awaiting_disambiguation
delegate_to_agent()           # initial/awaiting → agent_delegated
resolve_disambiguation()      # awaiting → agent_delegated
complete_conversation()       # agent_delegated → completed
timeout_session()             # * → session_timeout
reset()                        # * → initial
error()                        # * → error_state
Propiedades:

python
@property
def state(self) -> str            # Estado actual
    
@property
def context(self) -> Dict[str, Any]  # Contexto global
3. ConversationManager (conversation_manager.py)
Orquestador de alto nivel — La "inteligencia" de FSM:

python
class ConversationManager:
    def __init__(self, user_id: str)
    
    def process_input(self, message: str, candidate_intents: List[str] = None) 
        → Tuple[str, str, Dict[str, Any]]
Flujo central:

python
def process_input(self, message, intents):
    # 1. Recuperar estado actual
    state = self.fsm.state
    
    # 2. Validar sesión (30 min timeout)
    if self._is_session_expired():
        return self._handle_session_timeout()
    
    # 3. Enrutar según estado global
    if state == "initial":
        return self._handle_initial_state(message, intents)
    elif state == "awaiting_disambiguation":
        return self._handle_disambiguation_state(message)
    elif state == "agent_delegated":
        return self._handle_agent_delegated_state(message)
    # ... etc
    
    # 4. Retornar (respuesta, nuevo_estado, contexto)
Métodos privados (flujos):

_handle_initial_state() — Detecta intent → disambigua o delega

_handle_disambiguation_state() — Parsea elección user → resuelve

_handle_agent_delegated_state() — Envía mensaje a agente → procesa

_start_disambiguation() — Activa estado desambiguación

_generate_disambiguation_question() — Genera pregunta user-friendly

_parse_user_choice() — Parsea "nota" → "notas"

_resolve_disambiguation() — Delegate a agente elegido

_is_session_expired() — Verifica timeout (30 min)

_is_disambiguation_expired() — Verifica timeout desambiguación (5 min)

Properties:

python
@property
def state(self) -> str                # "initial" | "awaiting_disambiguation" | etc
    
@property
def context(self) -> Dict[str, Any]   # Contexto global completo
Límites configurables:

python
session_timeout_minutes = 30           # Sesión expira en 30 min
disambiguation_timeout_minutes = 5    # Desambiguación expira en 5 min
max_disambiguation_retries = 3        # Max 3 intentos fallidos
4. TransitionConfig (transitions.py)
Configuración declarativa de transiciones:

python
class TransitionConfig:
    transition_rules = {
        'request_disambiguation': {
            'source': 'initial',
            'dest': 'awaiting_disambiguation',
            'conditions': ['_has_multiple_intents'],
            'before': ['_prepare_disambiguation'],
            'after': ['_log_disambiguation_request']
        },
        'delegate_to_agent': {
            'source': 'initial',
            'dest': 'agent_delegated',
            'conditions': ['_has_single_intent'],
            'before': ['_prepare_agent_delegation'],
            'after': ['_log_agent_delegation']
        },
        # ... más transiciones
    }
Callbacks: Hooks before/after transiciones para logging, validación, etc.

5. AgendaConversationManager (agenda_conversation_manager.py)
FSM especializado para flujo multi-turno Agenda:

python
class AgendaConversationManager:
    def __init__(self, user_id: str)
    
    def handle_message(self, message: str, context: dict) 
        → Tuple[str, dict]
Usa states/agenda_states.py:

AwaitingDateState

AwaitingTimeState

AwaitingConfirmationState

Flujo:

text
awaiting_date
  ↓ (user: "mañana")
awaiting_time
  ↓ (user: "3 PM")
awaiting_confirmation
  ↓ (user: "sí")
completed ✅
🔄 Flujo Completo: Message → FSM → Response
text
1. User: "Agendar reunión"
   ↓
2. Router.handle_request()
   ├─ Intent Detector: ["agenda"]
   └─ ConversationManager.process_input(message, intents=["agenda"])
   ↓
3. FSM state = "initial"
   ├─ len(intents) == 1 → _handle_initial_state()
   ├─ Prepare delegation → fsm.delegate_to_agent()
   └─ state: initial → agent_delegated
   ↓
4. Delegate → AgendaAgent
   ├─ agent.handle_message(message, context)
   ├─ AgendaConversationManager.handle_message()
   ├─ States: awaiting_date → awaiting_time → awaiting_confirmation
   └─ Retorna: (response, new_state, updated_context)
   ↓
5. Global FSM: agent_delegated → completed (cuando agente termina)
   ↓
6. Response to user: "✅ Reunión agendada para mañana a las 3 PM"
💡 Patrones de Diseño
Pattern 1: State-based routing
text
Según state actual, ejecutar lógica diferente
Evita if-else profundo
→ Cleaner, más testeable
Pattern 2: Context persistence
text
context['user_id']           # Siempre presente
context['pending_message']   # En desambiguación
context['delegated_intent']  # Durante agent_delegated
context['active_agent']      # Nombre agente actual
Pattern 3: Timeout management
text
Session: 30 min inactividad → automatic cleanup
Disambiguation: 5 min sin respuesta → retry o fail
Ambos: max_retries limit para evitar loops infinitos
🔌 Integración con Core
Relación con otros módulos:

text
router.py (entry point)
   ├─ Crea ConversationManager por user_id
   ├─ Llama process_input(message)
   └─ Retorna response + state + context

fsm/ (orquestador)
   ├─ Gestiona estado global
   ├─ Valida transiciones
   ├─ Aplica timeouts
   └─ Delega a agentes

agents/ (ejecutores)
   ├─ Implementan lógica específica
   ├─ Retornan al FSM
   └─ FSM actualiza estado global
📊 Contexto Conversacional
Slots típicos en context:

python
context = {
    # Essentials (always present)
    'user_id': str,
    'session_id': str,
    'created_at': timestamp,
    
    # Global FSM
    'current_state': str,
    'previous_states': List[str],
    
    # Desambiguación
    'pending_message': str,
    'candidate_intents': List[str],
    'disambiguation_retry_count': int,
    
    # Delegación
    'delegated_intent': str,
    'active_agent': str,
    'original_message': str,
    
    # Agent-specific (depende de agente)
    'meeting_date': str,
    'meeting_time': str,
    'confirmed': bool,
    # ... más slots por tipo de tarea
}
🐛 Known Issues & Limitaciones
Alta prioridad
 Sin persistencia contexto en BD — Solo memoria RAM (v1.0)

 FSM acoplado a transitions library — Difícil cambiar engine (v1.0)

 Timeout sin notificación user — Usuario no sabe por qué se limpió sesión

Media prioridad
 Performance O(n) en validación transiciones — Debe ser O(1) caché

 Logs no estructurados — Debugging complicado

Baja prioridad
 Sin soporte nested states — No hay AGENDA.awaiting_time

 Condicionales transiciones solo bool — Debería soportar expresiones

📝 Uso en Aplicación
Inicializar FSM por usuario:
python
from src.theaia.core.fsm import ConversationManager

# Crear manager
manager = ConversationManager(user_id="alvaro_123")

# Procesar mensaje
response, state, context = manager.process_input(
    message="Quiero agendar una reunión",
    candidate_intents=["agenda"]
)

print(f"Response: {response}")
print(f"State: {state}")
print(f"Context: {context}")
Acceder estado actual:
python
current_state = manager.state                  # "agent_delegated"
current_context = manager.context              # Dict completo

# Validar transiciones
valid_transitions = manager.fsm.get_valid_transitions()
can_complete = manager.fsm.can_transition("complete_conversation")
Manejar múltiples usuarios:
python
from collections import defaultdict

managers = defaultdict(lambda: ConversationManager(user_id=...))

# Para cada user_id, mantener su propio FSM
for user_id, message in incoming_messages:
    mgr = managers[user_id]
    response, state, ctx = mgr.process_input(message)
    send_response(user_id, response)
📊 Métricas Actual (v1.0)
Métrica	Valor
Estados globales	6
Transiciones válidas	14+
Agentes soportados	8
Session timeout	30 min
Disambiguation timeout	5 min
Max retries desambiguación	3
Production ready	✅ SÍ
Test coverage	65%
🔗 Referencias
States: src/theaia/core/fsm/states/ (ver states-README.md)

Agentes: src/theaia/agents/ (8 handlers)

Core: src/theaia/core/core-README.md

Tests: src/theaia/tests/core/test_fsm*

📞 Soporte
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Email: alvarofernandezmota@gmail.com
Slack: #thea-ia-core
Issues: GitHub → label:core-fsm

Última actualización: 2025-11-10 15:20 CET (Sesión 38)
Próxima revisión: Post-H04 (FSM v2 con nested states)
Modelo: Inside-Out (states → fsm → core)