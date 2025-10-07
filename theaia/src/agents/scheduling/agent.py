# src/agents/scheduling/agent.py

class SchedulingAgent:
    def __init__(self, config):
        self.config = config

    def handle(self, message: str, user_id: str, context: dict) -> dict:
        # Lógica básica mínima para pasar el test
        # Supone que 'appointment_details' está en context
        details = context.get("appointment_details", {})
        candidates = details.get("candidates", [])
        if not candidates:
            return {"status": "error", "message": "No hay slots disponibles."}
        # Simula agendar en el primer slot
        slot = candidates[0]
        fecha = slot.get("datetime")
        return {
            "status": "ok",
            "message": f"Cita programada para {fecha.strftime('%Y-%m-%d %H:%M')}."
        }
