# src/theaia/agents/scheduler_agent/handler.py

from theaia.agents.base_agent import BaseAgent
from theaia.models.context import UserContext
from theaia.services.scheduler_service import SchedulerService

class SchedulerAgent(BaseAgent):
    """
    Agente para programar recordatorios y notificaciones.
    """
    INTENT = "schedule_reminder"

    def __init__(self):
        self.service = SchedulerService()

    async def handle(self, text: str, ctx: UserContext, entities: dict):
        if ctx.state is None:
            ctx.state = "scheduling"
            return "¿Cuándo quieres el recordatorio? (YYYY-MM-DD HH:MM)", ctx

        if ctx.state == "scheduling":
            scheduled = await self.service.schedule(ctx.user_id, text)
            ctx.state = None
            return f"Recordatorio programado para {text} ✅", ctx

        return "No entendí cuándo programar. Usa /help para más detalles.", ctx
