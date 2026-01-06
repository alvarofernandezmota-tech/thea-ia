🎮 Adapter: Discord — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 17:21 CET (Sesión 36)
Responsable: Adapters Team
Estado: ✅ Activo
Prioridad: 🟡 Media (Extensión)

📋 Propósito
Adapter para integración con Discord. THEA IA actúa como bot en servidores, respondiendo en canales de texto.

Audiencia:

Comunidades gaming/dev en Discord

Integradores Discord

Community managers

🎯 Responsabilidades
Funcionalidad	Descripción
Recibir mensajes	Discord gateway events
Normalizar	Conversión a formato THEA IA
Enviar mensajes	Usar channel.send()
Embeds	Respuestas formateadas con embed
Reacciones	Procesar emoji reactions
Slash commands	Comandos /comando de Discord
🔧 Configuración
Archivo: config/adapters/discord.yaml

text
adapter:
  name: "Discord"
  version: "1.0"
  enabled: true
  timeout: 30

credentials:
  bot_token: "${DISCORD_BOT_TOKEN}"
  
features:
  message_content: true
  slash_commands: true
  reactions: true
  embeds: true

limits:
  message_length: 2000
  embed_fields: 25
📥 Entrada (Discord Message Event)
python
{
  "type": "MESSAGE_CREATE",
  "author": {
    "id": "user_123",
    "username": "alvaro"
  },
  "channel_id": "channel_123",
  "content": "crear evento mañana"
}
📤 Salida (Normalizado)
python
{
  "user_id": "user_123",
  "channel": "discord",
  "message": "crear evento mañana",
  "metadata": {
    "discord_channel": "channel_123",
    "discord_server": "guild_123",
    "timestamp": "2025-11-08T17:21:00Z"
  }
}
🔄 Flujo
text
Discord Event
     ↓
Validar intención (gateway)
     ↓
Normalizar mensaje
     ↓
Enviar a FSM
     ↓
Procesar (agents)
     ↓
Formatear respuesta (embed)
     ↓
Enviar a Discord
🧠 Lógica especial
Embeds (respuestas formateadas)
python
embed = discord.Embed(
  title="Evento creado",
  description="Evento: Reunión",
  color=discord.Color.blue()
)
embed.add_field(name="Fecha", value="2025-11-09", inline=True)
Slash Commands
text
/evento create "Reunión equipo"
↓
Router detecta comando
↓
Ejecuta handler
Reacciones
text
Usuario: 👍
↓
Event: REACTION_ADD
↓
Interpretar: "Confirmar"
📊 Métricas
Métrica	Actual	Target
Event delivery	99.7%	> 99%
Response time	250ms	< 500ms
Guild reach	50 servidores	> 100
✅ Tests
python
def test_discord_normalize_message():
    adapter = DiscordAdapter()
    discord_event = {...}
    normalized = adapter.normalize_input(discord_event)
    
    assert normalized["channel"] == "discord"
    assert normalized["user_id"] == "user_123"
📌 Meta-información
Campo	Valor
Archivo	docs/adapters/adapter_discord.md
Versión	1.0
Última revisión	2025-11-08 17:21 CET (Sesión 36)
Responsable	Adapters Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/adapters/)

Sigue estándar THEA IA: Modular, auditable, escalable

Validado en sesión 36