📐 Standards de Auditoría — THEA IA PROFESSIONAL v2.0 (S38+)
Versión: v2.0.0 (PROFESSIONAL-SCALE)
Última actualización: 2025-11-10 17:58 CET
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ PRODUCTION STANDARDS

📋 Propósito
Estándares obligatorios de calidad, compliance y excelencia para auditoría THEA IA completa. Define métricas, benchmarks y criterios de aceptación aplicables a código, documentación, seguridad y operaciones para todo el proyecto (180+ archivos).

🎯 ESTÁNDARES GLOBALES
1. Versionado Semántico
text
Formato: MAJOR.MINOR.PATCH

v2.0.0 (Audit Professional Scale)
│      │      │
│      │      └─ PATCH: Bug fixes, doc corrections
│      └─ MINOR: New audit modules, new docs, features
└─ MAJOR: Architecture changes, release versions
Cadencia:

MAJOR: Anual (cambios arquitecturales)

MINOR: Mensual (fin de mes)

PATCH: Semanal (critical fixes)

Actual: v2.0.0 (Professional Scale Edition - Nov 10, 2025)

2. Documentación
Métrica	Standard	Status	Target
Cobertura	≥95% módulos documentados	✅ 35% (S38)	100% (S51)
Actualización	Max 1 semana lag	✅ <1 día	<24h
Ejemplos	Min 1 por sección técnica	✅ 100% (core/)	100% (all)
Links	100% validados	✅ 100%	100%
Meta-info	Header + tabla final	✅ 100%	100%
READMEs	1 por módulo principal	✅ 8 (core/)	30+ (total)
3. Calidad Código
Métrica	Standard	Tool	Target
Test Coverage	≥85%	pytest + coverage	85%
Linting	0 violations	flake8, black, isort	0
Type Hints	100% funciones públicas	mypy	100%
Docstrings	100% funciones públicas	pydoc	100%
Complexity	Max 10 cyclomatic	radon	<10
Performance	p95 <100ms endpoints	prometheus	<100ms
4. Seguridad
Control	Standard	Status	Target
Encryption	AES-256 data at rest	✅ v0.14.0	✅ Compliant
Auth	OAuth2 + JWT minimum	✅ v0.14.0	✅ Compliant
RBAC	Role-based access	✅ v0.14.0	✅ Compliant
GDPR	Data minimization	🟡 Q4 2025	✅ 2026 Q1
SOC 2	Type II compliance	⏳ Roadmap	✅ 2026 Q2
5. Rendimiento
API Endpoints

text
p50:  <20ms (ideal)
p95:  <100ms (target)
p99:  <500ms (acceptable)

Throughput: ≥100 req/s (minimum)
Uptime: ≥99.5% (production)
Database

text
Query p95: <100ms (95% of queries)
Connection pool: 10-20 connections
Replication: Async (eventual consistency)
Backup: Daily snapshots + point-in-time recovery
Infrastructure

text
Container startup: <5s
Pod ready: <10s
Service discovery: <1s
Graceful shutdown: <30s
📐 ESTÁNDARES POR ÁREA
Python Code Standards
Naming Convention
python
# Módulos: snake_case
src/theaia/core/fsm_engine.py

# Clases: PascalCase
class FSMEngine:
    pass

# Funciones/métodos: snake_case
def handle_message(self, msg):
    pass

# Constantes: UPPER_SNAKE_CASE
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30

# Privadas: _leading_underscore
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
from typing import Optional, List, Dict, Union

def get_agents(active_only: bool = True) -> List[Agent]:
    pass

def search(query: str, filters: Optional[Dict[str, Any]] = None) -> Dict:
    pass

# ❌ Incorrecto
def get_agents(active_only=True):  # Missing types
    pass
Markdown Files
Structure
text
# H1 Title — Project

**Version:** v2.0.0
**Last updated:** YYYY-MM-DD HH:MM CET (Session XX)
**Author:** Name (Role)
**Status:** ✅ Active

---

## 📋 Purpose
[1-2 paragraphs explaining content]

---

## Key Sections
[Use H2 headings max]

---

## 📌 Meta-information
| Key | Value |
|-----|-------|
| File | path/to/file.md |
| Status | ✅ Active |
| Last review | YYYY-MM-DD |

