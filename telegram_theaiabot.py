import logging
import re
from datetime import datetime, timedelta

import dateparser
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from db_connection import conectar_db

# =========================
# CONFIG
# =========================
TOKEN = "8297680422:AAGhueCQccdmc4vhVUma0lj6mL0p8h1OorI"
logging.basicConfig(level=logging.INFO)

# Evita procesar mensajes simultáneos del mismo usuario (previene pisar estados)
processing_users = {}

# =========================
# DB HELPERS
# =========================
def _get_usuario_id(conn, user_id_telegram: int):
    cur = conn.cursor()
    cur.execute("SELECT id FROM usuarios WHERE email = %s", (f"{user_id_telegram}@telegram.com",))
    res = cur.fetchone()
    return res[0] if res else None

def _tiene_solape(conn, usuario_id: int, inicio: datetime, fin: datetime):
    cur = conn.cursor()
    cur.execute(
        """
        SELECT id FROM citas
        WHERE usuario_id = %s
          AND estado IN ('pendiente','confirmada')
          AND NOT (fecha_fin <= %s OR fecha_inicio >= %s)
        """,
        (usuario_id, inicio, fin)
    )
    return cur.fetchone() is not None

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
# INTAKE INTELIGENTE
# =========================
INTENT_WORDS = ['agendar', 'reservar', 'evento', 'recordatorio', 'cita', 'crear']

def _analizar_intake_agendar(texto_original: str):
    """
    Detecta intención, intenta extraer fecha y título.
    Retorna dict: {tiene_intencion, fecha, titulo_inferido, siguiente_paso}
    """
    texto = texto_original.lower()
    tiene_intencion = any(p in texto for p in INTENT_WORDS)

    if not tiene_intencion:
        return {'tiene_intencion': False}

    # Extraer fecha con dateparser
    fecha = dateparser.parse(
        texto_original,
        settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()},
        languages=['es']
    )

    # Inferir título eliminando intención y expresiones temporales
    texto_limpio = texto_original
    for palabra in INTENT_WORDS:
        texto_limpio = re.sub(rf'\b{re.escape(palabra)}\b', ' ', texto_limpio, flags=re.IGNORECASE)

    expresiones_tiempo = [
        'hoy','mañana','pasado mañana','tarde','noche','mediodía','medianoche',
        'lunes','martes','miércoles','miercoles','jueves','viernes','sábado','sabado','domingo',
        'lun','mar','mie','mié','jue','vie','sab','sáb','dom',
        'esta','este','próximo','proximo','siguiente','semana','mes','año'
    ]
    for exp in expresiones_tiempo:
        texto_limpio = re.sub(rf'\b{re.escape(exp)}\b', ' ', texto_limpio, flags=re.IGNORECASE)

    # Quitar horas/fechas básicas
    texto_limpio = re.sub(r'\d{1,2}:\d{2}', ' ', texto_limpio)
    texto_limpio = re.sub(r'\b\d{1,2}(am|pm)\b', ' ', texto_limpio, flags=re.IGNORECASE)
    texto_limpio = re.sub(r'\b\d{1,2}/\d{1,2}/\d{2,4}\b', ' ', texto_limpio)

    titulo_inferido = ' '.join(texto_limpio.split()).strip()
    if len(titulo_inferido) < 3:
        titulo_inferido = None

    # Decidir siguiente paso
    if titulo_inferido and fecha:
        siguiente_paso = "pedir_duracion"
    elif fecha and not titulo_inferido:
        siguiente_paso = "pedir_titulo"
    elif titulo_inferido and not fecha:
        siguiente_paso = "pedir_fecha"
    else:
        siguiente_paso = "pedir_titulo"

    return {
        'tiene_intencion': True,
        'fecha': fecha,
        'titulo_inferido': titulo_inferido,
        'siguiente_paso': siguiente_paso
    }

# =========================
# JOBQUEUE: RECORDATORIOS
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
            text=f"⏰ Recordatorio: '{titulo}' empieza en {minutos} min (a las {fecha_str})."
        )

async def job_recordatorio_momento(context: ContextTypes.DEFAULT_TYPE):
    data = context.job.data or {}
    chat_id = data.get("chat_id")
    titulo = data.get("titulo")
    fecha_str = data.get("fecha_str")
    if chat_id:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"📣 Es el momento de tu evento: '{titulo}' ({fecha_str})."
        )

