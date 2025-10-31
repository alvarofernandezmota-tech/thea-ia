# SCHEMA — THEA IA v2.0 (Arquitectura & Orquestación)

**Proyecto:** THEA IA  
**Versión:** 2.0 / v0.14.0  
**Actualizado:** 2025-10-31 01:23 CET  
**Responsable:** Álvaro Fernández Mota (CEO)

---

## 🎯 Estado global del proyecto

| Métrica | Estado | % |
|---------|--------|-----|
| **Fase completada** | 1/4 ✅ | 25% |
| **Documentación raíz** | 100% ✅ | Profesional |
| **Hito H01** | ✅ COMPLETADO | Org & Tests |
| **Infraestructura** | Fase 1 ✅ | Core FSM OK |
| **Multi-agente** | Fase 2 🔄 | En desarrollo |

---

## 🏗️ Estructura THEA IA

### Raíz — Documentación profesional
├── README.md # Filosofía, 17 hitos, auditoría
├── ROADMAP.md # Plan 17 hitos + 4 fases
├── CHANGELOG.md # Versionado v0.14.0
├── CONTRIBUTING.md # Normas PR, Git Flow, tests ≥80%
├── SECURITY.md # Protocolo vulnerabilidades, encriptación AES-256
└── .env.example # 20 secciones, variables por módulo/entorno

text

### Carpetas — README/ROADMAP/CHANGELOG local (próxima sesión)
src/theaia/
├── core/ # FSM, router, managers, contexto
├── agents/ # Agenda, notas, eventos, query, etc
├── adapters/ # Telegram, WhatsApp, Web, API REST
├── ml/ # Intent detector, entity extractor, spacy
├── tests/ # Unit, integration, e2e, FSM tests
└── docs/ # Arquitectura, onboarding, audit checklist

text

---

## 🎖️ 17 Hitos principales (Roadmap maestro)

| # | Nombre | Estado | Deadline |
|---|--------|--------|----------|
| H01 | Org & Tests | ✅ | 2025-10-31 |
| H02 | Telegram & Web | 🔄 | 2025-11-10 |
| H03 | FSM & Manager | ⏳ | 2025-11-15 |
| H04 | Persistencia & DB | ⏳ | 2025-11-25 |
| H05 | Agentes verticales | ⏳ | 2025-12-01 |
| H06 | ML/NLP pipelines | ⏳ | 2025-12-10 |
| H07 | E2E Tests & QA | ⏳ | 2025-12-15 |
| H08 | Multi-empresa RBAC | ⏳ | 2026-01-10 |
| H09 | Docker/K8s & CI/CD | ⏳ | 2026-01-20 |
| H10 | WhatsApp & REST | ⏳ | 2026-02-01 |
| H11 | Observabilidad | ⏳ | 2026-02-15 |
| H12 | Integraciones ext | ⏳ | 2026-03-01 |
| H13 | Seguridad & Hardening | ⏳ | 2026-03-15 |
| H14 | Onboarding prof | ⏳ | 2026-04-01 |
| H15 | Performance & stress | ⏳ | 2026-04-20 |
| H16 | Plugins & custom | ⏳ | 2026-05-10 |
| H17 | Auditoría final | ⏳ | 2026-06-01 |

---

## 4️⃣ Fases orquestadas

### Fase 1: Core y FSM (Completada ✅)
- Estructura, tests, documentación raíz
- H01 completado

### Fase 2: Multi-agente y adaptadores (En curso 🔄)
- H02-H07: Adapters, agents, ML, E2E tests
- Deadline: 2025-12-15

### Fase 3: Infra, observabilidad, seguridad (Próxima ⏳)
- H08-H14: Multi-empresa, Docker/K8s, observabilidad, hardening, onboarding
- Deadline: 2026-04-01

### Fase 4: Escalabilidad y release (Futura ⏳)
- H15-H17: Performance, plugins, auditoría final, go-live
- Deadline: 2026-06-01

---

## 📊 Archivos por módulo

### Raíz (2025-10-31)
- ✅ README.md
- ✅ ROADMAP.md
- ✅ CHANGELOG.md
- ✅ CONTRIBUTING.md
- ✅ SECURITY.md
- ✅ .env.example

### Por carpeta (Próx sesión)
- ⏳ src/theaia/core/ — README, ROADMAP, CHANGELOG
- ⏳ src/theaia/agents/ — README, ROADMAP, CHANGELOG
- ⏳ src/theaia/adapters/ — README, ROADMAP, CHANGELOG
- ⏳ src/theaia/ml/ — README, ROADMAP, CHANGELOG
- ⏳ src/theaia/tests/ — README, ROADMAP, CHANGELOG
- ⏳ docs/ — architecture.md, agents.md, adapters.md, tests.md, onboarding.md, audit_checklist.md

---

**Última actualización:** 2025-10-31 01:23 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)