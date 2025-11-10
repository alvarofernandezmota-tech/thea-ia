BotFactory — Multi-Platform Bot Creation Pattern
Versión: v1.0
Ubicación: src/theaia/core/bot_factory.py
Última actualización: 2025-11-10 16:50 CET (S38)
Estado: ✅ Production Ready

📖 Overview
BotFactory es un factory pattern que permite crear bots para múltiples plataformas.

Ventajas:

Desacopla la lógica conversacional de la plataforma específica

Permite agregar nuevas plataformas sin modificar core

Testing simplificado con mock bots

Escalabilidad multi-canal

🔑 Clase Principal
python
class BotFactory:
    @staticmethod
    def create_bot(bot_type: str = "thea", config: Dict = None) → BaseBot:
        """Crear instancia de bot según tipo."""
        
        if bot_type == "thea":
            return TheaBot(config or {})
        elif bot_type == "whatsapp":
            return WhatsAppBot(config or {})
        elif bot_type == "telegram":
            return TelegramBot(config or {})
        elif bot_type == "test":
            return MockBot(config or {})
        else:
            raise ValueError(f"Unknown bot type: {bot_type}")
📋 Bot Types Soportados
1. Thea (Chat API Estándar)
python
bot = BotFactory.create_bot("thea")

# Send message
response = bot.send_message("user_123", "Hola desde THEA!")

# Send buttons
response = bot.send_buttons("user_123", "¿Qué quieres hacer?", [
    {"text": "Agendar", "payload": "agenda"},
    {"text": "Notas", "payload": "notes"}
])
Configuración: Mínima (local API)

2. WhatsApp Business API
python
bot = BotFactory.create_bot("whatsapp", config={
    'phone_number_id': '120363123456789',
    'access_token': 'EAABsZAZBZCxxx...',
    'webhook_verify_token': 'my_voice_is_my_password'
})

# Send text
bot.send_message("5491123456789", "¡Hola desde WhatsApp!")

# Send template
bot.send_template("5491123456789", "hello_world")

# Handle webhook
@app.post("/webhook/whatsapp")
async def whatsapp_webhook(request: Request):
    body = await request.json()
    return bot.handle_webhook(body)
Configuración:

phone_number_id — ID del número de teléfono

access_token — Token de acceso Meta

webhook_verify_token — Token para verificar webhook

3. Telegram Bot API
python
bot = BotFactory.create_bot("telegram", config={
    'token': '5123456789:ABCDefGhiJKlmnoPQRstUVWxyz123456789',
    'webhook_url': 'https://myserver.com/webhook/telegram'
})

# Send message
bot.send_message("987654321", "¡Hola desde Telegram!")

# Send keyboard
bot.send_keyboard("987654321", "Opciones:", [
    ["Agendar", "Notas"],
    ["Ayuda", "Salir"]
])

# Handle update
@app.post("/webhook/telegram")
async def telegram_webhook(update: dict):
    return bot.handle_webhook(update)
Configuración:

token — Bot token de Telegram

webhook_url — URL pública para webhook

4. Test (Mock Bot para Testing)
python
bot = BotFactory.create_bot("test")

# No necesita config
# Retorna respuestas simuladas

response = bot.send_message("test_user", "Mensaje de prueba")
assert response['status'] == 'success'
assert response['user_id'] == 'test_user'

# Testing completo sin APIs reales
from src.theaia.core.router import TheaRouter

router = TheaRouter()
bot = BotFactory.create_bot("test")

test_response, context = router.handle_request(
    user_id="test_user",
    message="Agendar reunión"
)

assert context['current_state'] in ['agent_delegated', 'completed']
🔌 BaseBot Interface (Abstracta)
Todos los bots implementan esta interfaz:

python
class BaseBot(ABC):
    @abstractmethod
    def send_message(self, user_id: str, text: str) → Dict:
        """Enviar mensaje de texto simple."""
        pass
    
    @abstractmethod
    def send_buttons(self, user_id: str, text: str, 
                     buttons: List[Dict]) → Dict:
        """Enviar mensaje con botones."""
        pass
    
    @abstractmethod
    def send_media(self, user_id: str, media_url: str, 
                   media_type: str) → Dict:
        """Enviar imagen/video."""
        pass
    
    @abstractmethod
    def handle_webhook(self, payload: Dict) → Dict:
        """Procesar webhook entrante."""
        pass
💡 Ejemplo Completo (Multi-Platform)
python
from src.theaia.core.bot_factory import BotFactory
from src.theaia.core.router import TheaRouter
import os

# Inicializar router
router = TheaRouter()

# Crear bot según env var
PLATFORM = os.getenv("BOT_PLATFORM", "thea")

if PLATFORM == "whatsapp":
    bot = BotFactory.create_bot("whatsapp", {
        'phone_number_id': os.getenv('WA_PHONE_ID'),
        'access_token': os.getenv('WA_ACCESS_TOKEN'),
        'webhook_verify_token': os.getenv('WA_WEBHOOK_TOKEN')
    })
elif PLATFORM == "telegram":
    bot = BotFactory.create_bot("telegram", {
        'token': os.getenv('TG_TOKEN'),
        'webhook_url': os.getenv('TG_WEBHOOK_URL')
    })
else:
    bot = BotFactory.create_bot("thea")

# Webhook handler (mismo código para TODOS los bots)
@app.post("/webhook/{platform}")
async def webhook_handler(platform: str, request: Request):
    payload = await request.json()
    
    # Parse usuario y mensaje
    user_id = payload.get('user_id')
    message = payload.get('message')
    
    # Route through THEA
    response, context = router.handle_request(user_id, message)
    
    # Send through bot (platform-agnostic)
    result = bot.send_message(user_id, response)
    
    return {"status": "ok", "message_id": result.get('message_id')}
📊 Plataformas Roadmap
Plataforma	v	Status	ETA
Thea	1.0	✅ Prod	NOW
WhatsApp	1.0	✅ Prod	NOW
Telegram	1.0	✅ Prod	NOW
Slack	1.1	🟡 Planned	H01
Discord	1.1	🟡 Planned	H01
Teams	1.2	🟡 Planned	H02
Google Chat	1.2	🟡 Planned	H02
🎯 Ventajas del Pattern
1. Desacoplamiento
text
TheaRouter (logic)
    ↓
BotFactory (abstraction)
    ↓
Specific Bot (platform)
2. Extensibilidad
text
# Agregar Slack sin tocar router
class SlackBot(BaseBot):
    def send_message(self, user_id, text):
        # Slack-specific logic
        pass
3. Testing
text
# Test con mock bot (sin APIs reales)
bot = BotFactory.create_bot("test")
# Mismo código, sin dependencias externas
4. Multi-Tenant
text
# Múltiples clientes/plataformas simultáneas
clients = {
    'client_a': BotFactory.create_bot("whatsapp", config_a),
    'client_b': BotFactory.create_bot("telegram", config_b),
    'client_c': BotFactory.create_bot("thea", config_c)
}
🐛 Known Issues
 Sin retry logic (v1.0)

 Sin rate limiting por plataforma (v1.0)

 Sin fallback automático entre plataformas (v1.1)

📞 Referencias
TheaRouter: router-README.md

Callbacks: callbacks-README.md

Core: core-README.md

Última actualización: 2025-11-10 16:50 CET (S38)
Versión: v1.0
Status: Production Ready ✅