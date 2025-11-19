ROADMAP — THEA IA (Raíz)
Proyecto: THEA IA
Actualizado por: Álvaro Fernández Mota (CEO THEA IA)
Última actualización: 2025-11-16 00:23 CET

⚠️ IMPORTANTE
El roadmap general orquesta los 17 hitos grandes y todos los micro-hitos del ecosistema THEA IA.

Cada área/carpeta tiene su propio roadmap y guía extendida, enlazada desde aquí para panel de auditoría y equipo.

Debe mantenerse actualizado por cada responsable y reflejar estado, porcentaje completado, dependencias y fechas clave.

🟩 Hitos principales (17)
H01: Organización y compatibilidad de tests, core y ecosistema ✅ COMPLETADO
Estructura carpetas, tests unitarios/integración/e2e, FSM base, pytest

README/ROADMAP/CHANGELOG por carpeta

Tests pasan 100%, coverage ≥80%

Docker básico implementado (Dockerfile, docker-compose.yml)

Completado: 2025-10-31

Horas reales: 53.3h en 15 sesiones

Ver detalle H01

H02: Database Layer & Telegram Adapter ✅ CORE COMPLETADO (70%)
✅ PostgreSQL Database Layer completo (7 modelos, 6 repositories, multi-tenant)

✅ TelegramAdapter funcional con persistencia

✅ Primera conversación real guardada (Usuario Entu, 12 nov 17:02)

✅ Migraciones Alembic operativas

✅ 12/12 tests database pasando

⏸️ Web Client → Aplazado a Post-H05

⏸️ OAuth2/JWT → Aplazado a H08

⏸️ Tests E2E completos → Aplazado a H07

Completado (core): 2025-11-12

Horas reales: 4h 17min (3h 57min core)

Decisión estratégica: Database Layer adelantado de H04 a H02

Ver detalle H02

H03: Agent Configuration & Entity Extraction ✅ COMPLETADO (100%)
🎉 COMPLETADO 15-16 Nov 2025

AgentConfig System:

✅ AgentConfig class implemented (38 statements, 100% coverage)

✅ Predefined configs for all 6 agents

✅ Intent management (add/remove/check)

✅ Serialization support (to_dict/from_dict)

✅ 15 unit tests passing

Entity Extraction Suite:

✅ DateTimeExtractor (75 statements, 91% coverage, 15 tests)

Relative dates, weekdays, time formats

Spanish language support complete

✅ LocationExtractor (39 statements, 100% coverage, 18 tests)

35+ Spanish cities, location types

Preposition pattern recognition

✅ PersonNameExtractor (48 statements, 98% coverage, 18 tests)

35+ common Spanish names, titles

Context-aware extraction

E2E Test Suites:

✅ AgendaAgent E2E (17 tests) - complete lifecycle

✅ NoteAgent E2E (14 tests) - CRUD + categories/tags

✅ ReminderAgent E2E (15 tests) - time-based + location

Test Suite:

✅ 173 tests total (+86 new tests)

✅ 50% coverage achieved (target met!)

✅ 100% pass rate (0 failures, 0 skips)

✅ ~8 seconds execution time

Documentation:

✅ 6 test README files updated/created

✅ Complete test documentation suite

✅ Testing guide updated

Completado: 2025-11-16

Horas reales: 7h 20min

Estado: 100% COMPLETADO ✅

Ver detalle H03

H04: Persistencia Avanzada & Optimizaciones ⏸️ PARCIALMENTE ADELANTADO
⚠️ Core adelantado y completado en H02

Pendiente: Optimizaciones queries, fallback JSON, coverage ≥85%

Modelos adicionales según necesidades H03-H05

Deadline: 2025-11-25

Horas restantes: 40h (reducido de 48h originales)

Nota: Database base ya operativo desde H02

H05: Agentes Verticales Inteligentes ⏳ PRÓXIMO
Agentes con arquitectura híbrida (Reglas + spaCy + LLM)

AgendaAgent, NotesAgent, EventsAgent, QueryAgent

Integración LLM básica para queries complejas

Tests e2e por agente

Deadline: 2025-12-05

