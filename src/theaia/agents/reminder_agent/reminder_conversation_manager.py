from typing import Dict, Any, Tuple

class ReminderConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_reminder_message"
            response = "¿Sobre qué quieres que te recuerde?"
            new_state = "awaiting_reminder_message"
        elif context["fsm_state"] == "awaiting_reminder_message":
            context["reminder_message"] = message
            context["fsm_state"] = "awaiting_reminder_time"
            response = "¿Cuándo te lo recuerdo?"
            new_state = "awaiting_reminder_time"
        elif context["fsm_state"] == "awaiting_reminder_time":
            context["reminder_time"] = message
            context["fsm_state"] = "completed"
            response = f"¡Listo! Te recordaré: '{context['reminder_message']}' a las {context['reminder_time']}."
            new_state = "completed"
        else:
            response = "El flujo de recordatorio ha finalizado."
            new_state = "completed"
        return response, new_state, context
