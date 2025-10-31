📐 docs/architecture/overview.md
text
# 🏗️ Arquitectura General — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:13 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 🎯 Visión

THEA IA es un **ecosistema modular de IA empresarial** basado en:
- **FSM Engine v2** — Orquestación de flujos conversacionales
- **Multi-agente** — Agenda, Notas, Eventos, Query independientes
- **Adapters** — Telegram, Web, WhatsApp, API REST
- **ML/NLP** — Intent detection, entity extraction con spaCy
- **Persistencia** — SQLAlchemy async + fallback JSON local
- **Observabilidad** — Prometheus, Grafana, Loki, Jaeger

---

## 🔄 Flujo Principal

Usuario → Adapter (Telegram/Web/API)
↓
CoreRouter
↓
FSM Engine (pre-callbacks)
↓
Intent Detector + Entity Extractor
↓
Agent Selector (Agenda/Notes/Events/Query/Fallback)
↓
Agent Handler (ejecuta lógica)
↓
Database (persist contexto)
↓
FSM Engine (post-callbacks)
↓
Adapter → Usuario

text

---

## 🧩 Componentes principales

| Componente | Ubicación | Responsabilidad |
|-----------|-----------|-----------------|
| FSM Engine | `src/theaia/core/fsm/` | Orquestación de estados |
| CoreRouter | `src/theaia/core/router/` | Ruteo de mensajes |
| Context Manager | `src/theaia/core/context/` | Persistencia contexto |
| Agents | `src/theaia/agents/` | Lógica de dominio |
| Adapters | `src/theaia/adapters/` | Integraciones externas |
| ML/NLP | `src/theaia/ml/` | Procesamiento lenguaje |
| Tests | `src/theaia/tests/` | Validación end-to-end |

---

## 🔗 Relaciones entre componentes

┌─────────────────────────────────────────┐
│ THEA IA Ecosystem v0.14.0 │
├─────────────────────────────────────────┤
│ Adapters (Entrada) │
│ ├─ Telegram (H02) │
│ ├─ Web Client (H02) │
│ ├─ API REST (H10) │
│ └─ WhatsApp (H10) │
├─────────────────────────────────────────┤
│ CoreRouter (Orquestación) │
│ ├─ FSM Engine v2 (H03) │
│ ├─ Callbacks (pre/post/error) │
│ └─ Manager Universal (H03) │
├─────────────────────────────────────────┤
│ ML/NLP Pipeline │
│ ├─ Intent Detector (spaCy) │
│ └─ Entity Extractor │
├─────────────────────────────────────────┤
│ Agents (Lógica) │
│ ├─ Agenda Agent (H05) │
│ ├─ Notes Agent (H05) │
│ ├─ Events Agent (H05) │
│ ├─ Query Agent (H05) │
│ └─ Fallback Agent │
├─────────────────────────────────────────┤
│ Persistencia (H04) │
│ ├─ SQLAlchemy async │
│ ├─ PostgreSQL │
│ ├─ JSON fallback (local) │
│ └─ Context Manager │
├─────────────────────────────────────────┤
│ Observabilidad (H11) │
│ ├─ Prometheus (métricas) │
│ ├─ Grafana (dashboards) │
│ ├─ Loki (logs) │
│ └─ Jaeger (tracing) │
└─────────────────────────────────────────┘

text

---

## 📖 Documentación relacionada

- [FSM Engine](./fsmengine.md) — Detalles técnicos
- [Decisiones arquitectónicas](./decisions.md) — ADRs
- [Roadmap maestro](../roadmap/master.md) — Plan de hitos

---

**Última actualización:** 2025-10-31 03:13 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)
