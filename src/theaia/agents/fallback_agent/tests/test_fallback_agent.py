from theaia.agents.fallback_agent.handler import FallbackAgent


def test_fallback_gives_suggestion():
    agent = FallbackAgent()
    resp, state, data = agent.process("u1", "xxxxx", "any", {})
    assert "prueba" in resp.lower()
    assert "agendar" in resp.lower()
    assert state == "initial"
