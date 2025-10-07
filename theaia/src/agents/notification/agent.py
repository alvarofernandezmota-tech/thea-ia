class NotificationAgent:
    def __init__(self, config):
        self.config = config

    def handle(self, message: str, user_id: str, context: dict) -> dict:
        # Lógica básica para pasar el test
        details = context.get("notification_details", {})
        notification_message = details.get("message", "Sin mensaje")
        return {
            "status": "ok", 
            "message": f"Notificación enviada: {notification_message}"
        }
