Agents API — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 21:40 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📌 Descripción
API de agentes especializados de THEA IA. Interacción con agentes de Agenda, Notes, Events, Query, Reminder, Scheduler, Help y Fallback.

🔌 Endpoints Principales
1. Listar Agentes Activos
text
GET /agents
Response (200 OK):

json
{
  "agents": [
    {
      "id": "agenda",
      "name": "Agenda Agent",
      "status": "active",
      "version": "1.0.0"
    },
    {
      "id": "notes",
      "name": "Notes Agent",
      "status": "active",
      "version": "1.0.0"
    },
    {
      "id": "events",
      "name": "Events Agent",
      "status": "active",
      "version": "1.0.0"
    },
    {
      "id": "query",
      "name": "Query Agent",
      "status": "active",
      "version": "1.0.0"
    }
  ],
  "total": 8,
  "active": 8
}
2. Procesar Request en Agente
text
POST /agents/{agent_id}/handle
Ejemplo: Agenda Agent

text
POST /agents/agenda/handle
Request:

json
{
  "intent": "schedule",
  "entities": {
    "date": "2025-11-15",
    "time": "14:00",
    "description": "Reunión proyecto"
  },
  "context": {
    "user_id": "user_123",
    "session_id": "sess_456"
  }
}
Response (200 OK):

json
{
  "status": "success",
  "agent_id": "agenda",
  "result": {
    "appointment_id": "apt_789",
    "scheduled_date": "2025-11-15",
    "scheduled_time": "14:00",
    "description": "Reunión proyecto"
  },
  "message": "Reunión agendada correctamente"
}
3. Establecer Contexto
text
POST /agents/{agent_id}/context
Request:

json
{
  "user_id": "user_123",
  "session_data": {
    "language": "es",
    "timezone": "Europe/Madrid",
    "preferences": {
      "notification": true,
      "reminder_minutes": 15
    }
  }
}
Response (200 OK):

json
{
  "status": "success",
  "context_id": "ctx_123",
  "message": "Contexto establecido"
}
📋 Agentes Disponibles
ID	Nombre	Propósito	Documentación
agenda	Agenda Agent	Gestionar agenda	docs/agents/agent_agenda.md
notes	Notes Agent	Gestionar notas	docs/agents/agent_note.md
events	Events Agent	Gestionar eventos	docs/agents/agent_event.md
query	Query Agent	Responder preguntas	docs/agents/agent_query.md
reminder	Reminder Agent	Recordatorios	docs/agents/agent_reminder.md
scheduler	Scheduler Agent	Planificar	docs/agents/agent_scheduler.md
help	Help Agent	Ayuda	docs/agents/agent_help.md
fallback	Fallback Agent	Manejo errores	docs/agents/agent-fallback.md
🔐 Autenticación
bash
Authorization: Bearer {API_TOKEN}
Content-Type: application/json
⚠️ Errores Comunes
Código	Descripción
400	Invalid request payload
404	Agent not found
500	Agent processing error
📌 Meta-información
Campo	Valor
Archivo	docs/api/agents.md
Versión	v0.14.0
Última revisión	2025-11-09 21:40 CET (S37)
Estado	✅ Activo
Última actualización: 2025-11-09 21:40 CET