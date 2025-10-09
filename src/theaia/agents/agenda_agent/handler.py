class AgendaAgent:
    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        if current_state == 'initial':
            response = "¿Para qué fecha y hora quieres agendar la cita?"
            new_state = 'awaiting_datetime'
            new_data = current_data
        elif current_state == 'awaiting_datetime':
            datetime_str = message.strip()
            new_data = {**current_data, 'appointment_datetime': datetime_str}
            response = f"Entendido, agendé tu cita para {datetime_str}. ¿Lo confirmas?"
            new_state = 'awaiting_confirmation'
        elif current_state == 'awaiting_confirmation':
            if message.lower() in ['sí', 'si', 'confirmo', 'confirmar']:
                appointment = current_data.get('appointment_datetime', 'desconocido')
                response = f"Cita confirmada para {appointment}. ¡Listo!"
                new_state = 'completed'
                new_data = current_data
            else:
                response = "Solicitud cancelada. ¿Necesitas otra cosa?"
                new_state = 'initial'
                new_data = {}
        else:
            response = "No entendí tu petición de citas."
            new_state = 'initial'
            new_data = {}

        return response, new_state, new_data
