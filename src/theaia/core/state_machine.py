from transitions import Machine
from theaia.core.context_manager import Context

class BotStates:
    IDLE = "idle"
    PROCESSING = "processing"
    RESPONDING = "responding"

class BotStateMachine:
    def __init__(self, context: Context):
        self.context = context
        self.states = [BotStates.IDLE, BotStates.PROCESSING, BotStates.RESPONDING]
        self.transitions = [
            {"trigger": "receive_message", "source": BotStates.IDLE,       "dest": BotStates.PROCESSING},
            {"trigger": "process_done",    "source": BotStates.PROCESSING, "dest": BotStates.RESPONDING},
            {"trigger": "response_sent",   "source": BotStates.RESPONDING, "dest": BotStates.IDLE},
        ]
        self.machine = Machine(model=self, states=self.states, transitions=self.transitions,
                               initial=self.context.state or BotStates.IDLE)

    def to_processing(self, message_text: str):
        self.context.last_message = message_text
        self.receive_message()

    def to_responding(self, response_text: str):
        self.context.last_response = response_text
        self.process_done()

    def reset(self):
        self.response_sent()

    def persist(self):
        # Persistir el nuevo estado en el contexto
        from theaia.core.context_manager import save_context
        save_context(self.context)
