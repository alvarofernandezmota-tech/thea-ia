# src/theaia/agents/help_agent/handler.py

from src.theaia.agents.help_agent.model.help_fsm import HelpFSM

class HelpAgent:
    """
    Agente de Thea IA 2.0 encargado de proporcionar ayuda,
    documentación y guías sobre el uso del sistema.
    Orquesta el flujo de conversación mediante su FSM interna.
    """

    def __init__(self):
        self.fsm = HelpFSM()

    def can_handle(self, intent: str) -> bool:
        """Determina si este agente puede manejar el intent proporcionado."""
        return intent.lower() in [
            "ayuda", "help", "comandos", "guía", "manual",
            "instrucciones", "cómo usar", "funciones"
        ]

    def handle(self, user_id: str, message: str, context: dict) -> dict:
        """
        Procesa el mensaje del usuario y actualiza el contexto mediante la FSM.
        
        Args:
            user_id: Identificador único del usuario
            message: Mensaje de entrada del usuario
            context: Contexto conversacional actual
            
        Returns:
            dict con status, message, fsm_state y context actualizados
        """
        self.fsm.context.update(context)
        response, state = self.fsm.process_message(message, context)
        status = "ok" if state not in ["error"] else "error"

        return {
            "status": status,
            "message": response,
            "fsm_state": state,
            "context": self.fsm.context
        }
