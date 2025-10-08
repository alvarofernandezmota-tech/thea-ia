# src/theaia/agents/note_agent/tests/test_note_agent.py

import pytest
from theaia.agents.note_agent.handler import NoteAgent
from theaia.models.context import UserContext

@pytest.mark.asyncio
async def test_note_creation_flow():
    agent = NoteAgent()
    ctx = UserContext(user_id=1)

    resp1, ctx1 = await agent.handle("nota", ctx, {})
    assert "¿Qué nota" in resp1
    assert ctx1.state == "creating_note"

    resp2, ctx2 = await agent.handle("Comprar leche", ctx1, {})
    assert "Nota guardada" in resp2
    assert ctx2.state is None
    assert "Comprar leche" in ctx2.data["notes"]
