Core API — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 21:40 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📌 Descripción
API central de THEA IA. Proporciona procesamiento de intents, extracción de entidades y orquestación del FSM.

🔌 Endpoints Principales
1. Detectar Intención
text
POST /intents/detect
Request:

json
{
  "text": "Necesito agendar una reunión para mañana",
  "language": "es",
  "context": {
    "user_id": "user_123",
    "session_id": "sess_456"
  }
}
Response (200 OK):

json
{
  "intent": "schedule",
  "confidence": 0.95,
  "entities": {
    "date": "2025-11-10",
    "event_type": "meeting"
  }
}
2. Extraer Entidades
text
POST /entities/extract
Request:

json
{
  "text": "Reunión con María el 15 de noviembre a las 10:30",
  "intent": "schedule"
}
Response (200 OK):

json
{
  "entities": [
    {
      "type": "person",
      "value": "María",
      "confidence": 0.98
    },
    {
      "type": "date",
      "value": "2025-11-15",
      "confidence": 0.99
    },
    {
      "type": "time",
      "value": "10:30",
      "confidence": 0.97
    }
  ]
}
3. Health Check
text
GET /health
Response (200 OK):

json
{
  "status": "healthy",
  "version": "0.14.0",
  "uptime_seconds": 3600,
  "models_loaded": true,
  "database_connected": true
}
🔐 Autenticación
bash
Authorization: Bearer {API_TOKEN}
Content-Type: application/json
⚠️ Errores Comunes
Código	Descripción
400	Invalid request payload
401	Unauthorized (missing/invalid token)
500	Internal server error
📌 Meta-información
Campo	Valor
Archivo	docs/api/core.md
Versión	v0.14.0
Última revisión	2025-11-09 21:40 CET (S37)
Estado	✅ Activo
Última actualización: 2025-11-09 21:40 CET