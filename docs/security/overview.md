# 🔐 Seguridad — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:27 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

**Cumplimiento:**
- ✅ GDPR-ready (datos en EU)
- ✅ SOC 2 Type II (H13)
- ✅ OWASP Top 10 mitigado

---

## 🎯 Principios de seguridad

| Principio | Implementación |
|-----------|-----------------|
| **Confidentiality** | AES-256 encryption at-rest |
| **Integrity** | HMAC validation + checksums |
| **Availability** | 99.5% SLA + failover |
| **Authenticity** | OAuth2 + JWT tokens |
| **Accountability** | Audit logging en DB + Loki |

---

## 🔒 Layers de seguridad

### 1. Network Layer
┌─────────────────────────────────┐
│ Client (Telegram/Web/API) │
└────────────────┬────────────────┘
│ TLS 1.3
▼
┌─────────────────────────────────┐
│ WAF (Cloudflare/AWS Shield) │ ← Rate limiting, DDoS protection
└────────────────┬────────────────┘
│
▼
┌─────────────────────────────────┐
│ Load Balancer (K8s Ingress) │ ← SSL termination
└────────────────┬────────────────┘
│
▼
┌─────────────────────────────────┐
│ THEA IA App (TLS internal) │
└─────────────────────────────────┘

text

### 2. Authentication Layer (H02+)
- **OAuth2 provider** (Google, GitHub, custom)
- **JWT tokens** (RS256 signing)
- **Refresh tokens** (14 days, rotated)
- **MFA** (optional, H13)

JWT Structure
{
"sub": "user_123",
"email": "user@example.com",
"roles": ["user"],
"tenant_id": "tenant_456",
"iat": 1635789600,
"exp": 1635793200
}

text

### 3. Authorization Layer (H08)
- **RBAC** (Role-Based Access Control)
- **Tenant isolation** (row-level security)
- **Resource-level permissions**

Roles
admin: acceso total

user: acceso a own resources

guest: read-only

Tenant isolation
SELECT * FROM agenda WHERE user_id = current_user AND tenant_id = current_tenant

text

### 4. Data Layer
- **At-rest encryption:** AES-256 (PostgreSQL pgcrypto)
- **In-transit encryption:** TLS 1.3
- **Key rotation:** annual (H13)

-- Encrypted columns
CREATE TABLE users (
id UUID PRIMARY KEY,
email TEXT NOT NULL,
password_hash VARCHAR(255) NOT NULL, -- Hashed, never plain
sensitive_data BYTEA, -- Encrypted with pgcrypto
created_at TIMESTAMPTZ
);

text

### 5. Application Layer
- **Input validation** (SQLAlchemy ORM previene SQL injection)
- **Output encoding** (XSS prevention)
- **CSRF tokens** en formularios
- **Rate limiting** (100 req/min por IP)

Input validation
from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
email: EmailStr # Validated email
name: str = Field(..., min_length=1, max_length=100)

text

### 6. Audit Layer
- **Audit trail** en tabla `Audit`
- **Logging centralizado** (Loki)
- **Tracing distribuido** (Jaeger)

-- Audit table
CREATE TABLE audit (
id UUID PRIMARY KEY,
user_id UUID NOT NULL,
action VARCHAR(50), -- CREATE, READ, UPDATE, DELETE
resource_type VARCHAR(50),
resource_id UUID,
changes JSONB,
timestamp TIMESTAMPTZ,
ip_address INET
);

text

---

## 🚨 Vulnerabilidades conocidas mitigadas

| OWASP Top 10 | Vulnerabilidad | Mitigación |
|---|---|---|
| A01 | Broken Access Control | RBAC + tenant isolation |
| A02 | Cryptographic Failures | AES-256 + TLS 1.3 |
| A03 | Injection | ORM (SQLAlchemy) + parameterized queries |
| A04 | Insecure Design | Security by design (H01+) |
| A05 | Security Misconfiguration | IaC (terraform/Helm) |
| A06 | Vulnerable Components | Dependabot + regular updates |
| A07 | Auth Failures | OAuth2 + JWT + MFA (H13) |
| A08 | Data Integrity Failures | Checksums + pgcrypto |
| A09 | Logging/Monitoring | Loki + Prometheus (H11) |
| A10 | SSRF | Input validation + firewall rules |

---

## 🔑 Key Management

### Master key storage
NEVER commit keys to git!

Options:

AWS Secrets Manager (production)

HashiCorp Vault (H13)

K8s Secrets (development)

text

### Key rotation strategy
JWT signing key: rotated annually (H13)

Database encryption key: rotated annually

API keys: rotated quarterly

Telegram bot token: if compromised

text

---

## 🛡️ Incident response

### Step 1: Detect
- Alerts en Prometheus (H11)
- Anomaly detection (H13)

### Step 2: Contain
- Revoke affected tokens
- Isolate compromised resources
- Rotate keys

### Step 3: Eradicate
- Patch vulnerabilities
- Update dependencies
- Security audit

### Step 4: Recover
- Restore from backup
- Test systems
- Re-enable access

### Step 5: Learn
- Post-mortem
- Update runbooks
- Training

---

## 📋 Security Checklist

- [ ] TLS certificado válido (renew antes de 30 días)
- [ ] Secrets en K8s, no en .env
- [ ] Audit logging activo
- [ ] Backups encriptadas
- [ ] MFA habilitado (admin)
- [ ] Dependencias actualizadas (Dependabot)
- [ ] Tests de seguridad en CI/CD
- [ ] WAF rules actualizadas

---

## 📖 Documentación relacionada

- [Security Controls](./controls.md) — Implementación técnica
- [Audit Policy](./audit.md) — Trazabilidad
- [H13 - Security Hardening](../roadmap/milestones/H03_17.md)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Última actualización:** 2025-10-31 03:27 CET