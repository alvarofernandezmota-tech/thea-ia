# Estructura Planificada - src/database/

**Módulo:** Database (Persistencia de datos)  
**Propósito:** Gestión completa de persistencia con PostgreSQL  
**Patrón:** Repository Pattern + SQLAlchemy ORM + Alembic Migrations

---

## 📋 Estado Actual (12 Nov 2025, 16:22 CET - H02 Day 1)

src/database/
│
├── init.py ✅
│ # Exports: engine, get_db, Base, all models
│ # Estado: COMPLETO
│
├── connection.py ✅
│ # AsyncEngine con asyncpg
│ # test_connection() utility
│ # URL: postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia
│ # Estado: COMPLETO
│
├── session.py ✅
│ # AsyncSessionLocal (session factory)
│ # get_db() async context manager
│ # init_db() / close_db() lifecycle
│ # Estado: COMPLETO
│
├── base.py ✅
│ # DeclarativeBase SQLAlchemy 2.0
│ # BaseModel con tenant_id, timestamps
│ # Estado: COMPLETO
│
├── models/ ✅
│ │
│ ├── init.py ✅
│ │ # Exports: User, Event, Note, Conversation, MessageHistory
│ │
│ ├── base.py ✅
│ │ # BaseModel abstracto
│ │ # Columns:
│ │ # - id: int (PK, autoincrement)
│ │ # - tenant_id: str(50) (not null, indexed)
│ │ # - created_at: datetime (auto, timezone-aware)
│ │ # - updated_at: datetime (auto, timezone-aware)
│ │ # Methods:
│ │ # - to_dict() -> dict
│ │ # - repr() -> str
│ │
│ ├── user.py ✅
│ │ # Modelo User
│ │ # Tabla: users
│ │ # Inherits: BaseModel
│ │ # Columns:
│ │ # - telegram_id: bigint (unique, not null, indexed)
│ │ # - username: str(255) (nullable)
│ │ # - first_name: str(255) (nullable)
│ │ # - last_name: str(255) (nullable)
│ │ # - language_code: str(10) (nullable)
│ │ # - timezone: str(50) (nullable)
│ │ # - is_active: bool (default=True, indexed)
│ │ # - preferences: JSONB (nullable)
│ │ # Relationships:
│ │ # - events: List[Event] (back_populates="user", cascade="all, delete-orphan")
│ │ # - notes: List[Note] (back_populates="user", cascade="all, delete-orphan")
│ │ # - conversations: List[Conversation] (back_populates="user", cascade="all, delete-orphan")
│ │ # Indexes:
│ │ # - ix_users_tenant_id (tenant_id)
│ │ # - ix_users_telegram_id (telegram_id)
│ │ # - ix_users_is_active (is_active)
│ │
│ ├── event.py ✅
│ │ # Modelo Event (ex Reminder)
│ │ # Tabla: events
│ │ # Inherits: BaseModel
│ │ # Columns:
│ │ # - user_id: int (FK → users.id, not null)
│ │ # - title: str(500) (not null)
│ │ # - description: text (nullable)
│ │ # - start_datetime: datetime (not null, timezone-aware, indexed)
│ │ # - end_datetime: datetime (nullable, timezone-aware)
│ │ # - location: str(500) (nullable)
│ │ # - event_type: str(50) (nullable)
│ │ # - status: str(20) (nullable, indexed) [pending|completed|cancelled]
│ │ # - reminder_minutes: int (nullable)
│ │ # - recurrence_rule: str(200) (nullable)
│ │ # - external_id: str(255) (nullable) [sync Google Calendar]
│ │ # - extra_data: JSONB (nullable) [metadata flexible]
│ │ # Relationships:
│ │ # - user: User (back_populates="events")
│ │ # Indexes:
│ │ # - ix_events_tenant_id (tenant_id)
│ │ # - ix_events_user_id (user_id)
│ │ # - ix_events_start_datetime (start_datetime)
│ │ # - ix_events_status (status)
│ │
│ ├── note.py ✅
│ │ # Modelo Note
│ │ # Tabla: notes
│ │ # Inherits: BaseModel
│ │ # Columns:
│ │ # - user_id: int (FK → users.id, not null)
│ │ # - title: str(500) (nullable)
│ │ # - content: text (not null)
│ │ # - category: str(100) (nullable, indexed)
│ │ # - tags: ARRAY[text] (nullable)
│ │ # - priority: int (nullable)
│ │ # - is_pinned: bool (default=False, indexed)
│ │ # - reminder_datetime: datetime (nullable, timezone-aware)
│ │ # - extra_data: JSONB (nullable)
│ │ # Relationships:
│ │ # - user: User (back_populates="notes")
│ │ # Indexes:
│ │ # - ix_notes_tenant_id (tenant_id)
│ │ # - ix_notes_user_id (user_id)
│ │ # - ix_notes_category (category)
│ │ # - ix_notes_is_pinned (is_pinned)
│ │
│ ├── conversation.py ✅
│ │ # Modelo Conversation (sesiones FSM)
│ │ # Tabla: conversations
│ │ # Inherits: BaseModel
│ │ # Columns:
│ │ # - user_id: int (FK → users.id, not null)
│ │ # - session_id: str(255) (not null, unique, indexed)
│ │ # - current_state: str(50) (not null, indexed)
│ │ # - context_data: JSONB (nullable) [FSM context]
│ │ # - last_message_id: str(255) (nullable)
│ │ # - is_active: bool (default=True, indexed)
│ │ # - started_at: datetime (not null, timezone-aware)
│ │ # - last_activity: datetime (not null, timezone-aware)
│ │ # Relationships:
│ │ # - user: User (back_populates="conversations")
│ │ # - messages: List[MessageHistory] (back_populates="conversation", cascade="all, delete-orphan")
│ │ # Indexes:
│ │ # - ix_conversations_tenant_id (tenant_id)
│ │ # - ix_conversations_user_id (user_id)
│ │ # - ix_conversations_session_id (session_id)
│ │ # - ix_conversations_current_state (current_state)
│ │ # - ix_conversations_is_active (is_active)
│ │
│ └── message_history.py ✅
│ # Modelo MessageHistory (auditoría ML)
│ # Tabla: message_history
│ # Inherits: BaseModel
│ # Columns:
│ # - conversation_id: int (FK → conversations.id, not null)
│ # - message_id: str(255) (not null, indexed)
│ # - user_message: text (nullable)
│ # - bot_response: text (nullable)
│ # - intent_detected: str(100) (nullable, indexed)
│ # - entities_extracted: JSONB (nullable) [NER results]
│ # - confidence_score: float (nullable)
│ # - processing_time_ms: int (nullable)
│ # Relationships:
│ # - conversation: Conversation (back_populates="messages")
│ # Indexes:
│ # - ix_message_history_tenant_id (tenant_id)
│ # - ix_message_history_conversation_id (conversation_id)
│ # - ix_message_history_message_id (message_id)
│ # - ix_message_history_intent_detected (intent_detected)
│
├── repositories/ ⏳ PRÓXIMO (H02 Day 2)
│ │
│ ├── init.py
│ │ # Exports: todos los repositories
│ │
│ ├── base_repository.py
│ │ # Repository base abstracto
│ │ # Patrón Repository para CRUD
│ │ #
│ │ # Class BaseRepository[T]:
│ │ # Methods:
│ │ # - async create(entity: T) -> T
│ │ # - async get_by_id(id: int, tenant_id: str) -> T | None
│ │ # - async get_all(tenant_id: str, skip: int, limit: int, filters: dict) -> List[T]
│ │ # - async update(entity: T) -> T
│ │ # - async delete(id: int, tenant_id: str) -> bool
│ │ # - async count(tenant_id: str, filters: dict) -> int
│ │
│ ├── user_repository.py
│ │ # UserRepository(BaseRepository[User])
│ │ # CRUD User + queries específicas
│ │ #
│ │ # Additional Methods:
│ │ # - async get_by_telegram_id(telegram_id: int, tenant_id: str) -> User | None
│ │ # - async get_or_create_from_telegram(telegram_data: dict, tenant_id: str) -> User
│ │ # - async update_preferences(user_id: int, tenant_id: str, preferences: dict) -> User
│ │ # - async get_active_users(tenant_id: str) -> List[User]
│ │
│ ├── event_repository.py
│ │ # EventRepository(BaseRepository[Event])
│ │ # CRUD Event + queries
│ │ #
│ │ # Additional Methods:
│ │ # - async get_by_user(user_id: int, tenant_id: str, status: str) -> List[Event]
│ │ # - async get_upcoming(user_id: int, tenant_id: str, hours: int) -> List[Event]
│ │ # - async mark_completed(event_id: int, tenant_id: str) -> Event
│ │ # - async get_by_date_range(user_id: int, tenant_id: str, start, end) -> List[Event]
│ │
│ ├── note_repository.py
│ │ # NoteRepository(BaseRepository[Note])
│ │ #
│ │ # Additional Methods:
│ │ # - async get_by_user(user_id: int, tenant_id: str, skip, limit) -> List[Note]
│ │ # - async search(user_id: int, tenant_id: str, query: str) -> List[Note]
│ │ # - async get_by_tags(user_id: int, tenant_id: str, tags: List[str]) -> List[Note]
│ │ # - async toggle_pin(note_id: int, tenant_id: str) -> Note
│ │
│ ├── conversation_repository.py
│ │ # ConversationRepository(BaseRepository[Conversation])
│ │ #
│ │ # Additional Methods:
│ │ # - async get_by_session_id(session_id: str, tenant_id: str) -> Conversation | None
│ │ # - async get_active(user_id: int, tenant_id: str) -> List[Conversation]
│ │ # - async update_state(conversation_id: int, tenant_id: str, state: str, context: dict) -> Conversation
│ │ # - async close_conversation(conversation_id: int, tenant_id: str) -> Conversation
│ │
│ └── message_history_repository.py
│ # MessageHistoryRepository(BaseRepository[MessageHistory])
│ #
│ # Additional Methods:
│ # - async add_message(conversation_id: int, tenant_id: str, data: dict) -> MessageHistory
│ # - async get_recent(conversation_id: int, tenant_id: str, limit: int) -> List[MessageHistory]
│ # - async get_by_intent(tenant_id: str, intent: str, limit: int) -> List[MessageHistory]
│ # - async get_conversation_history(conversation_id: int, tenant_id: str) -> List[MessageHistory]
│
├── migrations/ ✅
│ │
│ ├── env.py ✅
│ │ # Alembic environment configuration
│ │ # Async support
│ │ # Import Base metadata
│ │ # Import all models
│ │
│ ├── script.py.mako
│ │ # Template para nuevas migraciones
│ │
│ └── versions/
│ │
│ └── e0a17d850507_initial_schema.py ✅
│ # Primera migración (285 líneas)
│ # Crea 5 tablas:
│ # - users (12 cols + 3 indexes)
│ # - events (15 cols + 4 indexes)
│ # - notes (12 cols + 4 indexes)
│ # - conversations (12 cols + 5 indexes)
│ # - message_history (11 cols + 4 indexes)
│ # Crea 5 foreign keys CASCADE
│ # Crea 20+ indexes performance
│ # Elimina schema antiguo CASCADE
│ # Estado: APLICADA ✅ (12 Nov 16:11)
│
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅

