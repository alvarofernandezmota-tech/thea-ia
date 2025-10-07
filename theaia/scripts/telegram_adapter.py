import logging
import re
from datetime import datetime, timedelta

import dateparser
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from antiguothea.db_connection import conectar_db

# =========================
# CONFIGURACIÓN
# =========================
TOKEN = "8297680422:AAGhueCQccdmc4vhVUma0lj6mL0p8h1OorI"
logging.basicConfig(level=logging.INFO)

# Control anti-concurrencia
processing_users = {}

# =========================
# DICCIONARIO DE MENSAJES CENTRALIZADOS
# =========================
MESSAGES = {
    # Generales
    'saludo_inicial': "¡Hola {nombre}! 😊\n\n"
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
                     "¿En qué te ayudo?",

    'no_entiendo_ayuda': "🤔 No estoy segura de entenderte.\n\n"
                        "Puedes decirme:\n"
                        "• **'agendar'** - crear evento\n"
                        "• **'consultar'** - ver eventos\n"
                        "• **'modificar evento X'** - cambiar evento\n"
                        "• **'cancelar evento X'** - eliminar evento\n"
                        "• **'ayuda'** - más opciones\n\n"
                        "O dime qué necesitas en tus propias palabras 😊",

    'operacion_cancelada': "❌ **Operación cancelada.**\n\n"
                          "Cuando quieras hacer algo, solo dímelo 😊",

    # Agendar
    'pedir_titulo': "📝 ¿Cómo quieres llamar a tu evento?\n\n"
                   "Ejemplos:\n"
                   "• Dentista\n"
                   "• Cine con María\n"
                   "• Reunión equipo\n"
                   "• Entrenamiento gym",

    'titulo_muy_corto': "El nombre es un poco corto 🤏\n\n"
                       "Sé más específico:\n"
                       "• En vez de 'gym' → 'Entrenamiento gym'\n"
                       "• En vez de 'cita' → 'Cita médico'\n\n"
                       "¿Cómo prefieres llamarlo?",

    'pedir_fecha': "📅 ¿Cuándo será **'{titulo}'**?\n\n"
                  "Ejemplos:\n"
                  "• mañana 10:00\n"
                  "• viernes 15:30\n"
                  "• 12/11/2025 19:00\n"
                  "• próximo lunes 14:00",

    'fecha_no_entendida': "🤷‍♀️ No entendí esa fecha.\n\n"
                         "Prueba con:\n"
                         "• **mañana 10:00**\n"
                         "• **viernes 15:30**\n"
                         "• **12/11/2025 19:00**\n\n"
                         "¿Cuándo prefieres?",

    'fecha_pasada': "⏰ Esa fecha ya pasó.\n\n"
                   "Dime una fecha futura:\n"
                   "• mañana 19:00\n"
                   "• próximo viernes\n"
                   "• la próxima semana",

    'pedir_duracion': "⏱️ ¿Cuántos minutos durará **'{titulo}'**?\n\n"
                     "Ejemplos:\n"
                     "• **30** (media hora)\n"
                     "• **60** (una hora)\n"
                     "• **90** (hora y media)",

    'duracion_invalida': "🔢 Necesito un número válido.\n\n"
                         "Ejemplos: 30, 60, 90\n"
                         "¿Cuántos minutos?",

    'duracion_fuera_rango': "⚠️ Esa duración es extrema.\n\n"
                           "Entre 10 y 480 minutos por favor.\n"
                           "¿Cuántos minutos?",

    'confirmar_evento': "✅ **Revisa los detalles:**\n\n"
                       "📝 **Evento:** {titulo}\n"
                       "📅 **Fecha:** {fecha}\n"
                       "⏱️ **Duración:** {duracion} min\n\n"
                       "¿Confirmas? **'sí'** o **'no'**",

    'conflicto_horario': "⚠️ **¡Conflicto de horario!**\n\n"
                        "Ya tienes algo programado entonces.\n"
                        "¿Otra hora? Ejemplo: 'una hora después'",

    'evento_creado': "🎉 **¡Evento creado!**\n\n"
                    "📝 **{titulo}**\n"
                    "📅 {fecha}\n"
                    "⏱️ {duracion} min\n"
                    "🆔 ID: **{id}**\n\n"
                    "**Recordatorios:** {recordatorios}\n\n"
                    "💡 Escribe 'consultar' para ver todos.",

    # Consultar
    'sin_eventos': "📅 No tienes eventos aún.\n\n"
                  "¡Escribe 'agendar' para crear tu primer evento!",

    # Modificar
    'pedir_id_modificar': "🔍 ¿Cuál evento quieres modificar?\n\n"
                         "Ejemplo: 'modificar evento 12'\n"
                         "Usa 'consultar' para ver los IDs.",

    'evento_no_encontrado': "❌ No encontré ese evento o no es tuyo.\n\n"
                           "Usa 'consultar' para ver tus eventos con IDs.",

    'que_modificar': "✏️ ¿Qué quieres cambiar del evento **'{titulo}'**?\n\n"
                    "Opciones:\n"
                    "• **'fecha'** - cambiar fecha/hora\n"
                    "• **'duracion'** - cambiar duración\n"
                    "• **'titulo'** - cambiar nombre",

    'modificacion_exitosa': "✅ **Evento modificado:**\n\n"
                           "🆔 ID: {id}\n"
                           "📝 **{titulo}**\n"
                           "📅 {fecha}\n"
                           "⏱️ {duracion} min",

    # Cancelar
    'confirmar_cancelacion': "🗑️ ¿Confirmas cancelar **'{titulo}'**?\n\n"
                           "📅 {fecha}\n"
                           "🆔 ID: {id}\n\n"
                           "Responde **'sí'** o **'no'**",

    'cancelacion_exitosa': "✅ **Evento cancelado:**\n\n"
                          "📝 {titulo}\n"
                          "🆔 ID: {id}",
}

# =========================
# PALABRAS CLAVE PARA INTENCIONES
# =========================
INTENT_AGENDAR = [
    'agendar', 'reservar', 'evento', 'recordatorio', 'cita', 'crear',
    'programar', 'planificar', 'poner', 'anotar', 'apuntar',
    'quiero', 'necesito', 'tengo que', 'voy a',
    'reunion', 'reunión', 'meeting', 'appointment'
]

INTENT_CONSULTAR = [
    'consultar', 'ver', 'mostrar', 'mis', 'eventos', 'citas', 'agenda',
    'proximos', 'próximos', 'siguientes', 'calendario', 'horarios'
]

INTENT_MODIFICAR = [
    'modificar', 'cambiar', 'editar', 'actualizar', 'mover'
]

INTENT_CANCELAR = [
    'cancelar', 'eliminar', 'borrar', 'quitar', 'anular'
]

# =========================
# HELPERS BASE DE DATOS
# =========================
def _get_usuario_id(conn, user_id_telegram: int):
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE email = %s", (f"{user_id_telegram}@telegram.com",))
    res = cur.fetchone()
    return res[0] if res else None

def _tiene_solape(conn, usuario_id: int, inicio: datetime, fin: datetime, excluir_cita_id: int = None):
    cur = conn.cursor()
    if excluir_cita_id:
        cur.execute(
            """
            SELECT id FROM citas
            WHERE usuario_id = %s AND estado IN ('pendiente','confirmada')
              AND id <> %s AND NOT (fecha_fin <= %s OR fecha_inicio >= %s)
            """,
            (usuario_id, excluir_cita_id, inicio, fin)
        )
    else:
        cur.execute(
            """
            SELECT id FROM citas
            WHERE usuario_id = %s AND estado IN ('pendiente','confirmada')
              AND NOT (fecha_fin <= %s OR fecha_inicio >= %s)
            """,
            (usuario_id, inicio, fin)
        )
    return cur.fetchone() is not None

