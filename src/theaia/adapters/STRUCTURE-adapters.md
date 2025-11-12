Estructura Planificada - src/adapters/
Módulo: Adapters (Interfaces de canal)
Propósito: Abstraer comunicación con diferentes plataformas de mensajería
Patrón: Strategy Pattern + Abstract Factory

📋 Estado Actual (11 Nov 2025 - H01)
text
src/adapters/
├── __init__.py (placeholder)
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅
Estado: Prototipo documentado, sin implementación funcional

🎯 H02 (12-16 Nov): TelegramAdapter Funcional
Estructura Objetivo:
text
src/adapters/
│
├── __init__.py
│   # Exports: BaseAdapter, TelegramAdapter
│
├── base_adapter.py                 # 🆕 CREAR DÍA 1
│   # Clase abstracta BaseAdapter
│   # Métodos abstractos:
│   #   - async receive_message()
│   #   - async send_message()
│   #   - async normalize_message()
│   # Métodos concretos:
│   #   - handle_error()
│   #   - log_interaction()
│
├── telegram_adapter.py             # 🆕 CREAR DÍA 2
│   # Implementación TelegramAdapter
│   # Hereda: BaseAdapter
│   # Atributos:
│   #   - bot: aiogram.Bot
│   #   - dispatcher: aiogram.Dispatcher
│   #   - core_manager: CoreManager
│   # Métodos:
│   #   - async start()
│   #   - async stop()
│   #   - async receive_message()
│   #   - async send_message()
│   #   - async normalize_message()
│   #   - register_handlers()
│
├── telegram/                       # 🆕 CREAR DÍA 2-3
│   │
│   ├── __init__.py
│   │
│   ├── handlers.py                 # Handlers comandos y mensajes
│   │   # Funciones:
│   │   #   - async cmd_start(message: Message)
│   │   #   - async cmd_help(message: Message)
│   │   #   - async handle_text_message(message: Message)
│   │   #   - async handle_voice(message: Message)
│   │   #   - async handle_document(message: Message)
│   │
│   ├── callbacks.py                # Callback queries (botones inline)
│   │   # Funciones:
│   │   #   - async callback_confirm(callback: CallbackQuery)
│   │   #   - async callback_cancel(callback: CallbackQuery)
│   │   #   - async callback_settings(callback: CallbackQuery)
│   │
│   ├── middleware.py               # Middleware Telegram
│   │   # Clases:
│   │   #   - LoggingMiddleware (logs interacciones)
│   │   #   - AuthMiddleware (verifica usuario registrado)
│   │   #   - RateLimitMiddleware [H04] (limitar spam)
│   │   #   - MetricsMiddleware [H12] (métricas uso)
│   │
│   ├── keyboards.py                # Teclados inline/reply
│   │   # Funciones:
│   │   #   - get_main_menu_keyboard()
│   │   #   - get_confirm_keyboard()
│   │   #   - get_settings_keyboard()
│   │
│   ├── formatters.py               # Formateadores respuesta
│   │   # Funciones:
│   │   #   - format_reminder(reminder: Reminder) -> str
│   │   #   - format_note(note: Note) -> str
│   │   #   - format_event(event: Event) -> str
│   │   #   - format_error(error: Exception) -> str
│   │
│   └── utils.py                    # Helpers Telegram
│       # Funciones:
│       #   - extract_user_info(message: Message) -> dict
│       #   - is_command(text: str) -> bool
│       #   - parse_command(text: str) -> tuple[str, list]
│       #   - escape_markdown(text: str) -> str
│
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── STRUCTURE.md (este archivo)
└── DEPENDENCIES.md
Archivos por Día (H02):
Día 1 (12 Nov):

text
✅ base_adapter.py (interfaz abstracta)
Día 2 (13 Nov):

text
✅ telegram_adapter.py (implementación base)
✅ telegram/handlers.py (handlers básicos)
✅ telegram/middleware.py (logging middleware)
✅ telegram/utils.py (helpers)
Día 3 (14 Nov):

text
✅ telegram/callbacks.py (botones)
✅ telegram/keyboards.py (teclados)
✅ telegram/formatters.py (formateo respuestas)
✅ Integración completa con CoreManager
Día 4-5 (15-16 Nov):

text
✅ Refinamiento
✅ Error handling robusto
✅ Tests unitarios
✅ Documentación inline
🔮 H08 (Ene 2026): WebAdapter [CONDICIONAL]
Solo si usuarios demandan acceso web.

