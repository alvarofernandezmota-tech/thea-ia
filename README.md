THEA IA — IA Modular y Núcleo de Auditoría
Versión: 3.0 / v0.15.0
Actualizado: 2025-11-14
Autor: Álvaro Fernández Mota (CEO de THEA IA)
Equipo: Unidad Central THEA IA / Colaboración Enterprise
Contacto: alvarofernandezmota@gmail.com

🚀 Quick Start / Configuración Básica
bash
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

Configurar base de datos
cp .env.example .env # Personalizar antes de lanzar
alembic upgrade head # Aplicar migraciones PostgreSQL

Ejecutar bot Telegram
python -m src.theaia.adapters.telegram.bot

text

**Requisitos:**
- Python 3.11+
- PostgreSQL 14+ (obligatorio desde H02)
- Redis (opcional para cache)
- Docker (incluido, opcional para despliegue)

**Verifica:** Consulta `.env.example` y `SECURITY.md` antes de trabajar en producción.

---

## 📊 Estado del Proyecto (Actualizado 14 Nov 2025)

|| Fase | Hitos | Estado | Progreso |
|------|-------|--------|----------|
| **Fase 1: Core & FSM** | H01 | ✅ COMPLETADA | 100% |
| **Fase 2: Multi-agente & Adapters** | H02-H07 | 🔄 EN CURSO | 12% |
| **Fase 3: Infra & Seguridad** | H08-H14 | ⏳ PRÓXIMA | 0% |
| **Fase 4: Escalabilidad & Release** | H15-H17 | ⏳ FUTURA | 0% |

### Hitos Completados

**✅ H01: Organización & Tests** (31 oct 2025)
- Estructura profesional completa
- FSM base operativo
- Tests ≥80% coverage
- Docker básico implementado
- 53.3h en 15 sesiones

**✅ H02: Database & Telegram** (12 nov 2025) — CORE COMPLETADO (70%)
- PostgreSQL Database Layer completo (7 modelos, 6 repositories)
- Multi-tenant architecture desde el inicio
- TelegramAdapter funcional con persistencia
- **Primera conversación real** guardada (Usuario Entu, 12 nov 17:02)
- 12/12 tests database pasando
- 4.3h en 1 sesión intensiva
- Componentes web aplazados estratégicamente a H05-H08

### Próximo Hito

**⏳ H03: FSM Avanzado & CoreRouter** (15-20 nov 2025)
- Integración CoreRouter con Telegram
- Intent Detector y Entity Extractor básicos
- Primera conversación con NLP funcional

---

## 🧭 Filosofía y Arquitectura Modular

- **Orquestación modular:** Cada carpeta y feature tiene descripción, onboarding y control de auditoría
- **Desarrollo por hitos:** 17 hitos principales, micro-hitos por área/equipo
- **Documentación extensiva:** `/docs`, todos los README, ROADMAP, SECURITY con checklist y protocolos
- **Colaborativo/auditable:** Estructura para equipos distribuidos, PRs y auditorías públicas/privadas
- **Cloud/DevOps:** Pipelines CI/CD, coverage y control de releases automático
- **Seguridad y cumplimiento:** Cumple con mejores prácticas DevSecOps, encriptación y auditoría transversal
- **Multi-tenant desde el inicio:** Arquitectura empresarial escalable (implementado en H02)

---

## 📂 Estructura Clave

├── README.md # Esta guía rápida, filosofía, estructura, auditoría
├── ROADMAP.md # Panel de 17 hitos/micro-hitos, estados y cohortes
├── CHANGELOG.md # Historial pro, versión y milestones transversales
├── CONTRIBUTING.md # PRs, normas, checklist y flujo colaborativo
├── .env.example # Variables por entorno, bien comentado y seguro
├── SECURITY.md # Política de seguridad y protocolo incidente
├── requirements.txt # Dependencias Python (asyncpg, alembic, python-telegram-bot)
├── alembic.ini # Configuración migraciones database
├── Dockerfile # Docker básico (optimización en H09)
├── docker-compose.yml # Stack local con PostgreSQL
├── docs/ # Guías extendidas, onboarding, auditoría
│ ├── roadmap/ # Roadmaps detallados por hito
│ ├── diary/ # Diarios de sesiones de trabajo
│ ├── architecture/ # Decisiones arquitectónicas
│ └── audit/ # Checklists y auditorías
├── src/theaia/ # Código fuente principal
│ ├── core/ # FSM, state machine, routers
│ ├── agents/ # Agentes especializados
│ ├── adapters/ # TelegramAdapter, WebAdapter (futuro)
│ ├── database/ # Models, repositories, migrations ✨ NUEVO H02
│ ├── ml/ # Pipelines NLP/ML (H06)
│ └── tests/ # Tests unitarios, integración, e2e
├── migrations/ # Migraciones Alembic ✨ NUEVO H02
└── .archive/ # Dumps temporales, debugging, nunca en producción

text

***

## ⚡ Documentación Relacionada

### Documentación Principal
- [docs/README.md](docs/README.md) — Guía avanzada, rutas internas, API, detalle técnico
- [ROADMAP.md](ROADMAP.md) — Avance por hitos y equipos
- [CHANGELOG.md](CHANGELOG.md) — Control transversal de releases y auditoría
- [SECURITY.md](SECURITY.md) — Seguridad, privacidad y hardening
- [CONTRIBUTING.md](CONTRIBUTING.md) — Guía de contribución

