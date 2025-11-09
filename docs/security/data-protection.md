🛡️ Protección de Datos — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-08 18:42 CET (Sesión 37)
Responsable: Security Team / CEO
Estado: ✅ Activo

📋 Propósito
Encryption, backups, GDPR compliance para THEA IA.

🔐 Encryption Strategy
At-Rest (PostgreSQL pgcrypto)
sql
-- Enable pgcrypto extension
CREATE EXTENSION pgcrypto;

-- Encrypted column
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT NOT NULL,
  password_hash VARCHAR(255) NOT NULL, -- bcrypt(12)
  sensitive_data BYTEA,
  created_at TIMESTAMPTZ
);

-- Encrypt/decrypt
INSERT INTO users (sensitive_data) 
  VALUES (pgp_sym_encrypt('secret', 'key'));

SELECT pgp_sym_decrypt(sensitive_data, 'key') 
  FROM users;
In-Transit (TLS 1.3)
text
Client ←→ WAF (TLS 1.3)
  ↓
Load Balancer (TLS 1.3)
  ↓
THEA IA App (TLS internal)
  ↓
PostgreSQL (TLS required)
Passwords (bcrypt)
python
import bcrypt

# Hash
password_hash = bcrypt.hashpw(
  password.encode(), 
  bcrypt.gensalt(rounds=12)
)

# Verify
bcrypt.checkpw(password.encode(), password_hash)
💾 Backup Strategy
Daily Encrypted Backups
bash
# 0 2 * * * (02:00 UTC daily)
pg_dump thea_ia | \
  gpg --symmetric --cipher-algo AES256 \
  > s3://thea-backups/$(date +%Y-%m-%d).sql.gpg

# Retention: 30 days
aws s3 ls s3://thea-backups/
Testing
bash
# Monthly: restore backup to test DB
pg_restore -d test_db backup.sql
# Verify integrity
SELECT COUNT(*) FROM users;
📋 GDPR Compliance
Data Subject Rights
text
Right to:
✅ Access (export JSON)
✅ Rectification (update data)
✅ Erasure (delete cascade)
✅ Portability (JSON export)
✅ Restrict (disable account)
✅ Object (opt-out)
Implementation
python
# Right to deletion
@app.delete("/users/{user_id}")
async def delete_user(user_id: str):
    # Cascade delete all related data
    db.query(Event).filter_by(user_id=user_id).delete()
    db.query(Note).filter_by(user_id=user_id).delete()
    db.query(User).filter_by(id=user_id).delete()
    db.commit()
    
# Right to export
@app.get("/users/me/export")
async def export_user_data(user_id: str):
    user = db.query(User).get(user_id)
    return {
        "user": user.dict(),
        "events": [e.dict() for e in user.events],
        "notes": [n.dict() for n in user.notes],
    }
📌 Meta-información
Campo	Valor
Archivo	docs/security/data_protection.md
Versión	v0.14.0
Última revisión	2025-11-08 18:42 CET (S37)
Estado	✅ Activo
Última actualización: 2025-11-08 18:42 CET