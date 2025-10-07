class ModifyAgent:
    def __init__(self, config):
        self.config = config

    def handle(self, message: str, user_id: str, context: dict) -> dict:
        details = context.get("modify_details", {})
        field = details.get("field")
        new_value = details.get("new_value")
        if field == "fecha":
            fecha_str = new_value.strftime("%d/%m/%Y %H:%M")
            return {
                "status": "ok",
                "message": f"Evento modificado: nueva fecha {fecha_str}"
            }
        return {"status": "error", "message": "Campo no soportado"}
