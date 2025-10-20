# src/theaia/agents/note_agent/note_conversation_manager.py

from typing import Dict, Any, Tuple, Optional
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class NoteConversationManager:
    """
    FSM interna del flujo de notas.
    Implementa pasos secuenciales: inicial -> texto -> confirmación -> completado.
    """

    STATES = ["initial", "awaiting_text", "confirmation", "completed"]

    def __init__(self, user_id: str):
        self.user_id = user_id

    def process_message(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        state = context.get("fsm_state", "initial")

        if state == "initial":
            return self._ask_for_text(message, context)
        elif state == "awaiting_text":
            return self._receive_text(message, context)
        elif state == "confirmation":
            return self._confirm(message, context)
        elif state == "completed":
            return self._terminate(message, context)
        else:
            return self._reset(message, context)

    def _ask_for_text(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        context["fsm_state"] = "awaiting_text"
        return ("¿Qué texto quieres guardar en tu nota?", "awaiting_text", context)

    def _receive_text(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        context["pending_note"] = message
        context["fsm_state"] = "confirmation"
        return (f"¿Deseas guardar esta nota: “{message}”?", "confirmation", context)

    def _confirm(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        answer = message.lower().strip()
        if answer in ["sí", "si", "guardar", "ok", "vale"]:
            note = context.pop("pending_note", "")
            self._save_to_context(context, note)
            context["fsm_state"] = "completed"
            return ("Nota guardada correctamente. ¿Quieres crear otra?", "completed", context)
        elif answer in ["no", "cancelar"]:
            context.pop("pending_note", None)
            context["fsm_state"] = "completed"
            return ("Nota descartada. ¿Deseas crear una nueva?", "completed", context)
        else:
            return ("No te entendí, ¿quieres guardar la nota sí o no?", "confirmation", context)

    def _terminate(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        context["delegated_intent"] = "notas"
        return ("Flujo de notas completado. Puedes pedirme otra tarea.", "completed", context)

    def _reset(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        context["fsm_state"] = "initial"
        return self._ask_for_text(message, context)

    def _save_to_context(self, context: Dict[str, Any], text: str) -> None:
        notes = context.get("notes", [])
        notes.append({
            "text": text,
            "timestamp": datetime.now().isoformat()
        })
        context["notes"] = notes
