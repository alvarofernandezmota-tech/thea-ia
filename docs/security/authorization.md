👥 Autorización — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-08 18:40 CET (Sesión 37)
Responsable: Security Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
RBAC (Role-Based Access Control) + Tenant Isolation para THEA IA.

Audiencia:

Developers

DevOps

Security auditors

👥 Roles Model
Estándar Roles
text
admin:
  - Todas las acciones
  - Ver/editar todos users
  - Acceso audit logs
  
user:
  - Leer/escribir propios recursos
  - Crear eventos, notas, etc.
  - No acceso otros users
  
agent:
  - Ejecutar acciones delegadas
  - Leer contexto necesario
  - No acceso directo UI
  
guest:
  - Lectura pública
  - Sin escritura
Permissions
text
users:create, users:read, users:update, users:delete
events:create, events:read, events:update, events:delete
notes:create, notes:read, notes:update, notes:delete
audit:read
🏢 Tenant Isolation
Row-Level Security (RLS)
sql
-- Policy: user_owns_data
CREATE POLICY user_owns_data ON events
  USING (user_id = current_user_id 
    AND tenant_id = current_tenant_id);

-- Automático: cada query filtra por tenant
SELECT * FROM events;
-- → WHERE tenant_id = current_tenant
Multi-tenant Context
python
# Request headers
X-Tenant-ID: tenant_456
Authorization: Bearer {jwt}

# Middleware extrae tenant
@app.middleware("http")
async def add_tenant_context(request, call_next):
    tenant_id = request.headers.get("X-Tenant-ID")
    request.state.tenant_id = tenant_id
    response = await call_next(request)
    return response
🔐 Access Control Examples
python
# Decorator para RBAC
@require_role("admin")
def delete_user(user_id):
    pass

# Decorator para permisos específicos
@require_permission("events:delete")
def delete_event(event_id):
    pass

# Tenant-aware query
def get_user_events(user_id):
    return db.query(Event).filter(
        Event.user_id == user_id,
        Event.tenant_id == current_tenant_id
    ).all()
📋 Decision Matrix
Rol	Resource	Create	Read	Update	Delete
admin	Users	✅	✅	✅	✅
user	Own events	✅	✅	✅	✅
user	Other events	❌	❌	❌	❌
guest	Public	❌	✅	❌	❌
📌 Meta-información
Campo	Valor
Archivo	docs/security/authorization.md
Versión	v0.14.0
Última revisión	2025-11-08 18:40 CET (S37)
Responsable	Security Team / CEO
Estado	✅ Activo
Última actualización: 2025-11-08 18:40 CET