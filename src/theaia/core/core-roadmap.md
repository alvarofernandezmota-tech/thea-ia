ROADMAP — Core THEA IA
Versión actual: v0.14.0
Actualización: 2025-11-10 14:41 CET (S38)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Modelo: Hitos con fechas/horas estimadas

🎯 HITOS CLAVE (Q4 2025 - Q2 2026)
H01: Consolidar Context & ContextManager
Fecha estimada: 2025-11-20 10:00 CET
Duración: 2-3 horas
Estado: 🟡 Planificado

Descripción:
Unificar context.py + context_manager.py en una sola abstracción clara:

Crear CoreContext que absorba ambas funcionalidades

Deprecate context.py (keep backward compat)

Actualizar router para usar CoreContext

Tests unitarios para migración

Entregables:

 Clase CoreContext creada

 Router actualizado

 Tests migración

 Backward compatibility maintained

 Docs actualizada

Commit: [H01] refactor: Consolidar context managers

H02: Persistencia Context en BD
Fecha estimada: 2025-12-05 09:00 CET
Duración: 4-5 horas
Estado: 🟡 Planificado (después H01)

Descripción:
Trasladar contextos de memoria a BD (PostgreSQL):

Guardar UserContext en contexts table

Recuperar al iniciar sesión

Sincronización automática post-acción

TTL para limpiar contextos viejos

Entregables:

 Migration Alembic creada

 Repository para contextos

 SessionManager actualizado

 Tests BD

 Docs BD

Commit: [H02] feat: Persistencia contextos en BD

H03: Tests Coverage >85%
Fecha estimada: 2025-12-20 10:00 CET
Duración: 6-8 horas
Estado: 🟡 Planificado

Descripción:
Aumentar cobertura de tests en core/ de 65% → 85%:

Tests para router (flujos completos)

Tests para context managers (edge cases)

Tests para FSM transitions

Tests para callbacks

Tests para error handling

Métricas objetivo:

router.py: 90%+ coverage

context*.py: 85%+ coverage

fsm/: 80%+ coverage

Overall core/: 85%+

Entregables:

 40+ tests nuevos

 Coverage report >85%

 CI/CD actualizado

 Docs testing

Commit: [H03] test: Aumentar coverage core/ a 85%

H04: FSM v2 — Estados Anidados
Fecha estimada: 2026-01-15 09:00 CET
Duración: 8-10 horas
Estado: 🟡 Planificado (después H02)

Descripción:
Mejorar FSM con soporte para estados anidados:

Substates dentro de states principales

Callbacks on_enter/on_exit por estado

Rollback automático en errors

Transiciones condicionales

Timeout automático en estados

Ejemplo:

text
STATE.AGENDA
  ├─ SUBSTATE.AWAITING_DATE
  ├─ SUBSTATE.AWAITING_TIME
  └─ SUBSTATE.CONFIRMING
Entregables:

 FSM v2 engine

 Soporte substates

 Callbacks avanzados

 Transiciones condicionales

 Tests completos

 Migración de v1 → v2

Commit: [H04] feat: FSM v2 with nested states

H05: Multi-idioma Native
Fecha estimada: 2026-02-28 10:00 CET
Duración: 10-12 horas
Estado: ⏳ Backlog

Descripción:
Soporte nativo para múltiples idiomas:

Español (ES) ✅ Ya soportado

Inglés (EN) 🟡 A implementar

Francés (FR) 🟡 A implementar

Detección automática de idioma

Context translation entre idiomas

ML models por idioma

Entregables:

 Intent detector multiidioma

 Entity extractor multiidioma

 Language detector

 Context translator

 Tests multiidioma

 Docs i18n

Commit: [H05] feat: Multi-language support (ES/EN/FR)

H06: Performance Optimization
Fecha estimada: 2026-04-10 11:00 CET
Duración: 8-10 horas
Estado: ⏳ Backlog

Descripción:
Optimizar performance core/:

Caché inteligente de intents (reducir latencia 50%)

Async/await en router

Connection pooling BD

Lazy loading de agentes

Benchmarking

Objetivos:

Latencia: <100ms (actual: ~200ms)

Throughput: 100+ req/s

Memory: <50MB por 1000 usuarios

Entregables:

 Caché implementation

 Async refactor

 Benchmarks

 Monitoring dashboards

 Performance docs

Commit: [H06] perf: Optimizaciones core (latencia -50%)

📋 BACKLOG CORTO PLAZO (Próximas 2 semanas)
Inmediato (2025-11-15)
 Ejecutar tests core/ completos

 Verificar que no hay broken imports post-eliminación

 Actualizar imports en router.py

 CI/CD pipeline validar

Próximos 5 días (2025-11-20)
 Code review limpieza archivos

 Merge a main

 Deploy a staging

 Smoke tests en staging

Próximas 2 semanas (2025-11-25)
 Inicio H01 (consolidar contexts)

 Planificar H02 (BD)

🔗 Dependencias Entre Hitos
text
H01 (Context consolidation)
  └─→ H02 (BD persistence)
        └─→ H03 (Tests coverage)
              └─→ H04 (FSM v2)
                    └─→ H05 (Multi-idioma)
                          └─→ H06 (Performance)
📊 Estimaciones de Esfuerzo
Hito	Horas	Días	Prioridad	Bloqueantes
H01	2-3	1	🔴 Alta	Ninguno
H02	4-5	1	🔴 Alta	H01
H03	6-8	1-2	🟡 Media	H02
H04	8-10	2	🟡 Media	H02
H05	10-12	2-3	🟢 Baja	H03
H06	8-10	2	🟢 Baja	H03
TOTAL	38-48	10		
🎯 KPIs & Métricas
Actuales (v0.14.0 — 2025-11-10)
Latencia promedio: ~200ms

Tests coverage: 65%

Intenciones soportadas: 8

Idiomas: 1 (ES)

Usuarios concurrentes: <10

Objetivo Q1 2026
Latencia promedio: <100ms ↓50%

Tests coverage: >85% ↑20%

Intenciones soportadas: 12 ↑4

Idiomas: 3 (ES/EN/FR) ↑2

Usuarios concurrentes: 100+ ↑10x

Uptime: 99.9%

📅 Timeline Visual
text
NOV 2025
├─ 10-15: Limpieza legacy (DONE S38)
├─ 15-20: H01 Consolidar contexts
├─ 20-30: H02 BD persistence
│
DIC 2025
├─ 01-10: H03 Tests coverage
├─ 10-20: H04 FSM v2 (inicio)
├─ 20-31: Testing & debug
│
ENE 2026
├─ 01-15: H04 FSM v2 (finalizar)
├─ 15-31: H05 Multi-idioma (inicio)
│
FEB 2026
├─ 01-28: H05 Multi-idioma (finalizar)
│
MAR 2026
├─ 01-31: H06 Performance
│
ABR 2026
├─ 01-10: Finalizar Q1 goals
├─ 10-30: Release v0.15.0 (major)
🚀 Release Notes Futuros
v0.15.0 (Abril 2026) — "Enterprise Ready"
FSM v2 con substates

BD persistence

Multi-idioma

Tests >85%

Performance -50%

v1.0.0 (Julio 2026) — "Production Release"
Stable API

Full docs

Migration guides

Enterprise support

📞 Contacto
Responsable: Álvaro Fernández Mota
Team: THEA IA Core Developers
Slack: #thea-core-roadmap

Última actualización: 2025-11-10 14:41 CET (S38)
Próxima revisión: 2025-11-20 (post H01)