from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.fallback_agent.fallback_conversation_manager import FallbackConversationManager

class FallbackAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = FallbackConversationManager(user_id)

    def get_supported_intents(self):
        # Intención genérica para fallback o None
        return ["fallback", "ninguno", "desconocido"]

    def handle(self, user_id, message, context):
        response, new_state, new_context = self.conversation_manager.handle_message(user_id, message, context)
        return response, new_state, new_context
