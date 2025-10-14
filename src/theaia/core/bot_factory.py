# src/theaia/core/bot_factory.py

from typing import Dict, Type, Any

class BotFactory:
    """Registro e instanciación dinámica de agentes/bots para Thea IA 2.0."""
    def __init__(self):
        self._registry: Dict[str, Type] = {}

    def register_agent(self, name: str, agent_cls: Type):
        """Registra la clase del agente bajo un nombre clave."""
        self._registry[name] = agent_cls

    def create_agent(self, name: str, *args, **kwargs) -> Any:
        """Crea una instancia del agente si está registrado, devuelve None si no existe."""
        agent_cls = self._registry.get(name)
        if agent_cls:
            return agent_cls(*args, **kwargs)
        return None

    def list_agents(self) -> list:
        """Devuelve la lista de nombres de agentes registrados."""
        return list(self._registry.keys())

# Ejemplo de uso LOCAL (puedes eliminar antes de producción)
if __name__ == "__main__":
    class AgendaAgent:
        def __init__(self, usuario):
            self.usuario = usuario
        def __repr__(self):
            return f"<AgendaAgent usuario={self.usuario}>"

    factory = BotFactory()
    factory.register_agent("agenda", AgendaAgent)
    agent = factory.create_agent("agenda", "Daniel")
    print(agent)                 # <AgendaAgent usuario=Daniel>
    print(factory.list_agents()) # ['agenda']
