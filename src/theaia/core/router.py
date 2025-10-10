from typing import Tuple, Dict, Any
from theaia.database.repositories.context_repository import load_context, save_context
from theaia.agents.agenda_agent import AgendaAgent
from theaia.agents.notas_agent import NotasAgent
from theaia.agents.fallback_agent import FallbackAgent

class CoreRouter:
    def __init__(self):
        # Registra los agentes disponibles
        self.agents = {
            'agenda': AgendaAgent(),
            'notas': NotasAgent(),
            'fallback': FallbackAgent()
        }

    def handle(self, uid: str, message: str, state: str, context: Dict[str, Any]
              ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Procesa un mensaje del usuario dado un estado y contexto inicial.
        Retorna (response, next_state, next_context).
        """
        # 1. Si es la primera invocación, carga contexto persistido
        if state == "initial" and not context:
            saved = load_context(uid)
            if saved:
                state = saved['state']
                context = saved['data']

        # 2. Detecta intención
        intent = self._detect_intent(message)

        # 3. Selecciona el agente correspondiente
        agent = self.agents.get(intent, self.agents['fallback'])

        # 4. Procesa el mensaje con el agente
        response, new_state, new_data = agent.process(
            user_id=uid,
            message=message,
            current_state=state,
            current_data=context
        )

        # 5. Persiste el nuevo contexto
        save_context(uid, new_state, new_data)

        return response, new_state, new_data

    def _detect_intent(self, message: str) -> str:
        msg = message.lower()
        if any(w in msg for w in ['cita','agendar','reunión','meeting']):
            return 'agenda'
        if any(w in msg for w in ['nota','recordar','apuntar']):
            return 'notas'
        return 'fallback'
