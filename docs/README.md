# 📚 THEA IA - Documentation

**Version:** v3.0.0  
**Last Updated:** 06 January 2026  
**Status:** Production Ready (H01-H08) | In Development (H09+)

---

## 🎯 Quick Links

| Document | Purpose | Status |
|----------|---------|--------|
| **[SCHEMA.md](./SCHEMA.md)** | 📊 Master reference - Complete project state | ✅ Updated |
| **[Roadmap Master](./roadmap/master.md)** | 🗺️ H01-H17 development plan | ✅ Active |
| **[Agents Overview](./agents/overview.md)** | 🤖 4 specialized agents architecture | ✅ Current |
| **[Architecture](./architecture/overview.md)** | 🏗️ System architecture & design | ✅ Current |
| **[API Reference](./api/README.md)** | 🔌 API documentation | ✅ Available |
| **[Testing Guide](./testing/README.md)** | 🧪 Testing strategy & metrics | ✅ 786 tests |
| **[Security](./security/README.md)** | 🔒 Security & compliance | ✅ Active |

---

## 🚀 What is THEA IA?

**THEA IA** is a production-ready multi-agent conversational AI system with specialized agents, built on a robust FSM (Finite State Machine) engine and designed for enterprise scalability.

### Key Features
- ✅ **4 Specialized Agents** - No functional overlap
- ✅ **Multi-tenant Architecture** - PostgreSQL 14+ with full isolation
- ✅ **FSM Engine** - 786 tests, 85% coverage, production-ready
- ✅ **Repository Pattern** - 6 repositories + abstract base
- ✅ **Async/Await** - Python 3.11+, FastAPI, SQLAlchemy 2.0
- ✅ **Cross-Platform** - Windows/Mac/Linux compatible

---

## 📊 Current Project Status

### Milestones Completed (H01-H08) ✅

| Milestone | Name | Tests | Coverage | Status |
|-----------|------|-------|----------|--------|
| **H01** | Router & Orchestrator | 10 | 60% | ✅ Done |
| **H02** | Multi-tenancy & Database | 16 | 41-59% | ✅ Done |
| **H03** | AgentConfig & NLP Extractors | 18 | 84-87% | ✅ Done |
| **H04** | FSM Core System | 196 | 63-100% | ✅ Done |
| **H05** | FSM Advanced Patterns | 174 | 85%+ | ✅ Done |
| **H06** | FSM Integration & Polish | 261 | 90%+ | ✅ Done |
| **H07** | Callbacks Manager | 71 | 96% | ✅ Done |
| **H08** | FSM Production Ready | 40 | 95% | ✅ Done |

**Total:** 786 tests passing | 85% average coverage | 12,300+ LOC

### Current Sprint (H09) 🔴

**H09: Real Ecosystem** (January 2026 - 15 days, 75 hours)
- 🔴 Telegram Bot (20h)
- 🔴 Database Services (15h)
- 🔴 Calendar Engine (18h)
- 🔴 Groq LLM Integration (15h)
- 🔴 E2E Integration (7h)

**Agent Implemented:** AgendaAgent (Booking/Scheduling)

### Upcoming (H10-H17) ⏳

- **H10-H11:** QueryAgent, NoteAgent, ReminderAgent (Feb 2026)
- **H12-H14:** Scalability & Integrations (Mar-Apr 2026)
- **H15-H17:** Security, Monitoring, Web UI (May-Jun 2026)

---

## 🤖 The 4 Specialized Agents

### 1️⃣ AgendaAgent (Booking) 📅
**Status:** 🔴 H09 - In Development  
**Purpose:** Event/appointment management

**Responsibilities:**
- Create, modify, cancel appointments
- Detect scheduling conflicts
- Google Calendar integration
- Natural language date parsing
- Pre-event reminders

---

### 2️⃣ QueryAgent (Search) 🔍
**Status:** ⏳ H10 - Planned (Feb 2026)  
**Purpose:** Semantic search & question answering

**Responsibilities:**
- Semantic search (meaning-based, not keyword)
- Question answering ("When is my next appointment?")
- Multi-source search (notes + events + docs)
- Entity extraction
- Relevance ranking

---

### 3️⃣ NoteAgent (Notes) 📝
**Status:** ⏳ H10 - Planned (Feb 2026)  
**Purpose:** Note management & organization

**Responsibilities:**
- Create/edit/delete notes
- Full-text search
- Tag management & auto-tagging
- Archive old notes
- Duplicate detection
- Markdown support

---

### 4️⃣ ReminderAgent (Reminders) ⏰
**Status:** ⏳ H11 - Planned (Feb 2026)  
**Purpose:** Independent reminders (not tied to events)

**Responsibilities:**
- Create standalone reminders
- Recurring reminders (daily/weekly)
- Multi-channel notifications (Telegram, email, push)
- Snooze functionality
- Reminder management

---

## 🏗️ System Architecture

