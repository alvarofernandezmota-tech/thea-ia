📚 Documentación Central — THEA IA v3.0
Propósito:
Centro neurálgico de toda la documentación técnica, arquitectónica, de auditoría y operativa del ecosistema THEA IA.
Aquí navegas por sesiones, roadmap, arquitectura, seguridad, módulos, testing y checklist de auditoría del proyecto.

🚀 Inicio rápido para colaboradores
¿Nuevo en THEA IA?

Comienza por Onboarding

Revisar Filosofía THEA IA

Consulta Setup local

¿Necesitas auditar o reviewar?

Ve directamente a Checklist de Auditoría

Revisa Security & Compliance

¿Trabajas en un módulo específico?

Módulos y componentes

Cada módulo tiene su propio README, ROADMAP y CHANGELOG

🗂️ Navegación principal
Sección	Descripción	Ruta
Diario de sesiones	Trazabilidad diaria y por hito de trabajo	./diary/DIARY.md
Roadmap maestro	Plan ejecutivo y 17 hitos principales	./roadmap/master.md
Milestones	Objetivos, criterios y métricas por hito	./roadmap/milestones/
Arquitectura	Diagramas, decisiones y componentes clave	./architecture/overview.md
Agentes	Descripción y roles de todos los agentes	./agents/overview.md
Adapters	Integraciones multi-canal y cómo conectarlos	./adapters/overview.md
Testing & QA	Estrategia, localización y ejecución de tests	./testing/index.md
Seguridad	Políticas, controles y auditoría de seguridad	./security/overview.md
Guías y procedimientos	Onboarding, contributing, troubleshooting	./guides/
Módulos & Documentación local	README, ROADMAP, CHANGELOG por carpeta	./modules/
Checklist de auditoría	Auditoría documental, técnica y evidencias	./audit/checklist.md
🏗️ Estructura completa de la documentación
text
docs/
├── README.md (este archivo)
├── diary/
│   └── DIARY.md                    # Trazabilidad temporal, sesiones y hitos
├── roadmap/
│   ├── master.md                   # Plan maestro y 17 hitos
│   ├── milestones/
│   │   ├── milestone_01_setup.md
│   │   ├── milestone_02_core.md
│   │   └── ...
│   └── status.md                   # Estado actual del proyecto
├── architecture/
│   ├── overview.md                 # Visión arquitectónica general
│   ├── core/                       # Núcleo FSM y managers
│   ├── agents/                     # Sistema multi-agente
│   └── data-flow.md                # Flujos de datos principales
├── agents/
│   ├── overview.md                 # Catálogo y roles de agentes
│   ├── agent_agenda.md
│   ├── agent_note.md
│   ├── agent_event.md
│   ├── agent_query.md
│   ├── agent_reminder.md
│   ├── agent_scheduler.md
│   ├── agent_help.md
│   ├── agent_fallback.md
│   └── best_practices.md
├── adapters/
│   ├── overview.md                 # Multi-canal y arquitectura
│   ├── telegram.md
│   ├── rest_api.md
│   ├── whatsapp.md
│   ├── integration_guide.md
│   └── testing_adapters.md
├── testing/
│   ├── index.md                    # Estrategia general y ubicación
│   ├── unit_tests.md               # Guía para tests unitarios
│   ├── integration_tests.md        # Tests de integración
│   ├── e2e_tests.md                # Tests end-to-end
│   ├── coverage_report.md          # Análisis de cobertura
│   └── ci_cd.md                    # Pipeline automático
├── security/
│   ├── overview.md                 # Políticas y protocolo
│   ├── encryption.md               # Gestión de secretos
│   ├── access_control.md           # RBAC y permisos
│   ├── vulnerability_management.md # Incidentes y hardening
│   └── audit_log.md                # Registros de auditoría
├── guides/
│   ├── onboarding.md               # Primeros pasos
│   ├── setup.md                    # Configuración local
│   ├── contributing.md             # Normas de PR y Git Flow
│   ├── troubleshooting.md          # Resolución de problemas
│   ├── faq.md                      # Preguntas frecuentes
│   └── runbooks/                   # Procedimientos operativos
├── modules/
│   ├── core/
│   │   ├── README.md
│   │   ├── ROADMAP.md
│   │   └── CHANGELOG.md
│   ├── agents/
│   │   ├── README.md
│   │   ├── ROADMAP.md
│   │   └── CHANGELOG.md
│   ├── adapters/
│   │   ├── README.md
│   │   ├── ROADMAP.md
│   │   └── CHANGELOG.md
│   ├── ml/
│   │   ├── README.md
│   │   ├── ROADMAP.md
│   │   └── CHANGELOG.md
│   └── tests/
│       ├── README.md
│       ├── ROADMAP.md
│       └── CHANGELOG.md
└── audit/
    ├── checklist.md                # Auditoría documental y técnica
    ├── compliance.md               # Cumplimiento normativo
    └── evidence/                   # Artefactos y PRs vinculados
💡 Filosofía THEA IA
Principios fundamentales
1. Orquestación modular

Cada carpeta en src/theaia/ es un módulo funcional e independiente.

Cada módulo tiene su propio trío: README.md, ROADMAP.md, CHANGELOG.md.

Los módulos se comunican a través de interfaces claras y documentadas.

2. Desarrollo por hitos

El proyecto se estructura en 17 hitos principales y micro-hitos documentados por área.

