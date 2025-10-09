class FallbackAgent:
    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        response = (
            "Lo siento, no puedo ayudarte con eso. "
            "Prueba comandos como 'agendar', 'nota', 'recordar', 'ayuda'."
        )
        new_state = 'initial'
        new_data = {}
        return response, new_state, new_data
