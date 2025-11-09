# 🔌 API — Adapters Module

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:40 CET  
**Adapters:** Telegram (H02), Web Client (H02), WhatsApp (H10)

---

## 💬 Telegram Adapter (H02)

### Webhook Setup

Registrar webhook en Telegram
curl https://api.telegram.org/botTOKEN/setWebhook
-d url=https://your-domain.com/adapters/telegram/webhook
-d allowed_updates=message,callback_query

text

### POST /adapters/telegram/webhook

Endpoint que Telegram llama cuando usuario envía mensaje.

**Request body (desde Telegram):**

{
"update_id": 123456789,
"message": {
"message_id": 1,
"chat": {
"id": "user_123",
"type": "private"
},
"text": "quiero agendar cita",
"from": {
"id": "user_123",
"first_name": "John"
}
}
}

text

**Processing:**

Webhook handler
@app.post("/adapters/telegram/webhook")
async def telegram_webhook(update: dict):
user_id = update['message']['chat']['id']
message = update['message']['text']

text
# Procesar con CoreRouter
response = await core_router.handle(user_id, message)

# Enviar respuesta a Telegram
await telegram_client.send_message(
    chat_id=user_id,
    text=response['response']
)
text

### Send message to Telegram

from telegram import Bot

bot = Bot(token="YOUR_BOT_TOKEN")

await bot.send_message(
chat_id="user_123",
text="¿A qué hora te va bien la cita?"
)

text

---

## 🌐 Web Client (H02)

### WebSocket Connection

// Conectar WebSocket
const ws = new WebSocket('ws://localhost:8000/ws/user_123');

ws.onopen = () => {
console.log('Connected');
ws.send(JSON.stringify({
type: 'message',
data: 'quiero agendar cita'
}));
};

ws.onmessage = (event) => {
const response = JSON.parse(event.data);
console.log('Response:', response.data);
};

ws.onerror = (error) => {
console.error('Error:', error);
};

text

### Backend WebSocket handler

from fastapi import WebSocket

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
await websocket.accept()

text
try:
    while True:
        # Recibir mensaje del cliente
        data = await websocket.receive_json()
        
        if data['type'] == 'message':
            # Procesar con CoreRouter
            response = await core_router.handle(user_id, data['data'])
            
            # Enviar respuesta
            await websocket.send_json({
                'type': 'response',
                'data': response['response'],
                'state': response['state']
            })
except ConnectionClosed:
    print(f"User {user_id} disconnected")
text

### HTTP endpoints (Web)

POST mensaje
curl -X POST http://localhost:8000/web/chat/user_123
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{"message":"quiero agendar cita"}'

GET historial
curl -X GET http://localhost:8000/web/history/user_123
-H "Authorization: Bearer <token>"

text

---

## 📱 WhatsApp Adapter (H10 - Future)

### Webhook Setup

Registrar con Meta/WhatsApp
curl https://graph.instagram.com/v18.0/PHONE_ID/subscribed_apps
-X POST
-H "Authorization: Bearer $ACCESS_TOKEN"

text

### POST /adapters/whatsapp/webhook

@app.post("/adapters/whatsapp/webhook")
async def whatsapp_webhook(update: dict):
# Estructura similar a Telegram
message = update['messages']
user_id = message['from']
text = message['text']['body']

text
# Procesar
response = await core_router.handle(user_id, text)

# Enviar a WhatsApp
await whatsapp_client.send_message(
    to=user_id,
    text=response['response']
)
text

---

## 🔐 Authentication por adapter

### Telegram
- No requiere auth (Telegram maneja bot token)
- Webhook validación: CHECK secret token

@app.post("/adapters/telegram/webhook")
async def telegram_webhook(update: dict, x_telegram_bot_api_secret_token: str = Header(None)):
if x_telegram_bot_api_secret_token != TELEGRAM_SECRET:
raise HTTPException(status_code=403, detail="Invalid token")
# ...

text

### Web Client
- JWT token en header
- WebSocket: token en URL query

const token = localStorage.getItem('access_token');
const ws = new WebSocket(ws://localhost:8000/ws/user_123?token=${token});

text

### WhatsApp
- Meta webhook verify token
- Signature validation

@app.get("/adapters/whatsapp/webhook")
async def whatsapp_webhook_verify(
hub_mode: str = Query(...),
hub_challenge: str = Query(...),
hub_verify_token: str = Query(...)
):
if hub_verify_token != WHATSAPP_VERIFY_TOKEN:
raise HTTPException(status_code=403)
return hub_challenge

text

---

## 📊 Adapter Status

### GET /adapters/status

curl -X GET http://localhost:8000/adapters/status
-H "Authorization: Bearer <token>"

text

**Response:**

{
"adapters": {
"telegram": {
"status": "connected",
"webhook_url": "https://your-domain.com/adapters/telegram/webhook",
"last_message": "2025-10-31T03:40:00Z",
"messages_today": 156
},
"web": {
"status": "connected",
"active_sessions": 23,
"messages_today": 1245
},
"whatsapp": {
"status": "pending",
"webhook_url": null,
"messages_today": 0
}
}
}

text

---

## 🔄 Adapter Message Flow

┌─────────────────┐
│ Telegram User │
└────────┬────────┘
│ /message
▼
┌──────────────────────────────────────┐
│ POST /adapters/telegram/webhook │
│ (Telegram sends update) │
└────────┬─────────────────────────────┘
│ extract: user_id, message
▼
┌──────────────────────────────────────┐
│ CoreRouter.handle(user_id, message) │
│ (FSM, Intent, Agent) │
└────────┬─────────────────────────────┘
│ response
▼
┌──────────────────────────────────────┐
│ Telegram Bot API │
│ send_message(chat_id, text) │
└────────┬─────────────────────────────┘
│
▼
┌─────────────────┐
│ Telegram User │ ✅ Response received
└─────────────────┘

text

---

## 💬 Message Format Normalization

Cada adapter normaliza mensajes a formato estándar:

Telegram → Standard
{
"adapter": "telegram",
"user_id": "user_123",
"message": "quiero agendar cita",
"timestamp": "2025-10-31T03:40:00Z",
"metadata": {
"chat_id": "...",
"message_id": "...",
"name": "John"
}
}

Web → Standard
{
"adapter": "web",
"user_id": "user_123",
"message": "quiero agendar cita",
"timestamp": "2025-10-31T03:40:00Z",
"metadata": {
"ip": "192.168.1.100",
"browser": "Chrome"
}
}

text

---

## 📖 Documentación relacionada

- [API Core](./core.md) — Endpoints generales
- [API Agents](./agents.md) — Endpoints de agentes
- [H02 - Telegram & Web](../roadmap/milestones/H03_17.md)
- [H10 - WhatsApp & REST](../roadmap/milestones/H03_17.md)

---

**Última actualización:** 2025-10-31 03:40 CET