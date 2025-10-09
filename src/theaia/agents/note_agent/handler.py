class NoteAgent:
    def __init__(self):
        pass

    def process(self, user_id, message, current_state, current_data):
        if current_state == 'initial':
            response = "¿Qué nota quieres guardar?"
            new_state = 'awaiting_note_text'
            new_data = current_data
        elif current_state == 'awaiting_note_text':
            note_text = message.strip()
            new_data = {**current_data, 'note_text': note_text}
            response = f"Nota guardada: '{note_text}'. ¿Quieres añadir otra?"
            new_state = 'completed'
        else:
            response = "No entendí tu petición de nota. Intenta de nuevo."
            new_state = 'initial'
            new_data = {}

        return response, new_state, new_data
