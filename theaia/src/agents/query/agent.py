class QueryAgent:
    def __init__(self, config):
        self.config = config

    def handle(self, message: str, user_id: str, context: dict) -> dict:
        details = context.get("query_details", {})
        events = details.get("events", [])
        if not events:
            return {"status": "ok", "message": "No tienes eventos."}
        lines = []
        for e in events:
            fecha = e["fecha"].strftime("%d/%m %H:%M")
            lines.append(f"{fecha} - {e['titulo']} | ID {e['id']}")
        return {"status": "ok", "message": "\n".join(lines)}