def _get_cita_by_id(conn, usuario_id: int, cita_id: int):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, fecha_inicio, fecha_fin, servicio_nombre, estado, duracion_minutos
        FROM citas
        WHERE id = %s AND usuario_id = %s
        """,
        (cita_id, usuario_id)
    )
    return cur.fetchone()

def _guardar_conversacion(user_id_telegram: int, texto: str):
    conn = conectar_db()
    if not conn:
        return
    try:
        c = conn.cursor()
        c.execute(
            "INSERT INTO conversaciones (usuario_id, mensaje, tipo) VALUES ((SELECT id FROM usuarios WHERE email = %s), %s, 'usuario')",
            (f"{user_id_telegram}@telegram.com", texto)
        )
        conn.commit()
    except Exception:
        conn.rollback()
    finally:
        conn.close()

# =========================
# DETECCIÓN DE INTENCIONES INTELIGENTE
# =========================
def _detectar_intencion(texto: str):
    """Detecta la intención principal del mensaje"""
    t = texto.lower()
    
    # Buscar números para modificar/cancelar
    numeros = re.findall(r'\b\d+\b', texto)
    primer_numero = int(numeros[0]) if numeros else None
    
    if any(word in t for word in INTENT_AGENDAR):
        return {'tipo': 'agendar', 'datos': _extraer_datos_agendar(texto)}
    elif any(word in t for word in INTENT_CONSULTAR):
        return {'tipo': 'consultar', 'filtro': _extraer_filtro_consultar(t)}
    elif any(word in t for word in INTENT_MODIFICAR):
        return {'tipo': 'modificar', 'cita_id': primer_numero}
    elif any(word in t for word in INTENT_CANCELAR):
        return {'tipo': 'cancelar', 'cita_id': primer_numero}
    
    return {'tipo': 'desconocido'}

def _extraer_datos_agendar(texto: str):
    """Extrae título y fecha del mensaje de agendar"""
    # Fecha
    fecha = dateparser.parse(
        texto,
        settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()},
        languages=['es']
    )
    
    # Título
    texto_limpio = texto
    palabras_remover = INTENT_AGENDAR + [
        'hoy','mañana','pasado','tarde','noche','mediodía','medianoche',
        'lunes','martes','miércoles','jueves','viernes','sábado','domingo',
        'próximo','siguiente','esta','este','semana','mes','año'
    ]
    
    for palabra in palabras_remover:
        texto_limpio = re.sub(rf'\b{re.escape(palabra)}\b', ' ', texto_limpio, flags=re.IGNORECASE)
    
    texto_limpio = re.sub(r'\d{1,2}:\d{2}', ' ', texto_limpio)
    texto_limpio = re.sub(r'\b\d{1,2}(am|pm)\b', ' ', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', ' ', texto_limpio)
    
    titulo = ' '.join(texto_limpio.split()).strip()
    titulo = titulo if len(titulo) >= 3 else None
    
    return {'fecha': fecha, 'titulo': titulo}

def _extraer_filtro_consultar(texto: str):
    """Determina qué tipo de consulta quiere el usuario"""
    if any(p in texto for p in ['proximo', 'próximo', 'siguiente', 'futuro']):
        return 'proximos'
    elif any(p in texto for p in ['pasado', 'anterior', 'historial']):
        return 'pasados'
    else:
        return 'todos'

# =========================
# JOBQUEUE RECORDATORIOS
# =========================
async def job_recordatorio_previa(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data or {}
    chat_id = data.get("chat_id")
    titulo = data.get("titulo")
    fecha_str = data.get("fecha_str")
    minutos = data.get("min_previo")
    if chat_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⏰ **Recordatorio:**\n\n'{titulo}' empieza en {minutos} minutos ({fecha_str})",
            parse_mode='Markdown'
        )

async def job_recordatorio_momento(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data or {}
    chat_id = data.get("chat_id")
    titulo = data.get("titulo")
    fecha_str = data.get("fecha_str")
    if chat_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📣 **¡Es el momento!**\n\nTu evento '{titulo}' empieza ahora ({fecha_str})",
            parse_mode='Markdown'
        )

# =========================
# HANDLERS PRINCIPALES
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Crear usuario si no existe
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (f"{user.id}@telegram.com",))
            if not cursor.fetchone():
                cursor.execute(
                    "INSERT INTO usuarios (nombre, email) VALUES (%s, %s)",
                    (user.first_name or "Usuario", f"{user.id}@telegram.com")
                )
                conn.commit()
                print(f"✅ Usuario creado: {user.first_name}")
        finally:
            conn.close()
    
    await update.message.reply_text(
        MESSAGES['saludo_inicial'].format(nombre=user.first_name or "allí"),
        parse_mode='Markdown'
    )

async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    texto_original = update.message.text.strip()
    texto = texto_original.lower()

    # Control anti-concurrencia
    if processing_users.get(uid, False):
        await update.message.reply_text("⏳ Procesando tu mensaje anterior...")
        return
    processing_users[uid] = True
    
    _guardar_conversacion(uid, texto_original)

    try:
        # COMANDOS GLOBALES
        if texto in ["cancelar", "salir", "exit", "quit"]:
            context.user_data.clear()
            await update.message.reply_text(MESSAGES['operacion_cancelada'], parse_mode='Markdown')
            return

        if texto in ["ayuda", "help", "?"]:
            await update.message.reply_text(MESSAGES['no_entiendo_ayuda'], parse_mode='Markdown')
            return

        # MENSAJE SUELTO SIN FLUJO ACTIVO
        if not context.user_data.get("flujo"):
            intencion = _detectar_intencion(texto_original)
            
            if intencion['tipo'] == 'agendar':
                await iniciar_flujo_agendar(update, context, intencion['datos'])
                return
            elif intencion['tipo'] == 'consultar':
                await ejecutar_consultar(update, user, intencion['filtro'])
                return
            elif intencion['tipo'] == 'modificar':
                await iniciar_flujo_modificar(update, context, user, intencion['cita_id'])
                return
            elif intencion['tipo'] == 'cancelar':
                await iniciar_flujo_cancelar(update, context, user, intencion['cita_id'])
                return
            else:
                # Mensaje suelto sin intención clara
                await update.message.reply_text(MESSAGES['no_entiendo_ayuda'], parse_mode='Markdown')
                return

        # FLUJOS ACTIVOS
        if context.user_data.get("flujo") == "agendar":
            await procesar_flujo_agendar(update, context, user, texto_original, texto)
        elif context.user_data.get("flujo") == "modificar":
            await procesar_flujo_modificar(update, context, user, texto_original, texto)
        elif context.user_data.get("flujo") == "cancelar":
            await procesar_flujo_cancelar(update, context, user, texto)

    finally:
        processing_users[uid] = False

# =========================
# FLUJOS ESPECÍFICOS
# =========================

async def iniciar_flujo_agendar(update: Update, context: ContextTypes, datos: dict):
    """Inicia flujo de agendar con datos detectados"""
    context.user_data.clear()
    context.user_data["flujo"] = "agendar"
    
    if datos.get('fecha'):
        context.user_data["fecha"] = datos['fecha']
    if datos.get('titulo'):
        context.user_data["titulo_evento"] = datos['titulo']
    
    # Determinar siguiente paso
    if datos.get('titulo') and datos.get('fecha'):
        context.user_data["paso"] = "pedir_duracion"
        await update.message.reply_text(
            MESSAGES['pedir_duracion'].format(titulo=datos['titulo']),
            parse_mode='Markdown'
        )
    elif datos.get('fecha'):
        context.user_data["paso"] = "pedir_titulo"
        await update.message.reply_text(MESSAGES['pedir_titulo'])
    elif datos.get('titulo'):
        context.user_data["paso"] = "pedir_fecha"
        await update.message.reply_text(
            MESSAGES['pedir_fecha'].format(titulo=datos['titulo']),
            parse_mode='Markdown'
        )
    else:
        context.user_data["paso"] = "pedir_titulo"
        await update.message.reply_text(MESSAGES['pedir_titulo'])

async def procesar_flujo_agendar(update: Update, context: ContextTypes, user, texto_original: str, texto: str):
    """Procesa cada paso del flujo de agendar"""
    paso = context.user_data.get("paso")
    
    if paso == "pedir_titulo":
        if len(texto_original) < 3:
            await update.message.reply_text(MESSAGES['titulo_muy_corto'])
            return
        context.user_data["titulo_evento"] = texto_original
        context.user_data["paso"] = "pedir_fecha"
        await update.message.reply_text(
            MESSAGES['pedir_fecha'].format(titulo=texto_original),
            parse_mode='Markdown'
        )
        return
    
    elif paso == "pedir_fecha":
        fecha = dateparser.parse(
            texto_original,
            settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()},
            languages=['es']
        )
        if not fecha:
            errores = context.user_data.get("errores_fecha", 0) + 1
            context.user_data["errores_fecha"] = errores
            if errores >= 2:
                await update.message.reply_text(
                    "La fecha está complicada 😅\n\n"
                    "Prueba: 'mañana 10:00' o '15/11/2025 14:30'"
                )
                context.user_data["errores_fecha"] = 0
            else:
                await update.message.reply_text(MESSAGES['fecha_no_entendida'], parse_mode='Markdown')
            return
        
        if fecha < datetime.now():
            await update.message.reply_text(MESSAGES['fecha_pasada'])
            return
        
        context.user_data["fecha"] = fecha
        context.user_data["paso"] = "pedir_duracion"
        await update.message.reply_text(
            MESSAGES['pedir_duracion'].format(titulo=context.user_data["titulo_evento"]),
            parse_mode='Markdown'
        )
        return
    
    elif paso == "pedir_duracion":
        if len(texto.split()) > 3:
            await update.message.reply_text("Dime solo los minutos 😊")
            return
        
        try:
            duracion = int(texto.strip())
            if duracion < 10 or duracion > 480:
                await update.message.reply_text(MESSAGES['duracion_fuera_rango'])
                return
        except ValueError:
            await update.message.reply_text(MESSAGES['duracion_invalida'])
            return
        
        context.user_data["duracion_min"] = duracion
        context.user_data["paso"] = "confirmar"
        await update.message.reply_text(
            MESSAGES['confirmar_evento'].format(
                titulo=context.user_data["titulo_evento"],
                fecha=context.user_data["fecha"].strftime('%d/%m/%Y a las %H:%M'),
                duracion=duracion
            ),
            parse_mode='Markdown'
        )
        return
    
    elif paso == "confirmar":
        if texto in ["si", "sí", "s", "ok", "confirmar", "vale"]:
            context.user_data["paso"] = "preguntar_recordatorio"
            await update.message.reply_text("⏰ ¿Quieres aviso antes del evento? (sí/no)")
            return
        elif texto in ["no", "cancelar"]:
            context.user_data.clear()
            await update.message.reply_text(MESSAGES['operacion_cancelada'], parse_mode='Markdown')
            return
        else:
            await update.message.reply_text("Responde 'sí' para crear o 'no' para cancelar.")
            return
    
    elif paso == "preguntar_recordatorio":
        if texto in ["si", "sí", "s", "ok"]:
            context.user_data["quiere_recordatorio"] = True
            context.user_data["paso"] = "pedir_minutos_recordatorio"
            await update.message.reply_text("¿Cuántos minutos antes? (ej: 10, 30, 60)")
            return
        elif texto in ["no"]:
            context.user_data["quiere_recordatorio"] = False
            context.user_data["paso"] = "preguntar_aviso_momento"
            await update.message.reply_text("¿Aviso en el momento del evento? (sí/no)")
            return
        else:
            await update.message.reply_text("Responde 'sí' o 'no'")
            return
    
    elif paso == "pedir_minutos_recordatorio":
        try:
            minutos = int(texto.strip())
            if minutos < 1 or minutos > 1440:
                await update.message.reply_text("Entre 1 y 1440 minutos por favor.")
                return
        except ValueError:
            await update.message.reply_text("Un número por favor: 10, 30, 60")
            return
        
        context.user_data["minutos_recordatorio"] = minutos
        context.user_data["paso"] = "preguntar_aviso_momento"
        await update.message.reply_text("¿También aviso en el momento? (sí/no)")
        return
    
    elif paso == "preguntar_aviso_momento":
        if texto in ["si", "sí", "s", "ok"]:
            context.user_data["aviso_momento"] = True
        elif texto in ["no"]:
            context.user_data["aviso_momento"] = False
        else:
            await update.message.reply_text("Responde 'sí' o 'no'")
            return
        
        await crear_evento_final(update, context, user)
        return

async def crear_evento_final(update: Update, context: ContextTypes, user):
    """Crea el evento final con recordatorios"""
    titulo = context.user_data["titulo_evento"]
    fecha = context.user_data["fecha"]
    duracion = context.user_data["duracion_min"]
    fecha_fin = fecha + timedelta(minutes=duracion)
    
    conn = conectar_db()
    try:
        if not conn:
            await update.message.reply_text("❌ Error de conexión.")
            return
        
        usuario_id = _get_usuario_id(conn, user.id)
        if not usuario_id:
            await update.message.reply_text("❌ Usuario no encontrado. Envía /start")
            return
        
        # Verificar solapamiento
        if _tiene_solape(conn, usuario_id, fecha, fecha_fin):
            await update.message.reply_text(MESSAGES['conflicto_horario'])
            context.user_data["paso"] = "pedir_fecha"
            return
        
        # Crear evento
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO citas (usuario_id, fecha_inicio, fecha_fin, servicio_id, servicio_nombre, duracion_minutos, precio, estado)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pendiente') RETURNING id;
            """,
            (usuario_id, fecha, fecha_fin, None, titulo, duracion, 0.00)
        )
        cita_id = cur.fetchone()[0]
        conn.commit()
        
        # Programar recordatorios
        recordatorios_info = []
        jobq = context.job_queue
        fecha_str = fecha.strftime('%H:%M')
        
        # Recordatorio previo
        if context.user_data.get("quiere_recordatorio") and context.user_data.get("minutos_recordatorio"):
            minutos = context.user_data["minutos_recordatorio"]
            when_prev = fecha - timedelta(minutes=minutos)
            if when_prev > datetime.now():
                jobq.run_once(
                    job_recordatorio_previa,
                    when=when_prev,
                    data={
                        "chat_id": update.effective_chat.id,
                        "titulo": titulo,
                        "fecha_str": fecha_str,
                        "min_previo": minutos
                    },
                    name=f"previo_{user.id}_{cita_id}"
                )
                recordatorios_info.append(f"• {minutos} min antes ✅")
        
        # Recordatorio momento
        if context.user_data.get("aviso_momento"):
            if fecha > datetime.now():
                jobq.run_once(
                    job_recordatorio_momento,
                    when=fecha,
                    data={
                        "chat_id": update.effective_chat.id,
                        "titulo": titulo,
                        "fecha_str": fecha_str
                    },
                    name=f"momento_{user.id}_{cita_id}"
                )
                recordatorios_info.append("• En el momento ✅")
        
        if not recordatorios_info:
            recordatorios_info.append("• Sin recordatorios")
        
        await update.message.reply_text(
            MESSAGES['evento_creado'].format(
                titulo=titulo,
                fecha=fecha.strftime('%d/%m/%Y a las %H:%M'),
                duracion=duracion,
                id=cita_id,
                recordatorios="\n".join(recordatorios_info)
            ),
            parse_mode='Markdown'
        )
        
        context.user_data.clear()
        
    except Exception as e:
        if conn:
            conn.rollback()
        await update.message.reply_text("❌ Error creando evento.")
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

