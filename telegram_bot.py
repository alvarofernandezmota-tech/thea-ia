# ----------------- PASOS PARA INSTALAR, CONFIGURAR Y CORRER EL BOT DE TELEGRAM DE THEA IA -----------------

# 1. Abre la terminal en la carpeta raíz de tu proyecto (C:\Users\Admin\Desktop\thea_ia).

# 2. Crea el entorno virtual (solo si aún no existe):
#    python -m venv .venv

# 3. Activa el entorno virtual (PowerShell):
#    & .venv/Scripts/Activate.ps1

# 4. Instala todas las dependencias necesarias en el entorno virtual:
#    pip install python-dotenv telebot sqlalchemy psycopg2-binary

# 5. Crea un archivo .env en el proyecto y pon tu token de BotFather:
#    TELEGRAM_TOKEN=tu_token_de_bot_aqui
#    (agrega aquí variables y credenciales sensibles)

# 6. Configura un archivo settings.py para cargar las variables de entorno:
#    from dotenv import load_dotenv
#    import os
#    load_dotenv()
#    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
#    DB_URL = os.getenv('DB_URL')   # Si tienes variables para la BD

# 7. Asegúrate de tener instalado y configurado PostgreSQL
#    (Crea la base y tablas siguiendo los scripts que ya tienes: usuarios, citas, etc.)

# 8. Instala las dependencias de acceso a PostgreSQL:
#    pip install psycopg2-binary

# 9. En tu script principal, importa settings y configura el bot:
#    from settings import TELEGRAM_TOKEN
#    from telebot import TeleBot
#    bot = TeleBot(TELEGRAM_TOKEN)
#    # (Aquí implementa los handlers para agendar, consultar, modificar, cancelar...)

# 10. Corre el bot con:
#     python telegram_bot.py
#     # La terminal debe quedarse abierta y mostrar logs de actividad.

# 11. Ve a Telegram, busca tu bot y prueba estos comandos:
#     /start       -- mensaje de bienvenida
#     agendar      -- agendar una cita
#     consultar    -- consultar tus citas

# ----------------- FIN DE LA GUÍA DE INSTALACIÓN Y ACTIVACIÓN -----------------
import sys
import os
sys.path.append(os.path.abspath("thea-ai/src"))
from thea.core.scheduler_agent import SchedulerAgent
from telebot import TeleBot
from settings import TELEGRAM_TOKEN
bot = TeleBot(TELEGRAM_TOKEN)

from thea.core.scheduler_agent import SchedulerAgent


@bot.message_handler(commands=['start'])
def welcome(message):
    bot.reply_to(message, "¡Hola! Soy THEA, tu asistente de agendamiento de citas.")

@bot.message_handler(func=lambda m: 'agendar' in m.text.lower())
def agendar_cita_handler(message):
    user_id = message.from_user.id
    agent = SchedulerAgent(user_id)
    evento = agent.agendar_cita("mañana", "11:00", "Revisión")
    bot.reply_to(message, f"{evento}")

@bot.message_handler(func=lambda m: 'consultar' in m.text.lower())
def consultar_citas_handler(message):
    user_id = message.from_user.id
    agent = SchedulerAgent(user_id)
    citas = agent.consultar_citas()
    bot.reply_to(message, "\n".join(citas))

bot.polling()
