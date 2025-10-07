import os
import logging
import re
from datetime import datetime, timedelta
from dotenv import load_dotenv

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from theaia.src.services.metrics import record_request, start_metrics_server
from theaia.src.integrations.db_connection import conectar_db
from theaia.src.core.config import TELEGRAM_TOKEN, MESSAGES
from theaia.src.services.state_machine import ConversationalStateMachine

# =========================
# Configuración y métricas
# =========================

load_dotenv()
start_metrics_server(port=8000)
TOKEN = TELEGRAM_TOKEN
logging.basicConfig(level=logging.INFO)

# =========================
# Estado y preferencias por usuario
# =========================

user_states = {}
user_preferences = {}  # Guardará preferencias por usuario
processing_users = {}

def get_user_state(user_id):
    """Obtiene o crea la máquina de estados para un usuario"""
    if user_id not in user_states:
        user_states[user_id] = ConversationalStateMachine()
    return user_states[user_id]

def get_user_preferences(user_id):
    """Obtiene preferencias del usuario (duración típica, nombre, etc.)"""
    if user_id not in user_preferences:
        user_preferences[user_id] = {
            'duracion_tipica': 60,  # minutos por defecto
            'nombre': None,
            'eventos_recientes': []
        }
    return user_preferences[user_id]

# =========================
# Funciones de procesamiento inteligente
# =========================

def es_agendar(texto):
    """Detecta intención de agendar con sinónimos y frases largas"""
    palabras_clave = [
        'agendar', 'añadir evento', 'añadir una cita', 'añadir recordatorio',
        'crear evento', 'crear una cita', 'programar evento', 'programar una reunión',
        'nuevo evento', 'planificar evento', 'planificar cita', 'registrar evento',
        'poner recordatorio', 'apunta una cita', 'me gustaría agendar',
        'quiero recordar', 'tengo que recordar', 'recordatorio para'
    ]
    texto_normalizado = texto.lower().strip()
    
    # Buscar frases completas primero
    for frase in palabras_clave:
        if frase in texto_normalizado:
            return True
    
    # Buscar palabras sueltas como respaldo
    palabras_sueltas = ['agendar', 'añadir', 'crear', 'programar', 'planificar', 'recordar', 'registrar', 'apuntar']
    return any(palabra in texto_normalizado for palabra in palabras_sueltas)

def procesar_hora_flexible(texto):
    """Procesa diferentes formatos de hora"""
    texto = texto.lower().strip()
    
    patrones_hora = [
        r'(\d{1,2}):(\d{2})',                    # 14:30, 9:15
        r'(\d{1,2})\.(\d{2})',                   # 14.30, 9.15  
        r'(\d{1,2})\s*h\s*(\d{2})',              # 14h30, 9h15
        r'a\s*las\s*(\d{1,2}):(\d{2})',          # a las 14:30
        r'a\s*las\s*(\d{1,2})',                  # a las 14
        r'(\d{1,2})\s*(am|pm)',                  # 2pm, 10am
        r'(\d{1,2}):(\d{2})\s*(am|pm)',          # 2:30pm
    ]
    
    for i, patron in enumerate(patrones_hora):
        match = re.search(patron, texto)
        if match:
            grupos = match.groups()
            
            if i <= 2:  # Formatos 24h
                hora = int(grupos[0])
                minuto = int(grupos[1])
                return {"hora": hora, "minuto": minuto, "formato": "24h"}
            elif i == 3:  # a las 14:30
                hora = int(grupos[0]) 
                minuto = int(grupos[1])
                return {"hora": hora, "minuto": minuto, "formato": "24h"}
            elif i == 4:  # a las 14
                hora = int(grupos[0])
                return {"hora": hora, "minuto": 0, "formato": "24h"}
            elif i == 5:  # 2pm
                hora = int(grupos[0])
                am_pm = grupos[1]
                hora_24 = hora if am_pm == 'am' and hora != 12 else (0 if am_pm == 'am' else (hora if hora == 12 else hora + 12))
                return {"hora": hora_24, "minuto": 0, "formato": "12h"}
            elif i == 6:  # 2:30pm
                hora = int(grupos[0])
                minuto = int(grupos[1])
                am_pm = grupos[2]
                hora_24 = hora if am_pm == 'am' and hora != 12 else (0 if am_pm == 'am' else (hora if hora == 12 else hora + 12))
                return {"hora": hora_24, "minuto": minuto, "formato": "12h"}
    
    return None

