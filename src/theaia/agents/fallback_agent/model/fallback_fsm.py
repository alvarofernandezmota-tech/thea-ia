# src/theaia/agents/fallback_agent/model/fallback_fsm.py

class FallbackFSM:
    """
    FSM simple para el agente fallback.
    
    Estados:
    - unrecognized: Estado por defecto para mensajes no reconocidos
    - completed: Mensaje procesado
    """

    def __init__(self):
        self.state = "unrecognized"
        self.context = {}

    def process_message(self, message: str, context: dict):
        """
        Procesa un mensaje no reconocido y proporciona una respuesta de ayuda.
        """
        self.context.update(context)
        self.context["unrecognized_message"] = message.strip()
        
        self.state = "completed"
        
        response = (
            "Lo siento, no he entendido tu solicitud. "
            "Puedo ayudarte con:\n"
            "• Agendar citas\n"
            "• Crear notas\n"
            "• Programar recordatorios\n"
            "• Gestionar eventos\n"
            "• Responder consultas\n\n"
            "Escribe 'ayuda' para más información."
        )
        
        return response, self.state
