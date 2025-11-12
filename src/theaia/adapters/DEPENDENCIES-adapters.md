Dependencias - src/adapters/
Módulo: Adapters
Versión actual: 0.1.0 (H01 - Planificación)
Última actualización: 11 Nov 2025

📦 Dependencias Python
H02 (12-16 Nov): TelegramAdapter
Producción:
text
# Telegram
aiogram==3.3.0                  # Framework Telegram Bot moderno, async
python-telegram-bot==20.7       # Alternative (no usado, pero disponible)

# Validación
pydantic==2.5.0                 # Schemas y validación

# HTTP/Async
aiohttp==3.9.1                  # Cliente HTTP async (usado por aiogram)
certifi==2023.11.17             # Certificados SSL

# Utils
python-dateutil==2.8.2          # Parseo fechas
Desarrollo:
text
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1          # Tests async
pytest-mock==3.12.0             # Mocking
pytest-cov==4.1.0               # Coverage

# Mocking Telegram
aiogram-tests==1.0.0            # Utilidades testing aiogram

# Code Quality
black==23.12.0                  # Formatter
pylint==3.0.3                   # Linter
mypy==1.7.1                     # Type checking
H08 (Ene 2026): WebAdapter [CONDICIONAL]
Adicionales Producción:
text
# Web Framework
fastapi==0.108.0                # API REST + WebSocket
uvicorn[standard]==0.25.0       # ASGI server
websockets==12.0                # WebSocket support

# Auth
python-jose[cryptography]==3.3.0  # JWT tokens
passlib[bcrypt]==1.7.4          # Password hashing

# CORS
fastapi-cors==0.0.6             # CORS middleware
H09 (Feb 2026): WhatsAppAdapter
Adicionales Producción:
text
# WhatsApp (Twilio)
twilio==8.11.1                  # Twilio API client

# O Meta Business API
facebook-business==18.0.0       # Meta Business SDK
whatsapp-business-client==0.2.1 # WhatsApp Business client

# Media
pillow==10.1.0                  # Image processing
pydub==0.25.1                   # Audio processing
H10 (Feb 2026): Discord + Slack
Adicionales Producción:
text
# Discord
discord.py==2.3.2               # Discord bot framework
py-cord==2.4.1                  # Alternative Discord lib

# Slack
slack-sdk==3.26.2               # Slack SDK
slack-bolt==1.18.1              # Slack Bolt framework
🔗 Dependencias Internas (THEA IA)
Módulos THEA IA que usa adapters/:
python
# H02 (obligatorias)
from src.core.thea_manager import CoreManager
from src.models.message import MessageSchema
from src.models.response import ResponseSchema
from src.config.settings import Settings
from src.utils.text_utils import normalize_text
from src.utils.datetime_utils import parse_datetime

# H04 (post-MVP)
from src.database.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService

# H06 (NLP)
from src.ml.nlp_service import NLPService
Módulos que usan adapters/:
python
# main.py (entry point)
from src.adapters.telegram_adapter import TelegramAdapter

# core/ (orquestador)
# No importa adapters directamente (inyección dependencias)
🌐 Servicios Externos
H02: Telegram Bot API
text
Servicio: Telegram Bot API
URL: https://api.telegram.org
Auth: Bot Token (via BotFather)
Rate Limits:
  - 30 mensajes/segundo (mismo chat)
  - Sin límite total (uso normal)
Webhooks: Soportado (preferible para producción)
Configuración requerida:

bash
# .env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_WEBHOOK_URL=https://tu-dominio.com/webhook/telegram
TELEGRAM_WEBHOOK_SECRET=tu_secret_aleatorio
H08: FastAPI + WebSocket [CONDICIONAL]
text
Servicio: Propio (self-hosted)
URL: Configurable (ej: wss://thea-ia.com/ws)
Auth: JWT tokens
Rate Limits: Configurable (H04)
CORS: Configurable por dominio
Configuración requerida:

bash
# .env
WEB_HOST=0.0.0.0
WEB_PORT=8000
JWT_SECRET_KEY=tu_secret_super_seguro_256_bits
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=https://app.thea-ia.com,https://thea-ia.com
H09: Twilio (WhatsApp)
text
Servicio: Twilio WhatsApp API
URL: https://api.twilio.com/2010-04-01
Auth: Account SID + Auth Token
Rate Limits:
  - 80 mensajes/segundo (por número)
  - Templates pre-aprobados por Meta
Costos: ~$0.005 por mensaje
Configuración requerida:

bash
# .env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_BUSINESS_ACCOUNT_ID=123456789
O Meta Business API:

bash
# .env
META_APP_ID=your_app_id
META_APP_SECRET=your_app_secret
WHATSAPP_PHONE_NUMBER_ID=123456789
WHATSAPP_BUSINESS_ACCOUNT_ID=987654321
META_ACCESS_TOKEN=your_long_lived_token
H10: Discord Bot
text
Servicio: Discord Bot API
URL: https://discord.com/api/v10
Auth: Bot Token
Rate Limits:
  - 5 requests/segundo global
  - 1 request/segundo por channel
Permisos: Configurables (slash commands, messages, etc)
Configuración requerida:

bash
# .env
DISCORD_BOT_TOKEN=MTxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DISCORD_APPLICATION_ID=123456789012345678
DISCORD_GUILD_ID=987654321098765432  # Server ID para testing
H10: Slack Bot
text
Servicio: Slack API
URL: https://slack.com/api
Auth: OAuth 2.0 (Bot Token)
Rate Limits:
  - Tier-based (workspace dependent)
  - ~1 request/segundo típico
Scopes: chat:write, commands, im:read, etc
Configuración requerida:

bash
# .env
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_APP_TOKEN=xapp-x-xxxxxxxxxxxx-xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxx
SLACK_SIGNING_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SLACK_CLIENT_ID=123456789.987654321
SLACK_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
🔐 Variables de Entorno
Archivo .env.example (adapters):
bash
# ============================================
# ADAPTERS CONFIGURATION
# ============================================

# Telegram (H02 - OBLIGATORIO)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
TELEGRAM_WEBHOOK_URL=  # Opcional (polling por defecto)
TELEGRAM_WEBHOOK_SECRET=  # Requerido si webhook

# Web (H08 - CONDICIONAL)
WEB_HOST=0.0.0.0
WEB_PORT=8000
JWT_SECRET_KEY=  # Generar con: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# WhatsApp (H09)
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
TWILIO_WHATSAPP_NUMBER=
# O Meta Business
META_APP_ID=
META_APP_SECRET=
WHATSAPP_PHONE_NUMBER_ID=
META_ACCESS_TOKEN=

# Discord (H10)
DISCORD_BOT_TOKEN=
DISCORD_APPLICATION_ID=
DISCORD_GUILD_ID=

# Slack (H10)
SLACK_BOT_TOKEN=
SLACK_APP_TOKEN=
SLACK_SIGNING_SECRET=
SLACK_CLIENT_ID=
SLACK_CLIENT_SECRET=
📊 Tabla Resumen Dependencias por Hito
Hito	Deps Python	Servicios Externos	Variables .env
H02	8 prod + 7 dev	Telegram Bot API	3 vars
H08	+6 prod	Self-hosted (FastAPI)	+6 vars
H09	+4 prod	Twilio/Meta	+5 vars
H10	+4 prod	Discord + Slack	+10 vars
Total	22 prod + 7 dev	5 servicios	24 vars
🚀 Instalación Dependencias
H02 (Setup inicial):
bash
# Crear virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Instalar dependencias producción
pip install aiogram==3.3.0 pydantic==2.5.0 aiohttp==3.9.1 python-dateutil==2.8.2

# Instalar dependencias desarrollo
pip install pytest==7.4.3 pytest-asyncio==0.21.1 pytest-mock==3.12.0 pytest-cov==4.1.0
pip install black==23.12.0 pylint==3.0.3 mypy==1.7.1

# Guardar en requirements.txt
pip freeze > requirements.txt
Instalación desde requirements.txt:
bash
pip install -r requirements.txt
🔄 Actualización Dependencias
Política Versiones:
Major versions: Solo con aprobación explícita (breaking changes)

Minor versions: Actualizar cada 3 meses (nuevas features)

Patch versions: Actualizar cada mes (bug fixes)

Comando actualización:
bash
# Ver dependencias desactualizadas
pip list --outdated

# Actualizar específica
pip install --upgrade aiogram

# Actualizar todas (con cuidado)
pip install --upgrade -r requirements.txt
🧪 Testing Dependencias
Verificar instalación:
bash
# Verificar aiogram
python -c "import aiogram; print(aiogram.__version__)"

# Verificar todas
python -c "import aiogram, pydantic, aiohttp, pytest; print('OK')"
Tests compatibilidad:
bash
# Ejecutar tests después de actualizar deps
pytest src/tests/unit/test_adapters/ -v
⚠️ Notas Seguridad
Tokens y Secrets:
❌ NUNCA commitear tokens en código

✅ Siempre usar variables de entorno

✅ Incluir .env en .gitignore

✅ Rotar tokens cada 6 meses

✅ Usar secrets manager (H15) para producción

Dependencias:
✅ Fijar versiones exactas en producción

✅ Auditar dependencias con pip-audit

✅ Revisar CVEs periódicamente

❌ No instalar desde fuentes no confiables

bash
# Auditar vulnerabilidades
pip install pip-audit
pip-audit
📞 Soporte
Documentación Oficial:
aiogram: https://docs.aiogram.dev/en/latest/

FastAPI: https://fastapi.tiangolo.com/

Twilio: https://www.twilio.com/docs/whatsapp

Discord.py: https://discordpy.readthedocs.io/

Slack SDK: https://slack.dev/python-slack-sdk/

Issues:
Para bugs de dependencias externas: Reportar en repos oficiales

Para bugs de integración THEA: Reportar internamente

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota