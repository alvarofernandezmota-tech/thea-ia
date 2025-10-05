# settings.py
"""
Archivo de configuración general del proyecto Thea AI.
Aquí se centralizan todas las variables de entorno y parámetros de configuración clave,
siendo el punto único para gestionar settings sensibles y parámetros globales.

Lee los datos desde el archivo .env, nunca pongas claves en claro aquí.

Ejemplo de uso:
from settings import TELEGRAM_TOKEN
"""

import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

# ========= Configuración de Integraciones =========
# Token del bot de Telegram, obtenido de BotFather
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Clave de acceso al bot de Telegram

# Token de autenticación de Ngrok, necesario si tu cuenta tiene key privada
NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")  # Para controlar túneles de ngrok

# Endpoint para el webhook (usualmente lo genera ngrok dinámicamente)
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Dirección pública a usar en Telegram setWebhook

# ========= Configuración de Base de Datos =========
# URL de la base de datos principal (puede ser SQLite, PostgreSQL, etc.)
DB_URL = os.getenv("DB_URL")  # Conexión a la base de datos utilizada por el proyecto

# ========= Otros parámetros globales =========
# Por ejemplo, modo debug para el entorno de desarrollo
DEBUG = os.getenv("DEBUG", "False") == "True"  # Permite logs más detallados si está activo

# Timeout global para peticiones API externas (en segundos)
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # Tiempo máximo de espera en requests

# ========= Validación automática =========
def validate_settings():
    """
    Función para validar la presencia de todas las variables clave.
    Útil al arrancar el proyecto para evitar errores por falta de configuración.
    """
    required_vars = [
        "TELEGRAM_TOKEN",
        "NGROK_AUTH_TOKEN",
        "DB_URL",
        "WEBHOOK_URL"
    ]
    missing = [var for var in required_vars if not globals().get(var)]
    if missing:
        raise EnvironmentError(
            f"FALTAN VARIABLES DE CONFIGURACIÓN: {', '.join(missing)}. "
            "Revisa tu archivo .env y .env.example."
        )

# Llama a la validación automática al importar
validate_settings()

# ==== Aclaraciones ====
# - Nunca pongas valores en claro en este archivo, solo referencias a os.getenv("VAR").
# - Este archivo debe ser importado en main.py y cualquier módulo que requiera settings globales.
# - Usa .env para tus valores privados y .env.example para mostrar variables necesarias sin datos reales.