Estructura Planificada:
text
src/adapters/
├── base_adapter.py (sin cambios)
├── telegram_adapter.py (sin cambios)
├── telegram/ (sin cambios)
│
├── web_adapter.py                  # 🆕 H08
│   # Implementación WebAdapter
│   # Hereda: BaseAdapter
│   # Integración: FastAPI WebSocket + REST
│
├── web/                            # 🆕 H08
│   ├── __init__.py
│   ├── websocket_handler.py        # WebSocket real-time
│   ├── rest_endpoints.py           # REST API fallback
│   ├── middleware.py               # CORS, auth, logging
│   ├── schemas.py                  # Request/Response schemas
│   └── utils.py
│
└── ...
🌐 H09 (Feb 2026): WhatsAppAdapter
Estructura Planificada:
text
src/adapters/
├── base_adapter.py (sin cambios)
├── telegram_adapter.py (sin cambios)
├── web_adapter.py (sin cambios)
│
├── whatsapp_adapter.py             # 🆕 H09
│   # Implementación WhatsAppAdapter
│   # Integración: Twilio API o Meta Business API
│
├── whatsapp/                       # 🆕 H09
│   ├── __init__.py
│   ├── twilio_client.py            # Cliente Twilio
│   ├── message_parser.py           # Parser mensajes WhatsApp
│   ├── media_handler.py            # Audio/imagen/video
│   ├── template_manager.py         # Templates aprobados Meta
│   └── utils.py
│
└── ...
💬 H10 (Feb 2026): Discord/Slack Adapters
Estructura Planificada:
text
src/adapters/
├── base_adapter.py (sin cambios)
├── telegram_adapter.py (sin cambios)
├── web_adapter.py (sin cambios)
├── whatsapp_adapter.py (sin cambios)
│
├── discord_adapter.py              # 🆕 H10
│   # Implementación DiscordAdapter
│   # Integración: discord.py
│
├── discord/                        # 🆕 H10
│   ├── __init__.py
│   ├── bot_commands.py             # Slash commands
│   ├── events.py                   # Event handlers
│   └── utils.py
│
├── slack_adapter.py                # 🆕 H10
│   # Implementación SlackAdapter
│   # Integración: slack-sdk
│
├── slack/                          # 🆕 H10
│   ├── __init__.py
│   ├── bolt_app.py                 # Slack Bolt app
│   ├── event_handlers.py           # Event subscriptions
│   ├── slash_commands.py           # Slash commands
│   └── utils.py
│
└── ...
📐 Patrones de Diseño
Strategy Pattern:
BaseAdapter define interfaz común

Cada adapter (Telegram, Web, WhatsApp...) implementa estrategia específica

CoreManager trabaja con BaseAdapter, no implementaciones concretas

Template Method:
BaseAdapter.handle_error() es método concreto usado por todos

Subclases solo implementan métodos abstractos específicos

Dependency Injection:
Adapters reciben CoreManager en constructor

No instancian dependencias directamente

🔗 Dependencias Internas
text
src/adapters/ depende de:
├── src/core/thea_manager.py (CoreManager)
├── src/models/message.py (MessageSchema)
├── src/models/response.py (ResponseSchema)
├── src/config/settings.py (Settings)
└── src/utils/text_utils.py (normalización)
📊 Métricas Estimadas
H02 (TelegramAdapter):
Archivos: 9 archivos Python

Líneas código: ~1,200 LOC

Tests: ~800 LOC

Cobertura objetivo: >80%

H08 (WebAdapter):
Archivos adicionales: +6

LOC adicional: ~800

Tests adicionales: ~600 LOC

H09 (WhatsAppAdapter):
Archivos adicionales: +6

LOC adicional: ~900

Tests adicionales: ~650 LOC

H10 (Discord + Slack):
Archivos adicionales: +8

LOC adicional: ~1,000

Tests adicionales: ~700 LOC

🎯 Criterios de Completitud
H02 Done cuando:
✅ TelegramAdapter implementado completamente

✅ Puede recibir mensajes Telegram

✅ Puede enviar respuestas

✅ Normaliza mensajes a formato estándar

✅ Maneja errores gracefully

✅ Logging completo

✅ Tests unitarios >80% coverage

✅ Integración con CoreManager funcional

✅ Primera conversación real funciona

H08 Done cuando:
✅ WebAdapter implementado

✅ WebSocket bidireccional funciona

✅ REST API fallback funciona

✅ CORS configurado

✅ Auth JWT implementado

✅ Tests E2E pasan

H09 Done cuando:
✅ WhatsAppAdapter implementado

✅ Twilio/Meta API integrado

✅ Puede enviar/recibir mensajes

✅ Templates Meta aprobados

✅ Media handling funciona

✅ Business account verificado

H10 Done cuando:
✅ Discord + Slack adapters implementados

✅ Slash commands funcionan

✅ Event subscriptions activas

✅ Bots en producción

✅ Tests pasan

🚀 Comandos Desarrollo
Setup Telegram (H02):
bash
# Crear bot en BotFather
# Obtener token

# Configurar .env
echo "TELEGRAM_BOT_TOKEN=your_token" >> .env

# Instalar dependencias
pip install aiogram==3.3.0

# Ejecutar
python -m src.main
Ejecutar Tests:
bash
pytest src/tests/unit/test_adapters/ -v
pytest src/tests/integration/test_telegram_flow.py -v
Verificar Coverage:
bash
pytest --cov=src/adapters --cov-report=html
open htmlcov/index.html
📝 Notas Implementación
Error Handling:
Todos los métodos async usan try/except

Errores logeados con contexto completo

Usuario recibe mensaje error amigable

Errores críticos → notificación admin

Logging:
Cada interacción logeada (user_id, mensaje, respuesta)

Nivel INFO para operaciones normales

Nivel WARNING para errores recuperables

Nivel ERROR para errores críticos

Testing:
Mocks de aiogram.Bot para tests unitarios

Fixtures pytest para setup/teardown

Tests parametrizados para múltiples casos

Tests integración con Telegram test server

Performance:
Async/await en todos los métodos I/O

Connection pooling para HTTP requests

Caché respuestas comunes (H13)

Rate limiting (H04)

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota