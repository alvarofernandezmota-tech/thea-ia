🤖 Event FSM — Máquina de Estados para Eventos
Versión: v1.0.0
Status: ✅ Production

🔄 Estados (7)
text
awaiting_name → awaiting_date → awaiting_recurrence → confirmation → scheduled/cancelled
Estados:

awaiting_name — Capturar nombre evento

awaiting_date — Capturar fecha

awaiting_recurrence — ¿Se repite anualmente?

confirmation — Confirmar detalles

scheduled — Guardado ✅

cancelled — Cancelado ❌

error — Error

📊 Transitions
Estado Actual	Input	Nuevo Estado	Acción
awaiting_name	"Fiesta"	awaiting_date	Guardar nombre
awaiting_date	"15 nov"	awaiting_recurrence	Guardar fecha
awaiting_recurrence	"sí"	confirmation	Set is_recurrent=true
confirmation	"sí"	scheduled	✅ GUARDAR
confirmation	"no"	cancelled	❌ CANCELAR
any	error	error	Manejo error
💻 Métodos
python
class EventFSM:
    def process_message(self, message, context) → (response, new_state)
Lógica:

Guarda event_name, event_date, is_recurrent en contexto

Genera respuesta apropiada por estado

Retorna transición siguiente

🧪 Tests
✅ test_fsm_initialization()

✅ test_fsm_name_transition()

✅ test_fsm_date_transition()

✅ test_fsm_recurrence_transition()

✅ test_fsm_confirmation_positive()

✅ test_fsm_confirmation_negative()

✅ test_fsm_state_persistence()

Event FSM v1.0 — 7 estados bien definidos