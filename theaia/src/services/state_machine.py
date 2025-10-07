from transitions import Machine

class ConversationalStateMachine(object):
    states = [
        "IDLE", "ASK_TITLE", "ASK_DATE", "ASK_DURATION", "CONFIRM_EVENT", "EVENT_CREATED"
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=ConversationalStateMachine.states, initial="IDLE")

        self.machine.add_transition("start_agendar", "IDLE", "ASK_TITLE")
        self.machine.add_transition("ask_date", "ASK_TITLE", "ASK_DATE")
        self.machine.add_transition("ask_duration", "ASK_DATE", "ASK_DURATION")
        self.machine.add_transition("confirm_event", "ASK_DURATION", "CONFIRM_EVENT")
        self.machine.add_transition("evento_creado", "CONFIRM_EVENT", "EVENT_CREATED")
        self.machine.add_transition("reset", "*", "IDLE")

    def reset(self):
        self.to_IDLE()
