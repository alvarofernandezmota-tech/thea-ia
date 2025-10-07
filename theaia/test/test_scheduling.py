from datetime import datetime
from src.agents.scheduling.agent import SchedulingAgent

def test_scheduling_agent_basic():
    agent = SchedulingAgent(config={})
    now = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    slots = [
        {"datetime": now, "duration": 60},
        {"datetime": now.replace(hour=14), "duration": 60},
    ]
    context = {"appointment_details": {"candidates": slots, "service_id": None, "duration": 60}}
    result = agent.handle("test", user_id="u1", context=context)
    assert result["status"] == "ok"
    assert "Cita programada" in result["message"]
