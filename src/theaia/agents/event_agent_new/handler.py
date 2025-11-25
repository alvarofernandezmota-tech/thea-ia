"""
EventAgent - Gestión de eventos y calendario.

Handler principal para operaciones CRUD de eventos:
- Crear evento (con fecha/hora/ubicación)
- Listar eventos (hoy/semana/mes)
- Editar evento
- Cancelar evento
- Ver detalles de evento
"""

from typing import Dict, Any
from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.event_agent_new.event_conversation_manager import EventConversationManager


class EventAgent(BaseAgent):
    """
    EventAgent: Gestión completa de eventos.
    
    Intents soportados:
    - crear_evento
    - listar_eventos
    - editar_evento
    - cancelar_evento
    - ver_evento
    """
    
    def __init__(self, user_id: str):
        """
        Initialize EventAgent.
        
        Args:
            user_id: User ID
        """
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = EventConversationManager(user_id)
    
    def get_supported_intents(self):
        """Return list of supported intents."""
        return [
            "crear_evento",
            "evento",
            "agendar",
            "calendario",
            "listar_eventos",
            "mis_eventos",
            "editar_evento",
            "cancelar_evento",
            "ver_evento"
        ]
    
    async def handle(self, user_id: str, message: str, context: Dict[str, Any]):
        """
        Handle event message.
        
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
