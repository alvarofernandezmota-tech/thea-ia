# 📋 Decisiones Arquitectónicas — THEA IA (ADRs)

**Versión:** v0.14.0  
**Generadas:** 2025-10-31 03:19 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## ADR-001: FSM Engine vs Event-Driven Architecture

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-08  
**Contexto:**  
THEA IA necesita orquestar flujos conversacionales complejos con múltiples agentes, manejo de ambigüedades y callbacks predecibles.

**Opciones evaluadas:**
1. **FSM Engine** (elegida)
2. Event-driven messaging
3. Choreography pattern

**Decisión:**  
Implementar **FSM Engine v2** con callbacks pre/post/error.

**Razonamiento:**
- Control preciso de flujos (states → transitions → callbacks)
- Fácil debug (state visible siempre)
- Compatible con múltiples agentes
- Manejo de ambigüedades nativo
- Menos acoplamiento que event-driven

**Impacto:**
- ✅ Modelo predecible y testeable
- ✅ Latencia <10ms transiciones
- ⚠️ Escalabilidad limitada sin clustering (H09 resuelve con K8s)

**Alternativas rechazadas:**
- Event-driven: demasiado acoplamiento, difícil track state
- Choreography: imposible manejar ambigüedades

---

## ADR-002: SQLAlchemy Async + PostgreSQL

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-15  
**Contexto:**  
Persistencia de contexto, sesiones, usuarios y auditoría con alto throughput y baja latencia.

**Opciones evaluadas:**
1. **SQLAlchemy async + PostgreSQL** (elegida)
2. MongoDB
3. Redis + fallback SQL

**Decisión:**  
**Async SQLAlchemy + asyncpg** para PostgreSQL, con **JSON fallback local** (ContextStore.json).

**Razonamiento:**
- Async I/O optimizado para FastAPI
- ACID transactions (auditoría confiable)
- JSON fallback para desarrollo local
- Escalabilidad: índices, replicación, backup nativo

**Impacto:**
- ✅ 100ms latencia queries
- ✅ 99.5% uptime producción
- ✅ GDPR-ready (datos en EU)
- ⚠️ Dependencia de PostgreSQL (mitiga con fallback JSON)

**Alternativas rechazadas:**
- MongoDB: sin transactions ACID (auditoría no confiable)
- Redis: en-memory (no persistencia durable)

---

## ADR-003: Docker-first + Kubernetes (H09)

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-20  
**Contexto:**  
Necesidad de reproducibilidad, CI/CD automatizado y escalabilidad horizontal.

**Opciones evaluadas:**
1. **Docker + K8s** (elegida)
2. Heroku/managed services
3. VMs tradicionales

**Decisión:**  
**Dockerizar todo** (código, deps, config). **K8s en producción** (H09). **CI/CD con GitHub Actions**.

**Razonamiento:**
- Reproducibilidad: dev = staging = prod
- Escalabilidad horizontal: load balancing automático
- CI/CD: auto-deploy en merge a main
- Cloud-agnostic (AWS/GCP/Azure)

**Impacto:**
- ✅ Deploy reproducible
- ✅ Auto-scaling según carga
- ✅ Zero-downtime deployments
- ⚠️ Complejidad operacional (mitiga con Helm charts H09)

---

## ADR-004: Módulos con README/ROADMAP/CHANGELOG internos

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-28  
**Contexto:**  
Documentación debe estar cerca del código para evitar outdated docs.

**Opciones evaluadas:**
1. **README/ROADMAP/CHANGELOG en cada módulo** (elegida)
2. Documentación centralizada en docs/
3. Docstrings solo (sin markdown)

**Decisión:**  
Cada módulo (`src/theaia/core/`, `src/theaia/agents/`, etc.) tiene su propia documentación.

**Razonamiento:**
- Documentación viaja con código
- Maintainers actualizan docs mientras codean
- Menos outdated, más confiable
- Fácil onboarding para nuevos devs

**Impacto:**
- ✅ Documentación sempre sincronizada
- ✅ Mejor maintainability
- ✅ Menos deuda técnica

---

## ADR-005: Multi-agente con Agent Factory Pattern

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-12  
**Contexto:**  
Necesidad de instanciar y manejar múltiples agentes (Agenda, Notes, Events, Query) sin acoplamiento.

**Opciones evaluadas:**
1. **Factory Pattern** (elegida)
2. Direct instantiation
3. Service locator

**Decisión:**  
Implementar **BotFactory** para registro dinámico de agentes.

**Razonamiento:**
- Desacoplamiento: nuevos agentes sin cambiar CoreRouter
- Registry dinámico: fácil add/remove agentes
- Testeable: mock factories en tests

**Impacto:**
- ✅ Escalable a más agentes
- ✅ Fácil testing
- ✅ Bajo acoplamiento

---

## ADR-006: Callbacks over Webhooks en FSM

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-30  
**Contexto:**  
Necesidad de ejecutar lógica antes/después de transiciones FSM sin latencia de red.

