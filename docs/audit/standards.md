📐 Standards — THEA IA Quality & Compliance
Versión: v0.14.0
Última actualización: 2025-11-09 19:51 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Propósito
Estándares obligatorios de calidad, compliance y excelencia para THEA IA. Define métricas, benchmarks y criterios de aceptación aplicables a código, documentación, seguridad y operaciones.

🎯 Estándares Globales
1. Versioning
text
Formato: MAJOR.MINOR.PATCH

v0.14.0
├─ 0 = MAJOR (aún pre-release, cambios arquitecturales)
├─ 14 = MINOR (features nuevas)
└─ 0 = PATCH (bugfixes)

Cadencia: 
- MAJOR: Anual (cuando sea needed)
- MINOR: Mensual (fin de mes)
- PATCH: Semanal (critical bugs)
Actual: v0.14.0 (Release: 2025-11-09)

2. Documentación
Métrica	Standard	Status
Cobertura	≥95% de módulos documentados	✅ 95% (S37)
Actualización	Max 2 semanas de lag	✅ <1 semana (S37)
Ejemplos	Mínimo 1 por sección técnica	✅ 100%
Links	Todos validados cada sesión	✅ 100%
Meta-info	Header + meta-tabla obligatorios	✅ 100%
3. Code Quality
Métrica	Standard	Herramienta	Target
Test Coverage	≥85%	pytest + coverage	85%
Linting	0 violations	flake8, black	0
Type Hints	100% public functions	mypy	100%
Docstrings	All public functions	pydoc	100%
Performance	Latency p95 <100ms	Prometheus	<100ms
4. Security
Controles	Standard	Audit
Encryption	AES-256 data at rest	✅ Q4 2025
Auth	OAuth2 + JWT minimum	✅ v0.14.0
RBAC	Role-based access	✅ v0.14.0
GDPR	Data minimization	✅ Roadmap H08
SOC 2	Type II compliance target	⏳ 2026
5. Performance
API Endpoints
text
p50:  <20ms
p95:  <100ms
p99:  <500ms

Throughput: ≥100 req/s
Uptime: ≥99% (production)
Database
text
Queries <100ms: ≥95%
Connection pool: 10-20 connections
Replication: Async (eventual consistency)
Backup: Daily snapshots
Infrastructure
text
Container startup: <5s
Pod ready: <10s
Service discovery: <1s
📂 Estándares por Área
Código Python
Naming Convention
python
# Modules: snake_case
src/theaia/core/fsm_engine.py

# Classes: PascalCase
class FSMEngine:
    pass

# Functions/methods: snake_case
def handle_message(self, msg):
    pass

# Constants: UPPER_SNAKE_CASE
MAX_RETRIES = 3

# Private: _leading_underscore
def _internal_helper():
    pass
Docstrings (Google Style)
python
def schedule_meeting(date: str, time: str, user_id: str) -> Meeting:
    """Schedule a meeting for user.
    
    Args:
        date: Meeting date in YYYY-MM-DD format.
        time: Meeting time in HH:MM format.
        user_id: UUID of the user.
    
    Returns:
        Meeting object with confirmation ID.
    
    Raises:
        ValueError: If date/time invalid.
        PermissionError: If user not authorized.
    
    Example:
        >>> meeting = schedule_meeting('2025-11-15', '10:00', 'user123')
        >>> print(meeting.id)
        'conf_abc123'
    """
    pass
Type Hints
python
# ✅ Correcto
from typing import Optional, List, Dict

def get_agents(active_only: bool = True) -> List[Agent]:
    pass

def search(query: str, filters: Optional[Dict] = None) -> Dict:
    pass

# ❌ Incorrecto (sin type hints)
def get_agents(active_only=True):
    pass
Git & Commits
Branch Naming
text
feature/[feature-name]
bugfix/[issue-number]
hotfix/[issue-number]
docs/[topic]
refactor/[module]
Commit Message Format
text
[TYPE-SESSION]: Brief description

Detailed explanation (optional).
- Point 1
- Point 2

Closes #123
Co-authored-by: Name <email>
Types:

feat: Nueva feature

fix: Bugfix

docs: Documentación

test: Tests

refactor: Refactoring sin cambios funcionales

perf: Performance improvements

chore: Build, deps, etc.

