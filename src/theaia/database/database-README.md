# src/database/ - Database Module

**Módulo de persistencia de datos con PostgreSQL**

---

## 📋 Overview

El módulo `database/` gestiona TODA la persistencia de datos en THEA IA usando PostgreSQL, incluyendo:

- 🗄️ **Connection Management** (async engine + sessions)
- 📊 **Models** (SQLAlchemy ORM con multi-tenant)
- 🔄 **Repositories** (CRUD + queries) ⏳ Próximo
- 🔀 **Migrations** (Alembic versionado) ✅
- 🔒 **Multi-tenant Isolation** (cada tenant solo ve sus datos)

**Patrón:** Repository Pattern + SQLAlchemy ORM + Alembic Migrations

---

## 🎯 Propósito

### ¿Por qué PostgreSQL?

Comparado con JSON/NoSQL:

- ✅ **Integridad:** ACID transactions
- ✅ **Escalabilidad:** Millones de usuarios sin refactor
- ✅ **Seguridad:** Row Level Security (H04)
- ✅ **Performance:** Indexes, connection pooling
- ✅ **Fiabilidad:** Backup automático, replicación
- ✅ **Enterprise-ready:** Compliance, auditoría
- ✅ **Multi-tenant:** Aislamiento por tenant_id

---

## 📁 Estructura (H02 Day 1 - 12 Nov) ✅

src/database/
├── init.py # Exports: engine, get_db, Base, models ✅
├── connection.py # AsyncEngine + test_connection ✅
├── session.py # AsyncSessionLocal + get_db + init/close ✅
├── base.py # DeclarativeBase + BaseModel ✅
├── models/ # SQLAlchemy models ✅
│ ├── init.py # Exports all models ✅
│ ├── base.py # BaseModel con tenant_id ✅
│ ├── user.py # Usuario Telegram ✅
│ ├── event.py # Eventos/Recordatorios ✅
│ ├── note.py # Notas con tags ✅
│ ├── conversation.py # Sesiones FSM ✅
│ └── message_history.py # Auditoría ML ✅
├── repositories/ # CRUD + queries ⏳ PRÓXIMO
│ ├── init.py
│ ├── base_repository.py
│ ├── user_repository.py
│ ├── event_repository.py
│ ├── note_repository.py
│ ├── conversation_repository.py
│ └── message_history_repository.py
├── migrations/ # Alembic ✅
│ ├── env.py # Async environment ✅
│ ├── script.py.mako
│ └── versions/
│ └── e0a17d850507_initial_schema.py # Primera migración ✅
└── [docs]/ # Documentación ✅
├── README.md (este archivo)
├── ROADMAP.md
├── CHANGELOG.md
├── STRUCTURE.md
└── DEPENDENCIES.md

text

**Estado:** 50% completado (Database Layer ✅, falta Repositories + Adapter)

---

## 🏗️ Arquitectura

### Flujo de Datos:

Agent → Repository → SQLAlchemy Model → PostgreSQL

Example:
EventAgent → EventRepository.create()
→ Event (model) → events table

text

### Componentes:

**1. Connection (connection.py) ✅**
- AsyncEngine (asyncpg driver)
- test_connection() utility
- URL: `postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia`

**2. Session (session.py) ✅**
- AsyncSessionLocal (session factory)
- get_db() async context manager
- init_db() / close_db() lifecycle

