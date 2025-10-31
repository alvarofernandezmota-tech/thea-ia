# SECURITY — THEA IA

**Proyecto:** THEA IA  
**Versión:** 2.0 / v0.14.0  
**Actualizado:** 2025-10-31  
**Autor:** Álvaro Fernández Mota (CEO THEA IA)  
**Responsable de Seguridad:** Security Team THEA IA

---

> **IMPORTANTE: CONFIDENCIALIDAD**
>
> - Este documento contiene información sensible sobre seguridad de THEA IA.
> - **NUNCA** subas vulnerabilidades o exploits a issues públicos.
> - **SIEMPRE** reporta via email privado (ver contacto abajo).
> - Violaciones serán tratadas conforme a ley y políticas de confidencialidad.

---

## 🛡️ Filosofía de Seguridad en THEA IA

THEA IA está diseñado desde cero con seguridad y auditoría como pilares:

- **Hito H13:** Seguridad, gestión de secretos y hardening total.
- **Encriptación:** AES-256 para datos sensibles, JWT para autenticación.
- **Auditoría transversal:** Logs de acceso, cambios y eventos críticos.
- **Compliance:** GDPR, ISO 27001 ready (roadmap futuro).
- **Transparencia:** Todos los cambios de seguridad documentados en CHANGELOG.

---

## 🔐 Política de reporte de vulnerabilidades

### Proceso (RESPONSABILIDAD CRÍTICA)

**NO hagas:**
- ❌ Publicar vulnerabilidades en issues públicos
- ❌ Compartir exploits en Slack/Discord/redes sociales
- ❌ Intentar explotar la vulnerabilidad en producción
- ❌ Revelar información a terceros sin autorización

**SÍ haz:**
- ✅ Reporta **via email privado** inmediatamente
- ✅ Incluye descripción clara, pasos de reproducción, impacto
- ✅ Espera respuesta en **máximo 48 horas**
- ✅ Colabora con el equipo de seguridad en el fix
- ✅ Respeta embargo de 90 días antes de divulgar públicamente

### Contacto de seguridad

**Email:** security@theaia.com (cifrado obligatorio si es posible)  
**Respuesta SLA:** 48 horas máximo  
**Equipo:** Álvaro Fernández Mota (CEO), Security Lead  

**PGP Key (si aplica):**
gpg --recv-keys [security@theaia.com-key-id]

text

---

## 🔑 Gestión de secretos y credenciales

### Reglas estrictas:

1. **NUNCA** hardcodees secretos en código
2. **SIEMPRE** usa `.env` (protegido en `.gitignore`)
3. `.env.example` puede tener valores dummy
4. En producción: usar AWS Secrets Manager, Azure KeyVault, etc.

### Variables sensibles en `.env`:

SECRET_KEY=your_secret_key_here_change_in_production
JWT_SECRET=your_jwt_secret_key_here
DATABASE_PASSWORD=thea_password
ENCRYPTION_KEY=your_encryption_key_here_32_chars_minimum
TELEGRAM_BOT_TOKEN=your_bot_token_here
REDIS_PASSWORD=

text

### Rotación de secretos:

- **Cada 90 días:** Rotar SECRET_KEY, JWT_SECRET
- **Cada 180 días:** Rotar DATABASE_PASSWORD
- **Inmediatamente:** Si hay leak o compromiso detectado
- **Log:** Registrar rotación en audit.log con timestamp y responsable

---

## 🔒 Autenticación y autorización (H13)

### JWT (JSON Web Tokens)

Algoritmo: HS256
Expire: 24 horas (configurar en .env)
Refresh: 7 días máximo

text

**Implementación:**
tokens.py
import jwt
from datetime import datetime, timedelta

def create_token(user_id, role, expires_in=24):
payload = {
"user_id": user_id,
"role": role,
"iat": datetime.utcnow(),
"exp": datetime.utcnow() + timedelta(hours=expires_in)
}
return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)

def verify_token(token):
try:
payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
return payload
except jwt.ExpiredSignatureError:
return None # Token expirado
except jwt.InvalidTokenError:
return None # Token inválido

text

### RBAC (Role-Based Access Control)

Roles soportados:
- **admin**: Acceso total, gestión de usuarios, auditoría
- **user**: Acceso a agentes y adapters
- **auditor**: Acceso solo lectura a logs y auditoría
- **api_client**: Acceso vía API REST con límite de rate

---

## 🔐 Encriptación de datos (H13)

### AES-256 para datos en reposo

from cryptography.fernet import Fernet
import os

ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
cipher = Fernet(ENCRYPTION_KEY)

def encrypt_data(plaintext: str) -> str:
"""Encripta datos sensibles (contexto, credenciales)."""
encrypted = cipher.encrypt(plaintext.encode())
return encrypted.decode()

def decrypt_data(ciphertext: str) -> str:
"""Desencripta datos."""
decrypted = cipher.decrypt(ciphertext.encode())
return decrypted.decode()

text

### HTTPS/TLS en tránsito

- **Producción:** SSL/TLS 1.3 obligatorio
- **Certificados:** Let's Encrypt o CA corporativo
- **HSTS:** Cabecera `Strict-Transport-Security: max-age=31536000`

---

## 🛡️ Protección contra ataques comunes (OWASP Top 10)

### 1. Inyección SQL
✅ BIEN: Usar ORM (SQLAlchemy)
user = session.query(User).filter(User.id == user_id).first()

❌ MAL: Query string concatenado
query = f"SELECT * FROM users WHERE id = {user_id}"