**Opciones evaluadas:**
1. **Callbacks (decorator pattern)** (elegida)
2. Webhooks HTTP
3. Event listeners

**Decisión:**  
**Callbacks decorators** (pre_transition, post_transition, on_error).

**Razonamiento:**
- Latencia <1ms (in-process vs HTTP)
- Síncrono: predictibilidad
- Fácil debug (stack trace claro)
- Type-safe (Python decorators)

**Impacto:**
- ✅ Performance: <10ms transiciones
- ✅ Debugging easier
- ✅ No network dependency
- ⚠️ Menos distribuido (pero OK para v0.14.0)

---

## ADR-007: Observabilidad Stack (H11)

**Estado:** ✅ ACEPTADA (future)  
**Fecha:** 2025-10-31  
**Contexto:**  
Necesidad de metrics, logs, traces distribuidos en producción (H11).

**Opciones evaluadas:**
1. **Prometheus + Grafana + Loki + Jaeger** (elegida)
2. DataDog/New Relic (pago)
3. CloudWatch solo (AWS-locked)

**Decisión:**  
Stack open-source: **Prometheus** (metrics) + **Grafana** (dashboards) + **Loki** (logs) + **Jaeger** (tracing).

**Razonamiento:**
- Open-source: no lock-in
- Cloud-agnostic
- Integración fácil con FastAPI
- Comunidad activa

**Impacto (H11):**
- ✅ Observabilidad completa
- ✅ Cost-effective
- ✅ Portable

---

## ADR-008: OAuth2 + JWT para Autenticación (H02)

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-31  
**Contexto:**  
Integración Telegram/Web requiere autenticación segura y stateless.

**Opciones evaluadas:**
1. **OAuth2 + JWT** (elegida)
2. Session cookies
3. API keys solo

**Decisión:**  
**OAuth2 provider** + **JWT tokens** con refresh tokens.

**Razonamiento:**
- OAuth2: estándar industria
- JWT: stateless (escalable)
- Refresh tokens: seguridad sin expiry cortos
- RBAC: integrable en JWT claims

**Impacto (H02+):**
- ✅ Seguridad estándar
- ✅ Escalable (stateless)
- ✅ Compatible con terceros (Google, GitHub)

---

## ADR-009: JSON Fallback Storage (H04)

**Estado:** ✅ ACEPTADA  
**Fecha:** 2025-10-28  
**Contexto:**  
Desarrollo local sin PostgreSQL. Fallback en caso de DB down.

**Opciones evaluadas:**
1. **JSON local + DB async** (elegida)
2. SQLite (cambios no synced)
3. Sin fallback (dev pain)

**Decisión:**  
**ContextStore.json** como fallback local (dev) y recovery (outage).

**Razonamiento:**
- Desarrollo: no instalar PostgreSQL
- Resilencia: si DB cae, siguie en JSON
- Simple: read/write JSON vs alembic

**Impacto:**
- ✅ Mejor DX (developer experience)
- ✅ Resilencia
- ⚠️ Sincronización JSON ↔ DB manual

---

## ADR-010: RBAC Multi-tenant (H08)

**Estado:** ⏳ FUTURA  
**Fecha:** 2025-10-31  
**Contexto:**  
Soporte multi-empresa con aislamiento de datos (H08).

**Decisión planificada:**  
**RBAC model** (Role-Based Access Control) + **Tenant isolation** en DB.

**Razonamiento:**
- Escalabilidad: 1 deploy para N clientes
- Seguridad: datos aislados por tenant
- Compliance: GDPR multi-tenant ready

**Impacto (H08):**
- ✅ Modelo SaaS viable
- ✅ Seguridad
- ⚠️ Complejidad (rowlevelsecurity, etc.)

---

## 📊 Resumen de ADRs

| ADR | Tema | Estado | Impacto |
|-----|------|--------|--------|
| 001 | FSM vs Event-driven | ✅ | Predecibilidad, debug fácil |
| 002 | Async SQLAlchemy | ✅ | 100ms latencia, 99.5% uptime |
| 003 | Docker + K8s | ✅ | Reproducibilidad, escalabilidad |
| 004 | Docs internas | ✅ | Documentación sincronizada |
| 005 | Factory Pattern | ✅ | Desacoplamiento agentes |
| 006 | Callbacks vs Webhooks | ✅ | <10ms transiciones |
| 007 | Observabilidad stack | ⏳ H11 | Debugging, SRE ready |
| 008 | OAuth2 + JWT | ✅ | Autenticación estándar |
| 009 | JSON Fallback | ✅ | DX, resilencia |
| 010 | RBAC Multi-tenant | ⏳ H08 | SaaS viable |

---

## 🔗 Documentación relacionada

- [Architecture Overview](./overview.md)
- [FSM Engine v2](./fsmengine.md)
- [Roadmap maestro](../roadmap/master.md)

---

**Última actualización:** 2025-10-31 03:19 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)