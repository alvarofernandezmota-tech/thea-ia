from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.schedule_agent.schedule_conversation_manager import ScheduleConversationManager
from typing import Dict, Any, Tuple


class ScheduleAgent(BaseAgent):
    """
    ScheduleAgent - Gestión de horarios y programación de tareas.
    
    Funcionalidades:
    - Optimizar agenda diaria/semanal
    - Encontrar tiempo libre
    - Programar reuniones en mejor momento
    - Priorizar tareas
    - Balancear carga de trabajo
    - Resolver conflictos de agenda
    """
    
    def __init__(self, user_id: int):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = ScheduleConversationManager(user_id)

    def get_supported_intents(self):
        return [
            "horario", "agenda", "planning", "schedule",
            "optimizar", "tiempo libre", "reunión",
            "priorizar", "tareas", "conflictos"
        ]

    async def handle_message(
        self, 
        user_id: int, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """Handle incoming message and return response."""
        return await self.conversation_manager.handle_message(
            user_id, message, context
        )