text

**Estado:** H02 Day 1 COMPLETADO ✅ (50% H02 total)

---

## 🎯 H02 Completo (12-16 Nov 2025): Database Base + Adapter

### ✅ Día 1 (12 Nov) - COMPLETADO 100%

**Estructura Implementada:**

src/database/
├── init.py ✅ (exports engine, get_db, Base, models)
├── connection.py ✅ (AsyncEngine + test_connection)
├── session.py ✅ (AsyncSessionLocal + get_db + init/close)
├── base.py ✅ (BaseModel con tenant_id + timestamps)
├── models/ ✅
│ ├── init.py ✅
│ ├── base.py ✅
│ ├── user.py ✅
│ ├── event.py ✅
│ ├── note.py ✅
│ ├── conversation.py ✅
│ └── message_history.py ✅
└── migrations/ ✅
├── env.py ✅
└── versions/
└── e0a17d850507_initial_schema.py ✅ (aplicada)

text

**Criterio Done Día 1:** ✅ COMPLETO
- ✅ PostgreSQL conecta
- ✅ 5 tablas creadas
- ✅ Índices aplicados
- ✅ Multi-tenant operativo
- ✅ Migración aplicada exitosamente

---

### ⏳ Día 2 (13 Nov) - PENDIENTE

**Estructura a Implementar:**

