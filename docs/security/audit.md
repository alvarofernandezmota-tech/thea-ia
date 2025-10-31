# 📊 Auditoría Viva — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:31 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 🎯 Propósito

Trazabilidad completa de acciones en THEA IA para cumplimiento regulatorio (GDPR, SOC 2) y debugging de incidentes.

---

## 📋 Tabla Audit

CREATE TABLE audit (
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

text
-- Who
user_id UUID NOT NULL,
email TEXT,
ip_address INET,
user_agent TEXT,

-- What
action VARCHAR(50) NOT NULL,  -- CREATE, READ, UPDATE, DELETE, LOGIN, EXECUTE
resource_type VARCHAR(50),     -- user, agenda, event, note, session
resource_id UUID,

-- Details
changes JSONB,  -- Before/after comparison
result VARCHAR(20),  -- SUCCESS, FAILURE, ERROR
error_message TEXT,

-- When
timestamp TIMESTAMPTZ NOT NULL DEFAULT NOW(),

-- Context
tenant_id UUID,
session_id UUID,

-- Compliance
indexed: BOOL DEFAULT TRUE
);

-- Índices
CREATE INDEX idx_audit_user_id ON audit(user_id);
CREATE INDEX idx_audit_timestamp ON audit(timestamp);
CREATE INDEX idx_audit_resource ON audit(resource_type, resource_id);
CREATE INDEX idx_audit_action ON audit(action);

text

---

## 🔍 Ejemplos de auditoría

### Login

{
"user_id": "user_123",
"email": "user@example.com",
"action": "LOGIN",
"resource_type": "session",
"result": "SUCCESS",
"timestamp": "2025-10-31T03:31:00Z",
"ip_address": "192.168.1.100",
"user_agent": "Mozilla/5.0..."
}

text

### Crear evento (Agenda)

{
"user_id": "user_123",
"action": "CREATE",
"resource_type": "agenda",
"resource_id": "agenda_456",
"result": "SUCCESS",
"changes": {
"title": {"old": null, "new": "Reunión con cliente"},
"start_time": {"old": null, "new": "2025-11-01T10:00:00Z"},
"end_time": {"old": null, "new": "2025-11-01T11:00:00Z"},
"participants": {"old": null, "new": ["user@example.com", "client@example.com"]}
},
"timestamp": "2025-10-31T03:31:30Z"
}

text

### Update notas

{
"user_id": "user_123",
"action": "UPDATE",
"resource_type": "note",
"resource_id": "note_789",
"result": "SUCCESS",
"changes": {
"content": {
"old": "Nota antigua",
"new": "Nota actualizada con más detalles"
},
"tags": {
"old": ["importante"],
"new": ["importante", "urgente"]
}
},
"timestamp": "2025-10-31T03:31:45Z"
}

text

### Login fallido

{
"email": "user@example.com",
"action": "LOGIN",
"result": "FAILURE",
"error_message": "Invalid credentials",
"timestamp": "2025-10-31T03:32:00Z",
"ip_address": "192.168.1.101"
}

text

---

## 📝 Logging en código

### Middleware automático

from starlette.middleware import Middleware
from starlette.requests import Request
from datetime import datetime

async def audit_middleware(request: Request, call_next):
start = datetime.utcnow()
user_id = request.user.id if request.user else None
ip_address = request.client.host

text
response = await call_next(request)

duration = (datetime.utcnow() - start).total_seconds()

# Log automático
audit_log = {
    "user_id": user_id,
    "action": request.method,
    "resource_type": request.url.path.split('/'),[1]
    "result": "SUCCESS" if response.status_code < 400 else "FAILURE",
    "timestamp": start,
    "ip_address": ip_address,
    "duration_ms": duration * 1000
}

await save_audit_log(audit_log)
return response
app.add_middleware(Middleware(audit_middleware))

text

### Manual logging

from src.theaia.core.audit import AuditLogger

audit = AuditLogger()

@app.post("/agenda/create")
async def create_agenda(data: AgendaCreate, current_user: User = Depends(get_current_user)):
try:
agenda = await db.agenda.create(data)

