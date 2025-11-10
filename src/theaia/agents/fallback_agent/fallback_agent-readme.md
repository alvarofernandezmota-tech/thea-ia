🔄 Fallback Agent — Manejador de Intentos No Reconocidos
Versión: v1.0.0
Última actualización: 2025-11-10 20:14 CET (S14)
Status: ✅ Producción

📋 Propósito
El Fallback Agent es el componente encargado de manejar mensajes que no coinciden con ninguna intención de otros agentes. Proporciona respuestas educadas, sugiere funcionalidades disponibles y registra mensajes no reconocidos para mejora futura.

Responsabilidades principales:

✅ Detectar mensajes no reconocidos

✅ Generar respuestas contextualmente apropiadas

✅ Listar funcionalidades disponibles

✅ Sugerir acciones alternativas

✅ Mantener contexto conversacional

🏗️ Arquitectura
text
fallback_agent/
├── handler.py (FallbackAgent class)
├── fallback_conversation_manager.py
├── model/fallback_fsm.py (FSM 2 estados)
├── tests/
└── __init__.py
Intenciones soportadas: ["fallback", "ninguno", "desconocido"]

🔄 Flujo Conversacional
text
Usuario: "xyz123 gibberish"
↓
THEA: "Lo siento, no he entendido tu solicitud. Puedo ayudarte con: 
       • Agendar citas
       • Crear notas
       • Programar recordatorios
       • Gestionar eventos
       • Responder consultas
       Escribe 'ayuda' para más información."
[estado: completed]
💻 Componentes Principales
FallbackAgent (handler.py)
python
class FallbackAgent(BaseAgent):
    def __init__(self, user_id)
    def get_supported_intents() → ["fallback", "ninguno", "desconocido"]
    def handle(user_id, message, context) → (response, state, context)
Responsabilidades:

Hereda de BaseAgent

Soporta 3 intenciones genéricas

Delegación a conversation manager

FallbackConversationManager (fallback_conversation_manager.py)
python
class FallbackConversationManager:
    def __init__(self, user_id: str)
    def handle_message(user_id, message, context) → (response, state, context)
Lógica:

Devuelve respuesta fija amigable

Sugiere funcionalidades del sistema

Estado terminal: "completed"

FallbackFSM (model/fallback_fsm.py)
python
class FallbackFSM:
    def __init__(self)
    def process_message(message, context) → (response, state)
Estados: 2 (unrecognized → completed)

🧪 Testing
Coverage: 85%+

Flujos de prueba:

✅ Mensaje completamente sin sentido

✅ Generación de lista de funcionalidades

✅ Persistencia de contexto

✅ Transición de estados correcta

📊 Especificaciones
Propiedad	Valor
Versión	v1.0.0
Estados FSM	2 (unrecognized, completed)
Intenciones	3
Test Coverage	85%+
Status	✅ Production
Archivos	3 (.py) + 3 (tests)
Fallback Agent v1.0 — Manejador Robusto de Mensajes No Reconocidos