text

### 2. XSS (Cross-Site Scripting)
✅ BIEN: Sanitizar input
from bleach import clean
safe_input = clean(user_input, tags=[], strip=True)

❌ MAL: Renderizar directamente
html = f"<p>{user_input}</p>"

text

### 3. CSRF (Cross-Site Request Forgery)
✅ BIEN: Token CSRF en formularios
<input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
❌ MAL: Sin protección CSRF
text

### 4. Rate Limiting
.env
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS_PER_MINUTE=100
RATE_LIMIT_REQUESTS_PER_HOUR=1000

Implementación con Flask-Limiter
from flask_limiter import Limiter
limiter = Limiter(app, key_func=get_remote_address)
limiter.limit("100 per minute")(my_endpoint)

text

### 5. Validación de input
✅ BIEN: Validar y castear tipos
from pydantic import BaseModel, validator

class MessageInput(BaseModel):
text: str = None
user_id: int = None

text
@validator('text')
def text_not_empty(cls, v):
    if not v or len(v.strip()) == 0:
        raise ValueError('Texto vacío')
    return v.strip()
text

---

## 🚨 Auditoría y logging de seguridad (H13)

### Eventos críticos a loguear

audit.log — Cada evento debe incluir timestamp, user, acción, IP, resultado
import logging
audit_logger = logging.getLogger('audit')

Login exitoso
audit_logger.info(f"LOGIN_SUCCESS - user_id={user_id}, ip={request.remote_addr}, timestamp={datetime.utcnow()}")

Login fallido
audit_logger.warning(f"LOGIN_FAILED - user_id={user_id}, ip={request.remote_addr}, reason=invalid_password")

Cambio de configuración
audit_logger.info(f"CONFIG_CHANGED - user_id={user_id}, key={config_key}, old_value={old}, new_value={new}")

Acceso a datos sensibles
audit_logger.info(f"SENSITIVE_DATA_ACCESS - user_id={user_id}, resource={resource}, permission={permission_level}")

Error crítico
audit_logger.error(f"CRITICAL_ERROR - module={module}, error={error_msg}, severity=CRITICAL")

text

### Retención de logs

- **Logs activos:** 30 días en memoria/DB
- **Archivos:** 90 días en almacenamiento frío
- **Auditoría:** 1 año en backup encriptado
- **Limpieza:** Automática según políticas de retención

---

## 🔒 Vulnerabilidades conocidas y mitigación

### Dependencias y software obsoleto

Auditar dependencias regularmente
pip install -U pip pip-audit
pip-audit # Revisa vulnerabilidades CVE

Usa requirements.txt versionado y pinned
requests==2.28.1 # Específico, no >=2.28
cryptography==41.0.3 # Auditar cada actualización

text

### Scan de seguridad automatizado

Bandit (análisis estático Python)
bandit -r src/theaia/ -f json -o bandit-report.json

Safety (dependencias)
safety check --json

OWASP ZAP (dinámico)
zaproxy-cli quick-scan --self-contained -a https://app.theaia.com

text

---

## 🆘 Incidentes de seguridad

### Procedimiento ante brecha

1. **Detectar** → Logs/alertas/reporte
2. **Aislar** → Desactivar access, detener servicio si es crítico
3. **Investigar** → Root cause analysis (RCA)
4. **Contener** → Parches, cambio de credenciales
5. **Notificar** → CEO, equipo técnico, clientes si aplica (GDPR)
6. **Comunicar** → Status page, email actualización
7. **Post-mortem** → Documentar, prevención futura

### Escalamiento de severidad

| Severidad | Descripción | Tiempo de respuesta | Acción |
|-----------|-------------|-------------------|--------|
| **CRÍTICO** | Leak de datos, acceso no autorizado, downtime | 1 hora | Respuesta inmediata, comunicado público |
| **ALTO** | Vulnerabilidad explotable, riesgo de datos | 4 horas | Patch urgente, comunicado a clientes |
| **MEDIO** | Vulnerabilidad no explotada fácilmente | 24 horas | Plan de parcheo |
| **BAJO** | Información de debug, config no óptima | 7 días | Ticket backlog |

---

## 📋 Checklist de seguridad (Pre-release)

- [ ] No hay secretos hardcodeados en código
- [ ] `.env` está en `.gitignore`
- [ ] Todos los inputs validados (inyección SQL, XSS, etc)
- [ ] JWT/autenticación configurada correctamente
- [ ] Rate limiting activo
- [ ] CORS/CSRF protegido
- [ ] Logs de auditoría activos
- [ ] Dependencias auditadas (pip-audit, safety)
- [ ] Bandit scan sin HIGH/CRITICAL
- [ ] Cambios de seguridad en CHANGELOG.md
- [ ] Aprobado por Security Lead
- [ ] Notificado a compliance/legal si aplica

---

## 🔍 Auditoría externa y compliance

- **Auditoría anual:** Tercero independiente
- **Pentesting:** Semestral para producción
- **GDPR:** Política de privacidad y consentimiento
- **ISO 27001:** Roadmap futuro (H17)

---

## 📧 Contacto

- **Security Lead:** Álvaro Fernández Mota
- **Security Team:** security@theaia.com
- **Emergencia:** [número de crisis 24/7 si aplica]

---

**Seguridad es responsabilidad de todos.  
Contribuye a mantener THEA IA seguro, auditado y transparente.**

> Última actualización: 2025-10-31 · Álvaro Fernández Mota (CEO THEA IA)