src/database/
└── repositories/
├── init.py
├── base_repository.py
├── user_repository.py
├── event_repository.py
├── note_repository.py
├── conversation_repository.py
└── message_history_repository.py

text

**Criterio Done Día 2:**
- ✅ CRUD User funciona
- ✅ CRUD Event funciona
- ✅ CRUD Note funciona
- ✅ TelegramAdapter guarda en PostgreSQL
- ✅ tenant_id isolation verificado
- ✅ Tests repositories >80% coverage

---

### ⏳ Día 3 (14 Nov) - OBJETIVO FINAL

**Integration:**
- ⏳ Primera conversación completa (Telegram → DB → respuesta)
- ⏳ Conversation + MessageHistory guardados
- ⏳ Context recovery funciona
- ⏳ Multi-turn conversation persistente

**Criterio Done Día 3:**
- ✅ Todas las tablas operativas
- ✅ Todos los repositories funcionan
- ✅ Primera conversación completa funcional
- ✅ Tests >85% coverage

---

## 🔮 H04 (20-23 Nov 2025): Database Enterprise

### Estructura Ampliada:

src/database/
├── connection.py (extendido)
│ # Connection pooling avanzado
│ # Read replicas support
│ # Retry logic
│ # Health checks
│
├── base.py (extendido)
│ # SoftDeleteMixin activo
│ # AuditMixin (who, when, what)
│
├── security.py ← 🆕 H04
│ # Row Level Security (RLS)
│ # Policies PostgreSQL
│ # Tenant isolation enforcement
│
├── models/ (todos extendidos)
│ # Soft delete en todos (deleted_at, is_deleted)
│ # Audit fields (created_by, updated_by)
│ # RLS policies aplicadas
│
└── repositories/ (todos extendidos)
# Soft delete queries
# Audit logging
# Performance optimization

