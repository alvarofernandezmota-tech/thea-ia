# src/theaia/agents/note_agent/model/note_fsm.py

class NoteFSM:
    """
    Máquina de estados finitos para el flujo de creación de notas.
    
    Estados:
    - awaiting_content: Espera el contenido de la nota
    - confirmation: Espera confirmación antes de guardar
    - saved: Nota guardada correctamente
    - cancelled: Flujo cancelado por el usuario
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_content"
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

        if self.state == "awaiting_content":
            self.context["note_content"] = message.strip()
            self.state = "confirmation"
            return (
                f"¿Confirmo que guarde la nota: '{message}'? (responde sí o no)",
                self.state
            )

        elif self.state == "confirmation":
            user_response = message.strip().lower()
            if user_response in ["sí", "si", "s", "confirmar", "ok", "vale"]:
                self.state = "saved"
                return "✓ Nota guardada correctamente.", self.state
            else:
                self.state = "cancelled"
                return "Nota cancelada.", self.state

        else:
            self.state = "error"
            return "Ha ocurrido un error en el flujo de notas.", self.state
