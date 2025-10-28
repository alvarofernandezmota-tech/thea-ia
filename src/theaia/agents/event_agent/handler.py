from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.event_agent.event_conversation_manager import EventConversationManager

class EventAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = EventConversationManager(user_id)

    def get_supported_intents(self):
        # Añade todos los intents que debe manejar este agente
        return ["evento", "fiesta", "celebración", "conferencia"]

    def handle(self, user_id, message, context):
        response, new_state, new_context = self.conversation_manager.handle_message(user_id, message, context)
        return response, new_state, new_context