# =========================
# /start
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    # Crear o buscar usuario en DB
    conn = conectar_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM usuarios WHERE email = %s", (f"{user.id}@telegram.com",))
            usuario_db = cursor.fetchone()
            if not usuario_db:
                cursor.execute(
                    "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id",
                    (user.first_name or "Usuario", f"{user.id}@telegram.com")
                )
                conn.commit()
                print(f"✅ Nuevo usuario creado: {user.first_name}")
        finally:
            conn.close()

    await update.message.reply_text(
        f"¡Hola {user.first_name or 'allí'}! 👋\n\n"
        "Puedo crear eventos personales con recordatorios opcionales por Telegram.\n\n"
        "Comandos:\n"
        "- agendar: crear evento\n"
        "- consultar: ver tus eventos\n"
        "- cancelar: salir del flujo actual\n\n"
        "Ejemplos:\n"
        "• agendar\n• agendar cine mañana 20:00 90"
    )

# =========================
# Flujo AGENDAR con intake + recordatorios
# =========================
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    uid = user.id
    texto_original = update.message.text.strip()
    texto = texto_original.lower()

    # Anti-concurrencia por usuario
    if processing_users.get(uid, False):
        await update.message.reply_text("⏳ Un momento, estoy procesando tu mensaje anterior...")
        return
    processing_users[uid] = True

    # Log conversación
    _guardar_conversacion(uid, texto_original)

    try:
        # Cancelar global
        if texto in ["cancelar","salir","exit","quit"]:
            context.user_data.clear()
            await update.message.reply_text("✅ Operación cancelada. Escribe 'agendar' para empezar de nuevo.")
            return

        # Ayuda
        if any(p in texto for p in ["ayuda","help","?"]):
            await update.message.reply_text(
                "Puedo crear eventos con recordatorios opcionales.\n"
                "Ejemplos:\n"
                "• agendar\n• agendar cena mañana 21:00 120\n\n"
                "En cualquier momento escribe 'cancelar' para salir."
            )
            return

        # Intake inteligente si no hay flujo activo
        if not context.user_data.get("flujo"):
            intake = _analizar_intake_agendar(texto_original)
            if intake.get('tiene_intencion'):
                context.user_data.clear()
                context.user_data["flujo"] = "personal"

                if intake.get('fecha'):
                    context.user_data["fecha"] = intake['fecha']
                if intake.get('titulo_inferido'):
                    context.user_data["titulo_evento"] = intake['titulo_inferido']

                paso = intake['siguiente_paso']
                context.user_data["paso"] = paso

                if paso == "pedir_titulo":
                    await update.message.reply_text(
                        "📝 ¿Cómo se llama el evento?\nEj.: 'Cine con amigos', 'Entrenamiento', 'Reunión de equipo'"
                    )
                elif paso == "pedir_fecha":
                    await update.message.reply_text(
                        "📅 ¿Cuándo será? Ej.: 'mañana 20:00', 'viernes 10am', '15/11/2025 14:30'"
                    )
                elif paso == "pedir_duracion":
                    f = context.user_data.get("fecha")
                    t = context.user_data.get("titulo_evento","Evento")
                    await update.message.reply_text(
                        f"⏱️ Perfecto, '{t}' el {f.strftime('%d/%m/%Y %H:%M')}.\n"
                        "¿Cuánto durará? (minutos, ej.: 30, 60, 90)"
                    )
                return

        # Si estamos en el flujo personal (agendar)
        if context.user_data.get("flujo") == "personal":
            paso = context.user_data.get("paso")

            # 1) Título
            if paso == "pedir_titulo":
                if len(texto_original) < 3:
                    await update.message.reply_text("El título es muy corto. Escribe un nombre más descriptivo.")
                    return
                context.user_data["titulo_evento"] = texto_original
                context.user_data["paso"] = "pedir_fecha"
                await update.message.reply_text(
                    "📅 Indica fecha y hora. Ej.: 'mañana 20:00', 'viernes 10am', '15/11/2025 14:30'"
                )
                return

            # 2) Fecha
            if paso == "pedir_fecha":
                fecha = dateparser.parse(
                    texto_original,
                    settings={'PREFER_DATES_FROM': 'future', 'RELATIVE_BASE': datetime.now()},
                    languages=['es']
                )
                if not fecha:
                    await update.message.reply_text(
                        "No pude entender la fecha. Ej.: 'mañana 20:00' o '15/11/2025 14:30'."
                    )
                    return
                if fecha < datetime.now():
                    await update.message.reply_text("Esa fecha ya pasó. Indica una fecha futura.")
                    return
                context.user_data["fecha"] = fecha
                context.user_data["paso"] = "pedir_duracion"
                await update.message.reply_text("⏱️ ¿Cuánto durará? (minutos, ej.: 30, 45, 60)")
                return

            # 3) Duración
            if paso == "pedir_duracion":
                try:
                    duracion = int(texto)
                    if duracion < 10 or duracion > 480:
                        await update.message.reply_text("Indica una duración entre 10 y 480 minutos.")
                        return
                except ValueError:
                    await update.message.reply_text("Necesito un número en minutos. Ej.: 60")
                    return

                context.user_data["duracion_min"] = duracion
                context.user_data["paso"] = "confirmar"

                t = context.user_data.get("titulo_evento","Evento")
                f = context.user_data.get("fecha")
                await update.message.reply_text(
                    f"Revisa los datos:\n"
                    f"• Título: {t}\n"
                    f"• Fecha: {f.strftime('%d/%m/%Y %H:%M')}\n"
                    f"• Duración: {duracion} min\n\n"
                    f"¿Confirmas? Responde 'sí' para continuar o 'no' para cancelar."
                )
                return

            # 4) Confirmación → pasar a recordatorios
            if paso == "confirmar":
                if texto in ["si","sí","s","ok","confirmo","confirmar"]:
                    context.user_data["paso"] = "preguntar_recordatorio"
                    await update.message.reply_text(
                        "¿Quieres que te avise antes del evento por Telegram? (sí/no)"
                    )
                    return
                if texto in ["no","cancelar"]:
                    context.user_data.clear()
                    await update.message.reply_text("Operación cancelada. Escribe 'agendar' para intentarlo de nuevo.")
                    return
                await update.message.reply_text("Responde 'sí' para continuar o 'no' para cancelar.")
                return

            # 5) ¿Quieres aviso previo?
            if paso == "preguntar_recordatorio":
                if texto in ["si","sí","s","ok"]:
                    context.user_data["quiere_recordatorio_previo"] = True
                    context.user_data["paso"] = "pedir_minutos_recordatorio"
                    await update.message.reply_text(
                        "¿Cuántos minutos antes quieres que te avise? Ej.: 10, 30, 60"
                    )
                    return
                if texto in ["no","cancelar"]:
                    context.user_data["quiere_recordatorio_previo"] = False
                    context.user_data["paso"] = "preguntar_aviso_momento"
                    await update.message.reply_text("¿Quieres que te avise en el momento del evento? (sí/no)")
                    return
                await update.message.reply_text("Responde 'sí' o 'no'.")
                return

            # 6) Minutos de aviso previo
            if paso == "pedir_minutos_recordatorio":
                try:
                    min_prev = int(texto)
                    if min_prev < 1 or min_prev > 1440:
                        await update.message.reply_text("Elige entre 1 y 1440 minutos. Ej.: 10, 30, 60")
                        return
                except ValueError:
                    await update.message.reply_text("Necesito un número en minutos. Ej.: 30")
                    return

                context.user_data["minutos_recordatorio"] = min_prev
                context.user_data["paso"] = "preguntar_aviso_momento"
                await update.message.reply_text("¿Quieres además un aviso en el momento del evento? (sí/no)")
                return

            # 7) Aviso en el momento
            if paso == "preguntar_aviso_momento":
                if texto in ["si","sí","s","ok"]:
                    context.user_data["quiere_aviso_momento"] = True
                elif texto in ["no","cancelar"]:
                    context.user_data["quiere_aviso_momento"] = False
                else:
                    await update.message.reply_text("Responde 'sí' o 'no'.")
                    return

                # Crear evento y programar recordatorios
                titulo = context.user_data.get("titulo_evento","Evento")
                fecha = context.user_data.get("fecha")
                duracion = context.user_data.get("duracion_min", 60)
                fecha_fin = fecha + timedelta(minutes=duracion)

                conn = conectar_db()
                try:
                    if not conn:
                        await update.message.reply_text("No pude conectar a la base de datos.")
                        return
                    usuario_id = _get_usuario_id(conn, user.id)
                    if not usuario_id:
                        await update.message.reply_text("No encontré tu usuario. Envía /start e inténtalo de nuevo.")
                        conn.close()
                        return

                    # Anti-solapamiento final
                    if _tiene_solape(conn, usuario_id, fecha, fecha_fin):
                        await update.message.reply_text(
                            "Ya tienes un evento alrededor de esa hora. Indica otra fecha/hora."
                        )
                        context.user_data["paso"] = "pedir_fecha"
                        return

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
                    jobq = context.job_queue
                    fecha_str = fecha.strftime('%H:%M')

                    # Aviso previo
                    min_prev = context.user_data.get("minutos_recordatorio")
                    if context.user_data.get("quiere_recordatorio_previo") and min_prev:
                        when_prev = fecha - timedelta(minutes=min_prev)
                        if when_prev > datetime.now():
                            jobq.run_once(
                                job_recordatorio_previa,
                                when=when_prev,
                                data={
                                    "chat_id": update.effective_chat.id,
                                    "titulo": titulo,
                                    "fecha_str": fecha_str,
                                    "min_previo": min_prev
                                },
                                name=f"previo_{uid}_{cita_id}"
                            )
                        else:
                            await update.message.reply_text(
                                f"(Nota) El aviso {min_prev} min antes ya no es posible por la cercanía del evento."
                            )

                    # Aviso en el momento
                    if context.user_data.get("quiere_aviso_momento", False):
                        if fecha > datetime.now():
                            jobq.run_once(
                                job_recordatorio_momento,
                                when=fecha,
                                data={
                                    "chat_id": update.effective_chat.id,
                                    "titulo": titulo,
                                    "fecha_str": fecha_str
                                },
                                name=f"momento_{uid}_{cita_id}"
                            )

                    await update.message.reply_text(
                        f"✅ Evento creado:\n"
                        f"• Título: {titulo}\n"
                        f"• Fecha: {fecha.strftime('%d/%m/%Y %H:%M')}\n"
                        f"• Duración: {duracion} min\n"
                        f"• ID: {cita_id}\n\n"
                        f"Recordatorios:\n"
                        f"- {'Sí, ' + str(min_prev) + ' min antes' if context.user_data.get('quiere_recordatorio_previo') else 'No previo'}\n"
                        f"- {'Sí, en el momento' if context.user_data.get('quiere_aviso_momento') else 'No en el momento'}\n\n"
                        f"Escribe 'consultar' para ver tus eventos."
                    )
                    context.user_data.clear()
                    return
                except Exception as e:
                    if conn:
                        conn.rollback()
                    await update.message.reply_text("Ocurrió un error creando el evento.")
                    print("Error creando evento personal:", e)
                finally:
                    if conn:
                        conn.close()
                return

        # Consultar simple (últimos 5)
        if any(p in texto for p in ["consultar","mis citas","ver citas","ver eventos"]):
            conn = conectar_db()
            if conn:
                try:
                    cur = conn.cursor()
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
                finally:
                    conn.close()

                if citas:
                    resp = "📋 Tus últimos eventos:\n\n"
                    for c in citas:
                        ftxt = c[0].strftime('%d/%m/%Y %H:%M') if hasattr(c[0], 'strftime') else str(c[0])
                        resp += f"• {ftxt} - {c[1]} ({c[2]}) | ID {c[3]}\n"
                else:
                    resp = "No tienes eventos. Escribe 'agendar' para crear uno."
            else:
                resp = "No pude consultar tus eventos ahora."
            await update.message.reply_text(resp)
            return

        # Fallback
        await update.message.reply_text(
            "No entendí tu mensaje. Escribe 'agendar' para crear un evento con recordatorios opcionales, o 'ayuda' para ver opciones."
        )

    finally:
        processing_users[uid] = False

# =========================
# MAIN
# =========================
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    print("🤖 Thea IA Bot iniciado...")
    app.run_polling()

if __name__ == "__main__":
    main()
