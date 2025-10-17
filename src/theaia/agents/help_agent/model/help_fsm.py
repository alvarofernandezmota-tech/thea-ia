# src/theaia/agents/help_agent/model/help_fsm.py

class HelpFSM:
    """
    Máquina de estados finitos para el flujo de ayuda.
    
    Estados:
    - awaiting_topic: Espera el tema sobre el que necesita ayuda
    - providing_help: Proporciona la ayuda solicitada
    - follow_up: Pregunta si necesita más ayuda
    - completed: Ayuda completada
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_topic"
        self.context = {}
        self.help_topics = {
            "general": "Thea IA puede ayudarte con: agendar citas, tomar notas, crear recordatorios, gestionar eventos y responder consultas.",
            "agenda": "Para agendar una cita, di 'agendar' y te guiaré paso a paso para crear tu cita.",
            "notas": "Para crear una nota, di 'nota' y te ayudaré a guardar la información que necesites.",
            "recordatorio": "Para crear un recordatorio, di 'recordar' y te preguntaré qué deseas recordar y cuándo.",
            "eventos": "Para crear un evento, di 'evento' y podrás programar cumpleaños, aniversarios y más.",
            "comandos": "Comandos disponibles: 'ayuda', 'agenda', 'nota', 'recordar', 'evento', 'consulta'."
        }

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

        if self.state == "awaiting_topic":
            topic = self._identify_topic(message)
            self.context["help_topic"] = topic
            self.state = "providing_help"
            
            help_text = self.help_topics.get(topic, self.help_topics["general"])
            return (
                f"{help_text}\n\n¿Necesitas ayuda con algo más?",
                self.state
            )

        elif self.state == "providing_help":
            response = message.strip().lower()
            if response in ["sí", "si", "s"]:
                self.state = "awaiting_topic"
                return "¿Sobre qué tema necesitas ayuda?", self.state
            else:
                self.state = "completed"
                return "Perfecto. Si necesitas más ayuda, solo pregunta.", self.state

        elif self.state == "completed":
            self.state = "awaiting_topic"
            topic = self._identify_topic(message)
            self.context["help_topic"] = topic
            
            help_text = self.help_topics.get(topic, self.help_topics["general"])
            return (
                f"{help_text}\n\n¿Necesitas ayuda con algo más?",
                "providing_help"
            )

        else:
            self.state = "error"
            return "Ha ocurrido un error en el sistema de ayuda.", self.state

    def _identify_topic(self, message: str):
        """Identifica el tema de ayuda basándose en el mensaje."""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["agenda", "cita", "reunión"]):
            return "agenda"
        elif any(word in message_lower for word in ["nota", "apuntar", "guardar"]):
            return "notas"
        elif any(word in message_lower for word in ["recordar", "recordatorio", "notificación"]):
            return "recordatorio"
        elif any(word in message_lower for word in ["evento", "cumpleaños", "aniversario"]):
            return "eventos"
        elif any(word in message_lower for word in ["comando", "función", "qué puedes"]):
            return "comandos"
        else:
            return "general"
