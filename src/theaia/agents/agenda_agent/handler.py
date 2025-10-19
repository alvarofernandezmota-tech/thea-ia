# src/theaia/agents/agenda_agent/handler.py

from src.theaia.agents.base_agent import BaseAgent
from src.theaia.core.fsm.conversation_manager import ConversationManager

class AgendaAgent(BaseAgent):
    """
    Agente para gestionar el agendamiento de eventos utilizando una FSM centralizada.
    """
    def __init__(self):
        super().__init__()
        # Se renombra 'fsm' a 'conversation_manager' para mayor claridad
        self.conversation_manager = ConversationManager()

    async def handle(self, message: str, context: dict) -> str:
        """
        Delega el manejo del mensaje al ConversationManager para gestionar el diálogo.
        
        Args:
            message (str): El mensaje del usuario.
            context (dict): El contexto de la conversación.

        Returns:
            str: La respuesta generada por el estado actual de la conversación.
        """
        # El ConversationManager se encarga de toda la lógica de estados
        response = self.conversation_manager.handle_message(message, context)
        return response
