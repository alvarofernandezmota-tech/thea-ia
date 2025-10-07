import os
from dotenv import load_dotenv

# Carga variables de entorno desde .env
load_dotenv()

# Token de Telegram (asegúrate de definir TELEGRAM_TOKEN en tu .env)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Mensajes centralizados para usar en todo el bot
MESSAGES = {
    # Generales
    'saludo_inicial': (
        "¡Hola {nombre}! 😊\n\n"
        "Soy Thea, tu asistente personal de eventos.\n\n"
        "Puedo ayudarte a:\n"
        "• **Agendar** citas y recordatorios\n"
        "• **Consultar** tus eventos\n"
        "• **Modificar** citas existentes\n"
        "• **Cancelar** eventos\n\n"
        "Ejemplos:\n"
        "• 'agendar dentista mañana 10:00'\n"
        "• 'consultar próximos eventos'\n"
        "• 'modificar evento 12'\n"
        "• 'cancelar cita 15'\n\n"
        "¿En qué te ayudo?"
    ),
    'no_entiendo_ayuda': (
        "🤔 No estoy segura de entenderte.\n\n"
        "Puedes decirme:\n"
        "• **'agendar'** - crear evento\n"
        "• **'consultar'** - ver eventos\n"
        "• **'modificar evento X'** - cambiar evento\n"
        "• **'cancelar evento X'** - eliminar evento\n"
        "• **'ayuda'** - más opciones\n\n"
        "O dime qué necesitas en tus propias palabras 😊"
    ),
    'operacion_cancelada': (
        "❌ **Operación cancelada.**\n\n"
        "Cuando quieras hacer algo, solo dímelo 😊"
    ),
    # Agendar
    'pedir_titulo': (
        "📝 ¿Cómo quieres llamar a tu evento?\n\n"
        "Ejemplos:\n"
        "• Dentista\n"
        "• Cine con María\n"
        "• Reunión equipo\n"
        "• Entrenamiento gym"
    ),
    'titulo_muy_corto': (
        "El nombre es un poco corto 🤏\n\n"
        "Sé más específico:\n"
        "• En vez de 'gym' → 'Entrenamiento gym'\n"
        "• En vez de 'cita' → 'Cita médico'\n\n"
        "¿Cómo prefieres llamarlo?"
    ),
    'pedir_fecha': (
        "📅 ¿Cuándo será **'{titulo}'**?\n\n"
        "Ejemplos:\n"
        "• mañana 10:00\n"
        "• viernes 15:30\n"
        "• 12/11/2025 19:00\n"
        "• próximo lunes 14:00"
    ),
    'fecha_no_entendida': (
        "🤷‍♀️ No entendí esa fecha.\n\n"
        "Prueba con:\n"
        "• **mañana 10:00**\n"
        "• **viernes 15:30**\n"
        "• **12/11/2025 19:00**\n\n"
        "¿Cuándo prefieres?"
    ),
    'fecha_pasada': (
        "⏰ Esa fecha ya pasó.\n\n"
        "Dime una fecha futura:\n"
        "• mañana 19:00\n"
        "• próximo viernes\n"
        "• la próxima semana"
    ),
    'pedir_duracion': (
        "⏱️ ¿Cuántos minutos durará **'{titulo}'**?\n\n"
        "Ejemplos:\n"
        "• **30** (media hora)\n"
        "• **60** (una hora)\n"
        "• **90** (hora y media)"
    ),
    'duracion_invalida': (
        "🔢 Necesito un número válido.\n\n"
        "Ejemplos: 30, 60, 90\n"
        "¿Cuántos minutos?"
    ),
    'duracion_fuera_rango': (
        "⚠️ Esa duración es extrema.\n\n"
        "Entre 10 y 480 minutos por favor.\n"
        "¿Cuántos minutos?"
    ),
    'confirmar_evento': (
        "✅ **Revisa los detalles:**\n\n"
        "📝 **Evento:** {titulo}\n"
        "📅 **Fecha:** {fecha}\n"
        "⏱️ **Duración:** {duracion} min\n\n"
        "¿Confirmas? **'sí'** o **'no'**"
    ),
    'conflicto_horario': (
        "⚠️ **¡Conflicto de horario!**\n\n"
        "Ya tienes algo programado entonces.\n"
        "¿Otra hora? Ejemplo: 'una hora después'"
    ),
    'evento_creado': (
        "🎉 **¡Evento creado!**\n\n"
        "📝 **{titulo}**\n"
        "📅 {fecha}\n"
        "⏱️ {duracion} min\n"
        "🆔 ID: **{id}**\n\n"
        "**Recordatorios:** {recordatorios}\n\n"
        "💡 Escribe 'consultar' para ver todos."
    ),
    # Consultar
    'sin_eventos': (
        "📅 No tienes eventos aún.\n\n"
        "¡Escribe 'agendar' para crear tu primer evento!"
    ),
    # Modificar
    'pedir_id_modificar': (
        "🔍 ¿Cuál evento quieres modificar?\n\n"
        "Ejemplo: 'modificar evento 12'\n"
        "Usa 'consultar' para ver los IDs."
    ),
    'evento_no_encontrado': (
        "❌ No encontré ese evento o no es tuyo.\n\n"
        "Usa 'consultar' para ver tus eventos con IDs."
    ),
    'que_modificar': (
        "✏️ ¿Qué quieres cambiar del evento **'{titulo}'**?\n\n"
        "Opciones:\n"
        "• **'fecha'** - cambiar fecha/hora\n"
        "• **'duracion'** - cambiar duración\n"
        "• **'titulo'** - cambiar nombre"
    ),
    'modificacion_exitosa': (
        "✅ **Evento modificado:**\n\n"
        "🆔 ID: {id}\n"
        "📝 **{titulo}**\n"
        "📅 {fecha}\n"
        "⏱️ {duracion} min"
    ),
    # Cancelar
    'confirmar_cancelacion': (
        "🗑️ ¿Confirmas cancelar **'{titulo}'**?\n\n"
        "📅 {fecha}\n"
        "🆔 ID: {id}\n\n"
        "Responde **'sí'** o **'no'**"
    ),
    'cancelacion_exitosa': (
        "✅ **Evento cancelado:**\n\n"
        "📝 {titulo}\n"
        "🆔 ID: {id}"
    ),
}
