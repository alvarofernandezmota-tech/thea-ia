# Changelog - src/database/

Todos los cambios notables del módulo Database.

**Formato:** [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)  
**Versionado:** [Semantic Versioning](https://semver.org/)

---

## [0.3.0] - 2025-11-12 (H02 Day 1 COMPLETADO ✅)

**Sesión 8:** 14:30-17:20 (2h 50min)  
**Responsable:** Álvaro Fernández Mota  
**Estado:** H02 Database Layer COMPLETADO 100%

### ✅ Added (12 Nov 2025)

**Repositories (6 archivos, ~2,000 LOC):**
- `repositories/__init__.py` - Exports completos
- `repositories/base_repository.py` - CRUD genérico con multi-tenant
- `repositories/user_repository.py` - UserRepository con get_or_create_from_telegram
- `repositories/event_repository.py` - EventRepository con get_upcoming
- `repositories/note_repository.py` - NoteRepository con search y tags
- `repositories/conversation_repository.py` - ConversationRepository con FSM
- `repositories/message_history_repository.py` - MessageHistoryRepository con auditoría ML

**Tests (2 archivos, ~500 LOC):**
- `tests/database/test_repositories.py` - 12 tests completos
- `tests/database/README.md` - Documentación tests

**Características:**
- ✅ Repository Pattern completo
- ✅ CRUD operations (create, read, update, delete)
- ✅ Custom queries por repository
- ✅ Multi-tenant isolation automático
- ✅ Type hints completos
- ✅ Docstrings exhaustivos con ejemplos
- ✅ Async/await support
- ✅ Error handling

### ✅ Changed (12 Nov 2025)

**database/__init__.py:**
- Añadidos exports de repositories
- Ahora exporta: BaseRepository, UserRepository, EventRepository, NoteRepository, ConversationRepository, MessageHistoryRepository

**connection.py:**
- Añadido import `text` para queries raw
- Fix `test_connection()` con sintaxis SQLAlchemy 2.0

**Estructura:**
src/theaia/database/
├── models/ ✅ (7 archivos)
├── repositories/ ✅ (7 archivos) 🆕
├── migrations/ ✅ (2 archivos)
└── tests/database/ ✅ (2 archivos) 🆕

text

### ✅ Fixed (12 Nov 2025)

- Renombrado `conversacion_repository.py` → `conversation_repository.py` (typo)
- Fix imports en tests para usar `AsyncSessionLocal` directamente
- Fix `get_db()` context manager issue en tests

### ❌ Removed (12 Nov 2025)

- `repositories/context_repository.py` - Legacy JSON-based context (obsoleto con PostgreSQL)

### 🧪 Tests (12 Nov 2025)

**Estado:** ✅ 12/12 tests pasando (100% success rate)

**Tests añadidos:**
1. `test_database_connection` - Conexión PostgreSQL
2. `test_repositories_instantiate` - Instanciación repositories
3. `test_user_repository_create` - CRUD User
4. `test_user_repository_get_or_create` - Lógica Telegram
5. `test_event_repository_create` - CRUD Event
6. `test_event_repository_get_upcoming` - Query custom
7. `test_note_repository_create` - CRUD Note con tags
8. `test_note_repository_search` - Búsqueda full-text
9. `test_conversation_repository_get_or_create` - FSM Session
10. `test_conversation_repository_update_state` - FSM State Update
11. `test_message_history_repository_add_message` - Auditoría ML
12. `test_multi_tenant_isolation` - Multi-tenant security

**Coverage:**
- BaseRepository: 55%
- UserRepository: 58%
- EventRepository: 43%
- NoteRepository: 29%
- ConversationRepository: 48%
- MessageHistoryRepository: 27%
- **Total database layer:** ~40%

**Comando:**
pytest src/theaia/tests/database/test_repositories.py -v

Result: 12 passed, 41 warnings in 3.19s
text

### 📊 Métricas Sesión 8

**Archivos creados/modificados:** 25 archivos
- Código: 18 archivos (~3,000 LOC)
- Docs: 6 archivos
- Tests: 2 archivos (~500 LOC)

**Líneas de código:**
- Repositories: ~2,000 LOC
- Tests: ~500 LOC
- Docs: ~1,500 líneas

**Total acumulado Database:**
- Modelos: ~400 LOC
- Config: ~100 LOC
- Repositories: ~2,000 LOC
- Tests: ~500 LOC
- **Total:** ~3,000 LOC producción + 500 LOC tests

---

## [0.2.0] - 2025-11-12 (H02 Day 1 - Database Layer Base)

**Sesiones 6-7:** 14:30-16:17  
**Duración:** 1h 47min

### ✅ Added (12 Nov 2025)

**Models (7 archivos):**
- `models/base.py` - BaseModel con tenant_id, timestamps
- `models/user.py` - User (Telegram users)
- `models/event.py` - Event (ex Reminder)
- `models/note.py` - Note con tags ARRAY
- `models/conversation.py` - Conversation (FSM sessions)
- `models/message_history.py` - MessageHistory (ML audit)

**Configuration (3 archivos):**
- `connection.py` - AsyncEngine con asyncpg
- `session.py` - AsyncSessionLocal + get_db()
- `base.py` - DeclarativeBase SQLAlchemy 2.0

**Migrations (2 archivos):**
- `migrations/env.py` - Async environment config
- `migrations/versions/e0a17d850507_initial_schema.py` - Primera migración (5 tablas)

**Características:**
- ✅ SQLAlchemy 2.0 async
- ✅ Multi-tenant support (tenant_id)
- ✅ Timezone-aware timestamps
- ✅ JSONB metadata flexible
- ✅ ARRAY tags (PostgreSQL native)
- ✅ 20+ indexes performance
- ✅ CASCADE relationships

### ✅ Changed (12 Nov 2025)

**Renombrados:**
- `reminder.py` → `event.py` (más genérico)
- `metadata` → `extra_data` (palabra reservada)

**PostgreSQL:**
- 5 tablas creadas exitosamente
- Migración aplicada: e0a17d850507
- Índices: 20+ creados

### 🐛 Fixed (12 Nov 2025)

**Troubleshooting resuelto:**
- ✅ WinError 64: `localhost` → `127.0.0.1`
- ✅ Authentication failed: `pg_hba.conf` trust mode
- ✅ metadata reserved word: renombrado a `extra_data`
- ✅ CASCADE drops: añadido `CASCADE` a drops

---

## [0.1.0] - 2025-11-11 (H01 - Planificación)

**Sesión 5:** 11 Nov, 1h 30min  
**Estado:** Diseño y arquitectura

### ✅ Added (11 Nov 2025)

**Documentación (5 archivos):**
- `database-README.md` - Overview y guía uso
- `database-ROADMAP.md` - Planificación H02-H11
- `database-CHANGELOG.md` - Este archivo
- `database-STRUCTURE.md` - Arquitectura detallada
- `database-DEPENDENCIES.md` - Dependencias y setup

**Decisiones arquitectónicas:**
- PostgreSQL como database principal
- SQLAlchemy 2.0 async ORM
- Repository Pattern
- Multi-tenant desde H02
- Alembic para migrations

---

## 🎯 Próximos Pasos

### H02 Day 2 (13 Nov) - Adapter Integration
- [ ] TelegramAdapter con PostgreSQL
- [ ] Primera conversación persistente
- [ ] Tests integration adapter + database
- [ ] Coverage >85%

### H04 (20-23 Nov) - Database Enterprise
- [ ] Row Level Security (RLS)
- [ ] Soft delete (deleted_at)
- [ ] Audit logging completo
- [ ] Read replicas
- [ ] Connection retry logic
- [ ] Performance optimization

### H11 (Jan 2026) - Kubernetes Production
- [ ] High availability setup
- [ ] Auto-scaling database
- [ ] Backup automation
- [ ] Monitoring integration
- [ ] Disaster recovery

---

## 📋 Notas Técnicas

### Breaking Changes
**v0.2.0 → v0.3.0:**
- Eliminado `context_repository.py` (legacy)
- Todos los accesos a contexto ahora usan `ConversationRepository`

**Migración:**
Antes (v0.2.0)
from src.theaia.database.repositories.context_repository import save_context
save_context(user_id, state, context)

Ahora (v0.3.0)
from src.theaia.database.repositories import ConversationRepository
conv_repo = ConversationRepository(session)
await conv_repo.update_state(conv_id, tenant_id, state, context)

text

### Deprecations
- `context_repository.py` - Removido en v0.3.0

### Known Issues
**Warnings en tests:**
- `MovedIn20Warning`: `declarative_base()` → usar `DeclarativeBase` (low priority)
- `DeprecationWarning`: `datetime.utcnow()` → usar `datetime.now(UTC)` (low priority)

---

**Última actualización:** 12 Nov 2025, 17:20 CET  
**Versión actual:** 0.3.0  
**Estado:** ✅ H02 COMPLETADO