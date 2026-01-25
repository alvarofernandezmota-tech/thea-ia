ROADMAP — THEA IA (Raíz)
Proyecto: THEA IA
Actualizado por: Álvaro Fernández Mota (CEO THEA IA)
Última actualización: 2026-01-25 18:49 CET

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

H09: Real Ecosystem - AgendaAgent 🟡 EN CURSO (75% COMPLETADO)
🟡 UPDATED: 25 Enero 2026, 18:49 CET

Estado: 75% completado (45h/75h invertidas)

Tests: 40/81 pasando (50% coverage)

Target cierre: 2 Febrero 2026

✅ COMPLETADO:

✅ Groq LLM Integration (100%) - 15h

Tool calling, intent extraction, entity extraction

llama-3.3-70b-versatile model

16 tests pasando, 100% coverage

✅ BookingAgent (100%) - 12h

100% conversational AI (LLM-based)

Tool integration (create, check, cancel, list)

Spanish language support

Decisión: Conversational > FSM (mejor UX)

✅ Database Services (85%) - 10h

UserService, BookingService, AvailabilityEngine

Multi-tenant architecture

Repository Pattern aplazado a H10

✅ Telegram Bot Base (70%) - 8h

Conversational message handling

User auto-registration

BookingAgent integration

Pending: Commands + Menu

🔴 PENDIENTE (26 Enero - 2 Febrero):

🔴 Google Calendar API (CRÍTICO) - 12-15h

OAuth2 authentication

Bi-directional sync

Event CRUD operations

Target: 30 Enero

🟡 Command Handlers + Menu (ALTA) - 8-10h

6 comandos (/start, /help, /mis_citas, etc.)

Interactive keyboards (5 menus)

Callback handlers

Target: 1 Febrero

🟢 Tests E2E Completos (MEDIA) - 6-8h

15 tests Google Calendar

18 tests commands

8 tests menu flow

Target: 2 Febrero

Decisiones Arquitectónicas:

Conversational > FSM (mejor UX, más flexible)

Repository Pattern → Aplazado a H10 (no crítico)

Híbrido Commands + Conversation (mejor experiencia)

Horas totales: 71-78h (ajustado de 75h)

Deadline actualizado: 2 Febrero 2026

Ver detalle H09

H10: WhatsApp & REST API
WhatsApp adapter (patrón TelegramAdapter)

REST API pública OpenAPI 3.1

Webhooks WhatsApp

Deadline: 2026-02-15

Horas estimadas: 56h en 2-3 sesiones

H11: Observabilidad Stack Completo
Prometheus exporters

Grafana dashboards operacionales

Loki log aggregation

Jaeger distributed tracing

Alerting configurado

Deadline: 2026-02-28

Horas estimadas: 52h en 2 sesiones

H12: Integraciones Externas
Slack adapter

Teams adapter

Google Calendar sync

Notion integration

Deadline: 2026-03-15

Horas estimadas: 56h en 2-3 sesiones

H13: Seguridad & Hardening Enterprise
Security audit profesional

SOC 2 Type II compliance

Penetration testing

Vulnerability fixes

Deadline: 2026-03-31

Horas estimadas: 60h en 2-3 sesiones

H14: Onboarding Profesional & Documentación
Onboarding guide completo

Video training

Runbooks operativos

FAQ & troubleshooting

Deadline: 2026-04-15

Horas estimadas: 58h en 2-3 sesiones

H15: Performance & Stress Testing
Load testing suite

Performance optimization

Stress testing results

Benchmarks documentados

Deadline: 2026-05-05

Horas estimadas: 44h en 2 sesiones

H16: Plugins & Customización
Plugin architecture

SDK development

Example plugins

Deadline: 2026-05-25

Horas estimadas: 46h en 2 sesiones

H17: Auditoría Final & Go-Live
Final audit completo

Release checklist

Deployment & go-live

Post-launch monitoring

Deadline: 2026-06-15

Horas estimadas: 50h en 2 sesiones

📅 Fases y fechas críticas (Actualizado 2026-01-25)
Fase 1: Core y FSM — ✅ COMPLETADA (2025-10-08 ~ 2025-10-31)
H01: Tests, core, FSM, documentación raíz ✅

Horas reales: 53.3h

