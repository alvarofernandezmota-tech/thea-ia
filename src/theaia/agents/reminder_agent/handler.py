"""
ReminderAgent - Gestión de recordatorios y avisos.

Handler principal para operaciones CRUD de recordatorios:
- Crear recordatorio (con fecha/hora/ubicación)
- Listar recordatorios (pendientes/completados/todos)
- Editar recordatorio
- Completar recordatorio
- Eliminar recordatorio
- Recordatorios recurrentes (opcional)
"""

from typing import Dict, Any
from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.reminder_agent.reminder_conversation_manager import ReminderConversationManager


class ReminderAgent(BaseAgent):
    """
    ReminderAgent: Gestión completa de recordatorios.
    
    Intents soportados:
    - crear_recordatorio
    - listar_recordatorios
    - editar_recordatorio
    - completar_recordatorio
    - eliminar_recordatorio
    """
    
    def __init__(self, user_id: str):
        """
        Initialize ReminderAgent.
        
        Args:
            user_id: User ID
        """
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = ReminderConversationManager(user_id)
    
    def get_supported_intents(self):
        """Return list of supported intents."""
        return [
            "crear_recordatorio",
            "recordatorio",
            "avisar",
            "recordar",
            "listar_recordatorios",
            "mis_recordatorios",
            "editar_recordatorio",
            "completar_recordatorio",
            "eliminar_recordatorio"
        ]
    
    async def handle(self, user_id: str, message: str, context: Dict[str, Any]):
        """
        Handle reminder message.
        
        Args:
            user_id: User ID
            message: User message
            context: Conversation context
            
        Returns:
            Tuple[str, str, Dict]: (response, state, updated_context)
        """
        response, new_state, new_context = await self.conversation_manager.handle_message(
            user_id, message, context
        )
        return response, new_state, new_context