Horas estimadas: 78h en 3-4 sesiones

Arquitectura nueva: 3 niveles (14 nov 2025)

H06: ML/NLP Pipelines & Arquitectura Híbrida LLM
Intent detector spaCy

Entity extractor mejorado

LangChain para agentes autónomos

RAG para conocimiento THEA IA

Sistema caching LLM

Deadline: 2025-12-10

Horas estimadas: 84h en 3-4 sesiones

Decisión: Arquitectura híbrida inteligente (14 nov)

H07: E2E Tests & QA Completo
Tests e2e Telegram completos (pendientes H02)

Tests e2e agentes inteligentes

Tests e2e ML/NLP pipelines

Coverage ≥90% global

Performance benchmarks

Deadline: 2025-12-15

Horas estimadas: 62h en 2-3 sesiones

H08: Multi-empresa RBAC & Web Client
RBAC completo multi-tenant

Web Client completo (aplazado de H02)

OAuth2/JWT (aplazado de H02)

Authorization middleware

Deadline: 2026-01-10

Horas estimadas: 86h en 3-4 sesiones

Nota: Multi-tenant base ya en H02

H09: Docker/K8s Optimización & CI/CD
Dockerfiles optimizados producción (base ya existe)

K8s manifests completos

CI/CD pipelines GitHub Actions

Deployment strategy automatizada

Deadline: 2026-01-20

Horas estimadas: 52h en 2-3 sesiones

Nota: Docker básico ya implementado en H01

H10: WhatsApp & REST API
WhatsApp adapter (patrón TelegramAdapter)

REST API pública OpenAPI 3.1

Webhooks WhatsApp

Deadline: 2026-02-01

Horas estimadas: 56h en 2-3 sesiones

H11: Observabilidad Stack Completo
Prometheus exporters

Grafana dashboards operacionales

Loki log aggregation

Jaeger distributed tracing

Alerting configurado

Deadline: 2026-02-15

Horas estimadas: 52h en 2 sesiones

H12: Integraciones Externas
Slack adapter

Teams adapter

Google Calendar sync

Notion integration

Deadline: 2026-03-01

Horas estimadas: 56h en 2-3 sesiones

H13: Seguridad & Hardening Enterprise
Security audit profesional

SOC 2 Type II compliance

Penetration testing

Vulnerability fixes

Deadline: 2026-03-15

Horas estimadas: 60h en 2-3 sesiones

H14: Onboarding Profesional & Documentación
Onboarding guide completo

Video training

Runbooks operativos

FAQ & troubleshooting

Deadline: 2026-04-01

Horas estimadas: 58h en 2-3 sesiones

H15: Performance & Stress Testing
Load testing suite

Performance optimization

Stress testing results

Benchmarks documentados

Deadline: 2026-04-20

Horas estimadas: 44h en 2 sesiones

H16: Plugins & Customización
Plugin architecture

SDK development

Example plugins

Deadline: 2026-05-10

Horas estimadas: 46h en 2 sesiones

H17: Auditoría Final & Go-Live
Final audit completo

Release checklist

Deployment & go-live

Post-launch monitoring

Deadline: 2026-06-01

Horas estimadas: 50h en 2 sesiones

📅 Fases y fechas críticas (Actualizado 2025-11-16)
Fase 1: Core y FSM — ✅ COMPLETADA (2025-10-08 ~ 2025-10-31)
H01: Tests, core, FSM, documentación raíz ✅

Horas reales: 53.3h

Fase 2: Multi-agente y adaptadores — 🔄 EN CURSO (2025-11-01 ~ 2025-12-15) — 21% completado
H02: Database + Telegram ✅ (core 70% completado)

H03: Agent Config & Entity Extraction ✅ (100% completado)

H04: Persistencia avanzada ⏸️ (~50% adelantado en H02)

H05: Agentes inteligentes ⏳ (próximo)

H06: ML/NLP arquitectura híbrida ⏳

H07: E2E Tests completos ⏳

Horas completadas: 64.9h / ~490h estimadas

Fase 3: Infraestructura, observabilidad y seguridad — ⏳ PRÓXIMA (2025-12-16 ~ 2026-04-01)
H08: Multi-empresa RBAC + Web (incluye componentes H02)

