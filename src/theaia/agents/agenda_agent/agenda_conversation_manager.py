from typing import Dict, Any, Tuple

class AgendaConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_date"
            response = "¿Para qué día deseas agendar tu cita?"
            new_state = "awaiting_date"
        elif context["fsm_state"] == "awaiting_date":
            context["date"] = message
            context["fsm_state"] = "awaiting_time"
            response = "¿A qué hora deseas agendarla?"
            new_state = "awaiting_time"
        elif context["fsm_state"] == "awaiting_time":
            context["time"] = message
            context["fsm_state"] = "completed"
            response = f"Tu reunión ha sido agendada para el {context['date']} a las {context['time']}."
            new_state = "completed"
        else:
            response = "El flujo de agenda ha finalizado."
            new_state = "completed"
        return response, new_state, context
