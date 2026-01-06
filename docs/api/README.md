📝 README 3/7: /docs/api/README.md
Ejecuta:
powershell
notepad docs/api/README.md
Copia y pega ESTE contenido:
text
# 🌐 API Documentation

**Propósito:** Documentación de la API REST de THEA IA.

**Última actualización:** 06 Enero 2026

---

## 📋 ¿Qué es la API?

La API REST permite integrar THEA IA con aplicaciones externas mediante HTTP/JSON:
- **Endpoints RESTful** - CRUD operations
- **Authentication** - OAuth2/JWT (H08)
- **Webhooks** - Event notifications
- **OpenAPI Spec** - Swagger documentation

---

## 📁 Estructura

api/
├── endpoints/ # Documentación de endpoints
├── schemas/ # Pydantic schemas
├── examples/ # Ejemplos de uso
├── openapi.yaml # OpenAPI specification
└── README.md # Este archivo

text

---

## 🔗 Endpoints Principales

### Conversaciones
- `POST /api/v1/conversations` - Crear conversación
- `GET /api/v1/conversations/{id}` - Obtener conversación
- `PUT /api/v1/conversations/{id}` - Actualizar conversación
- `DELETE /api/v1/conversations/{id}` - Eliminar conversación

### Mensajes
- `POST /api/v1/messages` - Enviar mensaje
- `GET /api/v1/messages/{id}` - Obtener mensaje
- `GET /api/v1/conversations/{id}/messages` - Listar mensajes

### Usuarios
- `POST /api/v1/users` - Crear usuario
- `GET /api/v1/users/{id}` - Obtener usuario
- `PUT /api/v1/users/{id}` - Actualizar usuario

---

## 🔒 Autenticación

**Estado actual:** API Key (temporal)  
**Roadmap:** OAuth2 + JWT (H08, Q1 2026)

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
  https://api.theaia.com/v1/conversations
📚 Ejemplos de Uso
Python
python
import requests

response = requests.post(
    "https://api.theaia.com/v1/conversations",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
    json={"user_id": "user_123", "tenant_id": "tenant_1"}
)
cURL
bash
curl -X POST https://api.theaia.com/v1/conversations \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"user_id": "user_123", "tenant_id": "tenant_1"}'
🎯 Audiencia
Frontend Developers - Integrar UI con backend

Mobile Developers - Apps iOS/Android

Third-party Integrators - Sistemas externos

📚 Referencias
OpenAPI Specification

Authentication Guide

API Examples

Contacto: alvarofernandezmota@gmail.com