def extraer_duracion(texto):
    """Extrae duración en múltiples formatos"""
    texto = texto.lower()
    
    # Patrones específicos
    if "media hora" in texto:
        return 30
    if "hora y media" in texto or "una hora y media" in texto:
        return 90
    
    # Números + unidades
    match_min = re.search(r'(\d+)\s*(min|minuto|minutos)', texto)
    if match_min:
        return int(match_min.group(1))
    
    match_h = re.search(r'(\d+)\s*(h|hora|horas)', texto)
    if match_h:
        horas = int(match_h.group(1))
        # Buscar minutos adicionales
        match_min_extra = re.search(r'(\d+)\s*(min|minuto|minutos)', texto)
        if match_min_extra:
            return horas * 60 + int(match_min_extra.group(1))
        return horas * 60
    
    return None

def detectar_tipo_evento(texto):
    """Detecta el tipo de evento y sugiere duración apropiada"""
    tipos = {
        'medico': ['médico', 'doctor', 'dentista', 'cita médica', 'consulta', 'revisión'],
        'trabajo': ['reunión', 'meeting', 'trabajo', 'oficina', 'proyecto', 'cliente'],
        'personal': ['cumpleaños', 'cita', 'comida', 'cena', 'deporte', 'gimnasio'],
        'recordatorio': ['recordatorio', 'recordar', 'llamar', 'comprar', 'pagar']
    }
    
    duraciones_sugeridas = {
        'medico': 30,
        'trabajo': 60,
        'personal': 120,
        'recordatorio': 15
    }
    
    texto_lower = texto.lower()
    for tipo, palabras in tipos.items():
        if any(palabra in texto_lower for palabra in palabras):
            return tipo, duraciones_sugeridas[tipo]
    
    return None, 60  # Por defecto

def validar_hora_logica(hora_info, tipo_evento):
    """Valida si la hora tiene sentido según el tipo de evento"""
    if not hora_info:
        return True, ""
    
    hora = hora_info.get("hora", 12)
    
    # Validaciones por tipo
    if tipo_evento == 'medico' and (hora < 8 or hora > 20):
        return False, "🏥 Las citas médicas suelen ser entre 8:00 y 20:00"
    
    if tipo_evento == 'trabajo' and (hora < 7 or hora > 22):
        return False, "💼 Las reuniones de trabajo suelen ser en horario laboral"
    
    if hora < 6 or hora > 23:
        return False, "🌙 Esa hora parece muy temprano o muy tarde. ¿Estás seguro?"
    
    return True, ""

def hay_conflicto_cita(user_id, fecha_inicio, duracion):
    """Simula consulta de conflictos (aquí conectarías con tu BD)"""
    # Por ahora devolvemos False, pero aquí consultarías tu base de datos
    # eventos_existentes = consultar_eventos_bd(user_id, fecha_inicio.date())
    # return verificar_solapamiento(eventos_existentes, fecha_inicio, duracion)
    return False, None

def generar_emoji_evento(texto):
    """Genera emoji contextual según el tipo de evento"""
    emojis = {
        'médico': '🏥', 'doctor': '👨‍⚕️', 'dentista': '🦷',
        'reunión': '💼', 'trabajo': '💼', 'meeting': '🤝',
        'cumpleaños': '🎂', 'fiesta': '🎉',
        'deporte': '⚽', 'gimnasio': '💪',
        'comida': '🍽️', 'cena': '🍽️',
        'recordatorio': '⏰', 'llamar': '📞'
    }
    
    texto_lower = texto.lower()
    for palabra, emoji in emojis.items():
        if palabra in texto_lower:
            return emoji
    return '📅'