Cada hito tiene criterios de done claros, métricas y responsables.

El roadmap maestro vincula todos los hitos y su estado actual.

3. Documentación viva

Todo cambio relevante, sesión de trabajo, o tarea queda registrado y vinculado a:

Roadmap maestro y hitos

Diario de sesiones

CHANGELOG global y locales

Artefactos (PRs, commits, archivos generados)

4. Auditoría transversal

La documentación es "fuente de verdad" y cumple estándares profesionales y regulatorios.

Cada PR debe actualizar la documentación de su módulo.

Los cambios transversales se reflejan en el roadmap y changelog global.

5. Trabajo colaborativo y escalable

Máxima transparencia y trazabilidad.

Responsables claros por módulo y hito.

Onboarding técnico y operativo estandarizado.

Checklist de auditoría y compliance automático.

🔄 Convenciones THEA IA
Formato homogéneo por módulo
Cada carpeta funcional (core, agents, adapters, ml, tests, etc.) debe tener:

text
src/theaia/[módulo]/
├── README.md                  # Qué es, cómo usarlo, ejemplos rápidos
├── ROADMAP.md                 # Hitos y micro-tareas del módulo
├── CHANGELOG.md               # Historial de cambios y versiones
├── tests/                     # Tests específicos del módulo (o refs a src/theaia/tests)
└── [código]
Estructura de commits
text
[HITO-XX] [MÓDULO] Descripción breve

- Cambio 1
- Cambio 2

Refs: #PR, roadmap/milestone_XX.md
Actualización de documentación
Cada commit importante actualiza el CHANGELOG local.

Cada hito completado se marca en ROADMAP.md y roadmap maestro.

Cada sesión de trabajo se registra en DIARY.md con fecha y responsable.

📊 Estado actual del proyecto
Componente	Status	Hito	Responsable
Core FSM	✅	2	Álvaro Fernández Mota
Agentes	🟡	5	Equipo Agentes
Adapters	🟡	4	Equipo Adapters
ML/Intent	⏳	7	Equipo ML
Testing Suite	✅	3	QA Team
Docs Extendida	🟡	35 (actual)	Álvaro Fernández Mota
Security & Audit	🟡	6	DevOps/Security
Leyenda: ✅ Completado | 🟡 En progreso | ⏳ Planificado | ❌ Bloqueado

🛠️ Cómo usar esta documentación
Para desarrolladores
Lee ./guides/onboarding.md — Setup, estructura y primeros pasos.

Consulta ./roadmap/master.md — Entiende los hitos y dónde va tu módulo.

Accede a ./modules/ — README, ROADMAP y CHANGELOG de tu área.

Revisa ./testing/index.md — Dónde y cómo testear (src/theaia/tests).

Lee ./guides/contributing.md — Normas de PR y Git Flow.

Para auditores y reviewers
Ve a ./audit/checklist.md — Auditoría documental y técnica.

Revisa ./security/overview.md — Políticas y controles.

Consulta ./roadmap/status.md — Estado actual vs plan.

Accede a ./diary/DIARY.md — Trazabilidad diaria y de cambios.

Para operación y deployment
Revisa ./guides/setup.md — Configuración y deployment.

Lee ./guides/runbooks/ — Procedimientos de operación.

Consulta ./security/ — Secrets, acceso y compliance.

Accede a ./testing/ci_cd.md — Pipeline automático.

🔗 Enlaces rápidos críticos
Setup Local — Primeros pasos de desarrollo

Git Flow & Contributing — Normas de PR y commits

Roadmap Maestro — Plan ejecutivo del proyecto

Arquitectura General — Diagramas y decisiones

Testing & Coverage — Dónde y cómo testear (src/theaia/tests)

Security & Audit — Políticas y compliance

Checklist de Auditoría — Auditoría documental

📝 Mantenimiento y sincronización
Responsabilidades
CEO/Lead: Mantener roadmap maestro, DIARY, y checklist de auditoría.

Cada equipo/módulo: Mantener README, ROADMAP y CHANGELOG propios.

QA/DevOps: Mantener testing.md, security.md, ci_cd.md y compliance.

Todo colaborador: Actualizar CHANGELOG local tras cada PR importante.

Automatización recomendada
Se recomienda implementar scripts que:

Sincronicen roadmap maestro con milestones GitHub.

Generen reportes de cobertura y tests automáticamente.

Verifiquen que todo PR actualiza la documentación de su módulo.

Creen entradas en DIARY automáticamente tras cada merge.

📌 Meta-información
Campo	Valor
Versión	3.0 Session 35
Último actualizado	2025-11-03 (Session 35)
Responsable	Álvaro Fernández Mota (CEO THEA IA)
Status	✅ Activo y en evolución
Contacto	alvarofernandezmota@gmail.com
⚖️ Auditoría y cumplimiento
Este documento centraliza la navegación y filosofía documental de THEA IA.

Sigue el estándar THEA IA: Modular, auditable, escalable.

Cada enlace debe verificarse y actualizarse mensualmente.

Todos los cambios en estructura de docs deben reflejarse aquí y en roadmap maestro.

Cumple con normas de documentación técnica profesional y regulatoria.

Nota final:
Esta documentación es viva y evoluciona con el proyecto. Si encuentras enlaces rotos, información desactualizada o falta alguna sección, abre un issue o crea una PR siguiendo CONTRIBUTING.md.