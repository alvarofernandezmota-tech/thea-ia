from datetime import datetime, timedelta
from src.agents.modify.agent import ModifyAgent

def test_modify_agent_basic():
    agent = ModifyAgent(config={})
    # Datos de evento original
    original = {
        "id": 5,
        "fecha_inicio": datetime.now().replace(hour=9, minute=0, second=0, microsecond=0),
        "duracion": 60,
        "titulo": "Reunión"
    }
    # Queremos cambiar la fecha a +1 hora
    new_time = original["fecha_inicio"] + timedelta(hours=1)
    context = {
        "modify_details": {
            "user_id": "123",
            "cita_id": 5,
            "field": "fecha",
            "new_value": new_time,
            "original_event": original
        }
    }
    result = agent.handle("modificar", user_id="123", context=context)
    assert result["status"] == "ok"
    assert "modificado" in result["message"]
    assert str(new_time.strftime("%d/%m/%Y %H:%M")) in result["message"]
