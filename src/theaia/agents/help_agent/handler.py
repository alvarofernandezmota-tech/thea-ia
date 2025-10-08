# src/theaia/agents/help_agent/handler.py

from theaia.agents.base_agent import BaseAgent
from theaia.models.context import UserContext

class HelpAgent(BaseAgent):
    """
    Agente que muestra ayuda y lista de comandos.
    """
    INTENT = "help"

    async def handle(self, text: str, ctx: UserContext, entities: dict):
        commands = (
            "/start – Reiniciar conversación\n"
            "/help – Mostrar esta ayuda\n"
            "/crear_evento – Crear evento\n"
            "/nota – Guardar una nota\n"
            "/agenda – Listar eventos"
        )
        return f"Comandos disponibles:\n{commands}", ctx
