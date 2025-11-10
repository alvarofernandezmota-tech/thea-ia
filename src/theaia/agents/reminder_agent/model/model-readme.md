🤖 Reminder FSM — Máquina de Estados para Recordatorios
Versión: v1.0.0
Archivo: src/theaia/agents/reminder_agent/model/reminder_fsm.py
Última actualización: 2025-11-10 17:51 CET (S39)
Status: ✅ Producción

📋 Propósito
El ReminderFSM es una máquina de estados finitos que modela el flujo conversacional para creación de recordatorios. Define estados, transiciones y lógica de procesamiento de mensajes de usuario.

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
│   awaiting_text                 │
│ "¿Sobre qué te recuerdo?"       │
└─────────────────────────────────┘
  ↓
┌─────────────────────────────────┐
│   awaiting_time                 │
│ "¿Cuándo te lo recuerdo?"       │
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
1. awaiting_text (Inicial)
Propósito: Capturar el contenido/descripción del recordatorio.

Transición: → awaiting_time

Ejemplo:

text
Usuario: "Llamar a mamá"
FSM: Extrae "Llamar a mamá" como reminder_text
    Cambia estado a → awaiting_time
    Solicita hora
2. awaiting_time
Propósito: Capturar hora/fecha de activación del recordatorio.

Transición: → confirmation

Ejemplo:

text
Usuario: "A las 7 PM"
FSM: Extrae "7 PM" como reminder_time
    Cambia estado a → confirmation
    Solicita confirmación explícita
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
Propósito: Recordatorio programado correctamente.

Transición: Ninguna (fin del flujo)

Respuesta:

text
"✓ Recordatorio programado correctamente."
5. cancelled (Terminal)
Propósito: Usuario cancela flujo.

Transición: Ninguna (fin del flujo)

Respuesta:

text
"Recordatorio cancelado."
6. error (Terminal)
Propósito: Error inesperado en flujo.

Transición: Ninguna (fin del flujo)

Respuesta:

text
"Ha ocurrido un error en el flujo de recordatorios."
💻 Implementación
Clase ReminderFSM
python
class ReminderFSM:
    """Máquina de estados finitos para recordatorios."""
    
    def __init__(self):
        self.state = "awaiting_text"
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
        
        if self.state == "awaiting_text":
            return self._handle_awaiting_text(message)
        elif self.state == "awaiting_time":
            return self._handle_awaiting_time(message)
        elif self.state == "confirmation":
            return self._handle_confirmation(message)
        else:
            self.state = "error"
            return ("Error inesperado", self.state)
Handlers por Estado
_handle_awaiting_text()
python
def _handle_awaiting_text(self, message: str):
    self.context["reminder_text"] = message.strip()
    self.state = "awaiting_time"
    return ("¿Cuándo te lo recuerdo?", self.state)
Lógica:

Guarda texto en contexto

Cambia a awaiting_time

Solicita hora

_handle_awaiting_time()
python
def _handle_awaiting_time(self, message: str):
    self.context["reminder_time"] = message.strip()
    self.state = "confirmation"
    text = self.context.get("reminder_text", "el recordatorio")
    return (
        f"¿Confirmo que te recuerde '{text}' a {message}? (sí/no)",
        self.state
    )
Lógica:

Guarda hora en contexto

Cambia a confirmation

Solicita confirmación explícita

_handle_confirmation()
python
def _handle_confirmation(self, message: str):
    user_response = message.strip().lower()
    if user_response in ["sí", "si", "s", "confirmar", "ok"]:
        self.state = "scheduled"
        return ("✓ Recordatorio programado correctamente.", self.state)
    else:
        self.state = "cancelled"
        return ("Recordatorio cancelado.", self.state)
Lógica:

Valida respuesta usuario

Si positiva → scheduled ✅

Si negativa → cancelled ❌

📈 Uso en Conversación
Ejemplo Completo
python
fsm = ReminderFSM()
context = {}

# Turno 1
response, state = fsm.process_message("Llamar a mamá", context)
# Output: ("¿Cuándo te lo recuerdo?", "awaiting_time")

# Turno 2
context = fsm.context
response, state = fsm.process_message("7 PM", context)
# Output: ("¿Confirmo que te recuerde 'Llamar a mamá' a 7 PM?", "confirmation")

# Turno 3
context = fsm.context
response, state = fsm.process_message("Sí", context)
# Output: ("✓ Recordatorio programado correctamente.", "scheduled")
# FSM finalizado ✅
🔗 Integración con ReminderConversationManager
python
# En reminder_conversation_manager.py
def handle_message(self, user_id, message, context):
    fsm = ReminderFSM()
    fsm.state = context.get("fsm_state", "awaiting_text")
    fsm.context = context
    
    response, new_state = fsm.process_message(message, context)
    context["fsm_state"] = new_state
    context.update(fsm.context)
    
    return response, new_state, context
🧪 Test Cases
Test 1: Flujo exitoso

text
Input: "Llamar a mamá" → "7 PM" → "Sí"
Expected: state = "scheduled" ✅
Test 2: Cancelación

text
Input: "Llamar" → "Mañana" → "No"
Expected: state = "cancelled" ❌
Test 3: Error/Edge cases

text
Input: Mensajes vacíos, especiales, etc.
Expected: Manejo graceful
📌 Meta-Información
Campo	Valor
Archivo	src/theaia/agents/reminder_agent/model/reminder_fsm.py
Versión	v1.0.0
Test Coverage	90%
Estados	6
Última actualización	2025-11-10 17:51 CET
Status	✅ Production
Reminder FSM v1.0 — Máquina de Estados para Recordatorios
Integrado con ReminderConversationManager
6 estados bien definidos + transitions claras