Adapters API — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 21:40 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📌 Descripción
API de adapters de THEA IA. Integración con plataformas externas: Telegram, REST, Slack, Discord, WhatsApp.

🔌 Endpoints Principales
1. Listar Adapters Configurados
text
GET /adapters
Response (200 OK):

json
{
  "adapters": [
    {
      "id": "telegram",
      "name": "Telegram Adapter",
      "status": "active",
      "version": "1.0.0",
      "configured": true
    },
    {
      "id": "rest",
      "name": "REST Adapter",
      "status": "active",
      "version": "1.0.0",
      "configured": true
    },
    {
      "id": "slack",
      "name": "Slack Adapter",
      "status": "active",
      "version": "1.0.0",
      "configured": true
    }
  ],
  "total": 5,
  "active": 3
}
2. Enviar Mensaje
text
POST /adapters/{adapter_id}/message
Ejemplo: Telegram

text
POST /adapters/telegram/message
Request:

json
{
  "user_id": "telegram_123456",
  "chat_id": "123456789",
  "text": "Hola, ¿cómo estás?",
  "message_type": "text"
}
Response (200 OK):

json
{
  "status": "success",
  "adapter_id": "telegram",
  "message_id": "msg_789",
  "sent_at": "2025-11-09T21:40:00Z",
  "user_id": "telegram_123456"
}
3. Webhook Entrante
text
POST /adapters/{adapter_id}/webhook
Ejemplo: Telegram Webhook

text
POST /adapters/telegram/webhook
Request (enviado por Telegram):

json
{
  "update_id": 123456789,
  "message": {
    "message_id": 1,
    "from": {
      "id": 123456,
      "is_bot": false,
      "first_name": "Usuario"
    },
    "chat": {
      "id": 123456,
      "type": "private"
    },
    "date": 1699545600,
    "text": "Agendar reunión mañana"
  }
}
Response (200 OK):

json
{
  "status": "received",
  "update_id": 123456789,
  "processed": true,
  "intent": "schedule",
  "agent_id": "agenda"
}
📋 Adapters Disponibles
ID	Nombre	Estado	Documentación
telegram	Telegram Adapter	✅ Activo	docs/adapters/adapter_telegram.md
rest	REST Adapter	✅ Activo	docs/adapters/adapter-rest.md
slack	Slack Adapter	✅ Activo	docs/adapters/adapter_slack.md
discord	Discord Adapter	✅ Activo	docs/adapters/adapter_discord.md
whatsapp	WhatsApp Adapter	🔄 Próximo	docs/adapters/adapter_whatsapp.md
🔐 Autenticación
bash
Authorization: Bearer {API_TOKEN}
Content-Type: application/json
⚠️ Errores Comunes
Código	Descripción
400	Invalid request payload
404	Adapter not found
500	Adapter processing error
📌 Meta-información
Campo	Valor
Archivo	docs/api/adapters.md
Versión	v0.14.0
Última revisión	2025-11-09 21:40 CET (S37)
Estado	✅ Activo
Última actualización: 2025-11-09 21:40 CET