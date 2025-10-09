from theaia.agents.help_agent.handler import HelpAgent


def test_help_lists_commands():
    agent = HelpAgent()
    resp, state, data = agent.process("u1", "ayuda", "initial", {})
    assert "agendar" in resp.lower()
    assert "nota" in resp.lower()
    assert "recordar" in resp.lower()
    assert state == "initial"