text

---

## 📐 Patrones de Diseño

### Repository Pattern:
- Abstrae acceso a datos
- Encapsula queries complejas
- Facilita testing (mock repositories)
- Separa lógica negocio de persistencia

### Unit of Work:
- Session como transaction
- Commit explícito
- Rollback automático en error

### Active Record vs Data Mapper:
- **Data Mapper (elegido)**
- Modelos SQLAlchemy solo estructura
- Lógica en repositories
- Modelos Pydantic para validación

---

## 🔗 Dependencias Internas

src/database/ depende de:
├── src/config (settings, logger)
└── src/models (schemas Pydantic para validación) [H02 Day 2]

text
undefined
src/database/ es usado por:
├── src/agents/ (todos los agentes) [H02 Day 2+]
├── src/adapters/ (TelegramAdapter) [H02 Day 2]
├── src/core/ (ConversationRepository) [H02 Day 3]
└── src/services/ (H05-H06)

text

---

## 📊 Métricas Implementadas (12 Nov)

### H02 Day 1:
- **Archivos Python:** 15 archivos
- **Líneas código:** ~1,200 LOC (modelos + config)
- **Líneas migración:** 285 LOC
- **Tests:** 0 LOC (próximo Día 2)
- **Cobertura objetivo:** >85% (próximo)

