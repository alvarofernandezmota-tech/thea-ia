from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.help_agent.help_conversation_manager import HelpConversationManager

class HelpAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = HelpConversationManager(user_id)

    def get_supported_intents(self):
        # Añade más sinónimos si lo deseas
        return ["ayuda", "soporte", "help", "asistencia"]

    def handle(self, user_id, message, context):
        response, new_state, new_context = self.conversation_manager.handle_message(user_id, message, context)
        return response, new_state, new_context
