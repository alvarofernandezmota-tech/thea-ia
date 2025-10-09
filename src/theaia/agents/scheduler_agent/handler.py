class SchedulerAgent:
    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        if current_state == 'initial':
            response = "¿Para cuándo quieres programar el recordatorio?"
            new_state = 'awaiting_reminder_time'
            new_data = current_data
        elif current_state == 'awaiting_reminder_time':
            reminder_time = message.strip()
            new_data = {**current_data, 'reminder_time': reminder_time}
            response = f"¿Qué mensaje quieres que te recuerde para {reminder_time}?"
            new_state = 'awaiting_reminder_message'
        elif current_state == 'awaiting_reminder_message':
            reminder_message = message.strip()
            new_data = {**current_data, 'reminder_message': reminder_message}
            reminder_time = current_data.get('reminder_time', 'desconocido')
            response = f"Recordatorio programado para {reminder_time}: '{reminder_message}'. ¿Confirmas?"
            new_state = 'awaiting_confirmation'
        elif current_state == 'awaiting_confirmation':
            if message.lower() in ['sí', 'si', 'confirmo', 'confirmar']:
                reminder_time = current_data.get('reminder_time', 'desconocido')
                reminder_message = current_data.get('reminder_message', 'desconocido')
                response = f"¡Recordatorio confirmado para {reminder_time}!"
                new_state = 'completed'
                new_data = current_data
            else:
                response = "Recordatorio cancelado. ¿Quieres programar otro?"
                new_state = 'initial'
                new_data = {}
        else:
            response = "No entendí tu petición de recordatorio."
            new_state = 'initial'
            new_data = {}

        return response, new_state, new_data
