Adapters - Sistema de Canales Multicanal
Módulo: src/theaia/adapters/
Versión: 0.1.0
Estado: ⚠️ Estructura creada, sin implementación
Responsable: Álvaro Fernández Mota

📋 Descripción
Los Adapters son el puente entre los diferentes canales de comunicación (Telegram, Web, WhatsApp, Discord, Slack, Voice) y el núcleo de THEA IA.

Implementan el patrón Adapter para permitir que THEA funcione en múltiples plataformas sin modificar la lógica de negocio central (CoreManager, Router, Agents).

Propósito
✅ Desacoplar canales de comunicación del core

✅ Normalizar mensajes de diferentes plataformas a formato estándar

✅ Escalar horizontalmente según demanda

✅ Facilitar integración de nuevos canales

🏗️ Arquitectura
Diagrama de Flujo General
text
┌──────────────┐
│   USUARIO    │ (Telegram, Web, WhatsApp, etc.)
└──────┬───────┘
       │
       ▼
┌─────────────────────┐
│  ADAPTER ESPECÍFICO │ (TelegramAdapter, WebAdapter, etc.)
│                     │
│  Responsabilidades: │
│  1. Recibir mensaje │
│  2. Normalizar      │
│  3. Validar         │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│   CORE MANAGER      │ (src/theaia/core/core_manager.py)
│                     │
│  - Gestiona FSM     │
│  - Llama Router     │
│  - Orquesta Agents  │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│      ROUTER         │ (src/theaia/core/router.py)
│                     │
│  - Detecta intent   │
│  - Selecciona Agent │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│      AGENT          │ (AgendaAgent, NoteAgent, ReminderAgent...)
│                     │
│  - Procesa mensaje  │
│  - Ejecuta acción   │
│  - Genera respuesta │
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  CORE MANAGER       │ (devuelve respuesta)
└──────┬──────────────┘
       │
       ▼
┌─────────────────────┐
│  ADAPTER (vuelta)   │
│                     │
│  - Formatea para    │
│    canal específico │
│  - Envía al usuario │
└─────────────────────┘
🔧 Componentes
1. BaseAdapter (Interfaz Abstracta)
Ubicación: src/theaia/adapters/base_adapter.py (a crear en H02)

Clase abstracta que define el contrato que todos los adapters deben cumplir.

