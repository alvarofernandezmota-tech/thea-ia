📱 Adapter: Telegram — THEA IA
Versión: 1.0 | Última actualización: 2025-11-08 17:16 CET (Sesión 36) | Prioridad: 🔴 Alta (Core)

📋 Propósito
Adapter para comunicación con usuarios via Telegram Bot. Normaliza mensajes, maneja comandos y notificaciones.

🎯 Responsabilidades
Recibir mensajes de Telegram

Normalizar a formato THEA IA

Enviar respuestas formateadas

Manejar webhooks y polling

Registrar interacciones

🔧 Configuración
text
adapter:
  name: "Telegram"
  version: "1.0"
  enabled: true
  timeout: 30
  
credentials:
  token: "${TELEGRAM_BOT_TOKEN}"
  
features:
  webhooks: true
  polling: false
  markdown: true
  inline_keyboard: true
  
limits:
  max_message_length: 4096
  rate_limit: 30  # msg/sec
📥 Entrada
python
{
  "update_id": 123456,
  "message": {
    "message_id": 789,
    "from": {"id": "user_123", "first_name": "Álvaro"},
    "chat": {"id": "chat_123"},
    "text": "crear evento mañana 10am"
  }
}
📤 Salida (normalizado)
python
{
  "user_id": "user_123",
  "channel": "telegram",
  "message": "crear evento mañana 10am",
  "metadata": {
    "chat_id": "chat_123",
    "message_id": 789,
    "timestamp": "2025-11-08T17:16:00Z"
  }
}
🔄 Flujo
text
Mensaje Telegram
    ↓
Webhook/Polling recibe
    ↓
Normalizar a formato THEA IA
    ↓
Enviar a FSM
    ↓
Procesar (agents)
    ↓
Formatear respuesta (Markdown, botones)
    ↓
Enviar a Telegram
🧠 Lógica especial
Comandos: /start, /help, /stop (handlers especiales)

Inline buttons: Integración con teclado Telegram

Archivo compartido: Webhook vs polling (configurable)

Estado de sesión: User context en Telegram

📊 Métricas
Métrica	Actual	Target
Message throughput	100/min	> 50/min
Response time	200ms	< 500ms
Webhook delivery	99.5%	> 99%
📌 Meta
Archivo: docs/adapters/adapter_telegram.md | ID: | Estado: ✅ Activo