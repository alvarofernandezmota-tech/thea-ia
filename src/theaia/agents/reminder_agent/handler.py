# src/theaia/agents/reminder_agent/handler.py

from src.theaia.agents.reminder_agent.model.reminder_fsm import ReminderFSM

class ReminderAgent:
    """
    Gestiona el flujo de recordatorios/notificaciones:
    - recibe el texto a recordar
    - delega la lógica en el FSM
    """
    def __init__(self):
        self.fsm = ReminderFSM()

    def can_handle(self, intent: str) -> bool:
        """Indica si este agente puede manejar el intent dado."""
        return intent.lower() in ["recordatorio", "notificacion"]

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa el mensaje:
        - llama al FSM para obtener respuesta, nuevo estado y contexto
        - devuelve dict con status, message, fsm_state y context
        """
        # fusionar contexto previo
        self.fsm.context.update(context)

        response, new_state = self.fsm.process_message(message, context)
        return {
            "status": "ok" if new_state not in ("error",) else "error",
            "message": response,
            "fsm_state": new_state,
            "context": self.fsm.context
        }