Métodos Obligatorios
python
from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAdapter(ABC):
    """
    Interfaz base para todos los adapters de THEA IA.
    
    Garantiza que cualquier canal pueda comunicarse 
    con CoreManager de forma uniforme.
    """
    
    def __init__(self, core_manager):
        self.core_manager = core_manager
    
    @abstractmethod
    async def handle_message(self, raw_message: Any) -> None:
        """
        Procesar mensaje del canal específico.
        
        Args:
            raw_message: Mensaje en formato nativo del canal
        """
        pass
    
    @abstractmethod
    async def send_response(self, user_id: str, response: str) -> None:
        """
        Enviar respuesta al usuario en el canal.
        
        Args:
            user_id: ID del usuario
            response: Texto de respuesta
        """
        pass
    
    @abstractmethod
    def normalize_message(self, raw_message: Any) -> Dict[str, Any]:
        """
        Convertir mensaje nativo a formato estándar THEA.
        
        Returns:
            {
                "user_id": str,
                "message": str,
                "platform": str,
                "metadata": dict
            }
        """
        pass
    
    @abstractmethod
    async def start(self) -> None:
        """Iniciar el adapter (polling, webhook, etc.)"""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Detener el adapter de forma segura"""
        pass
2. TelegramAdapter
Ubicación: src/theaia/adapters/telegram_adapter.py (a implementar en H02)
Estado: ⚠️ Placeholder (0 bytes)
Prioridad: 🔴 CRÍTICA

Descripción
Adapter para bots de Telegram usando aiogram 3.2.0.

Características Planificadas
✅ Polling automático (desarrollo)

✅ Webhooks (producción)

✅ Comandos: /start, /help, /agenda, /nota, /recordatorio

✅ Formateo Markdown + emojis

✅ Botones inline para confirmaciones

✅ Manejo de errores robusto

Ejemplo de Uso (Futuro)
python
from src.theaia.adapters.telegram_adapter import TelegramAdapter
from src.theaia.core.core_manager import CoreManager

# Inicializar CoreManager
core_manager = CoreManager()

# Crear adapter
telegram_adapter = TelegramAdapter(
    token=os.getenv("TELEGRAM_BOT_TOKEN"),
    core_manager=core_manager
)

# Iniciar bot
await telegram_adapter.start()
3. WebAdapter
Ubicación: src/theaia/adapters/web_adapter.py (renombrar desde webhook_handler.py en H02)
Estado: ⚠️ Placeholder (0 bytes)
Prioridad: 🔴 ALTA

Descripción
Adapter para API REST usando FastAPI 0.104.1.

Características Planificadas
✅ Endpoint POST /api/chat

✅ Validación con Pydantic v2

✅ CORS configurado

✅ Rate limiting (10 req/min por IP)

✅ WebSocket para chat en tiempo real (opcional H03)

✅ OpenAPI docs automática (/docs)

Ejemplo de Endpoint (Futuro)
python
# POST /api/chat
{
    "user_id": "user123",
    "message": "Recuérdame comprar leche mañana a las 10am",
    "context": {}
}

# Response
{
    "response": "✅ Recordatorio creado: comprar leche mañana a las 10:00",
    "state": "completed",
    "context": {...}
}
4. WhatsAppAdapter
Ubicación: src/theaia/adapters/whatsapp_adapter.py (a implementar en H05)
Estado: ⚠️ Placeholder (0 bytes)
Prioridad: 🟢 MEDIA

Descripción
Adapter para WhatsApp Business usando Twilio API.

Características Planificadas
✅ Integración con Twilio

✅ Webhook para mensajes entrantes

✅ Formateo específico WhatsApp (plain text, sin markdown)

✅ Soporte multimedia (H06)

🔗 Formato de Mensaje Normalizado
Todos los adapters convierten mensajes a este formato estándar:

python
{
    "user_id": str,          # ID único del usuario en la plataforma
    "message": str,          # Texto del mensaje
    "platform": str,         # "telegram" | "web" | "whatsapp" | "discord" | "slack"
    "metadata": {
        "username": str,     # @username (opcional)
        "first_name": str,   # Nombre del usuario
        "timestamp": str,    # ISO 8601 (ej: "2025-11-10T22:30:00Z")
        "channel_id": str    # ID del canal/chat (opcional)
    }
}
¿Por qué Normalizar?
✅ CoreManager NO conoce el canal: Procesa formato estándar

✅ Fácil logging: Mismo formato para todos los canales

✅ Fácil analytics: Métricas uniformes

✅ Testeable: Mocks sencillos

🚀 Uso
Añadir un Nuevo Adapter
1. Heredar de BaseAdapter
python
from src.theaia.adapters.base_adapter import BaseAdapter

class DiscordAdapter(BaseAdapter):
    def __init__(self, token: str, core_manager):
        super().__init__(core_manager)
        self.bot = discord.Client(token)
    
    async def handle_message(self, message):
        # Normalizar mensaje de Discord
        normalized = self.normalize_message(message)
        
        # Pasar a CoreManager
        response = await self.core_manager.process_message(
            user_id=normalized["user_id"],
            message=normalized["message"],
            context=normalized.get("metadata", {})
        )
        
        # Enviar respuesta
        await self.send_response(message.author.id, response["response"])
    
    async def send_response(self, user_id, response):
        channel = self.bot.get_channel(user_id)
        await channel.send(response)
    
    def normalize_message(self, message):
        return {
            "user_id": str(message.author.id),
            "message": message.content,
            "platform": "discord",
            "metadata": {
                "username": message.author.name,
                "timestamp": message.created_at.isoformat()
            }
        }
    
    async def start(self):
        await self.bot.start()
    
    async def stop(self):
        await self.bot.close()
2. Registrar en Factory (H03)
python
from src.theaia.adapters.adapter_factory import AdapterFactory

AdapterFactory.register_adapter("discord", DiscordAdapter)
3. Crear Tests
python
# src/theaia/tests/adapters/test_discord_adapter.py

@pytest.mark.asyncio
async def test_discord_adapter_handles_message():
    # Arrange
    mock_core = AsyncMock()
    adapter = DiscordAdapter("token", mock_core)
    
    # Act
    await adapter.handle_message(mock_message)
    
    # Assert
    mock_core.process_message.assert_called_once()
4. Documentar
Actualizar este README

Añadir ejemplo de uso

Actualizar ROADMAP con timeline

🧪 Testing
Ejecutar Tests
bash
# Todos los tests de adapters
pytest src/theaia/tests/adapters/ -v

# Solo Telegram
pytest src/theaia/tests/adapters/test_telegram_adapter.py -v

# Con coverage
pytest src/theaia/tests/adapters/ --cov=src/theaia/adapters --cov-report=html
Estructura de Tests
text
src/theaia/tests/adapters/
├── __init__.py
├── test_telegram_adapter.py    # Tests unitarios Telegram
├── test_web_adapter.py          # Tests unitarios Web
├── test_whatsapp_adapter.py     # Tests unitarios WhatsApp
├── fixtures/
│   ├── telegram_messages.py     # Mensajes de prueba Telegram
│   ├── web_requests.py          # Requests de prueba Web
│   └── mock_core_manager.py     # Mock de CoreManager
└── integration/
    └── test_adapter_core_integration.py  # Tests E2E
📦 Dependencias
Telegram
text
aiogram==3.2.0         # Framework Telegram Bot
aiohttp>=3.8.0         # HTTP async (usado por aiogram)
Web
text
fastapi==0.104.1       # Framework API REST
uvicorn==0.24.0        # ASGI server
pydantic>=2.0.0        # Validación de datos
WhatsApp (H05)
text
twilio>=8.0.0          # Twilio API para WhatsApp
httpx>=0.24.0          # HTTP client async
Discord & Slack (H05)
text
discord.py>=2.3.0      # Discord API
slack-bolt>=1.18.0     # Slack Bolt framework
🔐 Configuración
Variables de Entorno
Configurar en .env:

bash
# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_token_here
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/webhook  # Solo si usas webhook

# Web API
WEB_API_HOST=0.0.0.0
WEB_API_PORT=8000
WEB_API_CORS_ORIGINS=http://localhost:3000,https://app.thea-ia.com

# WhatsApp (H05)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Discord (H05)
DISCORD_BOT_TOKEN=your_discord_token

# Slack (H05)
SLACK_BOT_TOKEN=xoxb-your-slack-token
SLACK_SIGNING_SECRET=your_signing_secret
📊 Métricas y Observabilidad
Métricas Expuestas
Cada adapter expone métricas Prometheus:

python
# Contador de mensajes
messages_received_total{platform="telegram"}
messages_sent_total{platform="telegram"}

# Latencia
message_processing_seconds{platform="telegram", percentile="p95"}

# Errores
adapter_errors_total{platform="telegram", error_type="timeout"}

# Estado
adapter_status{platform="telegram", status="running"}
Logs
Los adapters logean en:

text
logs/
├── adapters/
│   ├── telegram.log
│   ├── web.log
│   └── whatsapp.log
Formato de log (structlog):

json
{
  "timestamp": "2025-11-10T22:30:00Z",
  "level": "INFO",
  "adapter": "telegram",
  "user_id": "123456",
  "message": "Mensaje recibido",
  "latency_ms": 250
}
🐛 Debugging
Problemas Comunes
Telegram: "Unauthorized"
Síntoma: Bot no responde, error 401

Solución:

Verificar TELEGRAM_BOT_TOKEN en .env

Regenerar token en @BotFather si es necesario

Reiniciar bot

Web: "CORS blocked"
Síntoma: Requests desde navegador bloqueados

Solución:

Añadir origen en WEB_API_CORS_ORIGINS

Verificar que FastAPI CORS middleware esté configurado

Verificar headers en request

WhatsApp: "Invalid signature"
Síntoma: Webhook rechazado por Twilio

Solución:

Verificar TWILIO_AUTH_TOKEN correcto

Validar firma usando twilio.request_validator

Verificar HTTPS en webhook URL

Modo Debug
Activar logs detallados:

bash
export LOG_LEVEL=DEBUG
python -m src.theaia.adapters.telegram_adapter
🔒 Seguridad
Mejores Prácticas
Tokens en variables de entorno - NUNCA en código

Validación de entrada - Sanitizar todos los mensajes

Rate limiting - Limitar requests por usuario/IP

HTTPS obligatorio - En webhooks de producción

Validación de webhooks - Verificar firmas (Telegram, Twilio, etc.)

Timeouts - Evitar colgarse con mensajes maliciosos

Blacklist - Bloquear usuarios/IPs abusivos

🚀 Performance
Benchmarks Objetivo
Adapter	Latencia p95	Throughput	Usuarios Concurrentes
Telegram	<500ms	100 msg/s	100
Web API	<300ms	500 req/s	1,000
WhatsApp	<1s	50 msg/s	500
Optimizaciones
Message Queue (H03) - Buffer de 10K mensajes

Workers paralelos (H03) - 5-10 workers por adapter

Connection pooling - Reutilizar conexiones HTTP

Caching - Redis para contextos de usuario

Horizontal scaling (H08) - Múltiples instancias

🤝 Contribuciones
Proceso
Crear issue con propuesta

Fork del repositorio

Crear branch: feature/adapter-<platform>

Implementar adapter + tests

PR con documentación

Code review

Merge

Checklist PR
 Tests passing (coverage ≥80%)

 Documentación actualizada

 CHANGELOG updated

 Performance benchmarks

 Security review

📚 Referencias
Patrones de Diseño
Patrón Adapter

Hexagonal Architecture

Frameworks
Aiogram Documentation

FastAPI Documentation

Twilio WhatsApp API

Discord.py Documentation

Slack Bolt Python

Escalabilidad
Python Async Best Practices

Microservices Patterns

📞 Contacto
Mantenedor: Álvaro Fernández Mota
Email: alvarofernandezmota@gmail.com
GitHub: @alvarofernandezmota-tech

Issues: GitHub Issues
Propuestas: GitHub Discussions

📝 Licencia
MIT License - Ver LICENSE en raíz del proyecto

Última actualización: 11 noviembre 2025
Próxima revisión: 20 noviembre 2025 (post H02)