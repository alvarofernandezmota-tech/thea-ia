# src/theaia/agents/agenda_agent/handler.py

from datetime import datetime

class AgendaAgent:
    """
    Agente para gestionar el flujo de agendado de citas:
    - initial → awaiting_datetime → awaiting_confirmation → completed
    """

    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        # Paso 1: solicitar fecha y hora
        if current_state == 'initial':
            response = "¿Para qué fecha y hora quieres agendar la cita?"
            new_state = 'awaiting_datetime'
            new_data = current_data

        # Paso 2: procesar fecha y hora
        elif current_state == 'awaiting_datetime':
            datetime_str = message.strip()
            try:
                datetime.fromisoformat(datetime_str)
            except Exception:
                response = "No entendí la fecha. Por favor usa formato YYYY-MM-DD HH:MM"
                new_state = 'awaiting_datetime'
                new_data = current_data
                return response, new_state, new_data

            new_data = {**current_data, 'appointment_datetime': datetime_str}
            response = f"Confirmas la cita para {datetime_str}?"
            new_state = 'awaiting_confirmation'

        # Paso 3: confirmar o cancelar, guardando last_event con uid
        elif current_state == 'awaiting_confirmation':
            if message.lower() in ['sí', 'si', 'confirmo', 'confirmar']:
                fecha = current_data.get('appointment_datetime', 'desconocido')
                new_data = {
                    **current_data,
                    'last_event': {
                        'uid': user_id,
                        'type': 'appointment',
                        'datetime': fecha
                    }
                }
                response = f"Cita confirmada para {fecha}. ¡Listo!"
                new_state = 'completed'
            else:
                response = "Solicitud cancelada. ¿Necesitas otra cosa?"
                new_state = 'initial'
                new_data = {}

        # Fallback interno
        else:
            response = "No entendí tu petición de citas."
            new_state = 'initial'
            new_data = {}

        return response, new_state, new_data
