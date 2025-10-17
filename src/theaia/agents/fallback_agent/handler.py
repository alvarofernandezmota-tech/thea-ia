# src/theaia/agents/fallback_agent/handler.py

from src.theaia.agents.fallback_agent.model.fallback_fsm import FallbackFSM

class FallbackAgent:
    """
    Agente de Thea IA 2.0 que actúa como fallback para manejar
    mensajes no reconocidos por ningún otro agente.
    Proporciona ayuda y redirecciona al usuario.
    """

    def __init__(self):
        self.fsm = FallbackFSM()

    def can_handle(self, intent: str) -> bool:
        """
        El fallback siempre devuelve True porque es el último recurso.
        Solo se invoca si ningún otro agente reconoce el intent.
        """
        return True

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa mensajes no reconocidos y proporciona ayuda genérica.
        """
        self.fsm.context.update(context)
        response, state = self.fsm.process_message(message, context)
        status = "ok"

        return {
            "status": status,
            "message": response,
            "fsm_state": state,
            "context": self.fsm.context
        }
