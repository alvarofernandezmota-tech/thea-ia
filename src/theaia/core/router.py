"""
CoreRouter de Thea IA 2.0.
Gestiona el flujo de mensajes entre el IntentDetector y los agentes.
"""

from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.database.repositories.context_repository import load_context, save_context


class CoreRouter:
    def __init__(self):
        self.intent_detector = IntentDetector()
        self.agents = []  # Los agentes se cargarán dinámicamente desde tests o factoría
        print("CoreRouter inicializado.")

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa un mensaje del usuario y lo delega al agente apropiado.

        Args:
            user_id: ID del usuario
            message: Mensaje del usuario
            context: Contexto de la conversación (puede ser None)

        Returns:
            dict: Respuesta con status, message y context
        """
        # 1. Normalizar contexto
        if context is None:
            context = {}

        # 2. Cargar contexto previo de DB (si existe)
        try:
            saved = load_context(user_id)
            if saved:
                context.update(saved)
        except Exception:
            pass

        # 3. Delegación a agente activo en contexto
        if context.get("active_agent"):
            agent = self._get_agent_by_name(context["active_agent"])
            if agent:
                print(f"Delegando a agente activo: {agent.__class__.__name__}")
                return agent.handle(user_id, message, context)

        # 4. Detección de intenciones con ML
        try:
            intents = self.intent_detector.detect(message)
        except Exception as e:
            print(f"Error durante la detección de intenciones: {e}")
            intents = []

        # 5. Buscar agente que maneje la intención
        for agent in self.agents:
            if agent.__class__.__name__ != "FallbackAgent" and any(agent.can_handle(it) for it in intents):
                print(f"Delegando a agente único: {agent.__class__.__name__}")
                response = agent.handle(user_id, message, context)
                # 6. Guardar contexto actualizado (si aplica)
                try:
                    save_context(user_id, response.get("context", {}))
                except Exception:
                    pass
                return response

        # 7. Fallback si no hay agente específico
        fallback = self._get_fallback_agent()
        if fallback:
            print("Delegando a FallbackAgent.")
            response = fallback.handle(user_id, message, context)
            try:
                save_context(user_id, response.get("context", {}))
            except Exception:
                pass
            return response

        # 8. Sin agente ni fallback: error genérico
        return {"status": "error", "message": "No se pudo procesar la solicitud.", "context": context}

    def _get_agent_by_name(self, agent_name: str):
        """Busca un agente por nombre de clase."""
        return next((a for a in self.agents if a.__class__.__name__ == agent_name), None)

    def _get_fallback_agent(self):
        """Obtiene la instancia de FallbackAgent."""
        return next((a for a in self.agents if a.__class__.__name__ == "FallbackAgent"), None)
