import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from db_connection import conectar_db

# Configuración
TOKEN = "8297680422:AAGhueCQccdmc4vhVUma0lj6mL0p8h1OorI"  # Cambiar por tu token real
logging.basicConfig(level=logging.INFO)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Crear o buscar usuario en la DB
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM usuarios WHERE email = %s", (f"{user.id}@telegram.com",))
        usuario_db = cursor.fetchone()
        
        if not usuario_db:
            # Crear nuevo usuario
            cursor.execute(
                "INSERT INTO usuarios (nombre, email) VALUES (%s, %s) RETURNING id",
                (user.first_name or "Usuario", f"{user.id}@telegram.com")
            )
            conn.commit()
            print(f"✅ Nuevo usuario creado: {user.first_name}")
        
        conn.close()
    
    await update.message.reply_text(
        f"¡Hola {user.first_name}! 👋\n\n"
        "Soy **Thea**, tu asistente inteligente para citas.\n\n"
        "Puedes escribir:\n"
        "🗓️ **'agendar'** - Reservar una cita\n"
        "📋 **'consultar'** - Ver tus citas\n"
        "✏️ **'modificar'** - Cambiar una cita\n"
        "❌ **'cancelar'** - Anular una cita\n"
        "❓ **'ayuda'** - Más opciones",
        parse_mode='Markdown'
    )

# Manejar mensajes de texto
async def manejar_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    texto = update.message.text.lower()
    
    # Guardar conversación en DB
    conn = conectar_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversaciones (usuario_id, mensaje, tipo) VALUES ((SELECT id FROM usuarios WHERE email = %s), %s, 'usuario')",
            (f"{user.id}@telegram.com", texto)
        )
        conn.commit()
        conn.close()
    
    # Lógica de respuestas
    if "agendar" in texto or "cita" in texto:
        await update.message.reply_text(
            "📅 **Agendar nueva cita**\n\n"
            "¿Para qué fecha quieres agendar?\n"
            "Ejemplo: *mañana 10:00* o *15/11/2025 14:30*",
            parse_mode='Markdown'
        )
    
    elif "consultar" in texto or "ver" in texto:
        # Consultar citas del usuario
        conn = conectar_db()
        if conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT fecha_inicio, servicio_nombre, estado 
                   FROM citas WHERE usuario_id = (SELECT id FROM usuarios WHERE email = %s)
                   ORDER BY fecha_inicio DESC LIMIT 5""",
                (f"{user.id}@telegram.com",)
            )
            citas = cursor.fetchall()
            conn.close()
            
            if citas:
                respuesta = "📋 **Tus citas:**\n\n"
                for cita in citas:
                    respuesta += f"• {cita[0]} - {cita[1]} ({cita[2]})\n"
            else:
                respuesta = "No tienes citas registradas. ¿Quieres agendar una?"
        else:
            respuesta = "Error consultando las citas."
        
        await update.message.reply_text(respuesta, parse_mode='Markdown')
    
    elif "modificar" in texto:
        await update.message.reply_text(
            "✏️ **Modificar cita**\n\n"
            "¿Qué cita quieres modificar?\n"
            "Primero escribe 'consultar' para ver tus citas."
        )
    
    elif "cancelar" in texto:
        await update.message.reply_text(
            "❌ **Cancelar cita**\n\n"
            "¿Qué cita quieres cancelar?\n"
            "Primero escribe 'consultar' para ver tus citas."
        )
    
    elif "ayuda" in texto or "help" in texto:
        await update.message.reply_text(
            "🤖 **Ayuda de Thea IA**\n\n"
            "**Comandos principales:**\n"
            "🗓️ agendar - Reservar nueva cita\n"
            "📋 consultar - Ver citas existentes\n"
            "✏️ modificar - Cambiar una cita\n"
            "❌ cancelar - Anular una cita\n\n"
            "**Ejemplos:**\n"
            "• 'Quiero agendar para mañana'\n"
            "• 'Ver mis citas'\n"
            "• 'Cancelar mi cita del viernes'\n\n"
            "¿En qué más puedo ayudarte?",
            parse_mode='Markdown'
        )
    
    else:
        # Mensaje de fallback desde DB
        conn = conectar_db()
        mensaje_fallback = "No entendí tu mensaje. Escribe 'ayuda' para ver las opciones."
        
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mensaje FROM mensajes_sistema WHERE codigo = 'FALLBACK_DEFECTO' AND activo = TRUE")
            resultado = cursor.fetchone()
            if resultado:
                mensaje_fallback = resultado[0]
            conn.close()
        
        await update.message.reply_text(mensaje_fallback)

def main():
    # Crear aplicación
    app = Application.builder().token(TOKEN).build()
    
    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, manejar_mensaje))
    
    # Iniciar bot
    print("🤖 Thea IA Bot iniciado...")
    print("Presiona Ctrl+C para detener")
    app.run_polling()

if __name__ == "__main__":
    main()
