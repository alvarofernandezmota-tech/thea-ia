# 🛡️ Controles de Seguridad — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:29 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 🔐 Autenticación

### OAuth2 Provider (H02+)

Integración OAuth2
from fastapi_oauth2 import OAuth2PasswordBearer, get_password_hash, verify_password
from datetime import timedelta, datetime
import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

Crear token
def create_access_token(data: dict, expires_delta: timedelta = None):
to_encode = data.copy()
if expires_delta:
expire = datetime.utcnow() + expires_delta
else:
expire = datetime.utcnow() + timedelta(hours=1)

text
to_encode.update({"exp": expire})
encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
return encoded_jwt
Endpoint login
@app.post("/auth/login")
async def login(email: str, password: str):
user = await get_user(email)
if not user or not verify_password(password, user.password_hash):
raise HTTPException(status_code=401, detail="Invalid credentials")

text
access_token = create_access_token({"sub": user.id})
refresh_token = create_access_token({"sub": user.id, "type": "refresh"}, timedelta(days=14))

return {
    "access_token": access_token,
    "refresh_token": refresh_token,
    "token_type": "bearer"
}
Dependency: obtener usuario actual
async def get_current_user(token: str = Depends(oauth2_scheme)):
try:
payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
user_id: str = payload.get("sub")
if user_id is None:
raise HTTPException(status_code=401, detail="Invalid token")
except jwt.InvalidTokenError:
raise HTTPException(status_code=401, detail="Invalid token")

text
user = await get_user(user_id)
if user is None:
    raise HTTPException(status_code=404, detail="User not found")
return user
text

### JWT Token Structure

{
"sub": "user_123",
"email": "user@example.com",
"roles": ["user", "developer"],
"tenant_id": "tenant_456",
"iat": 1635789600,
"exp": 1635793200
}

text

### Refresh Token Rotation

@app.post("/auth/refresh")
async def refresh_token(refresh_token: str):
try:
payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
if payload.get("type") != "refresh":
raise HTTPException(status_code=401, detail="Invalid token type")

text
    user_id = payload.get("sub")
    # Invalidar refresh token anterior (agregar a blacklist)
    await add_to_blacklist(refresh_token)
    
    # Crear nuevo access token
    new_access_token = create_access_token({"sub": user_id})
    new_refresh_token = create_access_token(
        {"sub": user_id, "type": "refresh"}, 
        timedelta(days=14)
    )
    
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token
    }
except jwt.InvalidTokenError:
    raise HTTPException(status_code=401, detail="Invalid token")
text

---

## 🔒 Autorización (RBAC - H08)

### Role definitions

class Role(str, Enum):
ADMIN = "admin" # Acceso total
USER = "user" # Acceso a own resources
DEVELOPER = "developer" # Acceso a dev tools
GUEST = "guest" # Read-only

Usuario con roles
class User(Base):
tablename = "users"

text
id = Column(UUID, primary_key=True)
email = Column(String, unique=True)
roles = Column(ARRAY(String))  # PostgreSQL ARRAY
tenant_id = Column(UUID)  # Multi-tenant
text

### Permission checking

from functools import wraps

def require_role(roles: List[Role]):
async def decorator(func):
async def wrapper(*args, current_user: User = Depends(get_current_user), **kwargs):
if not any(role in current_user.roles for role in roles):
raise HTTPException(status_code=403, detail="Insufficient permissions")
return await func(*args, current_user=current_user, **kwargs)
return wrapper
return decorator

Usage
@app.delete("/admin/users/{user_id}")
@require_role([Role.ADMIN])
async def delete_user(user_id: str, current_user: User = Depends(get_current_user)):
# Solo admin puede borrar usuarios
await db.users.delete(user_id)
return {"status": "deleted"}

text

---

## 🛡️ Data Encryption

### At-rest encryption (PostgreSQL)

-- Instalar pgcrypto
CREATE EXTENSION pgcrypto;