┌─────────────────────────────────────────────────────┐
│ INTEGRATION LAYER (Adapters) │
│ ✅ TelegramAdapter (H02, H09) │
│ ⏳ APIAdapter (H12) │
│ ⏳ WhatsAppAdapter (H13) │
└─────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────┐
│ INTELLIGENCE LAYER (4 Agents) │
│ 🔴 AgendaAgent (H09) — Booking │
│ ⏳ QueryAgent (H10) — Semantic Search │
│ ⏳ NoteAgent (H10) — Notes Management │
│ ⏳ ReminderAgent (H11) — Reminders │
└─────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────┐
│ CORE LAYER (FSM + Context) │
│ ✅ State Machine (732 LOC, 63% coverage) │
│ ✅ Callbacks Manager (300 LOC, 96% coverage) │
│ ✅ FSM Advanced (435 tests) │
└─────────────────────────────────────────────────────┘
↓
┌─────────────────────────────────────────────────────┐
│ DATA LAYER (Repository Pattern) │
│ ✅ 6 Repositories + Base Abstract │
│ ✅ PostgreSQL 14+ (11 tables) │
│ ✅ SQLAlchemy 2.0 async │
└─────────────────────────────────────────────────────┘

text

---

## 💾 Database Schema

### Core Tables (H02) ✅
- **tenants** - Multi-tenant isolation
- **users** - User accounts
- **conversations** - Chat sessions
- **messages** - Message history
- **agent_configs** - Agent configurations
- **user_preferences** - User settings
- **api_keys** - API key management

### Agent Tables (H09-H11) ⏳
- **appointments** - AgendaAgent (H09)
- **availability** - AgendaAgent (H09)
- **notes** - NoteAgent (H10)
- **reminders** - ReminderAgent (H11)

---

## 🧪 Testing & Quality

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| **Total Tests** | 786 | 500+ | ✅ |
| **Code Coverage** | 85% | 80%+ | ✅ |
| **Test Duration** | ~5 min | <10 min | ✅ |
| **Pass Rate** | 100% | 100% | ✅ |

### Test Distribution
- **Unit Tests:** 450
- **Integration Tests:** 250
- **E2E Tests:** 86

---

## 📖 Documentation Structure

docs/
├── README.md ← You are here
├── SCHEMA.md ← 📊 Master reference (START HERE)
├── roadmap/
│ ├── master.md ← H01-H17 roadmap
│ └── milestones/ ← Individual milestone docs
├── agents/
│ ├── overview.md ← Agents architecture
│ ├── agent_agenda.md ← AgendaAgent spec
│ ├── agent_query.md ← QueryAgent spec
│ ├── agent_note.md ← NoteAgent spec
│ └── agent-reminder.md ← ReminderAgent spec
├── architecture/
│ ├── overview.md ← System architecture
│ ├── fsmengine.md ← FSM documentation
│ └── decisions.md ← ADRs
├── api/
│ └── README.md ← API reference
├── testing/
│ └── README.md ← Testing guide
├── security/
│ └── README.md ← Security docs
├── guides/
│ ├── getting-started.md ← Quick start
│ ├── installation.md ← Setup guide
│ └── quickstart.md ← 5-min demo
├── audit/
│ └── audit_diciembre_2025/ ← December audit
└── diary/
└── enero/2026-01-06.md ← Development diary

text

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Git

### Quick Setup
```bash
# Clone repository
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python scripts/setup.sh

# Run tests
pytest
See Installation Guide for detailed setup.

🔒 Security
✅ Multi-tenant isolation (tenant_id mandatory)

✅ Environment variables for secrets

✅ Input validation (Pydantic schemas)

✅ SQL injection protection (ORM)

⏳ OAuth2 + JWT (H12, Q1 2026)

⏳ Rate limiting (H12)

⏳ Row-level security (H15)

See Security Documentation

📊 Project Metrics
Metric	Value
Lines of Code	12,300+
Documentation	10/10
Test Coverage	85%
Technical Debt	0 (ZERO)
Code Quality	95%
Security Score	8.8/10
🎯 Development Philosophy
Ecosystem Functional > Beautiful Interfaces
Real Data > Mockups
Specialized Agents > General Agents
Testing > Untested Code
Documentation > Undocumented Code

📞 Contact & Support
Project Lead: Álvaro Fernández Mota
Email: alvarofernandezmota@gmail.com
GitHub: @alvarofernandezmota-tech

📄 License
Copyright © 2025-2026 THEA IA Project. All rights reserved.

🔗 Additional Resources
SCHEMA.md - Complete project state (START HERE)

Roadmap Master - Development roadmap

Architecture Overview - System design

API Reference - API documentation

Contributing Guide - How to contribute

FAQ - Frequently asked questions

Last Updated: 06 January 2026, 16:35 CET
Version: v3.0.0
Status: ✅ Production Ready (H01-H08) | 🔴 In Development (H09)
