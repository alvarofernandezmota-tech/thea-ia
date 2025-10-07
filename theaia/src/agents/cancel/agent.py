class CancelAgent:
    def __init__(self, config):
        self.config = config

    def handle(self, message: str, user_id: str, context: dict) -> dict:
        details = context.get("cancel_details", {})
        titulo = details.get("titulo", "Evento")
        return {
            "status": "ok",
            "message": f"Evento cancelado: {titulo}"
        }
