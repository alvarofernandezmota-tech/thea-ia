# src/theaia/agents/query_agent/tests/test_query_agent.py

import pytest
from theaia.agents.query_agent.handler import QueryAgent
from theaia.models.context import UserContext

class FakeEventRepo:
    async def list_by_user(self, user_id):
        return []

@pytest.mark.asyncio
async def test_query_no_events(monkeypatch):
    agent = QueryAgent()
    monkeypatch.setattr(agent, "repo", FakeEventRepo())
    ctx = UserContext(user_id=1)
    resp, _ = await agent.handle("agenda", ctx, {})
    assert "No tienes eventos" in resp