### Tablas:
- **5 tablas** principales ✅
- **~60 columnas** total ✅
- **20+ indexes** ✅
- **5 foreign keys** CASCADE ✅
- **Multi-tenant** en todas ✅

---

## 🎯 Criterios de Completitud

### H02 Done cuando:
- ✅ Connection funciona (async) **COMPLETO**
- ✅ 5 modelos definidos **COMPLETO**
- ⏳ 5 repositories funcionan (CRUD)
- ✅ Alembic migración ejecutada **COMPLETO**
- ✅ Tablas creadas en PostgreSQL **COMPLETO**
- ⏳ Tests >85% coverage
- ✅ Multi-tenant funciona **COMPLETO**
- ✅ Timestamps automáticos **COMPLETO**
- ✅ Foreign keys correctas **COMPLETO**
- ✅ Indexes creados **COMPLETO**
- ⏳ Primera conversación guarda en DB

**Progreso:** 50% ✅ (Database Layer completo, falta Adapter + Repos)

---

## 🚀 Comandos Desarrollo

### Setup PostgreSQL (COMPLETADO ✅):

PostgreSQL 18 instalado nativamente
Path: C:\Program Files\PostgreSQL\18\
Database: thea_ia creada
User: postgres
Auth: trust mode
text

### Migrations (APLICADAS ✅):

Estado actual
alembic current

Output: e0a17d850507 (head), Initial schema with tenant support
Historial
alembic history

Crear nueva migración (próximo)
alembic revision --autogenerate -m "add new feature"

Aplicar migraciones
alembic upgrade head

Rollback
alembic downgrade -1

text

### Testing (PRÓXIMO):

Ejecutar tests database
pytest src/tests/unit/test_database/ -v

Con coverage
pytest --cov=src/database --cov-report=html

Solo models
pytest src/tests/unit/test_database/test_models.py

Solo repositories
pytest src/tests/unit/test_database/test_repositories.py

text

---

## 📝 Notas Implementación

### AsyncIO ✅:
- Todos los métodos repository async (próximo)
- Usar asyncpg driver (no psycopg2 sync) ✅
- AsyncSession siempre con context manager ✅

### Multi-tenant Isolation ✅:
- tenant_id en todas las tablas ✅
- Todos los queries filtrarán por tenant_id (próximo)
- Foreign keys con ON DELETE CASCADE ✅
- Indexes en tenant_id para performance ✅

### Timestamps ✅:
- created_at: auto en INSERT ✅
- updated_at: auto en UPDATE ✅
- Usar BaseModel en todos los modelos ✅
- Timezone-aware (DateTime(timezone=True)) ✅

### Performance ✅:
- Connection pooling (5-10 connections) ✅
- Indexes en columnas frecuentes ✅
- Eager loading relationships cuando necesario (próximo)
- Lazy loading por defecto ✅

---

## 🔄 Cambios Arquitectónicos (12 Nov)

### vs Planificación Original (H01):

| Aspecto | Planificado H01 | Implementado H02 | Razón |
|---------|----------------|------------------|-------|
| Modelo reminder | reminder.py | **event.py** | Más genérico, soporta eventos + recordatorios |
| Campo metadata | metadata (Column) | **extra_data** | metadata es palabra reservada SQLAlchemy |
| Modelo task | task.py planificado | **No implementado** | No prioritario H02, próximo H03 |
| Modelo context | context.py historial | **conversation.py + message_history.py** | Separación FSM vs auditoría ML |
| Tablas | 6 planificadas | **5 implementadas** | Task pospuesta a H03 |
| Multi-tenant | Planeado | **Implementado** | Decisión Sesión 5 (11 Nov) |

---

**Última actualización:** 12 Nov 2025, 16:22 CET  
**Versión:** 2.0  
**Responsable:** Álvaro Fernández Mota

**Estado:** H02 Day 1 COMPLETADO ✅ | Database Layer 50% | Structure documented 🚀
