Thea IA 3.0 — Documentación Técnica y Auditoría
Última actualización: 2025-11-03
Autor principal: Álvaro Fernández Mota

Índice
Visión y contexto del proyecto

Características funcionales y arquitectura

Detalle de módulos y estructura de carpetas

Instalación avanzada y despliegue

FSM y orquestación multiagente

Stack tecnológico y dependencias críticas

Testing, QA y cobertura

Seguridad, privacidad y compliance

Planificación, auditoría y roadmap

Política de contribución y documentación interna

Licencia, contacto y créditos

1. Visión y contexto
Thea IA es una plataforma conversacional modular pensada para equipos/business, que integra IA, FSM, NLP y multiagente, con núcleo auditable y extensible para automatización de tareas, eventos y workflows empresariales y personales.

2. Características y arquitectura
FSM inteligente, desambiguación y agentes orquestados.

Detección de intenciones ML + reglas; NLP (spaCy, custom).

Integraciones: Telegram, webhooks, API REST, WhatsApp.

Métricas y logging exhaustivo—monitorización Prometheus y Grafana.

Persistencia y migración industrial: PostgreSQL, Alembic, Redis.

Containerización, CI/CD, DevOps y compliance integrados.

3. Estructura general del proyecto
text
theaia/
├── src/theaia/core/          # Núcleo FSM, state machine, context manager
├── src/theaia/agents/        # Agentes verticales multi-fase
├── src/theaia/adapters/      # Soporte multicanal y webhooks
├── src/theaia/ml/            # Modelos y pipelines NLP/ML
├── src/theaia/tests/         # Unittest, integración, e2e (README y TESTING.md)
├── scripts/                  # Automatización y pipelines
├── docs/                     # Esta documentación extendida y cross-linking
├── .env.example              # Config auditada y comentada
├── SECURITY.md               # Política seguridad avanzada
├── ROADMAP.md                # Hitos y despliegue actual
├── CHANGELOG.md              # Cambios y referencias cruzadas
├── onboarding.md             # Guía para incorporaciones nuevas
└── ...
4. Instalación & despliegue avanzado
Requerido: Python 3.11+, Postgres 14+, Redis, Docker, Git.

Setup recomendado:

make setup para entorno virtual

Edición de .env según ejemplo

docker-compose up -d y make migrate para BBDD

Uso recomendado de Makefile para flujos frecuentes

5. FSM & Orquestación Multiagente
[docs/fsm.md]: Fundamentos y API de la máquina de estados, gestión de sesiones, timeouts y fallback handler.

Submódulos documentados: conversation_manager.py, state_machine.py, maps de intents y agentes.

6. Stack y dependencias técnicas
Backend/Core: Python 3.11+, FastAPI, SQLAlchemy, Alembic, Transitions

ML/NLP: spaCy, scikit-learn, Transformers

Integraciones: aiogram, aiohttp, WebSockets

Infraestructura: Docker, Kubernetes (amaduración), Prometheus/Grafana para monitoreo, Terraform

7. Testing, QA y cobertura
Unittest, integración y e2e: pytest, coverage, casos en src/theaia/tests/

Scripts de automatización: make test, make lint, make format

Guía de testing: [docs/tests.md], [docs/test_strategies.md]

8. Seguridad, privacidad y compliance
Gestión exhaustiva de .env, compliance con GDPR y mejores prácticas DevSecOps

Checks de hardening y control de acceso en [SECURITY.md], [docs/audit_checklist.md]

Proceso de auditoría avanzada: backups, logging seguro, protocolo de incidentes

Política de repositorio privado en fases críticas

9. Planificación, auditoría y roadmap
Documentos clave:

Plan Auditoría Completo

ROADMAP.md

CHANGELOG.md

DIARY.md

Sesiones, responsables y avance por milestone referenciado

10. Contribución y documentación
Política detallada: [docs/contributing.md]

Checklist y convenciones: PR, test mínimo, cobertura y aprobación técnica/auditora

README, roadmap y changelog obligatorio/local en cada módulo

11. Licencia y contacto
Licencia MIT, uso e integración libre con atribución

Contacto principal: Álvaro Fernández Mota (alvarofernandezmota-tech)

REF cross-linking (guías especializadas)
[fsm.md]: FSM y lógica conversacional avanzada

[agents.md]: Detalle de agentes y estados

[ml.md]: Modelos, pipelines y métricas

[adapters.md]: Integraciones multicanal y API hooks

[tests.md]: Estrategias y cobertura

[onboarding.md]: Proceso alta equipo nuevo

[audit_checklist.md]: Auditoría ciberseguridad y revisión

[security.md]: Política y respuesta incidentes