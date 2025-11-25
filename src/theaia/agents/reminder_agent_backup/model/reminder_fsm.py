# src/theaia/agents/reminder_agent/model/reminder_fsm.py

class ReminderFSM:
    """
    Máquina de estados finitos para el flujo de creación de recordatorios.
    
    Estados:
    - awaiting_text: Espera el texto del recordatorio
    - awaiting_time: Espera la fecha/hora del recordatorio
    - confirmation: Espera confirmación antes de programar
    - scheduled: Recordatorio programado correctamente
    - cancelled: Flujo cancelado por el usuario
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_text"
        self.context = {}

    def process_message(self, message: str, context: dict):
        """
        Procesa el mensaje del usuario según el estado actual del FSM.
        
        Args:
            message: Mensaje del usuario
            context: Contexto conversacional
            
        Returns:
            Tupla (response, new_state)
        """
        self.context.update(context)

        if self.state == "awaiting_text":
            self.context["reminder_text"] = message.strip()
            self.state = "awaiting_time"
            return "¿Cuándo quieres que te lo recuerde?", self.state

        elif self.state == "awaiting_time":
            self.context["reminder_time"] = message.strip()
            self.state = "confirmation"
            text = self.context.get("reminder_text", "el recordatorio")
            return (
                f"¿Confirmo el recordatorio '{text}' para {message}? (sí/no)",
                self.state
            )

        elif self.state == "confirmation":
            user_response = message.strip().lower()
            if user_response in ["sí", "si", "s", "confirmar", "ok"]:
                self.state = "scheduled"
                return "✓ Recordatorio programado correctamente.", self.state
            else:
                self.state = "cancelled"
                return "Recordatorio cancelado.", self.state

        else:
            self.state = "error"
            return "Ha ocurrido un error en el flujo de recordatorios.", self.state