async def ejecutar_consultar(update: Update, user, filtro: str = 'todos'):
    """Ejecuta consulta de eventos"""
    conn = conectar_db()
    if not conn:
        await update.message.reply_text("❌ Error de conexión.")
        return
    
    try:
        cur = conn.cursor()
        if filtro == 'proximos':
            cur.execute(
                """
                SELECT fecha_inicio, servicio_nombre, estado, id
                FROM citas
                WHERE usuario_id = (SELECT id FROM usuarios WHERE email = %s)
                  AND fecha_inicio >= %s
                ORDER BY fecha_inicio ASC
                LIMIT 5
                """,
                (f"{user.id}@telegram.com", datetime.now())
            )
        elif filtro == 'pasados':
            cur.execute(
                """
                SELECT fecha_inicio, servicio_nombre, estado, id
                FROM citas
                WHERE usuario_id = (SELECT id FROM usuarios WHERE email = %s)
                  AND fecha_inicio < %s
                ORDER BY fecha_inicio DESC
                LIMIT 5
                """,
                (f"{user.id}@telegram.com", datetime.now())
            )
        else:
            cur.execute(
                """
                SELECT fecha_inicio, servicio_nombre, estado, id
                FROM citas
                WHERE usuario_id = (SELECT id FROM usuarios WHERE email = %s)
                ORDER BY fecha_inicio DESC
                LIMIT 5
                """,
                (f"{user.id}@telegram.com",)
            )
        
        citas = cur.fetchall()
        
        if citas:
            titulo_filtro = {
                'proximos': '📅 **Próximos eventos:**',
                'pasados': '📋 **Eventos pasados:**',
                'todos': '📋 **Tus eventos:**'
            }.get(filtro, '📋 **Tus eventos:**')
            
            resp = f"{titulo_filtro}\n\n"
            for c in citas:
                fecha_str = c[0].strftime('%d/%m %H:%M') if hasattr(c[0], 'strftime') else str(c[0])
                estado_emoji = "✅" if c[2] == 'confirmada' else "⏳" if c[2] == 'pendiente' else "❌"
                resp += f"{estado_emoji} **{fecha_str}** - {c[1]} | ID {c[3]}\n"
        else:
            resp = MESSAGES['sin_eventos']
    
    finally:
        conn.close()
    
    await update.message.reply_text(resp, parse_mode='Markdown')

