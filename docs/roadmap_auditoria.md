ROADMAP DE AUDITORÍA - THEA IA 2.0
Estructura modular profesional
Toda carpeta principal y módulo del proyecto se implementará siguiendo esta estructura:

core/: FSM, router, context manager, callbacks, bot factory, doc y tests

agents/: subcarpetas por agente (agenda, event, note, help, fallback, scheduler, query), con handler, doc y tests propios

api/: endpoints REST, salud, métricas, doc

config/: settings, logging config, doc

database/: modelos SQLAlchemy, migraciones Alembic, repositorios, doc

models/: modelos de dominio principales, doc

services/: lógica de negocio por feature, doc

ml/: intent_detector, entity_extractor, pipelines, models, notebooks, data, doc, tests modularizados

adapters/: adapters/middleware Telegram, Webhook, doc

utils/: formatters, validators, exceptions, doc

tests/: unitarios, integración, e2e, fixtures, doc y guía testing

scripts/: automatizaciones setup/migraciones/deploy/lint, doc

Además:
deployment/, monitoring/, .github/ (CI/CD), README.md general, changelog, env, requirements, Dockerfile, etc.

Tabla de tareas, hitos y auditoría
Estado	Tarea / Hito	Responsable	Comentario	Fecha
✔	Crear roadmap.md, changelog.md, README.md principal	Equipo	Documentación apertura proyecto	10/10/2025
✔	Auditar y actualizar diccionario_variables.md (7 bloques)	Álvaro	Completado	10/10/2025
✔	Revisar/actualizar esquemas_database.md según migraciones	Backend	Modelos DB alineados y migrados	10/10/2025
✔	Crear security.md, architecture.md, faq.md, contributing.md	Equipo	Documentación profesional lista	10/10/2025
✔	Crear scripts.md, documentar automatizaciones	DevOps	Scripts e instalación listos	10/10/2025
✔	Crear migraciones.md, registrar convenciones	DB Admin	Procedimiento migratorio	10/10/2025
✔	Definir estructura escalada: core, agents, tests, adapters...	Álvaro	Modularidad y onboarding aprobados	11/10/2025
✔	Validar cambios de nombre, revisión de core y docs de core (README.md/TESTING.md)	Equipo	Estructura profesional, homogeneización y doc de core	11/10/2025
✔	Auditar y cerrar bloque database (estructura, migraciones, tests, README, TESTING)	Backend	Auditoría y escalabilidad listas	11/10/2025
✔	Completar y auditar estructura ML: modularización, datasets, pipelines, tests y documentación	Equipo ML	Carpeta ML lista para implementación, auditoría y tests	11/10/2025
☐	Crear/Completar README.md y TESTING.md en cada módulo	Todos	Nada pasa sin doc y test propios	—
☐	Documentar API, database, models y services	Equipo	Guía y arquitectura modular propia	—
☐	Añadir guía global en tests/README.md	QA	Cobertura y ejemplos por feature/módulo	—
☐	Revisar onboarding y guías para colaboradores nuevos	Todos	Usar contrib/README y guía por módulo	—
☐	Checklist y E2E por core, agents, services, api, ml, utils	QA/Equipo	Scripts y coverage esperados	—
☐	Monitorización y dashboards (monitoring/, Prometheus/Grafana)	DevOps	Seguimiento, alertas y trazabilidad	—
☐	Actualizar ADRs, tests y roadmap cada sprint	Todos	Reflejar cambios y doc por equipo	—
☐	Auditoría final, revisión modular y doc/test	Todos	Validar cada feature/módulo antes de release	—
REGLA CRÍTICA DE ESCALADO Y DOCUMENTACIÓN
Ningún módulo o funcionalidad pasa a producción, test o roadmap principal sin:

Su propio README.md explicando función, arquitectura y cómo usar/importar.

Su propio TESTING.md con guía e indicadores claros, casos mínimos e integración/e2e si aplica.

Este control es bloqueante en auditorías, sprints y releases.
El roadmap de auditoría se actualiza con responsables, fechas y estado por módulo/documento revisado.

