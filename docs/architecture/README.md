# Architecture Documentation

**Status:** 🟡 PARTIAL (FSM documented, rest pending)  
**Implementation:** H01-H08 (Complete) → H12+ (Additional docs)  
**Priority:** HIGH  
**Last Updated:** 06 January 2026

---

## 🎯 Current State

### ✅ Documented (Available Now)

#### FSM Engine (H08 - Complete)
- **File:** `fsmengine.md` (7.5 KB)
- **Content:** Complete FSM technical documentation
  - FSM v2 architecture
  - State machine patterns
  - Callback system
  - Integration with agents
  - Performance optimizations (H08)
- **Status:** ✅ Complete and current
- **Last Updated:** November 2025 (H08 completion)

---

## 📅 Why Partial Now?

**Current focus (H09):** AgendaAgent implementation  
**Architecture docs priority:** Document as features are built

### Completed Milestones (Documented in FSM)
- ✅ H01-H08: Foundation complete (FSM, DB, NLP)
- ✅ FSM Engine: Fully documented

### In Progress (H09)
- 🔴 AgendaAgent architecture (being built now)
- 🔴 Telegram adapter integration

### Future Documentation Needs (H12+)
- ⏳ REST API architecture
- ⏳ Multi-platform adapter patterns
- ⏳ Horizontal scaling architecture
- ⏳ Security architecture

---

## 📚 Future Content (By Milestone)

### H12 (March 2026) - REST API
- `api_architecture.md` - FastAPI structure
- `api_security.md` - OAuth2 + JWT design
- `api_scalability.md` - Load balancing, caching

### H13 (March 2026) - Multi-Platform
- `adapter_patterns.md` - Unified adapter design
- `message_normalization.md` - Cross-platform messaging

### H14 (April 2026) - Scalability
- `horizontal_scaling.md` - Redis session, load balancing
- `caching_strategy.md` - Redis caching architecture
- `database_pooling.md` - Connection management

### H15 (May 2026) - Security
- `security_architecture.md` - RLS, encryption, audit
- `threat_model.md` - Security threat analysis

### H16 (May 2026) - Observability
- `monitoring_architecture.md` - Prometheus, Grafana
- `tracing_architecture.md` - Distributed tracing (Jaeger)

---

## 🏗️ Current Architecture Overview

### System Layers (H01-H09)

┌─────────────────────────────────────┐
│ Adapters Layer │
│ - TelegramAdapter (H09) 🔴 │
└─────────────────────────────────────┘
↓
┌─────────────────────────────────────┐
│ Orchestrator Layer (H01) │
│ - MessageRouter │
│ - Agent coordination │
└─────────────────────────────────────┘
↓
┌─────────────────────────────────────┐
│ Agents Layer (H09+) │
│ - AgendaAgent (H09) 🔴 │
│ - QueryAgent (H10) ⏳ │
│ - NoteAgent (H10) ⏳ │
│ - ReminderAgent (H11) ⏳ │
└─────────────────────────────────────┘
↓
┌─────────────────────────────────────┐
│ FSM Engine (H04-H08) ✅ │
│ - State machine │
│ - Callbacks │
│ - Persistence │
└─────────────────────────────────────┘
↓
┌─────────────────────────────────────┐
│ Data Layer (H02) ✅ │
│ - PostgreSQL │
│ - Repository pattern │
│ - Multi-tenancy │
└─────────────────────────────────────┘

text

---

## 📊 Documentation Roadmap

| Milestone | Architecture Docs | Status |
|-----------|-------------------|--------|
| **H01-H08** | FSM Engine ✅ | Complete |
| **H09** | AgendaAgent (in code) | 🔴 In progress |
| **H10-H11** | Agent patterns | ⏳ When implemented |
| **H12** | REST API architecture | ⏳ March 2026 |
| **H13** | Multi-platform adapters | ⏳ March 2026 |
| **H14** | Scalability patterns | ⏳ April 2026 |
| **H15** | Security architecture | ⏳ May 2026 |
| **H16** | Observability stack | ⏳ May 2026 |

---

## 🔍 Key Architecture Decisions

### Already Documented (in FSM)
- ✅ **Explicit state transitions** (no implicit flows)
- ✅ **Observer pattern** for callbacks
- ✅ **Repository pattern** for data access
- ✅ **Async/await** throughout
- ✅ **Multi-tenancy** by design

### To Be Documented (Future)
- ⏳ **API-first design** (H12)
- ⏳ **Horizontal scaling** (H14)
- ⏳ **Zero-downtime deployments** (H14)
- ⏳ **Event-driven architecture** (H16)

---

## 📖 Related Documentation

- [FSM Engine](./fsmengine.md) - **Complete FSM documentation** ✅
- [SCHEMA.md](../SCHEMA.md) - System-wide architecture
- [Roadmap Master](../roadmap/master.md) - Implementation timeline
- [H08 Milestone](../roadmap/milestones/H08/README.md) - FSM production ready

---

## 🗂️ Archived Documentation

**Location:** `docs/archive/architecture_nov2025/`

Archived files (Nov 2025):
- decisions.md, deployment.md, diagrams.md, overview.md, scalability.md

**Reason:** Outdated, will create fresh docs as features are implemented.

---

**Last Updated:** 06 January 2026, 19:50 CET  
**Next Update:** H12 (March 2026) - REST API architecture  
**Maintained by:** Architecture Team

---

**🟡 PARTIAL - FSM Complete, REST API Pending 🟡**