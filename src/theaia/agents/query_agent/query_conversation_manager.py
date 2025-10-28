from typing import Dict, Any, Tuple

class QueryConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_query"
            response = "¿Qué consulta o búsqueda quieres realizar?"
            new_state = "awaiting_query"
        elif context["fsm_state"] == "awaiting_query":
            context["user_query"] = message
            context["fsm_state"] = "completed"
            response = f"Recibida tu consulta: \"{context['user_query']}\". Buscaré la información correspondiente."
            new_state = "completed"
        else:
            response = "No se puede procesar más consultas en este flujo."
            new_state = "completed"
        return response, new_state, context
