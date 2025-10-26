# src/theaia/core/manager.py

from src.theaia.core.fsm.conversation_manager import ConversationManager
from src.theaia.core.router import CoreRouter
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.reminder_agent.handler import ReminderAgent
from src.theaia.agents.event_agent.handler import EventAgent
from src.theaia.agents.query_agent.handler import QueryAgent
from src.theaia.agents.help_agent.handler import HelpAgent
from src.theaia.agents.scheduler_agent.handler import SchedulerAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent

class CoreManager:
    def __init__(self):
        # Diccionario de managers FSM por usuario
        self.fsm_managers = {}

        # Inicializa agentes y router
        self.agents = [
            AgendaAgent(),
            NoteAgent(),
            ReminderAgent(),
            EventAgent(),
            QueryAgent(),
            HelpAgent(),
            SchedulerAgent(),
            FallbackAgent(),
        ]
        self.router = CoreRouter()
        self.router.agents = self.agents

    def get_fsm(self, user_id):
        # Crea o recupera el FSM para usuario
        if user_id not in self.fsm_managers:
            self.fsm_managers[user_id] = ConversationManager(user_id)
        return self.fsm_managers[user_id]

    def handle(self, user_id, message, state, context, metadata=None):
        # Ejecuta la lógica principal: FSM + Router + Agents
        fsm = self.get_fsm(user_id)
        response, new_state, new_context = fsm.process_input(message, context.get("intents", []))
        # Puedes conectar aquí el router, LLM o delegar agentes
        return response, new_state, new_context
