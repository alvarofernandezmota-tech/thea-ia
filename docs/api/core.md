# 🔌 API — Core Module

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:35 CET  
**Base URL:** `https://api.thea-ia.com/v1` (producción) / `http://localhost:8000` (desarrollo)

---

## 🔐 Autenticación

Todos los endpoints requieren JWT token en header:

Authorization: Bearer <token>

text

Obtener token:
curl -X POST http://localhost:8000/auth/login
-H "Content-Type: application/json"
-d '{"email":"user@example.com","password":"..."}'

text

Respuesta:
{
"access_token": "eyJhbGc...",
"refresh_token": "eyJhbGc...",
"token_type": "bearer",
"expires_in": 3600
}

text

---

## 📨 POST /chat/{user_id}

Procesar mensaje de usuario.

### Request

curl -X POST http://localhost:8000/chat/user_123
-H "Authorization: Bearer <token>"
-H "Content-Type: application/json"
-d '{
"message": "quiero agendar cita el 5 de noviembre",
"context": {}
}'

text

### Response (200 OK)

{
"response": "¿A qué hora te va bien?",
"state": "disambiguation",
"agent": "AgendaAgent",
"context": {
"user_id": "user_123",
"intent": "schedule_appointment",
"entities": {
"date": "2025-11-05",
"time": null
}
}
}

text

### Error (400 Bad Request)

{
"detail": "Message cannot be empty"
}

text

### Error (401 Unauthorized)

{
"detail": "Invalid or expired token"
}

text

---

## 👤 GET /users/{user_id}

Obtener info del usuario.

### Request

curl -X GET http://localhost:8000/users/user_123
-H "Authorization: Bearer <token>"

text

### Response (200)

{
"id": "user_123",
"email": "user@example.com",
"name": "John Doe",
"roles": ["user"],
"tenant_id": "tenant_456",
"created_at": "2025-10-01T12:00:00Z",
"last_login": "2025-10-31T03:35:00Z"
}

text

---

## 📝 POST /users

Crear usuario (solo admin).

### Request

curl -X POST http://localhost:8000/users
-H "Authorization: Bearer <admin_token>"
-H "Content-Type: application/json"
-d '{
"email": "newuser@example.com",
"name": "Jane Doe",
"password": "SecurePass123!",
"roles": ["user"]
}'

text

### Response (201 Created)

{
"id": "user_789",
"email": "newuser@example.com",
"name": "Jane Doe",
"roles": ["user"],
"created_at": "2025-10-31T03:35:00Z"
}

text

---

## 🏥 GET /health

Health check del sistema.

### Request

curl http://localhost:8000/health

text

### Response (200)

{
"status": "healthy",
"version": "v0.14.0",
"db": "connected",
"timestamp": "2025-10-31T03:35:00Z"
}

text

### Response (503 Service Unavailable)

{
"status": "unhealthy",
"db": "disconnected",
"timestamp": "2025-10-31T03:35:00Z"
}

text

---

## 📊 GET /metrics

Prometheus metrics.

curl http://localhost:8000/metrics

text

Output:
HELP thea_chat_duration_seconds Chat processing latency
TYPE thea_chat_duration_seconds histogram
thea_chat_duration_seconds_bucket{le="0.01"} 45
thea_chat_duration_seconds_bucket{le="0.1"} 234
thea_chat_duration_seconds_bucket{le="1.0"} 256

HELP thea_fsm_transitions FSM state transitions
TYPE thea_fsm_transitions counter
thea_fsm_transitions_total{state="processing"} 1000

text

---

## 📖 Documentación relacionada

- [API Agents](./agents.md) — Endpoints específicos de agentes
- [API Adapters](./adapters.md) — Integraciones Telegram, Web
- [Security](../security/overview.md) — Autenticación y autorización
- [Quickstart](../guides/quickstart.md) — Inicio rápido

---

**Última actualización:** 2025-10-31 03:35 CET