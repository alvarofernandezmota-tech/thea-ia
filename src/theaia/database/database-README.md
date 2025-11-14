src/database/ - Database Module
Módulo de persistencia de datos con PostgreSQL

📋 Overview
El módulo database/ gestiona TODA la persistencia de datos en THEA IA usando PostgreSQL, incluyendo:

🗄️ Connection Management (async engine + sessions)

📊 Models (SQLAlchemy ORM con multi-tenant)

🔄 Repositories (CRUD + queries) ✅

🔀 Migrations (Alembic versionado) ✅

🔒 Multi-tenant Isolation (cada tenant solo ve sus datos)

Patrón: Repository Pattern + SQLAlchemy ORM + Alembic Migrations

🎯 Propósito
¿Por qué PostgreSQL?
Comparado con JSON/NoSQL:

✅ Integridad: ACID transactions

✅ Escalabilidad: Millones de usuarios sin refactor

✅ Seguridad: Row Level Security (H04)

✅ Performance: Indexes, connection pooling

✅ Fiabilidad: Backup automático, replicación

✅ Enterprise-ready: Compliance, auditoría

✅ Multi-tenant: Aislamiento por tenant_id

📁 Estructura (H02 - 12 Nov) ✅
text
src/database/
├── __init__.py              # Exports: engine, get_db, Base, models ✅
├── connection.py            # AsyncEngine + test_connection ✅
├── session.py               # AsyncSessionLocal + get_db + init/close ✅
├── base.py                  # DeclarativeBase + BaseModel ✅
├── models/                  # SQLAlchemy models ✅
│   ├── __init__.py          # Exports all models ✅
│   ├── base.py              # BaseModel con tenant_id ✅
│   ├── user.py              # Usuario Telegram ✅
│   ├── event.py             # Eventos/Recordatorios ✅
│   ├── note.py              # Notas con tags ✅
│   ├── conversation.py      # Sesiones FSM ✅
│   └── message_history.py  # Auditoría ML ✅
├── repositories/            # CRUD + queries ✅
│   ├── __init__.py          # Exports all repositories ✅
│   ├── base_repository.py  # CRUD genérico ✅
│   ├── user_repository.py  # Usuarios Telegram ✅
│   ├── event_repository.py # Eventos ✅
│   ├── note_repository.py  # Notas ✅
│   ├── conversation_repository.py # Conversaciones ✅
│   └── message_history_repository.py # Auditoría ✅
├── migrations/              # Alembic ✅
│   ├── env.py               # Async environment ✅
│   ├── script.py.mako
│   └── versions/
│       └── e0a17d850507_initial_schema.py # Primera migración ✅
└── [docs]/                  # Documentación ✅
    ├── README.md (este archivo)
    ├── ROADMAP.md
    ├── CHANGELOG.md
    ├── STRUCTURE.md
    └── DEPENDENCIES.md
Estado: 100% completado Database Layer ✅ (12 Nov 2025)

🏗️ Arquitectura
Flujo de Datos:
text
Agent → Repository → SQLAlchemy Model → PostgreSQL

Example:
EventAgent → EventRepository.create()
           → Event (model) → events table
Componentes:
1. Connection (connection.py) ✅

AsyncEngine (asyncpg driver)

test_connection() utility

URL: postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia

2. Session (session.py) ✅

AsyncSessionLocal (session factory)

get_db() async context manager

init_db() / close_db() lifecycle

