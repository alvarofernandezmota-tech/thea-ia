💬 Adapter: Slack — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 17:20 CET (Sesión 36)
Responsable: Adapters Team
Estado: ✅ Activo
Prioridad: 🟡 Media (Extensión)

📋 Propósito
Adapter para integración con Slack. Permite a THEA IA actuar como bot en workspaces, recibiendo mensajes y enviando respuestas.

Audiencia:

Equipos usando Slack

Integradores Slack

DevOps desplegando workspace bot

🎯 Responsabilidades
Funcionalidad	Descripción
Recibir mensajes	Slack events API
Normalizar	Conversión a formato THEA IA
Enviar respuestas	Usar chat.postMessage
Manejar threads	Responder en threads
Reaction handling	Procesar emoji reactions
Slash commands	Comandos /comando
🔧 Configuración
Archivo: config/adapters/slack.yaml

text
adapter:
  name: "Slack"
  version: "1.0"
  enabled: true
  timeout: 30

credentials:
  bot_token: "${SLACK_BOT_TOKEN}"
  signing_secret: "${SLACK_SIGNING_SECRET}"
  
features:
  events_api: true
  slash_commands: true
  reactions: true
  threads: true

workspace:
  channel_default: "#general"
📥 Entrada (Slack Event)
python
{
  "type": "event_callback",
  "event": {
    "type": "message",
    "channel": "C123456",
    "user": "U123456",
    "text": "crear evento mañana",
    "ts": "1234567890.123456"
  }
}
📤 Salida (Normalizado)
python
{
  "user_id": "U123456",
  "channel": "slack",
  "message": "crear evento mañana",
  "metadata": {
    "slack_channel": "C123456",
    "slack_ts": "1234567890.123456",
    "timestamp": "2025-11-08T17:20:00Z"
  }
}
🔄 Flujo
text
Slack Event
     ↓
Validar firma (signing_secret)
     ↓
Normalizar mensaje
     ↓
Enviar a FSM
     ↓
Procesar (agents)
     ↓
Formatear respuesta (bloques Slack)
     ↓
Enviar a Slack
🧠 Lógica especial
Slash Commands
text
/evento crear evento mañana 10am
↓
Router detecta comando
↓
Ejecuta handler específico
Threads
text
Mensaje en thread
↓
Respuesta en mismo thread (reply_broadcast=false)
↓
Mantiene conversación ordenada
Reactions
text
Usuario reacciona con 👍
↓
Event handler trigger
↓
Interpretar como "confirmar"
📊 Métricas
Métrica	Actual	Target
Event delivery	99.8%	> 99%
Response time	300ms	< 500ms
Message parsing	0.95 accuracy	> 0.90
🚨 Errores comunes
Error	Causa	Solución
INVALID_SIGNATURE	Token incorrecto	Verificar SLACK_SIGNING_SECRET
NOT_IN_CHANNEL	Bot no invitado	Invitar bot al canal
RATE_LIMITED	Muchos requests	Backoff exponencial
✅ Tests
python
def test_slack_normalize_message():
    adapter = SlackAdapter()
    slack_event = {...}
    normalized = adapter.normalize_input(slack_event)
    
    assert normalized["channel"] == "slack"
    assert "message" in normalized
📌 Meta-información
Campo	Valor
Archivo	docs/adapters/adapter_slack.md
Versión	1.0
Última revisión	2025-11-08 17:20 CET (Sesión 36)
Responsable	Adapters Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/adapters/)

Sigue estándar THEA IA: Modular, auditable, escalable

Validado en sesión 36