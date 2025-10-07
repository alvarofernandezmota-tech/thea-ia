import os
from dotenv import load_dotenv

# Carga .env
load_dotenv()

# Token de Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Mensajes centralizados
MESSAGES = {
    'saludo_inicial': "¡Hola {nombre}! 😊\n\n"
                     "...",
    # Resto de mensajes…
}