H09: Docker/K8s optimización

H10: WhatsApp + REST API

H11: Observabilidad

H12: Integraciones externas

H13: Seguridad enterprise

H14: Onboarding profesional

Horas estimadas: ~420h

Fase 4: Escalabilidad, customización y release — ⏳ FUTURA (2026-04-01 ~ 2026-06-01)
H15: Performance & stress testing

H16: Plugins & customización

H17: Auditoría final y go-live

Horas estimadas: ~140h

Total proyecto: 947.6h estimadas (~28 semanas)
Completado hasta ahora: 64.9h (7%)

🎯 Decisiones Estratégicas Recientes
1. Adelanto Database Layer (11 nov 2025)
Decisión: Implementar PostgreSQL en H02 en lugar de H04

Razón: Establecer arquitectura multi-tenant desde el principio

Impacto: Adelanta 2 hitos la persistencia empresarial

Resultado: ✅ Arquitectura multi-tenant operativa desde día 1

2. Aplazamiento Web Client & OAuth2 (12 nov 2025)
Decisión: Posponer Web Client y OAuth2 de H02 a H05-H08

Razón: Priorizar conversaciones funcionales vía Telegram

Impacto: H02 cierra como "Core 70%" con componentes documentados

Resultado: ✅ Primera conversación real funcional

3. Arquitectura Híbrida LLM (14 nov 2025)
Decisión: Integrar 3 niveles (Reglas + spaCy + LLM) en H05-H06

Razón: Agentes actuales carecen de inteligencia competitiva

Impacto: H05 +20h, H06 +38h, experiencia usuario 8.5/10

Costo: $100-200/mes, mantenimiento Medio-Bajo

4. Agent Configuration & Entity Extraction (15-16 nov 2025)
Decisión: Complete Phase 3 en 1 sesión intensiva (7h 20min)

Razón: Establecer fundamentos NLP antes de agentes inteligentes

Impacto: +86 tests, 50% coverage, 3 extractors funcionales

Resultado: ✅ Fundamentos completos para H05-H06

📊 Progreso por Hito
Hito	Estado	Horas Est.	Horas Reales	Completado	Notas
H01	✅	20h	53.3h	100%	Completado 31 oct
H02	✅ 70%	18h	4.3h	70%	Core: Database + Telegram
H03	✅	66h	7.3h	100%	Complete 16 nov
H04	⏸️ 50%	48h	-	~50%	Parcialmente en H02
H05	⏳	78h	-	0%	Próximo - +Arquitectura LLM
H06	⏳	84h	-	0%	+LangChain, RAG
H07	⏳	62h	-	0%	+Tests H02 pendientes
H08-H17	⏳	555.3h	-	0%	Planificados 2026
🛡️ Auditoría y panel de equipo
Todos los hitos y cambios están reflejados en el CHANGELOG general y por carpeta

Checklist de auditoría extendida en docs/audit/ y docs/roadmap de cada área

Panel de avance y dependencias aquí y en cada README/roadmap

Diarios de sesiones actualizados en docs/diary/

Documentación detallada:

Roadmap Maestro — Tracking operativo H01-H17

H01 Milestone — Completado

H02 Milestone — Core completado, componentes aplazados

H03 Milestone — ✅ Complete

H03-H17 Milestones — Planificación completa

Diario Noviembre — Sesiones 1-10

🔗 Enlaces Relacionados
CHANGELOG.md — Historial de versiones

README.md — Guía principal del proyecto

CONTRIBUTING.md — Guía de contribución

SECURITY.md — Política de seguridad

docs/ — Documentación técnica completa

📝 Mantén este roadmap vivo
Actualízalo tras cada release de hito/versión, micro-hito importante o cambio estructural.

Así, todas las auditorías y equipos de THEA IA tienen acceso inmediato a la planificación y estado real del ecosistema.

Última actualización: 16 Nov 2025, 00:23 CET
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado actual: H01 ✅ | H02 ✅ (70%) | H03 ✅ COMPLETADO (100%) | H04-H05 ⏳ PRÓXIMOS