text
    # Log success
    await audit.log(
        user_id=current_user.id,
        action="CREATE",
        resource_type="agenda",
        resource_id=str(agenda.id),
        changes={"title": data.title, "start_time": data.start_time},
        result="SUCCESS"
    )
    
    return agenda
except Exception as e:
    # Log failure
    await audit.log(
        user_id=current_user.id,
        action="CREATE",
        resource_type="agenda",
        result="FAILURE",
        error_message=str(e)
    )
    raise
text

---

## 📊 Queries audit típicas

### Acciones por usuario (últimas 24h)

SELECT
user_id,
action,
COUNT(*) as count,
COUNT(CASE WHEN result = 'FAILURE' THEN 1 END) as failures
FROM audit
WHERE timestamp > NOW() - INTERVAL '24 hours'
GROUP BY user_id, action
ORDER BY count DESC;

text

### Cambios en un recurso

SELECT
user_id,
action,
changes,
timestamp
FROM audit
WHERE resource_type = 'agenda' AND resource_id = 'agenda_456'
ORDER BY timestamp DESC;

text

### Intentos de acceso fallidos

SELECT
email,
action,
COUNT() as failed_attempts,
MAX(timestamp) as last_attempt,
ip_address
FROM audit
WHERE result = 'FAILURE' AND action = 'LOGIN'
AND timestamp > NOW() - INTERVAL '1 hour'
GROUP BY email, ip_address
HAVING COUNT() > 3; -- Alert si >3 intentos fallidos

text

### Actividad por hora

SELECT
DATE_TRUNC('hour', timestamp) as hour,
COUNT(*) as total_actions,
COUNT(DISTINCT user_id) as unique_users,
COUNT(CASE WHEN result = 'FAILURE' THEN 1 END) as failures
FROM audit
WHERE timestamp > NOW() - INTERVAL '7 days'
GROUP BY hour
ORDER BY hour DESC;

text

---

## 🔍 Monitoreo con Loki (H11)

### Log query en Loki

Errores en últimas 24h
{job="thea-ia", level="error"} | json | timestamp > now - 24h

Failed logins
{job="thea-ia"} | json | action="LOGIN" and result="FAILURE"

Slow queries
{job="thea-ia"} | json | duration_ms > 100

text

### Grafana dashboard

{
"dashboard": {
"title": "THEA IA Audit",
"panels": [
{
"title": "Failed Logins",
"targets": [
{
"expr": "count by(email) ({job="thea-ia"} | json | action="LOGIN" | result="FAILURE")"
}
]
},
{
"title": "Actions by User",
"targets": [
{
"expr": "count by(user_id) ({job="thea-ia"} | json)"
}
]
}
]
}
}

text

---

## 🛡️ Retention policy

| Data | Retention | Reason |
|------|-----------|--------|
| Audit logs | 3 años | GDPR compliance |
| Failed logins | 90 días | Security investigation |
| Success logs | 1 año | Debugging |
| Sensitive changes | 3 años | Compliance |

-- Cleanup script (mensual)
DELETE FROM audit
WHERE timestamp < NOW() - INTERVAL '3 years'
AND action NOT IN ('CREATE', 'DELETE', 'UPDATE')
AND result = 'SUCCESS';

text

---

## 📋 Compliance checklist

- [ ] Todos los cambios de datos auditados
- [ ] Logs inmutables (append-only)
- [ ] Retention policy establecida
- [ ] Acceso a logs restringido (admin only)
- [ ] Alertas en eventos críticos (login fail, DELETE)
- [ ] Backup logs separado de DB
- [ ] Queries audit documentadas
- [ ] Dashboard Grafana activo

---

## 📖 Documentación relacionada

- [Security Overview](./overview.md) — Principios
- [Security Controls](./controls.md) — Implementación
- [H11 - Observabilidad](../roadmap/milestones/H03_17.md)
- [H13 - Security Hardening](../roadmap/milestones/H03_17.md)

---

**Última actualización:** 2025-10-31 03:31 CET