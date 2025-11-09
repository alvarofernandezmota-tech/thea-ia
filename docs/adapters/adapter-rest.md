🌐 Adapter: REST API — THEA IA
Versión: 1.0 | Última actualización: 2025-11-08 17:17 CET (Sesión 36) | Prioridad: 🔴 Alta

📋 Propósito
API REST HTTP para integración externa. Endpoints para recibir/enviar mensajes, webhook remoto.

🎯 Responsabilidades
Endpoints HTTP (/message, /webhook, /health)

Normalizar requests JSON

Autenticación API Key

CORS y validación

Logging de requests

🔧 Configuración
text
adapter:
  name: "REST"
  host: "0.0.0.0"
  port: 8000
  
security:
  api_key_header: "X-API-Key"
  cors_origins: ["*"]
📥 POST /api/message
python
{
  "user_id": "api_user_123",
  "message": "tu mensaje aquí"
}
📤 Response
python
{
  "status": "success",
  "response": "Respuesta del sistema",
  "timestamp": "2025-11-08T17:17:00Z"
}
📊 Métricas
Métrica	Actual	Target
Requests/sec	50	> 100
API response time	150ms	< 200ms
Uptime	99.8%	> 99.5%
📌 Meta
Archivo: docs/adapters/adapter_rest.md | ID: | Estado: ✅ Activo