# src/theaia/agents/agenda_agent/model/agenda_fsm.py

class AgendaFSM:
    """
    Máquina de estados finitos para el flujo de agendado de citas.
    
    Estados:
    - awaiting_title: Espera el asunto o título de la cita
    - awaiting_datetime: Espera la fecha y hora del evento
    - confirmation: Espera confirmación antes de agendar
    - scheduled: Cita agendada correctamente
    - cancelled: Flujo cancelado por el usuario
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_title"
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

        if self.state == "awaiting_title":
            self.context["event_title"] = message.strip()
            self.state = "awaiting_datetime"
            return "¿Para cuándo quieres agendar esta cita o reunión?", self.state

        elif self.state == "awaiting_datetime":
            self.context["event_datetime"] = message.strip()
            self.state = "confirmation"
            title = self.context.get("event_title", "la cita")
            return (
                f"¿Confirmo que agende '{title}' para {message}? (responde sí o no)",
                self.state
            )

        elif self.state == "confirmation":
            user_response = message.strip().lower()
            if user_response in ["sí", "si", "s", "confirmar", "ok"]:
                self.state = "scheduled"
                return "✓ Cita agendada correctamente.", self.state
            else:
                self.state = "cancelled"
                return "Cita cancelada.", self.state

        else:
            self.state = "error"
            return "Ha ocurrido un error en el flujo de agendado.", self.state
