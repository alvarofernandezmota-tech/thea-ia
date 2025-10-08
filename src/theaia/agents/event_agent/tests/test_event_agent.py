# src/theaia/agents/event_agent/tests/test_event_agent.py

import asyncio
import pytest
from theaia.agents.event_agent.handler import EventAgent
from theaia.models.context import UserContext

@pytest.mark.asyncio
async def test_event_creation_flow():
    agent = EventAgent()
    ctx = UserContext(user_id=1)

    # Paso 1: inicia flujo
    resp1, ctx1 = await agent.handle("crear evento", ctx, {})
    assert "¿Cuál es el título" in resp1
    assert ctx1.state == "creating_event"

    # Paso 2: recibo título
    resp2, ctx2 = await agent.handle("Reunión con equipo", ctx1, {})
    assert "¿Qué fecha" in resp2
    assert ctx2.state == "asking_date"
    assert ctx2.data["title"] == "Reunión con equipo"

    # Paso 3: recibo fecha
    resp3, ctx3 = await agent.handle("2025-10-09 15:00", ctx2, {})
    assert "creado ✅" in resp3
    assert ctx3.state is None
    assert ctx3.data["date"] == "2025-10-09 15:00"
