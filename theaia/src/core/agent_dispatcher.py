class AgentDispatcher:
    def __init__(self, config):
        self.config = config

    def dispatch(self, message, user_id, user_data):
        # Lógica mínima temporal para que funcione
        return {"message": f"Procesando: {message}"}
    
    def save_conversation(self, user_id, texto):
        # Implementación temporal vacía
        pass
