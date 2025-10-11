ROADMAP DE AUDITORÍA - THEA IA 2.0
Estructura modular profesional:
Todas las carpetas principales y módulos del proyecto se implementan siguiendo esta estructura:

core/: FSM, router, context manager, callbacks, bot factory, documentación y tests

agents/: subcarpetas por agente (agenda, event, note, help, fallback, scheduler, query), con handler, documentación y tests propios

api/: endpoints REST, salud, métricas, documentación

config/: settings, logging config, documentación

database/: modelos SQLAlchemy, migraciones Alembic, repositorios, documentación

models/: modelos de dominio principales, documentación

services/: lógica de negocio por feature, documentación

ml/: intent_detector, entity_extractor, pipelines, models, notebooks, data, documentación, tests modularizados

adapters/: adapters/middleware Telegram, Webhook, documentación

utils/: formatters, validators, exceptions, documentación

tests/: unitarios, integración, e2e, fixtures, documentación y guía testing

scripts/: automatizaciones setup/migraciones/deploy/lint, documentación

Adicional:
deployment/, monitoring/, .github/ (CI/CD), README.md general, changelog, .env, requirements, Dockerfile.

Tabla de tareas, hitos y auditoría
Hora	Fecha	Estado	Tarea / Hito	Responsable	Comentario
09:00	10/10/2025	✔	Crear roadmap.md, changelog.md, README.md principal	Equipo	Documentación apertura del proyecto
09:40	10/10/2025	✔	Auditar y actualizar diccionario_variables.md	Álvaro	Revisión y homogeneización de 7 bloques clave
10:15	10/10/2025	✔	Revisar/actualizar esquemas_database.md según migraciones	Backend	Modelos DB alineados y migrados
10:50	10/10/2025	✔	Crear security.md, architecture.md, faq.md, contributing.md	Equipo	Documentación profesional preparada
11:20	10/10/2025	✔	Crear scripts.md, documentar automatizaciones	DevOps	Scripts e instalación listos
11:45	10/10/2025	✔	Crear migraciones.md, registrar convenciones	DB Admin	Procedimiento migratorio
15:00	11/10/2025	✔	Definir estructura escalada: core, agents, tests, adapters...	Álvaro	Modularidad y onboarding aprobados
15:10	11/10/2025	✔	Validar cambios de nombre, revisión de core y docs de core	Equipo	Estructura profesional/homogeneización y doc de core
15:20	11/10/2025	✔	Auditar y cerrar bloque database	Backend	Estructura, migraciones, tests, README, TESTING; auditoría y escalabilidad listas
16:00-16:32	11/10/2025	✔	Completar y auditar estructura ML	Equipo ML	Modularización pipelines, entidades ML, tests, documentación y reglas en README.md
16:32-17:20	11/10/2025	✔	Auditar y cerrar carpeta models/	Equipo	Validación de modelos por entidad, README.md y TESTING.md, reglas para futuras ampliaciones
17:20-17:56	11/10/2025	✔	Auditar y cerrar carpeta services/	Equipo	Servicios por agente organizados, tests, README, TESTING. Preparada para escalabilidad/documentación
18:00-19:50	11/10/2025	✔	Organización y creación de subcarpetas en tests/	QA	Subcarpetas agents/, ml/, fixtures/, e2e/, core/, database/, services/, utils/ (Solo creadas, NO rellenadas con tests)
20:00	11/10/2025	✔	Actualización e integración del roadmap y changelog	Equipo	Roadmap con hitos y horarios finalizado, reglas de escalabilidad y control auditado
—	—	☐	Crear/Completar README.md y TESTING.md en cada módulo	Todos	Nada pasa sin doc y test propios
—	—	☐	Documentar API, database, models y services	Equipo	Guía y arquitectura modular propia
—	—	☐	Añadir guía global en tests/README.md	QA	Cobertura y ejemplos por feature/módulo
—	—	☐	Revisar onboarding y guías para colaboradores nuevos	Todos	Usar contrib/README y guía por módulo
—	—	☐	Checklist y E2E por core, agents, services, api, ml, utils	Equipo	Scripts y coverage esperados
—	—	☐	Monitorización y dashboards (monitoring/, Prometheus/Grafana)	DevOps	Seguimiento, alertas y trazabilidad
—	—	☐	Actualizar ADRs, tests y roadmap cada sprint	Todos	Reflejar cambios y doc por equipo
—	—	☐	Auditoría final, revisión modular y doc/test	Todos	Validar cada feature/módulo antes de release
Regla crítica de escalado y documentación
Ningún módulo o funcionalidad pasa a producción, test o roadmap principal sin:

Su propio README.md explicando función, arquitectura y cómo usar/importar.

Su propio TESTING.md con guía e indicadores claros, casos mínimos e integración/e2e si aplica.

Este control es bloqueante en auditorías, sprints y releases.
El roadmap se actualiza con responsables, fechas y estado por módulo/documento revisado.

Notas clave:

Todas las subcarpetas en tests/ han sido creadas, pero no rellenadas con pruebas.

Estructura, modularidad, documentación y control auditado hasta este punto.