### Roadmaps Detallados
- [docs/roadmap/master.md](docs/roadmap/master.md) — Roadmap maestro con tracking operativo
- [docs/roadmap/deployment.md](docs/roadmap/deployment.md) — Overview estratégico
- [docs/roadmap/milestones/H01.md](docs/roadmap/milestones/H01.md) — Hito 1 completado
- [docs/roadmap/milestones/H02.md](docs/roadmap/milestones/H02.md) — Hito 2 core completado
- [docs/roadmap/milestones/H03_17.md](docs/roadmap/milestones/H03_17.md) — Hitos futuros

### Diarios y Auditorías
- [docs/diary/diarynoviembre.md](docs/diary/diarynoviembre.md) — Sesiones noviembre 2025
- [docs/diary/diaryoctubre.md](docs/diary/diaryoctubre.md) — Sesiones octubre 2025
- [docs/onboarding.md](docs/onboarding.md) — Guía para nuevos colaboradores

***

## 🎯 Logros Destacados

### Primera Conversación Real (12 nov 2025, 17:02 CET)
- **Usuario:** Entu (Telegram ID: 6961767622)
- **Mensajes guardados:** 2 en PostgreSQL
- **Estado:** ✅ FUNCIONAL
- **Arquitectura:** Multi-tenant desde día 1

### Database Layer Empresarial
- 7 modelos SQLAlchemy multi-tenant
- 6 repositories con Repository Pattern
- 5 tablas operativas: users, events, notes, conversations, message_history
- 20+ índices optimizados
- JSONB para metadatos flexibles
- ARRAY nativo PostgreSQL para tags
- Async/await SQLAlchemy 2.0

### TelegramAdapter Funcional
- Persistencia automática de usuarios
- Persistencia de conversaciones (FSM state + context)
- Auditoría completa de mensajes
- Comandos: /start, /help, /reset

***

## 🛡️ Seguridad y Auditoría

- **Variables críticas** están en `.env` protegido (nunca en repo)
- **Checklist de despliegue** y auditoría: `SECURITY.md`, `docs/audit/`
- **Protocolos y compliance:** Control de roles, logs de auditoría, backups cifrados
- **Multi-tenant desde el inicio:** tenant_id obligatorio en todas las tablas
- **Nunca subir archivos sensibles:** `.gitignore` cubre logs, modelos, secretos
- **NO CODE sin documentar:** Cada función y PR debe reflejar cambios en README/local y CHANGELOG

### Configuración Database Segura (H02)
- PostgreSQL con autenticación (trust mode solo desarrollo)
- Migraciones Alembic versionadas
- Connection pooling configurado
- Timezone-aware timestamps
- Foreign keys con CASCADE para integridad

***

## 🤝 Contribuir y Escalar

1. **Usa CONTRIBUTING.md** y actualiza roadmap/changelog cada avance
2. **Aporta tests/PR basados en checklist:** calidad y seguridad ante todo
3. **Documenta tu módulo** antes y después de contribuir
4. **Coverage ≥80%** obligatorio para PRs
5. **Conventional Commits** para mensajes claros

### Workflow Recomendado
```bash```
# 1. Crear feature branch
git checkout -b feature/mi-feature

# 2. Desarrollar con tests
pytest src/theaia/tests/

# 3. Verificar coverage
pytest --cov=src/theaia --cov-report=html

# 4. Actualizar docs
# - README local del módulo
# - CHANGELOG local si aplica
# - Diario si es sesión larga

# 5. PR con checklist completo
🔗 Enlaces Rápidos
Desarrollo
src/theaia/ — Código fuente

src/theaia/database/ — Database Layer (H02) ✨

src/theaia/adapters/telegram/ — TelegramAdapter (H02) ✨

src/theaia/tests/ — Suite de tests

Configuración
.env.example — Variables de entorno documentadas

alembic.ini — Configuración migraciones

requirements.txt — Dependencias Python

docker-compose.yml — Stack local

Infraestructura
Dockerfile — Imagen Docker básica

.github/ — Workflows CI/CD (futuro H09)

📈 Métricas del Proyecto
|| Métrica | Valor | Estado |
|---------|-------|--------|
| Hitos completados | 2/17 (H01, H02 core) | 🔄 12% Fase 2 |
| Horas invertidas | 57.6h reales | vs. ~490h estimadas Fase 2 |
| Tests pasando | 12/12 database (100%) | ⚠️ Coverage global ~40% |
| LOC producción | ~7,000 | Database: 3,000 + Core: 4,000 |
| Primera conversación | ✅ 12 nov 2025 | Usuario real en producción |
| Multi-tenant | ✅ Implementado | Desde H02 |

🚀 Próximos Pasos
Inmediato (H03 - 15-20 nov)
Integrar CoreRouter con TelegramAdapter

Implementar Intent Detector básico

Implementar Entity Extractor básico

Primera conversación con NLP funcional

Corto Plazo (H04-H07 - dic 2025)
Optimizar queries database (coverage ≥85%)

Agentes verticales inteligentes con arquitectura híbrida LLM

Pipelines ML/NLP completos (LangChain, RAG)

Suite completa tests e2e

Medio Plazo (H08 - 2026)
Web Client completo (aplazado de H02)

OAuth2/JWT (aplazado de H02)

RBAC multi-tenant completo

📞 Contacto y Soporte
CEO y Responsable Técnico: Álvaro Fernández Mota
Email: alvarofernandezmota@gmail.com
Seguridad: security@theaia.com (protocolo de vulnerabilidades)
GitHub: @alvarofernandezmota-tech

THEA IA — IA modular, auditable y diseñada para colaboración profesional.

Última actualización: 2025-11-14 17:14 CET
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Versión: v0.15.0 (H02 Core Completado)
Estado: ✅ H01 Completado | ✅ H02 Core Completado (70%) | ⏳ H03 Próximo