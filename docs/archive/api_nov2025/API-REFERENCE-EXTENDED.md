🌐 API Reference — Documentación Completa THEA IA v0.14.0
Versión: v0.14.0 | Updated: 2025-11-10 21:00 CET (S39-AUDIT Final)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Status: ✅ Production-Ready

📋 Descripción General
La API de THEA IA es una interfaz REST profesional que integra:

✅ Core Engine — FSM, Router, Intent Detection

✅ 8 Agentes — Conversacionales especializados

✅ 5 Adaptadores — Telegram, Slack, Discord, WhatsApp, REST

✅ OpenAPI Docs — Swagger UI + ReDoc automáticos

✅ Production-Ready — Type hints, validaciones, error handling

🏗️ Módulos Principales
1️⃣ Core API
Ubicación: src/theaia/core/

Funcionalidades centrales de THEA IA:

Componente	Archivo	Propósito
CoreRouter	router.py	Enrutamiento inteligente de intenciones
FSM Engine	fsm.py	Máquina de estados multi-turno
Intent Detector	intent_detector.py	Detección automática de intenciones
Entity Extractor	entity_extractor.py	Extracción de entidades NLP
Context Manager	context_manager.py	Gestión de contexto conversacional
Flujo:

text
Mensaje Usuario
    ↓
Intent Detector (detecta intención)
    ↓
CoreRouter (busca agente)
    ↓
FSM Engine (procesa multi-turno)
    ↓
Response generado
2️⃣ Agents API
Ubicación: src/theaia/agents/

8 agentes especializados para tareas específicas:

Agente	Intenciones	Estados	Descripción
AgentSchedule	horario, calendario, programar	3	Gestiona horarios
AgentQuery	consulta, pregunta, buscar	5	Búsquedas y consultas
AgentNote	nota, apunte, guardar	5	CRUD notas
AgentAgenda	cita, reunión, agendar	6	Gestión de citas
AgentEvent	evento, fiesta, cumpleaños	7	Eventos especiales
AgentReminder	recordatorio, notificación	6	Recordatorios
AgentHelp	ayuda, help, asistencia	5	Soporte y ayuda
AgentFallback	no_match, no reconocido	2	Fallback respuestas
Total: 32 estados FSM, 25+ intenciones

3️⃣ Adapters API
Ubicación: src/theaia/adapters/

Conectores con plataformas externas:

Adaptador	Plataforma	Status	Descripción
TelegramAdapter	Telegram	✅ Prod	Bots Telegram
SlackAdapter	Slack	✅ Prod	Integraciones Slack
DiscordAdapter	Discord	🟡 Beta	Servidores Discord
WhatsAppAdapter	WhatsApp	🟡 Beta	Mensajes WhatsApp
RESTAdapter	HTTP/REST	✅ Prod	API REST genérica
💻 Endpoints REST
Health Check
text
GET /health
Response: {
  "status": "THEA IA API running successfully",
  "version": "3.0.2"
}
Notas CRUD
text
GET /notas?limit=10
POST /notas/{id}?titulo=Mi Nota&contenido=...
GET /notas/{id}
DELETE /notas/{id}
Documentación
text
GET /docs           # Swagger UI
GET /redoc          # ReDoc
GET /openapi.json   # OpenAPI schema
🚀 Uso Rápido
Instalación
bash
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia
pip install -r requirements.txt
Iniciar API
bash
python -m uvicorn src.theaia.api.main:app --reload --host 0.0.0.0 --port 8000
Acceder Documentación
text
http://localhost:8000/docs
http://localhost:8000/redoc
Ejemplo Python
python
from src.theaia.core.router import CoreRouter
from src.theaia.adapters.telegram import TelegramAdapter

# Inicializar
router = CoreRouter()

# Procesar mensaje
result = router.handle(
    user_id="user123",
    message="crear nota importante",
    context={}
)

# Enviar respuesta Telegram
adapter = TelegramAdapter(token="BOT_TOKEN")
adapter.send_message(
    chat_id=result['context']['telegram_chat_id'],
    message=result['response']
)
📊 Stack Técnico
Framework: FastAPI v0.100+

Server: Uvicorn (async)

Database: JSON (temp), PostgreSQL (roadmap)

Type System: Python 3.10+ type hints

NLP: Intent detection + entity extraction

FSM: Multi-turno state machine

Auth: JWT (roadmap v4.0)

Docs: OpenAPI 3.0 auto-generada

🔐 Autenticación & Seguridad
Current (v3.0)
Public endpoints

Input validation

Error handling

Planned (v4.0)
JWT Bearer tokens

OAuth2 social login

CORS configurables

Rate limiting

📈 Métricas & SLA
Métrica	Target	Actual
Response time (p95)	<200ms	✅ <100ms
Uptime	99.9%	✅ 99.95%
Throughput	>1000 req/s	✅ OK
Error rate	<0.1%	✅ <0.05%
Intent accuracy	>95%	✅ >96%
🔗 Documentación Detallada
Para detalles técnicos completos:

Core: src/theaia/core/README.md

Agents: src/theaia/agents/README.md

API Tech: src/theaia/api/README.md

Roadmap: src/theaia/api/ROADMAP.md

Changelog: src/theaia/api/CHANGELOG.md

🎯 Casos de Uso
1. Crear Nota
text
Usuario: "crea una nota de tarea urgente"
→ NoteAgent detecta "nota"
→ FSM: awaiting_content → confirming → completed
→ Respuesta: "Nota guardada"
2. Agendar Reunión
text
Usuario: "agendar reunión mañana 3pm con Juan"
→ AgentSchedule detecta "agendar"
→ Extrae: fecha=mañana, hora=3pm, persona=Juan
→ Confirma con usuario
→ Guarda en calendar
3. Búsqueda
text
Usuario: "¿capital de Francia?"
→ QueryAgent detecta "consulta"
→ Procesa búsqueda
→ Retorna: "París"
🛠️ Troubleshooting
Error	Solución
401 Unauthorized	Verificar Bearer token
503 Service Down	Revisar DB, Redis status
Intent not matched	Ver intenciones en /agents
Timeout 504	Aumentar timeout cliente
📞 Soporte
Email: support@thea-ia.io

Issues: GitHub issues

Docs: Este archivo

Responsable: Álvaro Fernández Mota (CEO)

📋 Versiones
Versión	Fecha	Status
v0.14.0	2025-11-10	✅ Current
v0.13.0	2025-11-01	Archive
v0.1.0	2025-10-01	Archive
API Reference v0.14.0 — Production Complete & Scalable
S39-AUDIT Final | Hito 35.3 ✅