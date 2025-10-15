# src/theaia/core/router.py

from typing import Tuple, Dict, Any
from src.theaia.core.fsm.conversation_manager import ConversationManager
from src.theaia.database.repositories.context_repository import load_context, save_context
from src.theaia.agents.agenda_agent import AgendaAgent
from src.theaia.agents.note_agent import NoteAgent
from src.theaia.agents.reminder_agent import ReminderAgent
from src.theaia.agents.fallback_agent import FallbackAgent
# ... otros imports de agentes

class CoreRouter:
    def __init__(self):
        self.agents = {
            'agenda': AgendaAgent(),
            'notas': NoteAgent(),
            'recordatorio': ReminderAgent(),
            'fallback': FallbackAgent(),
            # ... otros agentes
        }
        self.conversation_managers: Dict[str, ConversationManager] = {}

    def handle(self, uid: str, message: str, state: str, context: Dict[str, Any]
              ) -> Tuple[str, str, Dict[str, Any]]:

        # Obtener o crear ConversationManager para este usuario
        if uid not in self.conversation_managers:
            self.conversation_managers[uid] = ConversationManager(uid)
            saved = load_context(uid)
            if saved:
                cm = self.conversation_managers[uid]
                cm.fsm.state = saved.get("fsm_state", "initial")
                cm.fsm.context = saved.get("context", {})

        cm = self.conversation_managers[uid]

        # Detectar intents candidatos
        intents = self._detect_multiple_intents(message)

        # Procesar con FSM
        response, new_state, new_context = cm.process_input(message, intents)

        # Persistir estado y contexto
        save_context(uid, new_state, {
            "fsm_state": cm.fsm.state,
            "context": cm.fsm.context,
            **new_context
        })

        return response, new_state, new_context

    def _detect_multiple_intents(self, message: str) -> list:
        """Detecta múltiples intents candidatos usando palabras clave."""
        msg = message.lower()
        candidates = []

        if any(w in msg for w in ['cita','agendar','reunión','meeting']):
            candidates.append('agenda')
        if any(w in msg for w in ['nota','apuntar','escribir','documentar']):
            candidates.append('notas')
        if any(w in msg for w in ['recordatorio','recordar','avisar','alerta']):
            candidates.append('recordatorio')
        if any(w in msg for w in ['evento','calendar']):
            candidates.append('event')
        if any(w in msg for w in ['ayuda','help']):
            candidates.append('help')
        if any(w in msg for w in ['consulta','pregunta','query']):
            candidates.append('query')
        if any(w in msg for w in ['programar','schedule']):
            candidates.append('scheduler')
        # ... otros intents

        return candidates if candidates else ['fallback']
