# src/theaia/agents/query_agent/model/query_fsm.py

class QueryFSM:
    """
    Máquina de estados finitos para el flujo de consultas.
    
    Estados:
    - awaiting_query: Espera la pregunta o consulta del usuario
    - processing: Procesando la consulta
    - answered: Respuesta proporcionada
    - follow_up: Esperando seguimiento o nueva pregunta
    - error: Error en el flujo
    """

    def __init__(self):
        self.state = "awaiting_query"
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

        if self.state == "awaiting_query":
            self.context["user_query"] = message.strip()
            self.state = "processing"
            # Aquí se integraría con el sistema de búsqueda/IA
            return self._process_query(message)

        elif self.state == "answered":
            # Si el usuario hace follow-up
            if message.strip().lower() in ["gracias", "ok", "entendido", "vale"]:
                self.state = "completed"
                return "¿Hay algo más en lo que pueda ayudarte?", self.state
            else:
                # Nueva pregunta relacionada
                self.context["user_query"] = message.strip()
                self.state = "processing"
                return self._process_query(message)

        elif self.state == "completed":
            self.state = "awaiting_query"
            self.context["user_query"] = message.strip()
            return self._process_query(message)

        else:
            self.state = "error"
            return "Ha ocurrido un error procesando tu consulta.", self.state

    def _process_query(self, query: str):
        """
        Simula el procesamiento de una consulta.
        En producción, aquí se integraría con un LLM o sistema de búsqueda.
        """
        self.state = "answered"
        return (
            f"He procesado tu consulta: '{query}'. "
            f"Aquí está la información solicitada. ¿Necesitas más detalles?",
            self.state
        )
