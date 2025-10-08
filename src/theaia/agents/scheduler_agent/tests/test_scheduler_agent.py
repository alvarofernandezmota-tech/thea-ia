# src/theaia/agents/scheduler_agent/tests/test_scheduler_agent.py

import pytest
from theaia.agents.scheduler_agent.handler import SchedulerAgent
from theaia.models.context import UserContext

class FakeSchedulerService:
    async def schedule(self, user_id, time_str):
        return True

@pytest.mark.asyncio
async def test_scheduler_flow(monkeypatch):
    agent = SchedulerAgent()
    monkeypatch.setattr(agent, "service", FakeSchedulerService())
    ctx = UserContext(user_id=1)

    resp1, ctx1 = await agent.handle("recordar", ctx, {})
    assert "¿Cuándo quieres" in resp1
    assert ctx1.state == "scheduling"

    resp2, ctx2 = await agent.handle("2025-10-10 10:00", ctx1, {})
    assert "programado" in resp2
    assert ctx2.state is None
