from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.schedule_agent.schedule_conversation_manager import ScheduleConversationManager

class ScheduleAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = ScheduleConversationManager(user_id)

    def get_supported_intents(self):
        return ["horario", "agenda semanal", "planning", "schedule"]

    def handle(self, user_id, message, context):
        response, new_state, new_context = self.conversation_manager.handle_message(user_id, message, context)
        return response, new_state, new_context
