📝 README 4/7: /docs/architecture/README.md
Ejecuta:
powershell
notepad docs/architecture/README.md
Copia y pega ESTE contenido:
text
# 🏛️ Architecture Documentation

**Propósito:** Documentación de la arquitectura del sistema THEA IA.

**Última actualización:** 06 Enero 2026

---

## 📋 Visión General

THEA IA utiliza una arquitectura multi-tenant, modular y escalable:
- **Multi-tenant desde H02** - Aislamiento por tenant_id
- **Repository Pattern** - 6 repositories + base abstracto
- **Async/Await** - SQLAlchemy 2.0 asíncrono
- **FSM (Finite State Machine)** - Gestión de estados conversacionales
- **Event-driven** - Webhooks y notifications

---

## 📁 Estructura

architecture/
├── ARCHITECTURE.md # Documento principal
├── diagrams/ # Diagramas de arquitectura
├── decisions/ # ADRs (Architecture Decision Records)
├── patterns/ # Patrones de diseño utilizados
└── README.md # Este archivo

text

---

## 🏗️ Componentes Principales

### 1. Core Layer
- **FSM (State Machine)** - Estados conversacionales
- **Context Manager** - Gestión de contexto
- **Event Bus** - Sistema de eventos

### 2. Data Layer
- **PostgreSQL 14+** - Base de datos principal
- **7 Modelos SQLAlchemy** - Users, Conversations, Messages, etc.
- **20+ Índices optimizados** - Performance
- **JSONB metadata** - Flexibilidad

### 3. Integration Layer
- **TelegramAdapter** - Bot de Telegram
- **APIAdapter** - REST endpoints
- **DatabaseAdapter** - Acceso a BD

### 4. Intelligence Layer
- **AgentConfig System** - Configuración dinámica
- **Entity Extractors** - NLP español
- **Future: LLM Integration** - OpenAI/Anthropic (H07)

---

## 🎯 Patrones de Diseño

### Repository Pattern
- Abstracción del acceso a datos
- Testeable y mockeable
- 6 repositories especializados

### Dependency Injection
- FastAPI dependencies
- Facilita testing
- Bajo acoplamiento

### Multi-tenancy
- `tenant_id` obligatorio en todas las tablas
- Row-level isolation
- Futuro: PostgreSQL RLS (P1)

### Async/Await
- SQLAlchemy 2.0 async
- Non-blocking I/O
- Mejor performance

---

## 📊 Diagramas

### Arquitectura de Alto Nivel
![High-Level Architecture](./diagrams/high-level-architecture.png)

### Flujo de Datos
![Data Flow](./diagrams/data-flow.png)

### Database Schema
Ver [SCHEMA.md](../SCHEMA.md)

---

## 📚 ADRs (Architecture Decision Records)

- **ADR-001:** Multi-tenancy desde H02
- **ADR-002:** SQLAlchemy 2.0 async sobre Django ORM
- **ADR-003:** Repository Pattern sobre Active Record
- **ADR-004:** PostgreSQL sobre MongoDB

---

## 🎯 Audiencia

- **Arquitectos** - Decisiones arquitectónicas
- **Tech Leads** - Guías de implementación
- **Desarrolladores Senior** - Patrones y best practices

---

## 📚 Referencias

- [ARCHITECTURE.md](../../ARCHITECTURE.md)
- [Database Schema](../SCHEMA.md)
- [Design Patterns](./patterns/)

---

**Contacto:** alvarofernandezmota@gmail.com