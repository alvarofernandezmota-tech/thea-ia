States — FSM States Layer
Versión: v1.0
Ubicación: src/theaia/core/fsm/states/
Última actualización: 2025-11-10 15:15 CET (S38 Final)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Production

📖 Overview
El módulo states/ define los estados concretos que implementan cada agente conversacional en THEA IA 2.0.

Concepto clave: Inside-Out — Estados abstractos (inner) que los Agentes (outer) implementan.

text
states/ (lo específico)
   ↓ implementan
agents/ (lo general)
🏗️ Estructura Física
text
src/theaia/core/fsm/states/
├── __init__.py                    # Exportaciones públicas
├── base_states.py                 # Clase abstracta BaseState
├── global_states.py               # 6 estados globales FSM
├── agent_states.py                # Mapeo: 8 agentes + capabilities
├── agenda_states.py               # Estados especializados Agenda
├── disambiguation_state.py        # Desambiguación multi-intent
└── [más especializados si se agregan]
📚 Componentes Clave
1. BaseState (base_states.py)
Interfaz abstracta para TODOS los estados agente:

python
class BaseState(ABC):
    def on_enter(self, context: dict) -> str
        """Se ejecuta al entrar en estado. Retorna mensaje usuario."""
    
    @abstractmethod
    def on_message(self, message: str, context: dict) -> str
        """Procesa mensaje y retorna nombre del próximo estado."""
Patrón: Cada estado hereda de BaseState e implementa on_message().

Ejemplo:

python
class AwaitingDateState(BaseState):
    def on_enter(self, context):
        return "¿Para qué fecha quieres agendar?"
    
    def on_message(self, message, context):
        if "mañana" in message:
            context['date'] = message
            return 'awaiting_time'  # ← Próximo estado
        return 'awaiting_date'      # ← Reintentar
2. GlobalState (global_states.py)
Estados globales compartidos por TODO el sistema:

python
GlobalState (Enum):
  ├─ INITIAL              → Usuario inicia conversación
  ├─ AWAITING_DISAMBIGUATION → Múltiples intents detectados
  ├─ AGENT_DELEGATED      → Agente activo
  ├─ COMPLETED            → Tarea finalizada
  ├─ SESSION_TIMEOUT      → Sesión expirada (30 min)
  └─ ERROR_STATE          → Error recuperable
Validaciones: StateValidation mapea transiciones permitidas.

Ejemplos transiciones válidas:

text
INITIAL → AWAITING_DISAMBIGUATION (si 2+ intents)
INITIAL → AGENT_DELEGATED (si 1 intent claro)
AWAITING_DISAMBIGUATION → AGENT_DELEGATED (user resuelve)
AGENT_DELEGATED → COMPLETED (agent termina)
* → ERROR_STATE (si error en cualquier estado)
3. AgentStates (agent_states.py)
Mapeo: Intents → Agentes → Estados iniciales → Capabilities

8 Agentes THEA IA:

Agente	Intent	Estado Inicial	Capabilities
NoteAgent	nota, notas	awaiting_note_text	create, edit, delete, list
AgendaAgent	agenda, cita	awaiting_date_time	create, edit, delete, calendar
ReminderAgent	recordatorio	awaiting_reminder_details	create, edit, recurring, priority
EventAgent	evento	awaiting_event_details	create, location, duration
HelpAgent	ayuda	showing_help	guide, explain, contextual
QueryAgent	consulta	processing_query	search, retrieve, format
ScheduleAgent	schedule	awaiting_schedule_details	auto-schedule, conflicts
FallbackAgent	fallback	processing_fallback	error_handle, escalate
Clase: AgentStateMapping

python
INTENT_TO_AGENT = {
    "nota": AgentType.NOTE_AGENT,
    "agenda": AgentType.AGENDA_AGENT,
    "recordatorio": AgentType.REMINDER_AGENT,
    # ...
}

AGENT_INITIAL_STATES = {
    AgentType.NOTE_AGENT: "awaiting_note_text",
    AgentType.AGENDA_AGENT: "awaiting_date_time",
    # ...
}
Clase: AgentCapabilities

python
CAPABILITIES = {
    AgentType.NOTE_AGENT: {
        "actions": ["create_note", "edit_note", "delete_note"],
        "inputs": ["text", "title", "tags"],
        "outputs": ["confirmation", "note_content"],
        "features": ["text_storage", "search", "categorization"]
    },
    # ...
}
4. Agenda States (agenda_states.py)
FSM especializado para flujo de agendamiento multi-turno:

text
AwaitingDateState
  ├─ on_enter: "¿Para qué fecha quieres agendar?"
  └─ on_message: Parse "mañana" → AwaitingTimeState

AwaitingTimeState
  ├─ on_enter: "¿A qué hora?"
  └─ on_message: Parse "14:30" → AwaitingConfirmationState

AwaitingConfirmationState
  ├─ on_enter: "¿Confirmas cita para {date} a las {time}?"
  └─ on_message: 
      ├─ "sí" → completed
      └─ "no" → cancelled
Context slots (actualizados por los estados):

meeting_date (str) — Fecha ISO "2025-11-15"

meeting_time (str) — Hora "14:30"

meeting_description (str) — Descripción opcional

meeting_participants (list) — Participantes

confirmed (bool) — ¿Confirmado?

5. Disambiguation State (disambiguation_state.py)
Maneja situaciones donde hay ambigüedad en intents/parámetros:

Tipos de desambiguación:

