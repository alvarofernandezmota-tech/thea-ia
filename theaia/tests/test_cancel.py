from src.agents.cancel.agent import CancelAgent

def test_cancel_agent_basic():
    agent = CancelAgent(config={})
    context = {
        "cancel_details": {
            "user_id": "123",
            "cita_id": 10,
            "titulo": "Cita médica"
        }
    }
    result = agent.handle("cancelar", user_id="123", context=context)
    assert result["status"] == "ok"
    assert "cancelado" in result["message"]
    assert "Cita médica" in result["message"]
