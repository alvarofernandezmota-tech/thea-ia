# src/theaia/agents/note_agent/handler.py

from typing import Dict, Any, Tuple
from src.theaia.agents.note_agent.note_conversation_manager import NoteConversationManager

class NoteAgent:
    """
    Agente especializado en gestionar notas.
    Forma parte del ecosistema de agentes de Thea IA 3.0.
    """

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.manager = NoteConversationManager(user_id)

    def can_handle(self, intent: str) -> bool:
        """
        Indica si este agente puede manejar la intención actual.
        """
        return intent in ["nota", "notas", "guardar_nota", "recordar_nota"]

    def handle(self, message: str, context: Dict[str, Any]) -> Tuple[str, str, Dict[str, Any]]:
        """
        Procesa el mensaje con el FSM interno NoteConversationManager.
        """
        response, state, updated_context = self.manager.process_message(message, context)
        return response, state, updated_context
