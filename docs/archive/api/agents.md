# 🤖 API — Agents Module

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:39 CET  
**Agents:** Agenda, Notes, Events, Query, Fallback

---

## 🗓️ Agenda Agent

### POST /agents/agenda/create

Crear evento en agenda.

curl -X POST http://localhost:8000/agents/agenda/create
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"title": "Reunión cliente",
"start_time": "2025-11-05T10:00:00Z",
"end_time": "2025-11-05T11:00:00Z",
"participants": ["client@example.com"],
"location": "Zoom"
}'

text

**Response (201)**

{
"id": "agenda_123",
"title": "Reunión cliente",
"start_time": "2025-11-05T10:00:00Z",
"end_time": "2025-11-05T11:00:00Z",
"status": "scheduled",
"created_at": "2025-10-31T03:39:00Z"
}

text

### GET /agents/agenda

Listar eventos.

curl -X GET "http://localhost:8000/agents/agenda?start_date=2025-11-01&end_date=2025-11-30"
-H "Authorization: Bearer <token>"

text

**Response (200)**

{
"events": [
{
"id": "agenda_123",
"title": "Reunión cliente",
"start_time": "2025-11-05T10:00:00Z",
"end_time": "2025-11-05T11:00:00Z"
},
{
"id": "agenda_124",
"title": "Standup",
"start_time": "2025-11-05T09:00:00Z",
"end_time": "2025-11-05T09:30:00Z"
}
],
"total": 2
}

text

### DELETE /agents/agenda/{event_id}

Cancelar evento.

curl -X DELETE http://localhost:8000/agents/agenda/agenda_123
-H "Authorization: Bearer <token>"

text

**Response (200)**

{
"status": "cancelled",
"id": "agenda_123"
}

text

---

## 📝 Notes Agent

### POST /agents/notes/create

Crear nota.

curl -X POST http://localhost:8000/agents/notes/create
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"title": "Puntos de reunión",
"content": "1. Discutir presupuesto\n2. Revisar timeline",
"tags": ["importante", "cliente"]
}'

text

**Response (201)**

{
"id": "note_456",
"title": "Puntos de reunión",
"content": "1. Discutir presupuesto\n2. Revisar timeline",
"tags": ["importante", "cliente"],
"created_at": "2025-10-31T03:39:00Z"
}

text

### GET /agents/notes

Listar notas.

curl -X GET "http://localhost:8000/agents/notes?tag=importante"
-H "Authorization: Bearer <token>"

text

**Response (200)**

{
"notes": [
{
"id": "note_456",
"title": "Puntos de reunión",
"tags": ["importante", "cliente"],
"updated_at": "2025-10-31T03:39:00Z"
}
],
"total": 1
}

text

### PUT /agents/notes/{note_id}

Actualizar nota.

curl -X PUT http://localhost:8000/agents/notes/note_456
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"content": "1. Discutir presupuesto (URGENTE)\n2. Revisar timeline\n3. Enviar propuesta"
}'

text

**Response (200)**

{
"id": "note_456",
"content": "1. Discutir presupuesto (URGENTE)\n2. Revisar timeline\n3. Enviar propuesta",
"updated_at": "2025-10-31T03:39:30Z"
}

text

---

## 📅 Events Agent

### POST /agents/events/create

Crear evento (cumpleaños, aniversario, etc).

curl -X POST http://localhost:8000/agents/events/create
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"type": "birthday",
"person_name": "John",
"date": "2025-11-15",
"reminder_days_before": 3
}'

text

**Response (201)**

{
"id": "event_789",
"type": "birthday",
"person_name": "John",
"date": "2025-11-15",
"reminder_days_before": 3
}

text

### GET /agents/events/upcoming

Próximos eventos.

curl -X GET "http://localhost:8000/agents/events/upcoming?days=30"
-H "Authorization: Bearer <token>"

text

**Response (200)**

{
"events": [
{
"id": "event_789",
"type": "birthday",
"person_name": "John",
"date": "2025-11-15",
"days_until": 15
}
],
"total": 1
}

text

---

## 🔍 Query Agent

### POST /agents/query/search

Búsqueda inteligente en contexto.

curl -X POST http://localhost:8000/agents/query/search
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"query": "reuniones con cliente en noviembre"
}'

text

**Response (200)**

{
"results": [
{
"type": "agenda",
"id": "agenda_123",
"title": "Reunión cliente",
"date": "2025-11-05T10:00:00Z"
},
{
"type": "note",
"id": "note_456",
"title": "Puntos de reunión",
"snippet": "...cliente en noviembre..."
}
],
"query_time_ms": 45
}

text

---

## 🆘 Fallback Agent

### POST /agents/fallback/help

Ayuda general (cuando no se entiende intención).

curl -X POST http://localhost:8000/agents/fallback/help
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"user_input": "no entiendo qué hacer",
"context": {}
}'

text

**Response (200)**

{
"suggestion": "¿Necesitas ayuda con tu agenda, notas o eventos?",
"options": [
"Agendar cita",
"Crear nota",
"Recordar cumpleaños"
]
}

text

---

## 📊 Agent Status

### GET /agents/status

Estado de todos los agentes.

curl -X GET http://localhost:8000/agents/status
-H "Authorization: Bearer <token>"

text

**Response (200)**

{
"agents": {
"agenda": {
"status": "active",
"latency_ms": 45,
"last_used": "2025-10-31T03:39:00Z"
},
"notes": {
"status": "active",
"latency_ms": 32,
"last_used": "2025-10-31T03:38:00Z"
},
"events": {
"status": "active",
"latency_ms": 28,
"last_used": "2025-10-31T02:50:00Z"
},
"query": {
"status": "active",
"latency_ms": 67,
"last_used": "2025-10-31T03:25:00Z"
},
"fallback": {
"status": "active",
"latency_ms": 15,
"last_used": "2025-10-31T01:12:00Z"
}
}
}

text

---

## 📖 Documentación relacionada

- [API Core](./core.md) — Endpoints generales
- [API Adapters](./adapters.md) — Telegram, Web
- [H05 - Agentes Verticales](../roadmap/milestones/H03_17.md)

---

**Última actualización:** 2025-10-31 03:39 CET
