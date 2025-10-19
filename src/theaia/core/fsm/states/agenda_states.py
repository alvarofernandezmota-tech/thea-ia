# src/theaia/core/fsm/states/agenda_states.py

from src.theaia.core.fsm.states.base_states import BaseState

class AwaitingDateState(BaseState):
    """Estado esperando que el usuario proporcione una fecha."""
    def on_enter(self, context):
        return "¿Para qué fecha quieres agendar?"

    def on_message(self, message, context):
        # Aquí se podría integrar reconocimiento de fecha
        if "mañana" in message or "hoy" in message:
            context['date'] = message
            return 'awaiting_time'
        return 'awaiting_date'

class AwaitingTimeState(BaseState):
    """Estado esperando que el usuario proporcione un horario."""
    def on_enter(self, context):
        return "¿A qué hora quieres agendar?"

    def on_message(self, message, context):
        # Reconocimiento de hora simplificada (debe mejorarse)
        if any(c.isdigit() for c in message):
            context['time'] = message
            return 'awaiting_confirmation'
        return 'awaiting_time'

class AwaitingConfirmationState(BaseState):
    """Estado esperando que el usuario confirme la agenda."""
    def on_enter(self, context):
        date = context.get('date', 'sin fecha')
        time = context.get('time', 'sin hora')
        return f"¿Confirmas la cita para {date} a las {time}?"  

    def on_message(self, message, context):
        if 'sí' in message.lower():
            context['confirmed'] = True
            return 'completed'
        elif 'no' in message.lower():
            context['confirmed'] = False
            return 'cancelled'
        return 'awaiting_confirmation'