Example:

text
feat-S37: Add WhatsApp adapter support

Implement Twilio adapter for WhatsApp integration.
Supports text, media, and interactive messages.

- src/theaia/adapters/whatsapp/adapter.py
- tests/e2e/test_whatsapp.py
- docs/adapters/adapter_whatsapp.md

Closes #456
Co-authored-by: Álvaro Fernández <alvaro@thea-ia.com>
Markdown Files
Structure
text
# H1 Title — Project

**Version:** v0.14.0  
**Last updated:** YYYY-MM-DD HH:MM CET (Sesión XX)  
**Author:** Name (Role)  
**Status:** ✅ Active

---

## 📋 Purpose
[1-2 paragraphs]

---

## Content Sections
[H2 headings max]

---

## 📌 Meta-information
| Key | Value |
|-----|-------|

---

**Last updated:** YYYY-MM-DD HH:MM CET
Code Blocks
text
# ✅ Correcto
\`\`\`python
def hello():
    pass
\`\`\`

# ❌ Incorrecto (sin lenguaje)
\`\`\`
def hello():
    pass
\`\`\`
Database Schema
Naming
sql
-- Tables: plural, snake_case
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR NOT NULL
);

-- Columns: snake_case
-- FK: {table_name}_id
user_id UUID FOREIGN KEY REFERENCES users(id)

-- Indexes: idx_{table}_{column}
CREATE INDEX idx_users_email ON users(email);
Migration Format
bash
migrations/
├── 001_initial_schema.sql
├── 002_add_users_table.sql
└── 003_add_audit_log.sql
Testing
Coverage Targets
text
Overall: ≥85%
Unit:    ≥80%
Integration: ≥75%
E2E:     ≥70%
Test File Structure
text
tests/
├── unit/
│   ├── test_fsm.py
│   ├── test_agents.py
│   └── test_adapters.py
├── integration/
│   └── test_adapters_integration.py
└── e2e/
    ├── test_telegram_flow.py
    └── test_web_client.py
Test Naming
python
# ✅ Correcto
def test_schedule_meeting_with_valid_date():
    pass

def test_schedule_meeting_raises_error_with_invalid_date():
    pass

# ❌ Incorrecto
def test_meeting():
    pass
API Endpoints
REST Convention
text
GET    /api/v1/users              # List users
POST   /api/v1/users              # Create user
GET    /api/v1/users/{id}         # Get user
PUT    /api/v1/users/{id}         # Update user
DELETE /api/v1/users/{id}         # Delete user
Response Format
json
{
  "success": true,
  "data": {},
  "meta": {
    "version": "v1",
    "timestamp": "2025-11-09T19:51:00Z",
    "request_id": "req_abc123"
  }
}
Security
Password Requirements
text
Minimum length: 12 characters
Complexity: UPPERCASE + lowercase + digits + symbols
Hashing: bcrypt (≥12 rounds)
Rotation: 90 days (optional reminder)
API Keys
text
Format: tk_{environment}_{random32}
Example: tk_prod_abc123def456ghi789jkl012
Storage: Hashed (SHA-256 minimum)
Rotation: 90 days mandatory
Data Classification
text
Public:     No encryption required
Internal:   Encrypt at rest (AES-256)
Confidential: Encrypt at rest + in transit
Restricted:  Full audit trail required
🎯 Quality Checkpoints
Pre-Commit
 Tests pass (pytest)

 Linting passes (flake8)

 Type checking passes (mypy)

 No secrets in code

 Updated docs

Pre-Release
 Changelog updated

 Version bumped

 Security audit passed

 Performance benchmarks met

 All issues closed or moved

Production Deployment
 Blue-green deployment

 Health check passes

 Rollback plan ready

 Monitoring configured

 On-call team notified

📊 Compliance Matrix
Standard	v0.14	v1.0	v2.0
GDPR	80%	95%	100%
SOC 2	60%	80%	100%
CCPA	80%	95%	100%
Test Coverage	85%	90%	95%
Uptime	99%	99.9%	99.99%
📌 Meta-información
Campo	Valor
Archivo	docs/audit/standards.md
Versión	v0.14.0
Última revisión	2025-11-09 19:51 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Aplicabilidad	Proyecto global + módulos
Última actualización: 2025-11-09 19:51 CET