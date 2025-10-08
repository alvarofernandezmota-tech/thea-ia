# src/theaia/agents/help_agent/tests/test_help_agent.py

import pytest
from theaia.agents.help_agent.handler import HelpAgent
from theaia.models.context import UserContext

@pytest.mark.asyncio
async def test_help_response():
    agent = HelpAgent()
    resp, _ = await agent.handle("ayuda", UserContext(user_id=1), {})
    assert "Comandos disponibles" in resp
