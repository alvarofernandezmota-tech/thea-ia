🤖 Schedule FSM — Máquina de Estados (3 Simple)
Versión: v1.0.0 | Status: ✅ Producción

🔄 Diagrama
text
START
  ↓
awaiting_day (¿Qué día?)
  ↓
awaiting_action (¿Qué acción?)
  ↓
completed ✅
📊 Estados
Estado	Propósito	Transición
awaiting_day	Capturar día/período	→ awaiting_action
awaiting_action	Capturar tipo acción	→ completed
completed	Registro finalizado	(terminal)
💻 Lógica
python
class ScheduleFSM:
    def __init__(self):
        self.state = "awaiting_day"
        self.context = {}
    
    def process_message(self, message: str, context: dict):
        self.context.update(context)
        
        if self.state == "awaiting_day":
            self.context["day"] = message.strip()
            self.state = "awaiting_action"
            return ("¿Quieres consultar, añadir o eliminar?", self.state)
        
        elif self.state == "awaiting_action":
            self.context["action"] = message.strip()
            self.state = "completed"
            day = self.context.get("day", "la fecha")
            action = self.context.get("action", "la acción")
            return (
                f"Acción '{action}' registrada para {day}.",
                self.state
            )
        
        else:
            return ("Error en flujo.", "error")
🧪 Tests: 85%+
✅ test_fsm_init()

✅ test_day_transition()

✅ test_action_transition()

✅ test_completion()

Schedule FSM v1.0 — 3 Estados (Minimal Design)