async def iniciar_flujo_modificar(update: Update, context: ContextTypes, user, cita_id: int):
    """Inicia flujo de modificar evento"""
    if not cita_id:
        await update.message.reply_text(MESSAGES['pedir_id_modificar'])
        return
    
    conn = conectar_db()
    if not conn:
        await update.message.reply_text("❌ Error de conexión.")
        return
    
    try:
        usuario_id = _get_usuario_id(conn, user.id)
        cita = _get_cita_by_id(conn, usuario_id, cita_id)
        
        if not cita:
            await update.message.reply_text(MESSAGES['evento_no_encontrado'])
            return
        
        context.user_data.clear()
        context.user_data["flujo"] = "modificar"
        context.user_data["cita_id"] = cita_id
        context.user_data["cita_data"] = cita
        context.user_data["paso"] = "que_modificar"
        
        await update.message.reply_text(
            MESSAGES['que_modificar'].format(titulo=cita[3]),
            parse_mode='Markdown'
        )
        
    finally:
        conn.close()

async def procesar_flujo_modificar(update: Update, context: ContextTypes, user, texto_original: str, texto: str):
    """Procesa flujo de modificar evento"""
    paso = context.user_data.get("paso")
    cita_id = context.user_data["cita_id"]
    cita_data = context.user_data["cita_data"]
    
    if paso == "que_modificar":
        if texto in ["fecha", "f"]:
            context.user_data["modificar_que"] = "fecha"
            context.user_data["paso"] = "nueva_fecha"
            await update.message.reply_text("📅 Nueva fecha/hora:\nEj.: 'mañana 15:00'")
        elif texto in ["duracion", "duración", "d"]:
            context.user_data["modificar_que"] = "duracion"  
            context.user_data["paso"] = "nueva_duracion"
            await update.message.reply_text("⏱️ Nueva duración en minutos:\nEj.: 30, 60, 90")
        elif texto in ["titulo", "título", "nombre", "t"]:
            context.user_data["modificar_que"] = "titulo"
            context.user_data["paso"] = "nuevo_titulo"
            await update.message.reply_text("📝 Nuevo nombre del evento:")
        else:
            await update.message.reply_text("Responde: 'fecha', 'duracion' o 'titulo'")
        return
    
    elif paso == "nueva_fecha":
        fecha = dateparser.parse(
            texto_original,
            settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()},
            languages=['es']
        )
        if not fecha:
            await update.message.reply_text("No entendí la fecha. Ej.: 'mañana 15:00'")
            return
        if fecha < datetime.now():
            await update.message.reply_text("La fecha debe ser futura.")
            return
        
        # Verificar solapamiento
        duracion_actual = cita_data[5] or 60
        fecha_fin = fecha + timedelta(minutes=duracion_actual)
        
        conn = conectar_db()
        try:
            usuario_id = _get_usuario_id(conn, user.id)
            if _tiene_solape(conn, usuario_id, fecha, fecha_fin, cita_id):
                await update.message.reply_text("Conflicto con otro evento. Prueba otra hora.")
                return
            
            # Actualizar
            cur = conn.cursor()
            cur.execute(
                "UPDATE citas SET fecha_inicio = %s, fecha_fin = %s WHERE id = %s",
                (fecha, fecha_fin, cita_id)
            )
            conn.commit()
            
            await update.message.reply_text(
                MESSAGES['modificacion_exitosa'].format(
                    id=cita_id,
                    titulo=cita_data[3],
                    fecha=fecha.strftime('%d/%m/%Y a las %H:%M'),
                    duracion=duracion_actual
                ),
                parse_mode='Markdown'
            )
            context.user_data.clear()
            
        finally:
            conn.close()
        return
    
    elif paso == "nueva_duracion":
        try:
            nueva_dur = int(texto.strip())
            if nueva_dur < 10 or nueva_dur > 480:
                await update.message.reply_text("Entre 10 y 480 minutos.")
                return
        except ValueError:
            await update.message.reply_text("Un número por favor.")
            return
        
        # Verificar solapamiento con nueva duración
        fecha_actual = cita_data[1]
        fecha_fin = fecha_actual + timedelta(minutes=nueva_dur)
        
        conn = conectar_db()
        try:
            usuario_id = _get_usuario_id(conn, user.id)
            if _tiene_solape(conn, usuario_id, fecha_actual, fecha_fin, cita_id):
                await update.message.reply_text("La nueva duración causa conflicto.")
                return
            
            cur = conn.cursor()
            cur.execute(
                "UPDATE citas SET fecha_fin = %s, duracion_minutos = %s WHERE id = %s",
                (fecha_fin, nueva_dur, cita_id)
            )
            conn.commit()
            
            await update.message.reply_text(
                MESSAGES['modificacion_exitosa'].format(
                    id=cita_id,
                    titulo=cita_data[3],
                    fecha=fecha_actual.strftime('%d/%m/%Y a las %H:%M'),
                    duracion=nueva_dur
                ),
                parse_mode='Markdown'
            )
            context.user_data.clear()
            
        finally:
            conn.close()
        return
    
    elif paso == "nuevo_titulo":
        if len(texto_original) < 3:
            await update.message.reply_text("El título es muy corto.")
            return
        
        conn = conectar_db()
        try:
            cur = conn.cursor()
            cur.execute(
                "UPDATE citas SET servicio_nombre = %s WHERE id = %s",
                (texto_original, cita_id)
            )
            conn.commit()
            
            await update.message.reply_text(
                MESSAGES['modificacion_exitosa'].format(
                    id=cita_id,
                    titulo=texto_original,
                    fecha=cita_data[1].strftime('%d/%m/%Y a las %H:%M'),
                    duracion=cita_data[5] or 60
                ),
                parse_mode='Markdown'
            )
            context.user_data.clear()
            
        finally:
            conn.close()
        return

