class QueryAgent:
    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        # Simulación: contesta qué citas, notas o eventos tiene el usuario
        if current_state == 'initial':
            if "cita" in message.lower():
                response = "Tienes la siguiente cita registrada: " + str(current_data.get('appointment_datetime', 'No hay citas registradas.'))
            elif "nota" in message.lower():
                response = "Tu nota guardada es: " + str(current_data.get('note_text', 'No hay notas guardadas.'))
            elif "evento" in message.lower():
                response = "Tu evento registrado es: " + str(current_data.get('event_type', 'No hay eventos registrados.'))
            else:
                response = "¿Quieres consultar tus citas, notas o eventos?"
            new_state = 'completed'
            new_data = current_data
        else:
            response = "No entendí tu consulta. Puedes preguntar por 'citas', 'notas' o 'eventos'."
            new_state = 'initial'
            new_data = {}
        return response, new_state, new_data
