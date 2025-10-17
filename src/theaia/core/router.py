# Archivo: src/theaia/core/router.py

from src.theaia.ml.intent_detector.inference import IntentDetector
from src.theaia.database.repositories.context_repository import load_context, save_context

class CoreRouter:
    def __init__(self):
        self.agents = []
        self.intent_detector = IntentDetector()
        print("CoreRouter inicializado.")

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        if context.get("active_agent"):
            agent = self._get_agent_by_name(context["active_agent"])
            if agent:
                print(f"Delegando a agente activo: {agent.__class__.__name__}")
                return agent.handle(user_id, message, context)

        intents = self.intent_detector.detect(message)
        
        # --- LÓGICA CORREGIDA ---
        # 1. Buscar candidatos excluyendo el FallbackAgent
        candidate_agents = [
            agent for agent in self.agents
            if agent.__class__.__name__ != 'FallbackAgent' and any(agent.can_handle(intent) for intent in intents)
        ]

        if len(candidate_agents) == 1:
            # 2. Si hay un único agente, delegar a él.
            agent = candidate_agents[0]
            print(f"Delegando a agente único: {agent.__class__.__name__}")
            return agent.handle(user_id, message, context)
        
        elif len(candidate_agents) > 1:
            # 3. Si hay varios, preguntar para desambiguar.
            print(f"Ambigüedad detectada entre: {[a.__class__.__name__ for a in candidate_agents]}")
            return {
                "status": "disambiguation",
                "message": f"Entendido. ¿Te refieres a {candidate_agents[0].__class__.__name__} o {candidate_agents[1].__class__.__name__}?",
                "options": [a.__class__.__name__ for a in candidate_agents],
                "context": context,
            }
        
        else:
            # 4. Si NO hay candidatos, usar el FallbackAgent.
            fallback_agent = self._get_agent_by_name("FallbackAgent")
            if fallback_agent:
                print("Delegando a FallbackAgent.")
                return fallback_agent.handle(user_id, message, context)
            else:
                return {"status": "error", "message": "Error: FallbackAgent no encontrado.", "context": {}}

    def _get_agent_by_name(self, name: str):
        for agent in self.agents:
            if agent.__class__.__name__ == name:
                return agent
        return None