**Last updated:** YYYY-MM-DD HH:MM CET
Code Blocks
text
✅ Correcto
\`\`\`python
def hello():
    """Función ejemplo."""
    return "Hello"
\`\`\`

❌ Incorrecto (sin lenguaje)
\`\`\`
def hello():
    return "Hello"
\`\`\`
README Standards (Per Module)
Obligatorio:

Descripción clara (1-2 párrafos)

Propósito y responsabilidades

Estructura de archivos

Ejemplo de uso

Integración con otros módulos

Known issues + roadmap

Meta-information

Template estructura:

text
# Module Name — Description

**Version:** v0.14.0+
**Last updated:** [Date]
**Status:** ✅ Active

## 📋 Purpose
[Clear description]

## 🏗️ Architecture
[Structure diagram/list]

## 🚀 Usage
[Examples]

## 🔗 Integration
[How it connects]

## 📌 Meta-information
[Table]
CHANGELOG Standards
Format: Keep-a-Changelog 1.0.0

Secciones obligatorias:

Added (nuevas características)

Changed (cambios existentes)

Fixed (bug fixes)

Removed (deprecations)

Security (CVEs)

Known Issues

Ejemplo:

text
## [v1.0.0] — 2025-11-10

### Added
- Core module complete (24 files)
- FSM engine v1.0
- 8 agents mapped

### Fixed
- Legacy files removed (3 files)
- Documentation links validated

### Known Issues
- FSM state lookups O(n) → target H01

## [v0.14.0] — 2025-10-28
...
ROADMAP Standards
Secciones obligatorias:

Current status (% complete)

Next milestones (H01, H02, etc)

Timeline estimado

Dependencies

Success criteria

Formato:

text
# Roadmap — [Module Name]

## Current Status
- 35% complete (101/180 files)
- 15 docs generated
- Production ready

## H01: [Milestone] (Nov 20 - Dec 15)
- [ ] Task 1
- [ ] Task 2
- Estimated: 10h

## H02: [Milestone] (Dec 16 - Jan 20)
...

## Success Criteria
- ✅ 100% audited
- ✅ 30+ docs
- ✅ 0 issues
✅ AUDIT CHECKLIST ESTÁNDAR
Por cada módulo/carpeta:
 Discovery

 Listar archivos exactos

 Contar líneas de código

 Identificar dependencias

 Analysis

 Revisar propósito

 Analizar coupling

 Identificar legacy code

 Documentation

 Crear README

 Crear ROADMAP

 Crear CHANGELOG

 Quality

 Test coverage ≥85%

 Linting 0 violations

 Docstrings 100%

 Integration

 Validar dependencies

 Validar imports

 Actualizar índice

 Final

 Commit + push

 Actualizar diary

 Actualizar audit tracker

🎯 ENTREGA ESTÁNDAR POR SESIÓN
Documentos mínimos por módulo:

[module]-README.md (uso + arquitectura)

[module]-ROADMAP.md (timeline + hitos)

[module]-CHANGELOG.md (versiones)

Opcional (si aplica):
4. [module]-API.md (endpoints/interfaces)
5. [module]-DEPLOYMENT.md (configuración)
6. [module]-TESTING.md (test strategy)

📊 MÉTRICAS ESPERADAS
Por sesión (auditoría estándar 1-2h):

10-15 archivos auditados

2-3 módulos completados

3-6 documentos generados

0 quality violations

Proyecto final (S51 complete):

180+ archivos auditados (100%)

30+ módulos documentados (100%)

30+ documentos profesionales

≥85% test coverage

0 breaking issues

🔄 ESCALABILIDAD & MAINTENANCE
Templates Reutilizables
module-README-TEMPLATE.md

module-ROADMAP-TEMPLATE.md

module-CHANGELOG-TEMPLATE.md

module-TEST-TEMPLATE.md

Automatización
bash
# Validar todos los links
find docs -name "*.md" -exec grep -l "http" {} \;

# Verificar meta-información
grep -r "Last updated" docs/

# Generar índice maestro
ls -R docs/ > PROJECT-STRUCTURE.txt
GitHub Actions
text
# auto-validate-docs.yml
on: [pull_request]
jobs:
  validate:
    - Check links
    - Validate markdown
    - Verify meta-info
📞 META-INFORMACIÓN
Campo	Valor
Archivo	docs/audit/standards.md
Versión	v2.0.0
Responsable	Álvaro Fernández Mota
Estado	✅ PRODUCTION STANDARDS
Aplicable a	180+ archivos proyecto
Próxima revisión	S51 (proyecto completo)
Última actualización	2025-11-10 17:58 CET
Professional Audit Standards v2.0
Diseñados para escala industrial
Aplicables a 180+ archivos, 30+ sesiones, 18+ horas