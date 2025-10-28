from typing import Dict, Any, Tuple

class HelpConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        response = "¿En qué puedo ayudarte? Puedes pedirme funciones como gestionar tu agenda, eventos, notas, recordatorios y mucho más."
        new_state = "completed"
        context["fsm_state"] = "completed"
        return response, new_state, context
