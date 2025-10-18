"""
CoreRouter de Thea IA 2.0.
Gestiona el flujo de mensajes entre el IntentDetector y los agentes.
"""

from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.database.repositories.context_repository import load_context, save_context

class CoreRouter:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.agents = []  # Los agentes se cargarán dinámicamente

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa un mensaje del usuario y lo delega al agente apropiado.
        """
        if context is None:
            context = {}

        try:
            saved = load_context(user_id)
            if saved:
                context.update(saved)
        except Exception:
            pass

        if context.get("active_agent"):
            agent = self._get_agent_by_name(context["active_agent"])
            if agent:
                return agent.handle(user_id, message, context)

        try:
            raw_intents = self.intent_detector.detect(message)
            # Asegura que los intents sean siempre una lista de strings
            if hasattr(raw_intents, '__iter__') and not isinstance(raw_intents, str):
                intents = [str(i) for i in raw_intents]
            else:
                intents = [str(raw_intents)]
        except Exception as e:
            intents = []

        for agent in self.agents:
            if agent.__class__.__name__ != "FallbackAgent" and any(agent.can_handle(it) for it in intents):
                response = agent.handle(user_id, message, context)
                try:
                    save_context(user_id, response.get("context", {}))
                except Exception:
                    pass
                return response

        fallback = self._get_fallback_agent()
        if fallback:
            response = fallback.handle(user_id, message, context)
            try:
                save_context(user_id, response.get("context", {}))
            except Exception:
                pass
            return response

        return {"status": "error", "message": "No se pudo procesar la solicitud.", "context": context}

    def _get_agent_by_name(self, agent_name: str):
        return next((a for a in self.agents if a.__class__.__name__ == agent_name), None)

    def _get_fallback_agent(self):
        return next((a for a in self.agents if a.__class__.__name__ == "FallbackAgent"), None)
