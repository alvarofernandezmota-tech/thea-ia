from typing import Dict, Any, Tuple

class ScheduleConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_day"
            response = "¿Para qué día o periodo quieres ver o modificar tu horario?"
            new_state = "awaiting_day"
        elif context["fsm_state"] == "awaiting_day":
            context["day"] = message
            context["fsm_state"] = "awaiting_action"
            response = f"¿Quieres consultar, añadir o eliminar algo en tu horario de {context['day']}?"
            new_state = "awaiting_action"
        elif context["fsm_state"] == "awaiting_action":
            context["action"] = message
            context["fsm_state"] = "completed"
            response = f"Acción '{context['action']}' registrada para {context['day']} en tu agenda."
            new_state = "completed"
        else:
            response = "El flujo de gestión de agenda ha finalizado."
            new_state = "completed"
        return response, new_state, context