3. Models (models/*.py) ✅

7 SQLAlchemy declarative models

Tablas: users, events, notes, conversations, message_history

Relationships: User → has many Events/Notes/Conversations

Multi-tenant: tenant_id en todas las tablas

Timestamps: created_at, updated_at automáticos

JSONB: preferences, extra_data, context_data, entities_extracted

4. Repositories (repositories/*.py) ✅

CRUD operations (create, read, update, delete)

Custom queries (get_upcoming, search, etc)

Business logic encapsulada

Multi-tenant isolation automático

5. Migrations (migrations/) ✅

Alembic para versionado schema

Track cambios database over time

Rollback posible

Primera migración aplicada: e0a17d850507_initial_schema.py

📦 Dependencias
Python (INSTALADAS ✅):
text
sqlalchemy==2.0.23
asyncpg==0.29.0
psycopg2-binary==2.9.9
alembic==1.12.1
greenlet==3.0.1
Externa:
text
PostgreSQL 18 ✅ (instalado nativamente Windows)

Path: C:\Program Files\PostgreSQL\18\
Database: thea_ia
Puerto: 5432
Auth: trust mode (desarrollo)
🚀 Quick Start
1. Setup PostgreSQL ✅ (COMPLETADO):
PostgreSQL 18 ya instalado y corriendo.

Verificar:

powershell
Get-Process -Name postgres
Resultado: 33 procesos activos ✅

2. Configurar .env ✅ (COMPLETADO):
Ya configurado en .env:

text
DATABASE_URL=postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=False
3. Ejecutar Migrations ✅ (COMPLETADO):
Migración ya aplicada (12 Nov 16:11)

bash
alembic upgrade head

# Verificar
alembic current
Output: e0a17d850507 (head), Initial schema with tenant support

4. Verificar Tablas ✅ (COMPLETADO):
bash
psql -U postgres -d thea_ia -c "\dt"
Tablas creadas:

users

events

notes

conversations

message_history

alembic_version

5. Usar en Código ✅ (COMPLETADO H02):
python
from src.database import get_db
from src.database.repositories import EventRepository
from src.database.models import Event

async def create_event_example():
    async with get_db() as session:
        repo = EventRepository(session)
        
        event = await repo.create(
            user_id=1,
            tenant_id="default",
            title="Reunión",
            description="Reunión equipo",
            start_datetime=datetime(2025, 11, 15, 15, 0, tzinfo=timezone.utc)
        )
        
        await session.commit()
        
        print(f"Event created: {event.id}")
📚 Ejemplos de Uso Completos
Crear usuario desde Telegram
python
from src.database.repositories.user_repository import UserRepository
from src.database.config.session import AsyncSessionLocal

async def example_user():
    async with AsyncSessionLocal() as session:
        repo = UserRepository(session)
        
        # Get or create desde Telegram
        user = await repo.get_or_create_from_telegram(
            tenant_id="default_tenant",
            telegram_id=123456789,
            username="john_doe",
            first_name="John",
            last_name="Doe"
        )
        
        print(f"Usuario: {user.username}, ID: {user.id}")
        return user
Crear nota con tags ARRAY
python
from src.database.repositories.note_repository import NoteRepository

async def example_note():
    async with AsyncSessionLocal() as session:
        repo = NoteRepository(session)
        
        # Crear nota con tags
        note = await repo.create(
            tenant_id="default_tenant",
            user_id=1,
            title="Lista compras",
            content="Comprar leche, pan, huevos",
            tags=["shopping", "urgent"]  # PostgreSQL ARRAY nativo
        )
        
        # Buscar por tags
        urgent_notes = await repo.get_by_tags(
            tenant_id="default_tenant",
            user_id=1,
            tags=["urgent"]
        )
        
        return urgent_notes
Buscar notas por texto (Full-text search)
python
async def search_notes():
    async with AsyncSessionLocal() as session:
        repo = NoteRepository(session)
        
        # Búsqueda en título y contenido
        results = await repo.search(
            tenant_id="default_tenant",
            user_id=1,
            query="leche"
        )
        
        for note in results:
            print(f"- {note.title}: {note.content}")
Gestionar conversación FSM
python
from src.database.repositories.conversation_repository import ConversationRepository

async def example_conversation():
    async with AsyncSessionLocal() as session:
        repo = ConversationRepository(session)
        
        # Get or create conversación
        conv = await repo.get_or_create(
            tenant_id="default_tenant",
            user_id=1,
            session_id="telegram_123456789"
        )
        
        # Actualizar estado FSM
        await repo.update_state(
            conversation_id=conv.id,
            new_state="waiting_note_content",
            context_update={
                "last_intent": "crear_nota",
                "expecting": "note_text"
            }
        )
        
        return conv
Auditoría de mensajes con ML metadata
python
from src.database.repositories.message_history_repository import MessageHistoryRepository

async def example_audit():
    async with AsyncSessionLocal() as session:
        repo = MessageHistoryRepository(session)
        
        # Registrar mensaje con ML metadata
        await repo.add_message(
            tenant_id="default_tenant",
            user_id=1,
            session_id="telegram_123456789",
            user_message="crear nota: comprar leche",
            bot_response="✅ Nota creada",
            intent_detected="crear_nota",
            entities_extracted={"text": "comprar leche", "tags": ["shopping"]},
            confidence_score=0.95
        )
        
        # Obtener estadísticas
        stats = await repo.get_statistics(
            tenant_id="default_tenant",
            user_id=1
        )
        
        print(f"Mensajes totales: {stats['total_messages']}")
        print(f"Intents únicos: {stats['unique_intents']}")
        return stats
Crear evento con recurrencia
python
from src.database.repositories.event_repository import EventRepository

async def create_recurring_event():
    async with AsyncSessionLocal() as session:
        repo = EventRepository(session)
        
        event = await repo.create(
            tenant_id="default_tenant",
            user_id=1,
            title="Reunión semanal",
            description="Standup equipo",
            start_datetime=datetime(2025, 11, 18, 10, 0, tzinfo=timezone.utc),
            end_datetime=datetime(2025, 11, 18, 10, 30, tzinfo=timezone.utc),
            recurrence_rule="FREQ=WEEKLY;BYDAY=MO",  # Cada lunes
            extra_data={"location": "Sala 1", "attendees": ["john", "jane"]}
        )
        
        return event
Obtener eventos próximos
python
async def get_upcoming():
    async with AsyncSessionLocal() as session:
        repo = EventRepository(session)
        
        # Próximos 7 días
        events = await repo.get_upcoming(
            tenant_id="default_tenant",
            user_id=1,
            days_ahead=7
        )
        
        for event in events:
            print(f"- {event.title}: {event.start_datetime}")
🔑 Conceptos Clave
Repository Pattern:
Separa lógica acceso datos de lógica negocio:

python
# ❌ Sin Repository (malo)
class EventAgent:
    async def create_event(self, data):
        # SQL directo en agent (acoplado)
        await session.execute("INSERT INTO events...")

# ✅ Con Repository (bueno)
class EventAgent:
    async def create_event(self, data):
        # Repository abstrae SQL
        event = await event_repo.create(**data)
Beneficios:

Testeable (mock repositories)

Reutilizable (mismo repo en múltiples agentes)

Mantenible (cambios SQL centralizados)

Async/Await:
Todo asyncio para no bloquear:

python
# Connection ✅
engine = create_async_engine(url)

# Session ✅
async with get_db() as session:
    # Queries
    result = await session.execute(select(User))
    await session.commit()
Multi-tenant Isolation:
Cada tenant solo ve sus datos:

python
# Todos los queries filtran por tenant_id
events = await repo.get_by_tenant(tenant_id="default")

# Foreign keys garantizan integridad
class Event(BaseModel):
    user_id = Column(Integer, ForeignKey('users.id'))
    tenant_id = Column(String(50), nullable=False, index=True)
🔒 Multi-Tenant Best Practices
Siempre incluir tenant_id
python
# ✅ CORRECTO: tenant_id explícito
users = await user_repo.get_all(tenant_id="company_a", filters={"is_active": True})

# ❌ INCORRECTO: falta tenant_id (query fallará)
users = await user_repo.get_all(filters={"is_active": True})
Isolation automático en queries
Todos los repositories automáticamente filtran por tenant_id en:

.get_all() → WHERE tenant_id = ?

.get_by_id() → WHERE id = ? AND tenant_id = ?

.update() → WHERE id = ? AND tenant_id = ?

.delete() → WHERE id = ? AND tenant_id = ?

Cambiar de tenant
python
# Mismo usuario, diferentes tenants
user_tenant_a = await repo.get_by_id(tenant_id="company_a", id=1)
user_tenant_b = await repo.get_by_id(tenant_id="company_b", id=1)

# Son usuarios diferentes, aunque tengan mismo ID local
assert user_tenant_a.tenant_id != user_tenant_b.tenant_id
🧪 Testing (COMPLETADO H02) ✅
Test Models:
python
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
Test Repositories:
python
@pytest.mark.asyncio
async def test_event_repository_create(test_session):
    repo = EventRepository(test_session)
    
    event = await repo.create(
        user_id=1,
        tenant_id="default",
        title="Test",
        start_datetime=datetime.now(timezone.utc)
    )
    
    assert event.id is not None
    assert event.title == "Test"
Test Multi-tenant Isolation:
python
@pytest.mark.asyncio
async def test_multi_tenant_isolation(test_session):
    repo = NoteRepository(test_session)
    
    # Crear nota tenant A
    note_a = await repo.create(
        tenant_id="tenant_a",
        user_id=1,
        title="Nota A"
    )
    
    # Buscar desde tenant B (no debe encontrar)
    notes_b = await repo.get_all(tenant_id="tenant_b", user_id=1)
    
    assert len(notes_b) == 0  # Isolation works ✅
Ejecutar Tests:
bash
# Tests específicos database
pytest src/tests/database/ -v

# Con coverage
pytest --cov=src/database --cov-report=html

# Tests pasando: 12/12 (100%) ✅
📊 Schema Database (IMPLEMENTADO ✅)
Tablas H02:
Tabla	Descripción	Columnas Clave	Estado
users	Usuarios Telegram	telegram_id (unique), tenant_id, preferences (JSONB)	✅
events	Eventos/Recordatorios	tenant_id, user_id, start_datetime, recurrence_rule, extra_data (JSONB)	✅
notes	Notas con tags	tenant_id, user_id, tags (ARRAY), category, is_pinned	✅
conversations	Sesiones FSM	tenant_id, session_id (unique), current_state, context_data (JSONB)	✅
message_history	Auditoría ML	tenant_id, conversation_id, intent_detected, entities_extracted (JSONB)	✅
Relationships:
text
User (1) ←→ (N) Event
User (1) ←→ (N) Note
User (1) ←→ (N) Conversation
Conversation (1) ←→ (N) MessageHistory
Características:

✅ 5 foreign keys con CASCADE delete

✅ 20+ índices de performance

✅ Multi-tenant support (tenant_id en todas)

✅ JSONB para metadata flexible

✅ ARRAY para tags (PostgreSQL native)

✅ Timezone-aware timestamps

🔐 Seguridad
Multi-tenant Isolation ✅:
tenant_id en todas las tablas

Foreign keys con ON DELETE CASCADE

Índices en tenant_id para performance

Row Level Security (H04)

SQL Injection ✅:
SQLAlchemy protege automáticamente

Usar siempre parámetros, nunca string formatting

Connection Security ✅:
SSL en producción (DATABASE_SSL_MODE=require)

Credentials en .env, nunca en código

Connection pooling limita conexiones

Auth trust mode solo en desarrollo

📈 Performance
Indexes (APLICADOS ✅):
✅ tenant_id en todas las tablas

✅ user_id en todas las tablas relacionadas

✅ datetime fields (start_datetime, created_at, last_activity)

✅ status, is_active para filtros comunes

✅ session_id, message_id para lookups únicos

✅ current_state, intent_detected para queries FSM/ML

Total: 20+ índices aplicados

Connection Pooling (CONFIGURADO ✅):
Pool size: 5 (desarrollo)

Max overflow: 10

Recycle: 3600 seconds (1h)

Timeout: 30 seconds

Query Optimization:
python
# ✅ Query optimizado (usa índice tenant_id + telegram_id)
user = await repo.get_by_telegram_id(tenant_id="default", telegram_id=123)

# ⚠️ Query lento (full table scan)
all_users = await repo.get_all(tenant_id="default")
target = [u for u in all_users if u.telegram_id == 123]
Batch Operations:
python
# ✅ Crear múltiples notas en una transacción
async with AsyncSessionLocal() as session:
    repo = NoteRepository(session)
    
    notes_data = [
        {"title": "Nota 1", "content": "..."},
        {"title": "Nota 2", "content": "..."},
    ]
    
    for data in notes_data:
        await repo.create(tenant_id="default", user_id=1, **data)
    
    await session.commit()  # Un solo commit
Eager Loading Relationships:
python
# ✅ Load user con sus notas en una query
from sqlalchemy.orm import selectinload

user = await session.execute(
    select(User)
    .where(User.tenant_id == "default", User.id == 1)
    .options(selectinload(User.notes))
)

# Ahora user.notes está cargado, sin N+1 queries
🔮 Próximos Pasos
H03: CoreRouter Integration (15-20 Nov)
Integrar repositories con CoreRouter

Intent Detector + Entity Extractor usarán database

Primera conversación con NLP completo

H04: Enterprise Features
Row Level Security (RLS)

Soft delete (deleted_at)

Audit logging (who, when, what)

Read replicas

Connection retry logic

Coverage ≥85%

H11: Kubernetes
High availability

Auto-scaling

Backup automation

Monitoring integrado

📝 Comandos Útiles
Migrations:
bash
# Ver estado actual ✅
alembic current

# Ver historial
alembic history

# Crear nueva migración
alembic revision --autogenerate -m "descripcion"

# Aplicar migraciones
alembic upgrade head

# Rollback
alembic downgrade -1
PostgreSQL:
bash
# Conectar a database
psql -U postgres -d thea_ia

# Dentro de psql:
\dt                    # List tables ✅
\d users               # Describe table
\di                    # List indexes
\q                     # Quit

# Ver datos
SELECT * FROM users LIMIT 5;
SELECT * FROM events WHERE tenant_id = 'default';
Testing:
bash
# Tests específicos
pytest src/tests/database/ -v

# Con coverage
pytest --cov=src/database --cov-report=html

# Output esperado: 12/12 tests passed ✅
🐛 Troubleshooting
1. WinError 64: Connection refused (Windows)
Síntoma:

text
OSError: [WinError 64] The specified network name is no longer available
Causa: PostgreSQL no responde en localhost en Windows

Solución:

text
# ❌ No funciona en Windows
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/theaia

# ✅ Usar 127.0.0.1 explícitamente
DATABASE_URL=postgresql+asyncpg://user:pass@127.0.0.1:5432/theaia
2. pg_hba.conf: authentication failed
Síntoma:

text
FATAL: password authentication failed for user "theaia_user"
Causa: PostgreSQL requiere password pero .env tiene otra config

Solución (Desarrollo):

Editar pg_hba.conf:

Windows: C:\Program Files\PostgreSQL\18\data\pg_hba.conf

macOS: /opt/homebrew/var/postgresql@16/pg_hba.conf

Linux: /etc/postgresql/16/main/pg_hba.conf

Cambiar método a trust:

text
# TYPE  DATABASE  USER   ADDRESS        METHOD
host    all       all    127.0.0.1/32   trust
Reiniciar PostgreSQL:

bash
# Windows (CMD como Administrador)
net stop postgresql-x64-18
net start postgresql-x64-18

# macOS
brew services restart postgresql@16

# Linux
sudo systemctl restart postgresql
3. Tests fallan: relation does not exist
Síntoma:

text
sqlalchemy.exc.ProgrammingError: relation "users" does not exist
Causa: Migraciones no aplicadas

Solución:

bash
# Verificar estado migraciones
alembic current

# Aplicar migraciones pendientes
alembic upgrade head

# Verificar tablas creadas
psql -U postgres -d thea_ia -c "\dt"
4. Async context manager error
Síntoma:

text
RuntimeError: Working outside of async context
Causa: Usar repository sin AsyncSessionLocal correctamente

Solución:

python
# ✅ CORRECTO: Async context manager
async with AsyncSessionLocal() as session:
    repo = UserRepository(session)
    users = await repo.get_all(tenant_id="default")

# ❌ INCORRECTO: Sin async context
repo = UserRepository()  # No session
users = await repo.get_all()  # Error
5. "metadata is a reserved word"
Síntoma:

text
sqlalchemy.exc.ProgrammingError: column "metadata" is a reserved word
Causa: Usar palabras reservadas PostgreSQL como nombres de columna

Solución:

python
# ❌ Evitar palabras reservadas
metadata = Column(JSON)

# ✅ Usar nombres alternativos
extra_data = Column(JSON)
📚 Recursos
SQLAlchemy 2.0

Alembic

asyncpg

PostgreSQL 18

Database Setup Guide

Tests Database

📊 Estado Actual (14 Nov 2025, 18:30 CET)
Versión: 0.3.0
H02 Progreso: 100% ✅
Última actualización: Sesión 11 (documentación completa)

Completado ✅:
✅ 7 Modelos SQLAlchemy con multi-tenant

✅ 6 Repositories CRUD con custom queries

✅ 12/12 tests pasando (100%)

✅ Async SQLAlchemy 2.0 configurado

✅ Alembic migrations setup

✅ Primera migración aplicada

✅ 5 tablas PostgreSQL operativas

✅ 20+ índices aplicados

✅ CASCADE relationships

✅ JSONB metadata flexible

✅ TelegramAdapter integration funcional

✅ Primera conversación real (12 nov 17:02)

✅ Troubleshooting documentado

✅ Ejemplos de uso completos

Próximo ⏳:
⏳ H03 CoreRouter + NLP básico (15-20 Nov)

⏳ Coverage ≥85% (H04)

⏳ Row Level Security (H04)

⏳ Optimizaciones avanzadas (H04)

Responsable: Álvaro Fernández Mota
Estado: H02 Database Layer 100% COMPLETO ✅ | Primera conversación funcional ✅ | H03 próximo 🚀