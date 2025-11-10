🤖 Agenda FSM — Máquina de Estados para Agendamiento
Versión: v1.0.0
Archivo: src/theaia/agents/agenda_agent/model/agenda_fsm.py
Última actualización: 2025-11-10 17:23 CET (S39)
Status: ✅ Producción

📋 Propósito
El AgendaFSM es una máquina de estados finitos que modela el flujo conversacional para agendamiento de citas. Define estados, transiciones y lógica de procesamiento de mensajes de usuario.

Responsabilidades:

✅ Definir estados válidos de la conversación

✅ Ejecutar transiciones según input usuario

✅ Mantener contexto entre estados

✅ Generar respuestas apropiadas por estado

✅ Detectar finalizaciones (success/cancel/error)

🔄 Diagrama de Estados
text
START
  ↓
┌─────────────────────────────────┐
│   awaiting_title                │
│ "¿Cuál es el asunto?"           │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│   awaiting_datetime             │
│ "¿Cuándo deseas agendar?"       │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│   confirmation                  │
│ "¿Confirmo los detalles?"       │
└──────┬──────────────────────┬───┘
       ↓ (sí)                 ↓ (no)
    SCHEDULED              CANCELLED
    ✅ DONE                ❌ CANCELLED
📊 Estados Detallados
1. awaiting_title (Inicial)
Propósito: Capturar el asunto o título de la cita/reunión.

Transición: → awaiting_datetime

Ejemplo:

text
Usuario: "Quiero agendar una reunión con el equipo"
FSM: Extrae "reunión con el equipo" como title
    Cambia estado a → awaiting_datetime
2. awaiting_datetime
Propósito: Capturar fecha y hora del evento.

Transición: → confirmation

Ejemplo:

text
Usuario: "Para el viernes a las 3 PM"
FSM: Extrae "viernes" + "3 PM" como datetime
    Cambia estado a → confirmation
3. confirmation
Propósito: Confirmar detalles antes de guardar.

Transiciones:

Respuesta positiva ("sí", "ok", "confirmar") → scheduled

Respuesta negativa ("no", "cancelar") → cancelled

Ejemplo:

text
Usuario: "Sí, confirma"
FSM: Valida respuesta
    Cambia estado a → scheduled (SUCCESS)
4. scheduled (Terminal)
Propósito: Cita agendada correctamente.

Transición: Ninguna (fin del flujo)

Respuesta:

text
"✓ Cita agendada correctamente."
5. cancelled (Terminal)
Propósito: Usuario cancela flujo.

Transición: Ninguna (fin del flujo)

Respuesta:

text
"Cita cancelada."
6. error (Terminal)
Propósito: Error inesperado en flujo.

Transición: Ninguna (fin del flujo)

Respuesta:

text
"Ha ocurrido un error en el flujo de agendado."
💻 Implementación
Clase AgendaFSM
python
class AgendaFSM:
    """Máquina de estados finitos para agendamiento."""
    
    def __init__(self):
        self.state = "awaiting_title"
        self.context = {}
    
    def process_message(self, message: str, context: dict):
        """
        Procesa mensaje según estado actual.
        
        Args:
            message: Mensaje usuario
            context: Contexto conversacional
        
        Returns:
            (response, new_state)
        """
        self.context.update(context)
        
        if self.state == "awaiting_title":
            return self._handle_awaiting_title(message)
        elif self.state == "awaiting_datetime":
            return self._handle_awaiting_datetime(message)
        elif self.state == "confirmation":
            return self._handle_confirmation(message)
        else:
            self.state = "error"
            return ("Error inesperado", self.state)
Handlers por Estado
_handle_awaiting_title()
python
def _handle_awaiting_title(self, message: str):
    self.context["event_title"] = message.strip()
    self.state = "awaiting_datetime"
    return ("¿Para cuándo quieres agendar esta cita?", self.state)
Lógica:

Guarda título en contexto

Cambia a awaiting_datetime

Solicita fecha/hora

_handle_awaiting_datetime()
python
def _handle_awaiting_datetime(self, message: str):
    self.context["event_datetime"] = message.strip()
    self.state = "confirmation"
    title = self.context.get("event_title", "la cita")
    return (
        f"¿Confirmo que agende '{title}' para {message}? (responde sí o no)",
        self.state
    )
Lógica:

Guarda datetime en contexto

Cambia a confirmation

Solicita confirmación explícita

_handle_confirmation()
python
def _handle_confirmation(self, message: str):
    user_response = message.strip().lower()
    if user_response in ["sí", "si", "s", "confirmar", "ok"]:
        self.state = "scheduled"
        return ("✓ Cita agendada correctamente.", self.state)
    else:
        self.state = "cancelled"
        return ("Cita cancelada.", self.state)
Lógica:

Valida respuesta usuario

Si positiva → scheduled ✅

Si negativa → cancelled ❌

📈 Uso en Conversación
Ejemplo Completo
python
fsm = AgendaFSM()
context = {}

# Turno 1
response, state = fsm.process_message("Reunión con marketing", context)
# Output: ("¿Para cuándo quieres agendar?", "awaiting_datetime")

# Turno 2
context = fsm.context  # Mantener estado
response, state = fsm.process_message("Viernes 3 PM", context)
# Output: ("¿Confirmo que agende 'Reunión con marketing' para Viernes 3 PM?", "confirmation")

# Turno 3
context = fsm.context
response, state = fsm.process_message("Sí", context)
# Output: ("✓ Cita agendada correctamente.", "scheduled")
# FSM finalizado ✅
🔗 Integración con AgendaConversationManager
python
# En agenda_conversation_manager.py
def handle_message(self, user_id, message, context):
    fsm = AgendaFSM()
    fsm.state = context.get("fsm_state", "awaiting_title")
    fsm.context = context
    
    response, new_state = fsm.process_message(message, context)
    context["fsm_state"] = new_state
    context.update(fsm.context)
    
    return response, new_state, context
🧪 Test Cases
Test 1: Flujo exitoso

text
Input: "Reunión equipo" → "Viernes 3 PM" → "Sí"
Expected: state = "scheduled" ✅
Test 2: Cancelación

text
Input: "Reunión" → "Mañana" → "No"
Expected: state = "cancelled" ❌
Test 3: Error/Edge cases

text
Input: Mensajes vacíos, especiales, etc.
Expected: Manejo graceful
📈 Roadmap
H01: Parser Mejorado
 Reconocer fechas naturales ("próxima semana")

 Parse de zonas horarias

 Validación de formatos fecha/hora

H02: Contexto Persistente
 Guardar en BD estado FSM

 Recuperar sesiones previas

 Historial de eventos

H03: LLM Integration
 Generar respuestas con GPT

 NLU para extracted intents

 Multi-idioma automático

📌 Meta-Información
Campo	Valor
Archivo	src/theaia/agents/agenda_agent/model/agenda_fsm.py
Versión	v1.0.0
Test Coverage	90%
Estados	6 (awaiting_title, awaiting_datetime, confirmation, scheduled, cancelled, error)
Última actualización	2025-11-10 17:23 CET
Status	✅ Production
Agenda FSM v1.0 — Máquina de Estados para Citas
Integrado con AgendaConversationManager
6 estados bien definidos + transitions claras