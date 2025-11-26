from typing import Dict, Any, Tuple
from src.theaia.agents.schedule_agent.model.scheduler_fsm import SchedulerFSM


class ScheduleConversationManager:
    """Manages conversation flow for ScheduleAgent using FSM."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.fsm = SchedulerFSM()

    async def handle_message(
        self, 
        user_id: int, 
        message: str, 
        context: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """Process message through FSM and return response."""
        
        # Initialize FSM state in context if not present
        if "fsm_state" not in context:
            context["fsm_state"] = "awaiting_intent"
        
        # Process message through FSM
        response, new_state = await self.fsm.process_message(message, context)
        
        # Update context with new state
        context["fsm_state"] = new_state
        
        return response, new_state, context
