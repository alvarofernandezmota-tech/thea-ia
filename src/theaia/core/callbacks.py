# src/theaia/core/callbacks.py

def handle_agenda(context):
    return "Agenda gestionada correctamente."

def handle_scheduler(context):
    return "Tarea programada correctamente."

def handle_event(context):
    return "Evento registrado correctamente."

def handle_note(context):
    return "Nota guardada correctamente."

def handle_query(context):
    return "Consulta respondida correctamente."

def handle_help(context):
    return "Ayuda de Thea IA mostrada."

def handle_fallback(context):
    return "No se entendió la petición. Fallback aplicado."

def handle_completed(context):
    return "Conversación completada correctamente."

def handle_error(context):
    return "Error en flujo conversacional."
