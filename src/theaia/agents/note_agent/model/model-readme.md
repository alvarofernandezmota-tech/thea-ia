🤖 Note FSM — Máquina de Estados para Notas
Versión: v1.0.0
Status: ✅ Production

🔄 Estados (5)
text
awaiting_content → confirmation → saved/cancelled
Estados:

awaiting_content — Capturar contenido nota

confirmation — Confirmar antes de guardar

saved — Nota guardada ✅

cancelled — Cancelado ❌

error — Error

📊 Transitions
Estado	Input	Nuevo Estado	Acción
awaiting_content	"texto"	confirmation	Guardar contenido
confirmation	"sí/ok/vale"	saved	✅ GUARDAR
confirmation	"no"	cancelled	❌ CANCELAR
any	error	error	Manejo error
💻 Métodos
python
class NoteFSM:
    def process_message(self, message, context) → (response, new_state)
Lógica:

Captura note_content en contexto

Solicita confirmación explícita

Valida respuesta usuario

Retorna estado final

🧪 Tests
✅ test_fsm_initialization()

✅ test_fsm_content_transition()

✅ test_fsm_confirmation_positive()

✅ test_fsm_confirmation_negative()

✅ test_fsm_state_persistence()

Note FSM v1.0 — 5 estados simples + claros