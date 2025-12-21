# THEA IA - Architecture Overview

**Version:** 3.0.0 | **Last Updated:** December 21, 2025

## Table of Contents
- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Core Components](#core-components)
- [Data Flow](#data-flow)
- [Technology Stack](#technology-stack)
- [Design Principles](#design-principles)
- [Further Documentation](#further-documentation)

---

## Introduction

THEA IA is an enterprise-grade modular conversational AI assistant built with Python 3.11+. The architecture is designed for scalability, maintainability, and extensibility across 17 planned milestones (H01-H17).

**Current Status:** H03 Complete (50% coverage, 173 tests passing)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ADAPTERS LAYER                           │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ Telegram │  │   Web    │  │   CLI    │  │   API    │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    CORE FSM LAYER                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │          State Machine (Transitions)                 │  │
│  │  idle → agent_selection → processing → response     │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  MULTI-AGENT SYSTEM                         │
│  ┌───────────┐  ┌───────────┐  ┌───────────┐             │
│  │  Agenda   │  │   Note    │  │ Reminder  │  + MORE     │
│  │  Agent    │  │   Agent   │  │   Agent   │             │
│  └───────────┘  └───────────┘  └───────────┘             │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                   ML/NLP PIPELINES                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐    │
│  │  DateTime    │  │   Location   │  │  PersonName  │    │
│  │  Extractor   │  │  Extractor   │  │  Extractor   │    │
│  └──────────────┘  └──────────────┘  └──────────────┘    │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                  DATABASE LAYER (H02)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Multi-Tenant Architecture               │  │
│  │  - Users  - Events  - Notes  - Conversations       │  │
│  │  - MessageHistory  - AgentConfig  - Repositories   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. FSM (Finite State Machine)
- **Location:** `src/theaia/core/`
- **Technology:** Python Transitions library
- **States:** idle, agent_selection, processing, response
- **Purpose:** Orchestrates conversation flow and state management

### 2. Multi-Agent System
- **Location:** `src/theaia/agents/`
- **Agents:** AgendaAgent, NoteAgent, ReminderAgent
- **Pattern:** Agent Configuration System with intent management
- **Tests:** 46 E2E tests (100% passing)

### 3. NLP Entity Extraction
- **Location:** `src/theaia/ml/entity_extractor/`
- **Extractors:**
  - DateTimeExtractor (91% coverage, 15 tests)
  - LocationExtractor (100% coverage, 18 tests)
  - PersonNameExtractor (98% coverage, 18 tests)
- **Language:** Spanish NLP support

### 4. Database Layer (H02)
- **Location:** `src/theaia/database/`
- **ORM:** SQLAlchemy 2.0 (async/await)
- **Database:** PostgreSQL 14+
- **Architecture:** Multi-tenant from day 1
- **Models:** 7 models, 6 repositories
- **Tests:** 12 tests (100% passing)

### 5. Adapters
- **TelegramAdapter** (H02): Fully functional with persistence
- **WebAdapter** (H08): Planned
- **Pattern:** Adapter pattern for multi-channel support

---

## Data Flow

1. **User Input** → Adapter (Telegram/Web/CLI)
2. **Adapter** → FSM Core (state transition)
3. **FSM** → Agent Selection (based on intent)
4. **Agent** → NLP Pipeline (entity extraction)
5. **Agent** → Database Layer (persistence via repositories)
6. **Agent** → Response Generation
7. **FSM** → Adapter (send response)
8. **Adapter** → User Output

---

## Technology Stack

### Core
- **Language:** Python 3.11+
- **FSM:** Transitions 0.9.0+
- **Testing:** pytest (173 tests, 50% coverage)

### Database
- **Database:** PostgreSQL 14+
- **ORM:** SQLAlchemy 2.0 (async)
- **Migrations:** Alembic 1.12.1+

### NLP/ML
- **NLP:** spaCy 3.7.2+
- **Entity Extraction:** Custom Spanish extractors
- **Future:** LangChain, RAG (H05-H07)

### Adapters
- **Telegram:** python-telegram-bot 3.2.0+ (aiogram)
- **Web:** FastAPI 0.104.1+ (H08)
- **API:** FastAPI + Uvicorn

### DevOps
- **Containerization:** Docker, docker-compose
- **CI/CD:** GitHub Actions (.github/workflows/)
- **Deployment:** Railway (current)

---

## Design Principles

### 1. Modularity
- Each component is self-contained with its own README
- Clear separation of concerns (adapters, core, agents, database)

### 2. Testability
- Comprehensive test suite (unit, integration, e2e)
- 50%+ coverage target (achieved in H03)
- Repository Pattern for database abstraction

### 3. Scalability
- Multi-tenant architecture from day 1
- Async/await patterns throughout
- PostgreSQL with optimized indexes

### 4. Maintainability
- Extensive documentation (README, CHANGELOG, ROADMAP)
- Conventional Commits for version control
- Pre-commit hooks for code quality

### 5. Security
- SECURITY.md with vulnerability reporting
- Bandit security checks
- Environment variable management
- Multi-tenant data isolation

---

## Further Documentation

### Architecture Details
- **[FSM Architecture](docs/architecture/fsm.md)** - State machine design
- **[Database Schema](docs/architecture/database.md)** - Entity relationships
- **[Agent System](docs/architecture/agents.md)** - Multi-agent design
- **[NLP Pipeline](docs/architecture/nlp.md)** - Entity extraction

### Development
- **[ROADMAP.md](ROADMAP.md)** - 17 milestones (H01-H17)
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development guide
- **[Testing Guide](docs/testing/README.md)** - Test suite overview

### Operations
- **[Deployment Guide](docs/roadmap/deployment.md)** - Production setup
- **[Security Policy](SECURITY.md)** - Security best practices

---

**For detailed technical documentation, see [docs/README.md](docs/README.md)**