**3. Models (models/*.py) ✅**
- 7 SQLAlchemy declarative models
- Tablas: users, events, notes, conversations, message_history
- Relationships: User → has many Events/Notes/Conversations
- Multi-tenant: tenant_id en todas las tablas
- Timestamps: created_at, updated_at automáticos
- JSONB: preferences, extra_data, context_data, entities_extracted

**4. Repositories (repositories/*.py) ⏳ PRÓXIMO**
- CRUD operations (create, read, update, delete)
- Custom queries (get_upcoming, search, etc)
- Business logic encapsulada

**5. Migrations (migrations/) ✅**
- Alembic para versionado schema
- Track cambios database over time
- Rollback posible
- Primera migración aplicada: e0a17d850507_initial_schema.py

---

## 📦 Dependencias

### Python (INSTALADAS ✅):

sqlalchemy==2.0.23
asyncpg==0.29.0
psycopg2-binary==2.9.9
alembic==1.12.1
greenlet==3.0.1

text

### Externa:

PostgreSQL 18 ✅ (instalado nativamente Windows)

Path: C:\Program Files\PostgreSQL\18\

Database: thea_ia

Puerto: 5432

Auth: trust mode (desarrollo)

text

---

## 🚀 Quick Start

### 1. Setup PostgreSQL ✅ (COMPLETADO):

PostgreSQL 18 ya instalado y corriendo.

**Verificar:**
Get-Process -Name postgres

Resultado: 33 procesos activos ✅
text

### 2. Configurar .env ✅ (COMPLETADO):

Ya configurado en .env:
DATABASE_URL=postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=False

text

### 3. Ejecutar Migrations ✅ (COMPLETADO):

Migración ya aplicada (12 Nov 16:11)
alembic upgrade head

Verificar
alembic current

Output: e0a17d850507 (head), Initial schema with tenant support
text

### 4. Verificar Tablas ✅ (COMPLETADO):

psql -U postgres -d thea_ia -c "\dt"

Tablas creadas:
- users
- events
- notes
- conversations
- message_history
- alembic_version
text

### 5. Usar en Código (PRÓXIMO H02 Day 2):

from src.database import get_db
from src.database.repositories import EventRepository
from src.database.models import Event

async def create_event_example():
async with get_db() as session:
repo = EventRepository(session)

text
    event = await repo.create(
        user_id=1,
        tenant_id="default",
        title="Reunión",
        description="Reunión equipo",
        start_datetime=datetime(2025, 11, 15, 15, 0, tzinfo=timezone.utc)
    )
    
    await session.commit()
    
    print(f"Event created: {event.id}")
text

---

## 🔑 Conceptos Clave

### Repository Pattern:

Separa lógica acceso datos de lógica negocio:

❌ Sin Repository (malo)
class EventAgent:
async def create_event(self, data):
# SQL directo en agent (acoplado)
await session.execute("INSERT INTO events...")

✅ Con Repository (bueno)
class EventAgent:
async def create_event(self, data):
# Repository abstrae SQL
event = await event_repo.create(**data)

text

**Beneficios:**
- Testeable (mock repositories)
- Reutilizable (mismo repo en múltiples agentes)
- Mantenible (cambios SQL centralizados)

### Async/Await:

Todo asyncio para no bloquear:

Connection ✅
engine = create_async_engine(url)

Session ✅
async with get_db() as session:
# Queries
result = await session.execute(select(User))
await session.commit()

text

### Multi-tenant Isolation:

Cada tenant solo ve sus datos:

Todos los queries filtran por tenant_id
events = await repo.get_by_tenant(tenant_id="default")

Foreign keys garantizan integridad
class Event(BaseModel):
user_id = Column(Integer, ForeignKey('users.id'))
tenant_id = Column(String(50), nullable=False, index=True)

text

---

## 🧪 Testing (PRÓXIMO H02 Day 2)

### Test Models:

@pytest.mark.asyncio
async def test_user_model_creation():
user = User(
tenant_id="default",
telegram_id=123456,
username="test_user",
first_name="Test"
)
assert user.telegram_id == 123456
assert user.tenant_id == "default"

text

### Test Repositories:

@pytest.mark.asyncio
async def test_event_repository_create(test_session):
repo = EventRepository(test_session)

text
event = await repo.create(
    user_id=1,
    tenant_id="default",
    title="Test",
    start_datetime=datetime.now(timezone.utc)
)

assert event.id is not None
assert event.title == "Test"
text

### Ejecutar:

pytest src/tests/unit/test_database/ -v
pytest --cov=src/database

text

---

## 📊 Schema Database (IMPLEMENTADO ✅)

### Tablas H02:

| Tabla | Descripción | Columnas Clave | Estado |
|-------|-------------|----------------|--------|
| **users** | Usuarios Telegram | telegram_id (unique), tenant_id, preferences (JSONB) | ✅ |
| **events** | Eventos/Recordatorios | tenant_id, user_id, start_datetime, recurrence_rule, extra_data (JSONB) | ✅ |
| **notes** | Notas con tags | tenant_id, user_id, tags (ARRAY), category, is_pinned | ✅ |
| **conversations** | Sesiones FSM | tenant_id, session_id (unique), current_state, context_data (JSONB) | ✅ |
| **message_history** | Auditoría ML | tenant_id, conversation_id, intent_detected, entities_extracted (JSONB) | ✅ |

### Relationships:

User (1) ←→ (N) Event
User (1) ←→ (N) Note
User (1) ←→ (N) Conversation
Conversation (1) ←→ (N) MessageHistory

text

**Características:**
- ✅ 5 foreign keys con CASCADE delete
- ✅ 20+ índices de performance
- ✅ Multi-tenant support (tenant_id en todas)
- ✅ JSONB para metadata flexible
- ✅ ARRAY para tags (PostgreSQL native)
- ✅ Timezone-aware timestamps

---

## 🔐 Seguridad

### Multi-tenant Isolation ✅:
- `tenant_id` en todas las tablas
- Foreign keys con ON DELETE CASCADE
- Índices en tenant_id para performance
- Row Level Security (H04)

### SQL Injection ✅:
- SQLAlchemy protege automáticamente
- Usar siempre parámetros, nunca string formatting

### Connection Security ✅:
- SSL en producción (DATABASE_SSL_MODE=require)
- Credentials en .env, nunca en código
- Connection pooling limita conexiones
- Auth trust mode solo en desarrollo

---

## 📈 Performance

### Indexes (APLICADOS ✅):
- ✅ tenant_id en todas las tablas
- ✅ user_id en todas las tablas relacionadas
- ✅ datetime fields (start_datetime, created_at, last_activity)
- ✅ status, is_active para filtros comunes
- ✅ session_id, message_id para lookups únicos
- ✅ current_state, intent_detected para queries FSM/ML

**Total:** 20+ índices aplicados

### Connection Pooling (CONFIGURADO ✅):
- Pool size: 5 (desarrollo)
- Max overflow: 10
- Recycle: 3600 seconds (1h)
- Timeout: 30 seconds

### Query Optimization (PRÓXIMO):
- Eager loading cuando necesario (selectinload)
- Lazy loading por defecto
- Evitar N+1 queries

---

## 🔮 Próximos Pasos

### H02 Day 2 (13 Nov):
- ⏳ Repositories (User, Event, Note, Conversation, MessageHistory)
- ⏳ TelegramAdapter integration
- ⏳ Tests repositories
- ⏳ Primera conversación persistente

### H04: Enterprise Features
- Row Level Security (RLS)
- Soft delete (deleted_at)
- Audit logging (who, when, what)
- Read replicas
- Connection retry logic

### H11: Kubernetes
- High availability
- Auto-scaling
- Backup automation
- Monitoring integrado

---

## 📝 Comandos Útiles

### Migrations:

Ver estado actual ✅
alembic current

Ver historial
alembic history

Crear nueva migración
alembic revision --autogenerate -m "descripcion"

Aplicar migraciones
alembic upgrade head

Rollback
alembic downgrade -1

text

### PostgreSQL:

Conectar a database
psql -U postgres -d thea_ia

Dentro de psql:
\dt # List tables ✅
\d users # Describe table
\di # List indexes
\q # Quit

Ver datos
SELECT * FROM users LIMIT 5;
SELECT * FROM events WHERE tenant_id = 'default';

text

### Testing (próximo):

pytest src/tests/unit/test_database/ -v
pytest --cov=src/database --cov-report=html

text

---

## 🆘 Troubleshooting

### Problemas Resueltos (12 Nov):

**1. WinError 64 - "network name no longer available"**
- ✅ **Solución:** Cambiar `localhost` → `127.0.0.1`

**2. "authentication failed for user postgres"**
- ✅ **Solución:** Editar `pg_hba.conf` a trust mode

**3. "metadata is a reserved word"**
- ✅ **Solución:** Renombrar columna `metadata` → `extra_data`

**4. "cannot drop table servicios because other objects depend on it"**
- ✅ **Solución:** Usar `DROP TABLE ... CASCADE`

Ver `DEPENDENCIES.md` para troubleshooting completo.

---

## 📚 Recursos

- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [asyncpg](https://magicstack.github.io/asyncpg/)
- [PostgreSQL 18](https://www.postgresql.org/docs/18/)

---

## 📊 Estado Actual (12 Nov 2025, 16:22 CET)

**Versión:** 0.2.0  
**H02 Progreso:** 50% ✅  
**Última sesión:** Sesión 8 (14:30-16:17, 1h 47min)

### Completado ✅:
- ✅ 7 Modelos SQLAlchemy con multi-tenant
- ✅ Async SQLAlchemy configurado
- ✅ Alembic migrations setup
- ✅ Primera migración aplicada
- ✅ 5 tablas PostgreSQL operativas
- ✅ 20+ índices aplicados
- ✅ CASCADE relationships
- ✅ JSONB metadata flexible
- ✅ Troubleshooting conexión resuelto

### Próximo ⏳:
- ⏳ Repositories CRUD (13 Nov)
- ⏳ TelegramAdapter integration
- ⏳ Tests >85% coverage
- ⏳ Primera conversación funcional

---

**Responsable:** Álvaro Fernández Mota  
**Estado:** H02 Day 1 COMPLETADO ✅ | Database Layer ready | Adapter próximo 🚀