async def iniciar_flujo_cancelar(update: Update, context: ContextTypes, user, cita_id: int):
    """Inicia flujo de cancelar evento"""
    if not cita_id:
        await update.message.reply_text("🔍 ¿Cuál evento cancelas?\nEj.: 'cancelar evento 12'")
        return
    
    conn = conectar_db()
    if not conn:
        await update.message.reply_text("❌ Error de conexión.")
        return
    
    try:
        usuario_id = _get_usuario_id(conn, user.id)
        cita = _get_cita_by_id(conn, usuario_id, cita_id)
        
        if not cita:
            await update.message.reply_text(MESSAGES['evento_no_encontrado'])
            return
        
        context.user_data.clear()
        context.user_data["flujo"] = "cancelar"
        context.user_data["cita_id"] = cita_id
        context.user_data["cita_data"] = cita
        context.user_data["paso"] = "confirmar_cancelacion"
        
        await update.message.reply_text(
            MESSAGES['confirmar_cancelacion'].format(
                titulo=cita[3],
                fecha=cita[1].strftime('%d/%m/%Y a las %H:%M'),
                id=cita_id
            ),
            parse_mode='Markdown'
        )
        
    finally:
        conn.close()

async def procesar_flujo_cancelar(update: Update, context: ContextTypes, user, texto: str):
    """Procesa flujo de cancelar evento"""
    cita_id = context.user_data["cita_id"]
    cita_data = context.user_data["cita_data"]
    
    if texto in ["si", "sí", "s", "ok", "confirmar"]:
        conn = conectar_db()
        try:
            cur = conn.cursor()
            cur.execute("UPDATE citas SET estado = 'cancelada' WHERE id = %s", (cita_id,))
            conn.commit()
            
            await update.message.reply_text(
                MESSAGES['cancelacion_exitosa'].format(
                    titulo=cita_data[3],
                    id=cita_id
                ),
                parse_mode='Markdown'
            )
            context.user_data.clear()
            
        finally:
            conn.close()
    elif texto in ["no", "cancelar"]:
        context.user_data.clear()
        await update.message.reply_text("Cancelación abortada.")
    else:
        await update.message.reply_text("Responde 'sí' para confirmar o 'no' para abortar.")

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("🤖 Thea IA Bot MVP Completo iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
