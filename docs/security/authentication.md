🔐 Autenticación — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-08 18:35 CET (Sesión 37)
Responsable: Security Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Implementación de autenticación OAuth2 + JWT para THEA IA.

Audiencia:

Backend developers

DevOps engineers

Security auditors

🔐 OAuth2 + JWT Flow
text
┌─────────────────┐
│ Client (Web)    │
└────────┬────────┘
         │ Login request
         ▼
┌──────────────────────────┐
│ OAuth2 Authorization     │
│ Endpoint                 │
└────────┬─────────────────┘
         │ Authorization code
         ▼
┌──────────────────────────┐
│ Token Exchange           │
│ (code → JWT + refresh)   │
└────────┬─────────────────┘
         │ JWT token
         ▼
┌──────────────────────────┐
│ API Calls                │
│ Authorization: Bearer {} │
└──────────────────────────┘
🔑 JWT Structure (RS256)
json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-1"
  },
  "payload": {
    "sub": "user_123",
    "email": "user@example.com",
    "roles": ["user"],
    "tenant_id": "tenant_456",
    "iat": 1635789600,
    "exp": 1635793200
  },
  "signature": "HMACSHA256(base64UrlEncode(header) + '.' + base64UrlEncode(payload), secret)"
}
⏰ Token Lifecycle
Token	Lifetime	Rotation
Access	15 minutos	N/A
Refresh	7 días	Si expira access
Revocation	Inmediato	Redis blacklist
🔄 Refresh Token Strategy
python
# Cliente obtiene: {access_token, refresh_token}

# Cuando access expira (15 min):
POST /auth/refresh
{refresh_token: "..."}
→ {new_access_token, new_refresh_token}

# Blacklist token antiguo en Redis
BLACKLIST:access_token:old_jwt → TTL 24h
🛡️ Security Headers
text
Authorization: Bearer {jwt}
X-CSRF-Token: {token}
X-Request-ID: {uuid}
📌 Meta-información
Campo	Valor
Archivo	docs/security/authentication.md
Versión	v0.14.0
Última revisión	2025-11-08 18:35 CET (S37)
Responsable	Security Team / CEO
Estado	✅ Activo
Última actualización: 2025-11-08 18:35 CET
Responsable: Álvaro Fernández Mota (CEO THEA IA)