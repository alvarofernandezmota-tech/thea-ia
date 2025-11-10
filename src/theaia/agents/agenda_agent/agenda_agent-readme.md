🗓️ Agenda Agent — Gestor de Citas y Reuniones
Versión: v1.0.0
Última actualización: 2025-11-10 17:22 CET (S39)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Status: ✅ Producción

📋 Propósito
El Agenda Agent es el componente encargado de gestionar todas las operaciones relacionadas con agendamiento de citas, reuniones y eventos en THEA IA. Proporciona una interfaz conversacional fluida para que los usuarios puedan programar, consultar y modificar sus eventos de forma natural.

Responsabilidades principales:

✅ Capturar intenciones de agendamiento

✅ Recopilar información (fecha, hora, asunto)

✅ Confirmar detalles antes de guardar

✅ Gestionar conversaciones multi-turno

✅ Mantener estado FSM durante sesión

🏗️ Arquitectura
Estructura de Carpeta
text
agenda_agent/
├── handler.py (AgendaAgent class)
├── agenda_conversation_manager.py (ConversationManager)
├── model/
│   ├── agenda_fsm.py (FSM states + transitions)
│   └── __init__.py
├── tests/
│   ├── test_handler.py (unit tests handler)
│   ├── test_agenda_fsm.py (unit tests FSM)
│   └── __init__.py
└── README.md (este archivo)
Componentes Principales
1. AgendaAgent (handler.py)
python
class AgendaAgent(BaseAgent):
    """Agente responsable de gestionar citas y eventos."""
    
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = AgendaConversationManager(user_id)
    
    def get_supported_intents(self):
        return ["agenda", "cita", "reunión", "evento", "agendar"]
    
    def handle(self, user_id, message, context):
        # Delega a conversation_manager
        return self.conversation_manager.handle_message(user_id, message, context)
Responsabilidades:

✅ Hereda de BaseAgent (patrón polimórfico)

✅ Define intenciones soportadas

✅ Delegación a conversation manager

✅ Integración con router de THEA IA

2. AgendaConversationManager (agenda_conversation_manager.py)
python
class AgendaConversationManager:
    """Gestor de flujo conversacional para agendamiento."""
    
    def handle_message(self, user_id, message, context):
        # FSM-driven conversation flow
        # Retorna: (response, new_state, updated_context)
Responsabilidades:

✅ Orquestar flujo FSM

✅ Mantener contexto conversacional

✅ Generar respuestas naturales

✅ Transiciones entre estados

3. AgendaFSM (model/agenda_fsm.py)
Máquina de estados que modela el flujo de agendamiento:

text
awaiting_title
     ↓
awaiting_datetime
     ↓
confirmation
     ↓
scheduled / cancelled
🔄 Flujo de Conversación
Ejemplo Completo
text
Usuario: "Quiero agendar una cita"
THEA: "¿Para qué día deseas agendar tu cita?"
      [Estado: awaiting_date]

Usuario: "Para el viernes"
THEA: "¿A qué hora deseas agendarla?"
      [Estado: awaiting_time]

Usuario: "A las 3 PM"
THEA: "Tu reunión ha sido agendada para el viernes a las 3 PM."
      [Estado: completed]
Estados FSM
Estado	Descripción	Transición
awaiting_title	Espera asunto cita	→ awaiting_datetime
awaiting_datetime	Espera fecha/hora	→ confirmation
confirmation	Confirmar antes de guardar	→ scheduled o cancelled
scheduled	Cita guardada ✅	(finalizado)
cancelled	Usuario cancela	(finalizado)
error	Error en flujo	(finalizado)
💻 API & Uso
Inicialización
python
from src.theaia.agents.agenda_agent import AgendaAgent

agent = AgendaAgent(user_id="user_123")
Handling de Mensajes
python
# Primer mensaje
context = {"fsm_state": None}
response, state, context = agent.handle(
    user_id="user_123",
    message="Quiero agendar una cita",
    context=context
)
# Output: ("¿Para qué día deseas agendar?", "awaiting_date", {...})

# Siguiente mensaje
context["fsm_state"] = state  # Mantener estado
response, state, context = agent.handle(
    user_id="user_123", 
    message="Para el viernes",
    context=context
)
# Output: ("¿A qué hora?", "awaiting_time", {...})
Intenciones Soportadas
python
agent.get_supported_intents()
# Output: ["agenda", "cita", "reunión", "evento", "agendar"]
🔗 Integración
Con Router Principal
python
# En src/theaia/core/router.py
if message_intent in agenda_agent.get_supported_intents():
    response = agenda_agent.handle(user_id, message, context)
Con BaseAgent
python
# Patrón herencia
AgendaAgent → BaseAgent → AbstractAgent

# Implementa métodos abstractos:
- handle()
- get_supported_intents()
Con ContextManager
python
# Mantiene estado entre turnos
context = {
    "user_id": "user_123",
    "fsm_state": "awaiting_datetime",
    "event_title": "Reunión con marketing",
    "date": "2025-11-15",
    "time": "10:00"
}
📊 Dependencias
text
agenda_agent/
├── BaseAgent (src.theaia.agents.base_agent)
├── AgendaFSM (model/agenda_fsm.py)
├── ContextManager (src.theaia.core.context_manager)
└── Router (src.theaia.core.router)
🧪 Testing
Coverage: 85%+ (ver tests/README.md)

Tests principales:

✅ test_handler.py — AgendaAgent.handle()

✅ test_agenda_fsm.py — FSM transitions

✅ Edge cases (cancellation, errors)

Ejecutar tests:

bash
pytest src/theaia/agents/agenda_agent/tests/ -v
📈 Roadmap
H01: Perfeccionamiento FSM
 Mejor manejo de fechas (parsing natural)

 Soporte zona horaria

 Integración calendario real

H02: Multi-idioma
 Soporte español + inglés

 Adaptación respuestas por idioma

H03: Persistencia
 Guardar citas en BD

 Validar conflictos horarios

 Notificaciones antes de evento

🐛 Known Issues
⚠️ Parse de fechas simple (solo "viernes", "mañana")

⚠️ No valida conflictos con calendario existente

⚠️ Respuestas hard-coded (no use LLM aún)

📌 Meta-Información
Campo	Valor
Archivo	src/theaia/agents/agenda_agent/README.md
Versión	v1.0.0
Tamaño	~3.2 KB código + docs
Test Coverage	85%
Última actualización	2025-11-10 17:22 CET
Status Producción	✅ Activo
Agenda Agent v1.0 — Gestor de Citas Conversacional
Integrado con FSM core + BaseAgent
Production ready con cobertura de tests