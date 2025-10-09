class EventAgent:
    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        if current_state == 'initial':
            response = "¿Qué tipo de evento quieres gestionar?"
            new_state = 'awaiting_event_type'
            new_data = current_data
        elif current_state == 'awaiting_event_type':
            event_type = message.strip()
            new_data = {**current_data, 'event_type': event_type}
            response = f"¿Qué fecha y hora tendrá el evento '{event_type}'?"
            new_state = 'awaiting_event_datetime'
        elif current_state == 'awaiting_event_datetime':
            event_datetime = message.strip()
            new_data = {**current_data, 'event_datetime': event_datetime}
            response = f"Evento '{current_data.get('event_type', 'desconocido')}' registrado para {event_datetime}. ¿Lo confirmas?"
            new_state = 'awaiting_event_confirmation'
        elif current_state == 'awaiting_event_confirmation':
            if message.lower() in ['sí', 'si', 'confirmo', 'confirmar']:
                event_type = current_data.get('event_type', 'desconocido')
                event_datetime = current_data.get('event_datetime', 'desconocido')
                response = f"¡Evento '{event_type}' confirmado para {event_datetime}!"
                new_state = 'completed'
                new_data = current_data
            else:
                response = "Evento cancelado. ¿Quieres gestionar otro evento?"
                new_state = 'initial'
                new_data = {}
        else:
            response = "No entendí tu petición sobre eventos."
            new_state = 'initial'
            new_data = {}

        return response, new_state, new_data
