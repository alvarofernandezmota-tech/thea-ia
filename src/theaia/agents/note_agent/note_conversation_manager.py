from typing import Dict, Any, Tuple

class NoteConversationManager:
    def __init__(self, user_id: str):
        self.user_id = user_id

    def handle_message(self, user_id: str, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_note_content"
            response = "¿Qué nota quieres guardar?"
            new_state = "awaiting_note_content"
        elif context["fsm_state"] == "awaiting_note_content":
            context["note"] = message
            context["fsm_state"] = "completed"
            response = f"Nota guardada: {context['note']}"
            new_state = "completed"
        else:
            response = "No hay más acciones para notas."
            new_state = "completed"
        return response, new_state, context
