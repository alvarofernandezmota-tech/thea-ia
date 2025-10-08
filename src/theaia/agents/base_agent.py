# src/theaia/agents/base_agent.py

from theaia.models.context import UserContext

class BaseAgent:
    """
    Interfaz base para todos los agentes.
    Cada agente debe definir la constante INTENT y el método handle().
    """
    INTENT: str

    async def handle(
        self,
        text: str,
        ctx: UserContext,
        entities: dict
    ) -> (str, UserContext):
        raise NotImplementedError("Cada agente debe implementar handle()")
