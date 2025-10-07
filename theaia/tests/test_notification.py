from datetime import datetime
from src.agents.notification.agent import NotificationAgent

def test_notification_agent_basic():
    agent = NotificationAgent(config={})
    now = datetime.now()
    context = {
        "notification_details": {
            "message": "Recordatorio de cita",
            "user_id": "123",
            "scheduled_time": now
        }
    }
    result = agent.handle("send_notification", user_id="123", context=context)
    assert result["status"] == "ok"
    assert "Notificación enviada" in result["message"]
