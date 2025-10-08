# src/theaia/agents/query_agent/handler.py

from theaia.agents.base_agent import BaseAgent
from theaia.models.context import UserContext
from theaia.database.repositories.event_repository import EventRepository

class QueryAgent(BaseAgent):
    """
    Agente para consultas generales sobre agenda y eventos.
    """
    INTENT = "list_events"

    def __init__(self):
        self.repo = EventRepository()

    async def handle(self, text: str, ctx: UserContext, entities: dict):
        events = await self.repo.list_by_user(ctx.user_id)
        if not events:
            return "No tienes eventos programados.", ctx
        lines = [f"- {e.title} @ {e.date}" for e in events]
        return "Tus eventos:\n" + "\n".join(lines), ctx
