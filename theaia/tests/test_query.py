from datetime import datetime
from src.agents.query.agent import QueryAgent

def test_query_agent_basic():
    agent = QueryAgent(config={})
    now = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
    context = {
        "query_details": {
            "user_id": "123",
            "filter": "proximos",
            "events": [
                {"fecha": now, "titulo": "Evento 1", "id": 1},
                {"fecha": now.replace(hour=14), "titulo": "Evento 2", "id": 2},
            ]
        }
    }
    result = agent.handle("consultar", user_id="123", context=context)
    assert result["status"] == "ok"
    assert "ID 1" in result["message"] and "ID 2" in result["message"]