python
DisambiguationType.INTENT_AMBIGUITY
  Ejemplo: "Guarda esto"
  Pregunta: "¿Como nota o como cita?"
  Timeout: 5 min, max 3 reintentos

DisambiguationType.CONTEXT_AMBIGUITY
  Ejemplo: Usuario proporciona info incompleta
  Pregunta: "¿Puedes ser más específico sobre X?"
  Timeout: 10 min

DisambiguationType.PARAMETER_AMBIGUITY
  Ejemplo: Usuario da parámetro ambiguo
  Pregunta: "¿Te refieres a A o B?"
  Timeout: 5 min
Handler: DisambiguationHandler

python
def generate_disambiguation_question(
    self,
    disambiguation_type: DisambiguationType,
    options: List[str],
    context: Optional[str] = None
) -> str:
    """Genera pregunta de desambiguación personalizada."""
Context: DisambiguationContext

Tracking reintentos (máx 3)

Timeout handling automático

Logging de todos los intentos

🔄 Flujo Típico: User Message → States
text
1. User: "Quiero agendar una reunión para mañana a las 3"
   ↓
2. Router detects intent: "agenda" (1 intent claro)
   ↓
3. ConversationManager: INITIAL → AGENT_DELEGATED
   ↓
4. Delegate → AgendaAgent
   ↓
5. AgendaAgent FSM (using states/):
   awaiting_date_time.on_message("mañana a las 3")
     → Extrae: date="mañana", time="3"
     → Retorna "awaiting_confirmation"
     ↓
   awaiting_confirmation.on_enter()
     → Returns "¿Confirmas cita para mañana a las 3?"
     ↓
6. User: "sí"
   ↓
   awaiting_confirmation.on_message("sí")
     → context['confirmed'] = True
     → Retorna "completed"
     ↓
7. Global FSM: AGENT_DELEGATED → COMPLETED ✅
💡 Patrones de Diseño
Pattern 1: Sequential States (Agenda)
text
State1 → State2 → State3 → completed
Cada estado se encadena secuencialmente (fecha → hora → confirmación).

Pattern 2: Conditional States (Disambiguation)
text
INITIAL → [User has 1 intent?]
           ├─ YES → AGENT_DELEGATED
           └─ NO → AWAITING_DISAMBIGUATION
Pattern 3: Retry States (Help)
text
show_help → [User satisfied?]
            ├─ YES → completed
            └─ NO → show_help (retry)
🔌 Integración con Router
ConversationManager (en fsm/) usa states indirectamente:

python
# 1. Router detecta intent
intent = intent_detector.predict(message)

# 2. Selecciona agente basado en intent
agent_class = AgentStates.get_agent_for_intent(intent)
agent = instantiate(agent_class, user_id)

# 3. Agente usa sus propios estados internos
response, new_state, updated_context = agent.handle_message(message, context)

# 4. Retorna a router con estado actualizado
Responsabilidades:

Router (global FSM): Gestiona INITIAL → DISAMBIG → DELEGATED → COMPLETED

Agent (internal FSM): Gestiona estados específicos del dominio

States: Definen transiciones y lógica de cada estado

🐛 Known Issues & Limitaciones
Alta prioridad
 Sin persistencia desambiguación — Pending data no se guardan en BD (v1.0)

 Timeouts sin callback — Usuario no notificado de timeout (v1.0)

 Sin validación transiciones — BaseState no valida on_message returns

Media prioridad
 Performance O(n) lookups — get_valid_transitions() itera estados

 Logs no estructurados — Debugging difícil con logs planos

Baja prioridad
 Sin substates — No hay estados anidados (AGENDA.awaiting_time)

 Sin condicionales complejas — Transiciones solo bool (true/false)

📝 Uso en Código
Crear nuevo estado:
python
from src.theaia.core.fsm.states.base_states import BaseState

class MyCustomState(BaseState):
    def on_enter(self, context):
        # Mensaje inicial
        return "Pregunta al usuario..."
    
    def on_message(self, message: str, context: dict) -> str:
        # Procesar respuesta
        if valid_input(message):
            context['my_slot'] = message
            return 'next_state_name'
        return 'my_custom_state'  # Reintentar
Usar estado en agente:
python
from mymodule import MyCustomState

class MyAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.states = {
            'my_state': MyCustomState(),
            'next_state': AnotherState(),
            # ...
        }
    
    def handle_message(self, message, context):
        current_state_name = context.get('current_state')
        current_state = self.states[current_state_name]
        
        next_state_name = current_state.on_message(message, context)
        next_state = self.states[next_state_name]
        
        response = next_state.on_enter(context)
        context['current_state'] = next_state_name
        
        return response, next_state_name, context
📊 Estado Actual (v1.0)
Métrica	Valor
Estados globales	6
Agentes soportados	8
Estados especializados	5 (agenda, help, query, etc.)
Tipos desambiguación	4
Coverage tests	65%
Prod ready	✅ SÍ
🔗 Referencias
FSM Engine: src/theaia/core/fsm/ (state_machine.py, conversation_manager.py)

Agentes: src/theaia/agents/ (8 handlers)

Tests: src/theaia/tests/core/test_states*

Core README: src/theaia/core/core-README.md

FSM README: src/theaia/core/fsm-README.md

📞 Soporte
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Email: alvarofernandezmota@gmail.com
Slack: #thea-ia-core
Issues: GitHub → label:core-states

Última actualización: 2025-11-10 15:15 CET (Sesión 38)
Próxima revisión: Post-H04 (FSM v2 con substates)
Modelo: Inside-Out (states → agents)