-- Crear master key (NEVER commit!)
SELECT set_config('encryption.key', 'your-256-bit-key', false);

-- Tabla con encrypted columns
CREATE TABLE users (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
email TEXT NOT NULL,
password_hash TEXT NOT NULL,

text
-- Encrypted sensitive data
ssn BYTEA,  -- Social Security Number
phone BYTEA,

created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Encrypt on insert
INSERT INTO users (email, password_hash, ssn, phone) VALUES (
'user@example.com',
crypt('password123', gen_salt('bf')),
pgp_sym_encrypt('123-45-6789', current_setting('encryption.key')),
pgp_sym_encrypt('+34-666-777-888', current_setting('encryption.key'))
);

-- Decrypt on select
SELECT
email,
pgp_sym_decrypt(ssn::bytea, current_setting('encryption.key')) as ssn,
pgp_sym_decrypt(phone::bytea, current_setting('encryption.key')) as phone
FROM users;

text

### In-transit encryption (TLS 1.3)

FastAPI with HTTPS
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain("cert.pem", keyfile="key.pem")

Docker/K8s: Ingress handles TLS
Kubernetes Ingress
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
name: thea-ia-ingress
spec:
tls:

hosts:

thea-ia.example.com
secretName: thea-ia-tls # K8s secret with cert
rules:

host: thea-ia.example.com
http:
paths:

path: /
pathType: Prefix
backend:
service:
name: thea-ia-service
port:
number: 8000

text

---

## 🔐 Input Validation

### Pydantic models

from pydantic import BaseModel, EmailStr, Field, validator

class UserCreate(BaseModel):
email: EmailStr # Validates email format
name: str = Field(..., min_length=1, max_length=100)
password: str = Field(..., min_length=8)

text
@validator('password')
def password_strong(cls, v):
    if not any(c.isupper() for c in v):
        raise ValueError('Password must contain uppercase')
    if not any(c.isdigit() for c in v):
        raise ValueError('Password must contain digit')
    return v
class AgendaCreate(BaseModel):
title: str = Field(..., max_length=200)
start_time: datetime
end_time: datetime

text
@validator('end_time')
def end_after_start(cls, v, values):
    if 'start_time' in values and v <= values['start_time']:
        raise ValueError('end_time must be after start_time')
    return v
text

---

## 🔑 Rate Limiting

### FastAPI + Slowapi

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

Rate limit by IP
@app.post("/chat/{user_id}")
@limiter.limit("100/minute")
async def send_message(user_id: str):
# Max 100 requests per minute per IP
pass

Rate limit by user
@app.post("/auth/login")
@limiter.limit("5/minute")
async def login(email: str, password: str):
# Max 5 login attempts per minute
pass

text

---

## 🛡️ CSRF Protection

### CSRF tokens en formularios

from fastapi_csrf_protect import CsrfProtect

@app.post("/users/update")
async def update_user(user_data: dict, csrf_token: str = Header(...)):
# Validar CSRF token
if not verify_csrf_token(csrf_token):
raise HTTPException(status_code=403, detail="CSRF validation failed")

text
# Actualizar usuario
pass
text

---

## 📋 Controles por layer

| Layer | Control | Implementación |
|-------|---------|---|
| Network | TLS 1.3 | K8s Ingress + cert |
| Auth | OAuth2 + JWT | FastAPI dependency |
| Authorization | RBAC | Role-based decorator |
| Data | AES-256 | pgcrypto PostgreSQL |
| Input | Pydantic validation | @validator |
| Rate limiting | 100 req/min | slowapi |
| CSRF | Token validation | Header checking |
| Audit | Logging centralizado | Loki (H11) |

---

## 📖 Documentación relacionada

- [Security Overview](./overview.md) — Principios
- [Audit Policy](./audit.md) — Trazabilidad
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Última actualización:** 2025-10-31 03:29 CET