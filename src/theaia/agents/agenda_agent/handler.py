from src.theaia.agents.base_agent import BaseAgent
from src.theaia.agents.agenda_agent.agenda_conversation_manager import AgendaConversationManager

class AgendaAgent(BaseAgent):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.conversation_manager = AgendaConversationManager(user_id)

    def get_supported_intents(self):
        return ["agenda", "cita", "reunión", "evento", "agendar"]

    def handle(self, user_id, message, context):
        response, new_state, new_context = self.conversation_manager.handle_message(user_id, message, context)
        return response, new_state, new_context
