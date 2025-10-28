from typing import Dict, Any, Tuple

class EventConversationManager:
    """
    Gestor conversacional FSM para el EventAgent.
    """
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_event_title"
            response = "¿Qué evento deseas crear o consultar?"
            new_state = "awaiting_event_title"
        elif context["fsm_state"] == "awaiting_event_title":
            context["event_title"] = message
            context["fsm_state"] = "awaiting_event_date"
            response = "¿Qué fecha es el evento?"
            new_state = "awaiting_event_date"
        elif context["fsm_state"] == "awaiting_event_date":
            context["event_date"] = message
            context["fsm_state"] = "completed"
            response = f"Evento '{context['event_title']}' para {context['event_date']} ha sido agendado."
            new_state = "completed"
        else:
            response = "Finalizado el proceso de evento."
            new_state = "completed"
        return response, new_state, context
