📜 Compliance y Cumplimiento — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 18:55 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Propósito
Asegurar cumplimiento normativo (GDPR, SOC 2) y respuesta a incidentes para THEA IA.

Audiencia:

Security auditors

Legal team

DevOps

CEO

🌍 GDPR Compliance
Datos Personales
python
# Categorías de datos
PERSONAL_DATA = {
    "Identificación": ["email", "nombre", "user_id"],
    "Contexto": ["conversaciones", "preferencias", "historial"],
    "Metadata": ["IP", "timestamps", "device_info"]
}
Derechos de los Usuarios
Derecho	Implementación	SLA
Acceso	GET /users/me/export	30 días
Rectificación	PUT /users/me	Inmediato
Supresión	DELETE /users/me	30 días
Portabilidad	GET /users/me/export (JSON)	30 días
Oposición	PUT /users/me/preferences	Inmediato
Restricción	PUT /users/me/disable	Inmediato
Implementación GDPR
python
@app.delete("/users/me")
async def delete_user(current_user: User = Depends(get_current_user)):
    """
    Derecho a supresión (GDPR Art. 17)
    Borra todos los datos personales del usuario.
    """
    # Cascade delete
    await db.conversations.delete_many({"user_id": current_user.id})
    await db.events.delete_many({"user_id": current_user.id})
    await db.notes.delete_many({"user_id": current_user.id})
    await db.users.delete_one({"id": current_user.id})
    
    # Log audit
    await audit.log("USER_DELETED", user_id=current_user.id)
    
    return {"status": "deleted", "message": "All personal data removed"}

@app.get("/users/me/export")
async def export_user_data(current_user: User = Depends(get_current_user)):
    """
    Derecho a portabilidad (GDPR Art. 20)
    Exporta todos los datos en formato JSON.
    """
    return {
        "user": current_user.dict(),
        "conversations": await db.conversations.find({"user_id": current_user.id}).to_list(),
        "events": await db.events.find({"user_id": current_user.id}).to_list(),
        "notes": await db.notes.find({"user_id": current_user.id}).to_list(),
        "exported_at": datetime.utcnow()
    }
Consentimiento
python
# Registro usuario requiere consentimiento explícito
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    terms_accepted: bool = Field(..., description="Must be True")
    privacy_accepted: bool = Field(..., description="Must be True")
    
    @validator('terms_accepted', 'privacy_accepted')
    def must_accept(cls, v):
        if not v:
            raise ValueError("Must accept terms and privacy policy")
        return v
🏛️ SOC 2 Type II
Trust Services Criteria
Criterio	Control	Evidencia
Security	OAuth2 + RBAC + TLS 1.3	Logs autenticación
Availability	99.9% uptime SLA	Prometheus metrics
Processing Integrity	Pydantic validation	Input validation logs
Confidentiality	AES-256 encryption	Audit logs acceso
Privacy	GDPR compliance	Data export logs
Controles SOC 2
text
# Security
- Control: Multi-factor authentication
  Status: Implemented
  Evidence: MFA logs in audit table
  
- Control: Encryption at-rest and in-transit
  Status: Implemented
  Evidence: TLS 1.3 + pgcrypto PostgreSQL

# Availability  
- Control: High availability architecture
  Status: Implemented
  Evidence: Kubernetes multi-replica deployment

# Confidentiality
- Control: Access control (RBAC)
  Status: Implemented
  Evidence: Role-based access logs
Auditoría SOC 2
sql
-- Query: Cambios en permisos (último mes)
SELECT 
    user_id,
    action,
    changes->>'roles' as role_changes,
    timestamp
FROM audit
WHERE action = 'UPDATE' 
  AND resource_type = 'user'
  AND timestamp > NOW() - INTERVAL '30 days'
ORDER BY timestamp DESC;

-- Query: Accesos no autorizados
SELECT 
    email,
    ip_address,
    COUNT(*) as failed_attempts
FROM audit
WHERE action = 'LOGIN' 
  AND result = 'FAILURE'
  AND timestamp > NOW() - INTERVAL '7 days'
GROUP BY email, ip_address
HAVING COUNT(*) > 5;
🚨 Incident Response Plan
Clasificación de Incidentes
Severidad	Descripción	SLA Respuesta
Critical	Breach datos, downtime total	15 min
High	Vulnerabilidad explotable	1 hora
Medium	Anomalía detectada	4 horas
Low	Mejora de seguridad	24 horas
Proceso de Respuesta
text
graph LR
    A[Detección] --> B[Clasificación]
    B --> C[Contención]
    C --> D[Erradicación]
    D --> E[Recuperación]
    E --> F[Post-mortem]
Equipo de Respuesta
text
Security Incident Response Team (SIRT):
- CEO (Álvaro Fernández Mota) — Decisiones ejecutivas
- Tech Lead — Coordinación técnica
- DevOps — Infraestructura
- Legal — Cumplimiento normativo
Playbook: Data Breach
text
# 1. Detección (0-15 min)
- Alert: Anomalía en acceso a BD
- Verificar: Revisar audit logs
- Clasificar: Severity = Critical

# 2. Contención (15-30 min)
- Aislar: Desconectar sistema afectado
- Backup: Snapshot actual estado
- Comunicar: Notificar SIRT

# 3. Investigación (30 min - 2h)
- Analizar: ¿Qué datos fueron accedidos?
- Determinar: ¿Cuántos usuarios afectados?
- Documentar: Timeline de eventos

# 4. Notificación (24-72h)
- Legal: Determinar obligación notificación GDPR
- Usuarios: Email a afectados (si aplica)
- Autoridades: Notificar DPA (si >72h desde breach)

# 5. Remediación (72h - 7 días)
- Fix: Parchear vulnerabilidad
- Deploy: Nueva versión
- Monitorear: Alertas adicionales

# 6. Post-mortem (7-14 días)
- Documentar: Lecciones aprendidas
- Actualizar: Security playbooks
- Comunicar: Stakeholders
📊 Compliance Checklist
GDPR
 Política de privacidad publicada

 Consentimiento explícito en registro

 Derecho a acceso implementado

 Derecho a supresión implementado

 Derecho a portabilidad implementado

 Encriptación datos sensibles

 Retention policy definida (3 años)

 DPO designado (CEO interino)

SOC 2
 MFA implementado

 Encryption at-rest y in-transit

 Access logs auditables

 High availability (K8s)

 Backup automático diario

 Incident response plan documentado

 Vulnerability scanning (mensual)

 Penetration testing externo (Q1 2026)

📌 Meta-información
Campo	Valor
Archivo	docs/security/compliance.md
Versión	v0.14.0
Última revisión	2025-11-09 18:55 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 18:55 CET