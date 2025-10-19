# src/theaia/core/conversation_manager.py

from src.theaia.core.fsm.states.agenda_states import AwaitingDateState, AwaitingTimeState, AwaitingConfirmationState
from src.theaia.core.fsm.state_machine import ConversationStateMachine

class ConversationManager:
    def __init__(self):
        self.state_machine = ConversationStateMachine(states={
            'awaiting_date': AwaitingDateState(),
            'awaiting_time': AwaitingTimeState(),
            'awaiting_confirmation': AwaitingConfirmationState(),
            'completed': None, # Estado final
            'cancelled': None  # Estado final
        })

    def handle_message(self, message, context):
        # Obtiene el estado actual del contexto o empieza desde el inicio
        current_state_name = context.get('state', 'awaiting_date')
        self.state_machine.set_state(current_state_name)

        # Procesa el mensaje con el estado actual y obtiene el siguiente estado
        next_state_name = self.state_machine.current_state.on_message(message, context)
        context['state'] = next_state_name
        self.state_machine.set_state(next_state_name)

        # Obtiene la respuesta para el usuario (el "on_enter" del nuevo estado)
        if self.state_machine.current_state:
            response_text = self.state_machine.current_state.on_enter(context)
        else:
            # Si el estado es final (completed/cancelled)
            response_text = "¡Cita agendada!" if context.get('confirmed') else "Cita cancelada."
            
        return response_text