Fase 2: Multi-agente y adaptadores — 🔄 EN CURSO (2025-11-01 ~ 2026-02-15) — 30% completado
H02: Database + Telegram ✅ (core 70% completado)

H03: Agent Config & Entity Extraction ✅ (100% completado)

H04: Persistencia avanzada ⏸️ (~50% adelantado en H02)

H05: Agentes inteligentes ⏳ (aplazado)

H06: ML/NLP arquitectura híbrida ⏳ (aplazado)

H07: E2E Tests completos ⏳ (aplazado)

H09: Real Ecosystem AgendaAgent 🟡 (75% EN CURSO) ✨ NUEVO

Horas completadas: 109.9h / ~550h estimadas

Fase 3: Infraestructura, observabilidad y seguridad — ⏳ PRÓXIMA (2026-02-15 ~ 2026-04-15)
H08: Multi-empresa RBAC + Web (incluye componentes H02)

H10: WhatsApp + REST API

H11: Observabilidad

H12: Integraciones externas

H13: Seguridad enterprise

H14: Onboarding profesional

Horas estimadas: ~368h

Fase 4: Escalabilidad, customización y release — ⏳ FUTURA (2026-04-15 ~ 2026-06-15)
H15: Performance & stress testing

H16: Plugins & customización

H17: Auditoría final y go-live

Horas estimadas: ~140h

Total proyecto: 947.6h estimadas (~28 semanas)
Completado hasta ahora: 109.9h (11.6%) ✨ UPDATED

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

5. H09 Real Ecosystem - AgendaAgent (06-25 ene 2026) ✨ NUEVO
Decisión: Crear primer agente funcional completo (Telegram + DB + Google Calendar + LLM)

Razón: Probar arquitectura completa end-to-end

Impacto: Primera prueba real del ecosistema

Progreso: 75% completado (45h/75h)

Pendiente: Google Calendar API (crítico), Commands + Menu

6. Conversational > FSM (enero 2026) ✨ NUEVO
Decisión: BookingAgent 100% conversacional (LLM-based) en lugar de FSM

Razón: Mejor UX, más flexible, interacciones naturales

Impacto: Trade-off: Más flexible pero requiere LLM activo (costo)

Resultado: ✅ Mantenido - Mejor experiencia de usuario

7. Repository Pattern → H10 (enero 2026) ✨ NUEVO
Decisión: Aplazar Repository Pattern de H09 a H10

Razón: Services directos funcionan bien, no crítico para funcionalidad

Impacto: Ahorra 6-8h en H09, puede refactorizar después si necesario

Resultado: ⚪ Neutral - Enfoque en features críticos primero

📊 Progreso por Hito (Actualizado 25 Enero 2026)
Hito	Estado	Horas Est.	Horas Reales	Completado	Notas
H01	✅	20h	53.3h	100%	Completado 31 oct
H02	✅ 70%	18h	4.3h	70%	Core: Database + Telegram
H03	✅	66h	7.3h	100%	Complete 16 nov
H04	⏸️ 50%	48h	-	~50%	Parcialmente en H02
H05	⏳	78h	-	0%	Aplazado - +Arquitectura LLM
H06	⏳	84h	-	0%	+LangChain, RAG
H07	⏳	62h	-	0%	+Tests H02 pendientes
H09	🟡 75%	75h	45h	75%	✨ EN CURSO - Cierre 2 Feb
H08-H17	⏳	541.3h	-	0%	Planificados 2026
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

H09 Milestone — ✨ 75% Complete - En cierre

H03-H17 Milestones — Planificación completa

Diario Enero 2026 — Sesiones H09

🔗 Enlaces Relacionados
CHANGELOG.md — Historial de versiones

README.md — Guía principal del proyecto

CONTRIBUTING.md — Guía de contribución

SECURITY.md — Política de seguridad

docs/ — Documentación técnica completa

📝 Mantén este roadmap vivo
Actualízalo tras cada release de hito/versión, micro-hito importante o cambio estructural.

Así, todas las auditorías y equipos de THEA IA tienen acceso inmediato a la planificación y estado real del ecosistema.

Última actualización: 25 Ene 2026, 18:49 CET
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado actual: H01 ✅ | H02 ✅ (70%) | H03 ✅ (100%) | H09 🟡 (75% - EN CIERRE) | H04-H08, H10-H17 ⏳ PLANIFICADOS