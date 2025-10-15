# src/theaia/agents/reminder_agent/model/reminder_fsm.py

class ReminderFSM:
    """
    FSM para gestionar el flujo de recordatorios/notificaciones:
    - awaiting_text: espera el texto de la notificación
    - awaiting_time: espera la fecha/hora
    - confirmation: pide confirmación al usuario
    - scheduled: estado final cuando se programa
    - cancelled: estado final cuando se cancela
    - error: cualquier error de flujo
    """
    def __init__(self):
        self.state = "awaiting_text"
        self.context = {}

    def process_message(self, message: str, context: dict):
        """
        Procesa el mensaje según el estado actual.
        Retorna (response: str, new_state: str).
        """
        # Aseguramos usar context actualizado
        self.context.update(context)

        if self.state == "awaiting_text":
            # Guardar texto y preguntar la hora
            self.context["notification_text"] = message
            self.state = "awaiting_time"
            return "¿Cuándo quieres la notificación?", self.state

        if self.state == "awaiting_time":
            # Guardar hora y pedir confirmación
            self.context["notification_time"] = message
            self.state = "confirmation"
            return (
                f"¿Confirmo que te notifique '{self.context['notification_text']}' el {message}? (sí/no)",
                self.state
            )

        if self.state == "confirmation":
            if message.strip().lower() in ("sí", "si", "s"):
                self.state = "scheduled"
                # Aquí podrías invocar registro en BD o scheduler real
                return "Notificación programada correctamente.", self.state
            else:
                self.state = "cancelled"
                return "Notificación cancelada.", self.state

        # Cualquier otro caso es error
        self.state = "error"
        return "Error en el flujo de notificación.", self.state
