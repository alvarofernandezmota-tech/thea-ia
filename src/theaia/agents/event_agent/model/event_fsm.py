# src/theaia/agents/event_agent/model/event_fsm.py

class EventFSM:
    """
    Máquina de estados finitos para el flujo de gestión de eventos.
    
    Estados:
    - awaiting_name: Espera el nombre del evento
    - awaiting_date: Espera la fecha del evento
    - awaiting_recurrence: Pregunta si el evento es recurrente
    - confirmation: Espera confirmación antes de guardar
    - scheduled: Evento programado correctamente
    - cancelled: Flujo cancelado por el usuario
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_name"
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

        if self.state == "awaiting_name":
            self.context["event_name"] = message.strip()
            self.state = "awaiting_date"
            return "¿Cuándo es este evento?", self.state

        elif self.state == "awaiting_date":
            self.context["event_date"] = message.strip()
            self.state = "awaiting_recurrence"
            return "¿Este evento se repite cada año? (sí/no)", self.state

        elif self.state == "awaiting_recurrence":
            user_response = message.strip().lower()
            self.context["is_recurrent"] = user_response in ["sí", "si", "s"]
            self.state = "confirmation"
            
            event_name = self.context.get("event_name", "el evento")
            event_date = self.context.get("event_date", "la fecha")
            recurrence = "anualmente" if self.context["is_recurrent"] else "una sola vez"
            
            return (
                f"¿Confirmo el evento '{event_name}' para {event_date}, "
                f"que se repetirá {recurrence}? (sí/no)",
                self.state
            )

        elif self.state == "confirmation":
            user_response = message.strip().lower()
            if user_response in ["sí", "si", "s", "confirmar", "ok"]:
                self.state = "scheduled"
                return "✓ Evento programado correctamente.", self.state
            else:
                self.state = "cancelled"
                return "Evento cancelado.", self.state

        else:
            self.state = "error"
            return "Ha ocurrido un error en el flujo de eventos.", self.state
