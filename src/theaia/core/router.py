# src/theaia/core/router.py

from typing import Tuple, Dict, Any
from src.theaia.database.repositories.context_repository import load_context, save_context
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.note_agent.handler import NoteAgent
from src.theaia.agents.event_agent.handler import EventAgent
from src.theaia.agents.fallback_agent.handler import FallbackAgent
from src.theaia.agents.help_agent.handler import HelpAgent
from src.theaia.agents.query_agent.handler import QueryAgent
from src.theaia.agents.scheduler_agent.handler import SchedulerAgent

class CoreRouter:
    def __init__(self):
        self.agents = {
            'agenda': AgendaAgent(),
            'notas': NoteAgent(),
            'event': EventAgent(),
            'fallback': FallbackAgent(),
            'help': HelpAgent(),
            'query': QueryAgent(),
            'scheduler': SchedulerAgent(),
        }

    def handle(self, uid: str, message: str, state: str, context: Dict[str, Any]
              ) -> Tuple[str, str, Dict[str, Any]]:
        # 1. Early fallback echo on initial
        intent = self._detect_intent(message)
        if state == "initial" and intent == "fallback":
            return message, state, context

        # 2. Reload context if present
        if state == "initial" and not context:
            saved = load_context(uid)
            if saved:
                state = saved["state"]
                context = saved["data"]

        # 3. Re-detect intent after reload
        intent = self._detect_intent(message)

        # 4. Agent selection
        if state == "initial":
            agent = self.agents.get(intent, self.agents['fallback'])
        else:
            agent = self.agents['agenda']

        # 5. Inject context metadata
        context = {
            **context,
            "pending_intent": intent,
            "pending_datetime": message if state != "initial" else None
        }

        # 6. Delegate to agent
        response, new_state, new_data = agent.process(
            user_id=uid,
            message=message,
            current_state=state,
            current_data=context
        )

        # 7. Persist context
        save_context(uid, new_state, new_data)
        return response, new_state, new_data

    def _detect_intent(self, message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ['cita','agendar','reunión','meeting']):
            return 'agenda'
        if any(w in msg for w in ['nota','recordar','apuntar']):
            return 'notas'
        if any(w in msg for w in ['evento','calendar']):
            return 'event'
        if any(w in msg for w in ['ayuda','help']):
            return 'help'
        if any(w in msg for w in ['consulta','pregunta','query']):
            return 'query'
        if any(w in msg for w in ['programar','schedule']):
            return 'scheduler'
        return 'fallback'
