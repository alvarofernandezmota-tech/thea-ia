from typing import Dict, Any, Tuple

class FallbackConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        response = "Lo siento, no puedo responder a esa petición. ¿Puedes expresarlo de otra forma o probar otra función?"
        new_state = "completed"
        context["fsm_state"] = "completed"
        return response, new_state, context
