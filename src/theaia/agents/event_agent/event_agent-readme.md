🎉 Event Agent — Gestor de Eventos y Celebraciones
Versión: v1.0.0
Última actualización: 2025-11-10 17:30 CET (S39)
Status: ✅ Producción

📋 Propósito
Event Agent gestiona la creación, programación y consulta de eventos, fiestas, celebraciones y conferencias. Proporciona flujo conversacional para capturar detalles del evento y confirmación antes de guardar.

Responsabilidades:

✅ Capturar nombre del evento

✅ Recopilar fecha/hora

✅ Detectar si es recurrente

✅ Confirmar detalles antes de guardar

✅ Mantener estado FSM

🏗️ Arquitectura
text
event_agent/
├── handler.py (EventAgent class)
├── event_conversation_manager.py
├── model/
│   ├── event_fsm.py (FSM 7 estados)
│   └── __init__.py
├── tests/
│   ├── test_handler.py
│   ├── test_event_fsm.py
│   └── __init__.py
└── README.md (este archivo)
🔄 Flujo de Conversación
text
Usuario: "Quiero crear un evento"
↓
THEA: "¿Qué evento deseas crear o consultar?"
[Estado: awaiting_event_title]
↓
Usuario: "Fiesta de cumpleaños"
↓
THEA: "¿Qué fecha es el evento?"
[Estado: awaiting_event_date]
↓
Usuario: "15 de noviembre"
↓
THEA: "¿Confirmo que tenemos 'Fiesta de cumpleaños' para el 15 de noviembre?"
[Estado: confirmation]
↓
Usuario: "Sí"
↓
THEA: "✓ Evento programado correctamente."
[Estado: scheduled]
💻 Componentes
EventAgent (handler.py)
python
class EventAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = EventConversationManager(user_id)
    
    def get_supported_intents(self):
        return ["evento", "fiesta", "celebración", "conferencia"]
    
    def handle(self, user_id, message, context):
        return self.conversation_manager.handle_message(user_id, message, context)
Intenciones soportadas:

evento

fiesta

celebración

conferencia

EventConversationManager
Orquesta el flujo FSM multi-turno y mantiene contexto entre mensajes.

🧪 Testing
Test Coverage: 85%+

Tests clave:

✅ Flujo completo (title → date → confirmation → scheduled)

✅ Cancelación

✅ Validación recurrencia

✅ Contexto persistente

📌 Meta-Información
Campo	Valor
Versión	v1.0.0
Intenciones	4
Estados FSM	7
Test Coverage	85%
Status	✅ Production
Event Agent v1.0 — Gestor de Eventos Conversacional