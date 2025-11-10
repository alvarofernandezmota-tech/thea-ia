API Reference
Documentación completa de la API de THEA IA.

Módulos principales
api_core.md - Core API (FSM, Router, Managers)

api_agents.md - Agents API (todos los agentes disponibles)

api_adapters.md - Adapters API (Telegram, Slack, REST, etc.)

api_index.md - Índice general de la API

Estructura
Core API
Funcionalidades principales del núcleo de THEA IA:

CoreRouter

FSM Engine

Intent Detector

Entity Extractor

Context Manager

Agents API
Agentes especializados para tareas específicas:

AgentScheduler (agendar eventos)

AgentQuery (búsquedas)

AgentNote (notas)

AgentAgenda (agenda)

AgentEvent (eventos)

AgentReminder (recordatorios)

AgentHelp (ayuda)

AgentFallback (respaldo)

Adapters API
Conectores con plataformas externas:

TelegramAdapter

SlackAdapter

DiscordAdapter

WhatsAppAdapter

RESTAdapter

Uso rápido
python
from src.theaia.core.router import CoreRouter
from src.theaia.adapters.telegram import TelegramAdapter

# Inicializar core
router = CoreRouter()

# Procesar mensaje
result = router.handle("user123", "crear nota importante", {})

# Enviar respuesta vía Telegram
adapter = TelegramAdapter(token="TOKEN")
adapter.send_message(result['response'])
Versión
Versión actual: v0.14.0
Última actualización: 2025-11-10 CET

Documentación completa
Para ver la documentación detallada de cada módulo, consulta los archivos individuales:

api_core.md

api_agents.md

api_adapters.md

Contacto
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Última actualización: 2025-11-10 13:59 CET