def es_confirmacion_positiva(texto):
    """Detecta confirmaciones positivas más naturalmente"""
    positivos = ['sí', 'si', 'yes', 'ok', 'vale', 'perfecto', 'confirmo', 'correcto', 'exacto', 'bien']
    return any(p in texto.lower().strip() for p in positivos)

def es_confirmacion_negativa(texto):
    """Detecta negaciones y cancelaciones"""
    negativos = ['no', 'nope', 'cancelar', 'mal', 'incorrecto', 'cambiar']
    return any(n in texto.lower().strip() for n in negativos)

# =========================
# Handlers principales
# =========================

@record_request
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler mejorado para /start con personalización"""
    user = update.effective_user
    user_id = str(user.id)
    
    # Resetear estado y guardar nombre
    state_machine = get_user_state(user_id)
    state_machine.reset()
    
    prefs = get_user_preferences(user_id)
    prefs['nombre'] = user.first_name or "Usuario"
    
    # Registrar en BD si es necesario
    conn = conectar_db()
    if conn:
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id FROM usuarios WHERE email = %s",
                (f"{user.id}@telegram.com",)
            )
            if not cur.fetchone():
                cur.execute(
                    "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)",
                    (user.first_name or "Usuario", f"{user.id}@telegram.com")
                )
                conn.commit()
        except Exception as e:
            logging.error(f"Error BD en start: {e}")
        finally:
            conn.close()

    # Saludo personalizado
    await update.message.reply_text(
        f"¡Hola {prefs['nombre']}! 👋\n\n"
        "Soy tu asistente personal para agenda. Puedo ayudarte a:\n"
        "📅 Agendar eventos, citas y recordatorios\n"
        "👁️ Consultar tu agenda\n"
        "✏️ Modificar eventos existentes\n"
        "❌ Cancelar citas\n\n"
        "Solo escribe algo como 'agendar cita médica' o 'crear recordatorio' para empezar.",
        parse_mode='Markdown'
    )

@record_request
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler principal con todas las mejoras de intuitividad"""
    user = update.effective_user
    user_id = str(user.id)
    texto = update.message.text.strip()

    state_machine = get_user_state(user_id)
    prefs = get_user_preferences(user_id)
    estado_actual = state_machine.state

    # Control anti-concurrencia
    if processing_users.get(user_id, False):
        await update.message.reply_text("⏳ Procesando tu mensaje anterior...")
        return
    processing_users[user_id] = True

    try:
        # === COMANDOS DE ESCAPE EN CUALQUIER MOMENTO ===
        if estado_actual != "IDLE" and any(cmd in texto.lower() for cmd in ['cancelar', 'salir', 'stop', 'empezar de nuevo']):
            state_machine.reset()
            context.user_data.clear()
            await update.message.reply_text(f"✅ Operación cancelada, {prefs['nombre']}. ¿En qué más te ayudo?")
            return

        # === ESTADO IDLE - DETECTAR INTENCIONES ===
        if estado_actual == "IDLE":
            if es_agendar(texto):
                # Detectar tipo de evento y sugerir duración
                tipo_evento, duracion_sugerida = detectar_tipo_evento(texto)
                prefs['tipo_evento_actual'] = tipo_evento
                prefs['duracion_sugerida'] = duracion_sugerida
                
                state_machine.start_agendar()
                emoji = generar_emoji_evento(texto)
                await update.message.reply_text(
                    f"{emoji} ¡Perfecto! Vamos a agendar tu evento.\n\n"
                    f"📝 ¿Cómo quieres llamarlo?\n"
                    f"💡 Ejemplo: '{texto}' está bien, o puedes ser más específico."
                )
            else:
                await update.message.reply_text(
                    f"🤔 No entendí bien, {prefs['nombre']}.\n\n"
                    "Puedes escribir cosas como:\n"
                    "• 'Agendar cita con el dentista'\n"
                    "• 'Crear recordatorio para llamar a mamá'\n"
                    "• 'Programar reunión de trabajo'\n"
                    "• 'Nuevo evento de cumpleaños'\n\n"
                    "¿En qué te ayudo?"
                )

        # === ESTADO ASK_TITLE - RECOGER TÍTULO ===
        elif estado_actual == "ASK_TITLE":
            if len(texto) < 2:
                await update.message.reply_text(
                    "📝 El nombre del evento es un poco corto.\n"
                    "¿Podrías ser un poco más descriptivo? Por ejemplo:\n"
                    "• 'Cita con Dr. García'\n"
                    "• 'Reunión equipo marketing'\n"
                    "• 'Recordatorio comprar regalo'"
                )
            else:
                context.user_data["titulo"] = texto
                state_machine.ask_date()
                emoji = generar_emoji_evento(texto)
                await update.message.reply_text(
                    f"{emoji} Genial: '{texto}'\n\n"
                    f"📅 ¿Cuándo será?\n"
                    f"Puedes escribir:\n"
                    f"• 'Mañana a las 15:30'\n"
                    f"• 'El viernes 14:00'\n"
                    f"• '10.45' o '2:30pm'"
                )

        # === ESTADO ASK_DATE - RECOGER Y VALIDAR FECHA/HORA ===
        elif estado_actual == "ASK_DATE":
            hora_info = procesar_hora_flexible(texto)
            
            if hora_info and 0 <= hora_info['hora'] <= 23:
                # Validar lógica de la hora según tipo de evento
                tipo_evento = prefs.get('tipo_evento_actual')
                hora_valida, mensaje_validacion = validar_hora_logica(hora_info, tipo_evento)
                
                if not hora_valida:
                    await update.message.reply_text(mensaje_validacion + "\n¿Quieres cambiar la hora?")
                    return
                
                # Verificar conflictos (simulado por ahora)
                fecha_tentativa = datetime.now() + timedelta(days=1)  # Simplificado
                hay_conflicto, evento_conflicto = hay_conflicto_cita(user_id, fecha_tentativa, 60)
                
                if hay_conflicto:
                    await update.message.reply_text(
                        "⚠️ Ya tienes un evento en esa hora.\n"
                        "¿Te sirven estas alternativas?\n"
                        "• Una hora antes\n"
                        "• Una hora después\n"
                        "• Al día siguiente"
                    )
                    return
                
                # Todo OK, continuar
                hora_formateada = f"{hora_info['hora']:02d}:{hora_info['minuto']:02d}"
                context.user_data["fecha"] = texto
                context.user_data["hora_procesada"] = hora_formateada
                
                state_machine.ask_duration()
                titulo = context.user_data.get("titulo", "tu evento")
                duracion_sugerida = prefs.get('duracion_sugerida', 60)
                
                await update.message.reply_text(
                    f"✅ '{titulo}' el {texto} ({hora_formateada})\n\n"
                    f"⏱️ ¿Cuánto tiempo necesitas?\n"
                    f"💡 Sugerencia: {duracion_sugerida} minutos\n\n"
                    f"Ejemplos: '30 min', '1 hora', '1h 15m', 'media hora'"
                )
            else:
                await update.message.reply_text(
                    "🤔 No entendí bien la fecha/hora.\n\n"
                    "Puedes escribir:\n"
                    "• '14:30' o '2:30pm'\n"
                    "• 'Mañana a las 10'\n"
                    "• '15.45' o '10h30'\n\n"
                    "¿A qué hora será?"
                )

        # === ESTADO ASK_DURATION - RECOGER DURACIÓN ===
        elif estado_actual == "ASK_DURATION":
            duracion = extraer_duracion(texto)
            duracion_sugerida = prefs.get('duracion_sugerida', 60)
            
            # Aceptar sugerencia si solo escriben "sí" o similar
            if not duracion and es_confirmacion_positiva(texto):
                duracion = duracion_sugerida
            
            if duracion and 5 <= duracion <= 480:  # Entre 5 min y 8 horas
                context.user_data["duracion"] = duracion
                prefs['duracion_tipica'] = duracion  # Aprender preferencia
                
                state_machine.confirm_event()
                titulo = context.user_data.get("titulo", "Evento")
                fecha = context.user_data.get("fecha", "Fecha")
                emoji = generar_emoji_evento(titulo)
                
                await update.message.reply_text(
                    f"{emoji} ¡Perfecto! Resumen de tu evento:\n\n"
                    f"📋 **{titulo}**\n"
                    f"📅 {fecha}\n"
                    f"⏱️ {duracion} minutos\n\n"
                    f"¿Todo correcto? ¡Responde 'sí' para confirmar!",
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "⏱️ No entendí la duración.\n\n"
                    "Puedes escribir:\n"
                    "• '30 min' o 'media hora'\n"
                    "• '1 hora' o 'una hora y media'\n"
                    "• '45 minutos' o '1h 15m'\n"
                    f"• O simplemente 'sí' para {duracion_sugerida} minutos"
                )

        # === ESTADO CONFIRM_EVENT - CONFIRMACIÓN FINAL ===
        elif estado_actual == "CONFIRM_EVENT":
            if es_confirmacion_positiva(texto):
                # Crear evento (aquí conectarías con tu BD)
                evento_creado = await crear_evento_en_bd(user_id, context.user_data)
                
                if evento_creado:
                    state_machine.evento_creado()
                    titulo = context.user_data.get("titulo", "Evento")
                    fecha = context.user_data.get("fecha", "Fecha")
                    duracion = context.user_data.get("duracion", 60)
                    emoji = generar_emoji_evento(titulo)
                    
                    # Agregar a eventos recientes del usuario
                    prefs['eventos_recientes'].append({
                        'titulo': titulo,
                        'fecha': fecha,
                        'duracion': duracion
                    })
                    
                    await update.message.reply_text(
                        f"{emoji} ¡Evento creado exitosamente!\n\n"
                        f"📋 **{titulo}**\n"
                        f"📅 {fecha}\n"
                        f"⏱️ {duracion} minutos\n"
                        f"🔔 Te recordaré 15 minutos antes\n\n"
                        f"¿Necesitas agendar algo más, {prefs['nombre']}?",
                        parse_mode='Markdown'
                    )
                    
                    context.user_data.clear()
                    state_machine.reset()
                else:
                    await update.message.reply_text("❌ Error al crear evento. Inténtalo de nuevo.")
                    state_machine.reset()
                    
            elif es_confirmacion_negativa(texto):
                state_machine.reset()
                context.user_data.clear()
                await update.message.reply_text(f"✅ Operación cancelada, {prefs['nombre']}. ¿Quieres empezar de nuevo?")
            else:
                await update.message.reply_text(
                    "🤔 No estoy seguro de tu respuesta.\n"
                    "Por favor responde:\n"
                    "• 'Sí', 'OK' o 'Confirmo' para crear el evento\n"
                    "• 'No' o 'Cancelar' para cancelar"
                )

        # === ESTADO NO RECONOCIDO ===
        else:
            state_machine.reset()
            await update.message.reply_text(f"🔄 Algo salió mal. Empecemos de nuevo, {prefs['nombre']}. ¿En qué te ayudo?")

    except Exception as e:
        logging.error(f"Error procesando mensaje del usuario {user_id}: {e}")
        state_machine.reset()
        context.user_data.clear()
        await update.message.reply_text(
            f"😅 Ups, algo salió mal. Pero no te preocupes, {prefs['nombre']}, "
            f"empecemos de nuevo. ¿En qué te ayudo?"
        )
        
    finally:
        processing_users[user_id] = False

# =========================
# Funciones auxiliares
# =========================

async def crear_evento_en_bd(user_id, datos_evento):
    """Simula creación de evento en BD"""
    try:
        # Aquí conectarías con tu base de datos real
        logging.info(f"Creando evento para usuario {user_id}: {datos_evento}")
        return True
    except Exception as e:
        logging.error(f"Error creando evento: {e}")
        return False

# =========================
# Main
# =========================

def main():
    """Función principal mejorada"""
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    
    logging.info("🤖 Thea IA Bot iniciado con funciones avanzadas...")
    logging.info("✨ Características activas:")
    logging.info("   • Reconocimiento de múltiples formatos de hora")
    logging.info("   • Detección inteligente de tipos de evento") 
    logging.info("   • Personalización por usuario")
    logging.info("   • Validaciones contextuales")
    logging.info("   • Comunicación natural con emojis")
    
    app.run_polling()

if __name__ == "__main__":
    main()