# Archivo: src/theaia/agents/base_agent.py

class BaseAgent:
    """
    Clase base para todos los agentes del sistema.
    Define la interfaz común que todos los agentes deben implementar.
    """
    
    def get_supported_intents(self) -> list[str]:
        """
        Devuelve la lista de intenciones que este agente puede manejar.
        """
        raise NotImplementedError("Los agentes deben implementar get_supported_intents()")
    
    def can_handle(self, intent: str) -> bool:
        """
        Verifica si el agente puede manejar la intención dada.
        """
        return intent.lower() in [i.lower() for i in self.get_supported_intents()]
    
    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa el mensaje del usuario y devuelve una respuesta.
        Por defecto, devuelve un mensaje indicando que no se reconoció la solicitud.
        """
        context["unrecognized_message"] = message
        return {
            "status": "ok",
            "message": f"El agente {self.__class__.__name__} recibió el mensaje pero no pudo procesarlo completamente.",
            "context": context,
        }
