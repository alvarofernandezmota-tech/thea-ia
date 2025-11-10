📚 API Reference — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 21:40 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📌 Visión General
THEA IA expone sus funcionalidades a través de tres capas API principales:

Core API — Procesamiento de intents y entidades

Agents API — Operaciones de agentes especializados

Adapters API — Integraciones con plataformas externas

🔗 APIs Disponibles
Core API
Procesamiento central del sistema, detector de intents y extractor de entidades.

Archivo: core.md

Endpoints principales:

POST /intents/detect — Detectar intención

POST /entities/extract — Extraer entidades

GET /health — Status del sistema

Agents API
Interacción con agentes especializados (Agenda, Notes, Events, Query, etc.).

Archivo: agents.md

Endpoints principales:

POST /agents/{agent_id}/handle — Procesar request

GET /agents — Listar agentes activos

POST /agents/{agent_id}/context — Establecer contexto

Adapters API
Integración con plataformas externas (Telegram, Slack, WhatsApp, etc.).

Archivo: adapters.md

Endpoints principales:

POST /adapters/{adapter_id}/message — Enviar mensaje

GET /adapters — Listar adapters configurados

POST /adapters/{adapter_id}/webhook — Webhook entrante

📖 Documentación Completa
Para documentación detallada sobre arquitectura, agentes y adapters, consulta:

Arquitectura: docs/architecture/

Agentes: docs/agents/

Adapters: docs/adapters/

Testing: docs/testing/

🔐 Autenticación
Todas las APIs requieren:

bash
Authorization: Bearer {API_TOKEN}
Content-Type: application/json
📌 Meta-información
Campo	Valor
Archivo	docs/api/index.md
Versión	v0.14.0
Última revisión	2025-11-09 21:40 CET (S37)
Estado	✅ Activo
Última actualización: 2025-11-09 21:40 CET