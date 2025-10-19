# src/theaia/core/fsm/agenda_conversation_manager.py

from transitions import Machine
from .states.agenda_states import AwaitingDateState, AwaitingTimeState, AwaitingConfirmationState

class AgendaFSMModel:
    """
    [translate:Un objeto modelo para la FSM del especialista de agenda.]
    """
    pass

class AgendaConversationManager:
    """
    [translate:Manager especializado para el diálogo multi-turno de agendamiento.]
    """
    def __init__(self, user_id=None):
        self.user_id = user_id
        self.model = AgendaFSMModel()
        
        self.state_objects = {
            'awaiting_date': AwaitingDateState(),
            'awaiting_time': AwaitingTimeState(),
            'awaiting_confirmation': AwaitingConfirmationState(),
        }

        self.machine = Machine(
            model=self.model, 
            states=list(self.state_objects.keys()) + ['completed', 'cancelled'], 
            initial='awaiting_date'
        )

    def handle_message(self, message: str, context: dict) -> tuple[str, dict]:
        """
        [translate:Gestiona un turno de la conversación de agendamiento.]
        """
        current_state_name = context.get('fsm_state') or 'awaiting_date'
        self.model.state = current_state_name

        if current_state_name in ['completed', 'cancelled']:
            return "[translate:La conversación sobre la cita ya ha finalizado.]", context

        current_state_obj = self.state_objects.get(self.model.state)
        
        next_state_name = current_state_obj.on_message(message, context)
        
        # --- LA VICTORIA ESTÁ AQUÍ (PARTE 1) ---
        # [translate:Actualizamos el estado interno en el contexto INMEDIATAMENTE.]
        context['fsm_state'] = next_state_name
        
        self.model.state = next_state_name
        next_state_obj = self.state_objects.get(self.model.state)

        if next_state_obj:
            response_text = next_state_obj.on_enter(context)
        else:
            # --- LA VICTORIA ESTÁ AQUÍ (PARTE 2) ---
            # [translate:Nos aseguramos de que el contexto refleje el estado final correcto.]
            if context.get('confirmed'):
                context['fsm_state'] = 'completed'
                response_text = "[translate:¡Perfecto! He agendado la cita.]"
            else:
                context['fsm_state'] = 'cancelled'
                response_text = "[translate:De acuerdo, he cancelado el proceso.]"
            
        return response_text, context
