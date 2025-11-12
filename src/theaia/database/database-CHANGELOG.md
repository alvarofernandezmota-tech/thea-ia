
# Changelog - src/database/

Todos los cambios notables en el módulo database/ serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),  
y este proyecto adhiere a [Semantic Versioning](https://semver.org/lang/es/).

---

## [Unreleased]

### Planificado para H02 Day 2 (13 Nov 2025)
- Repositories pattern completo
- TelegramAdapter integration
- CRUD operations (User, Event, Note, Conversation, MessageHistory)
- Integration tests bot + database
- Primera conversación persistente

### Planificado para H04 (20-23 Nov 2025)
- Soft delete (SoftDeleteMixin)
- Row Level Security (RLS)
- Audit logging (AuditMixin)
- Read replicas support
- Connection retry logic
- Performance optimization

### Planificado para H11 (Feb 2026)
- High availability (primary + replicas)
- Automatic failover
- Backup automation
- Prometheus metrics
- Horizontal scaling

---

## [0.2.0] - 2025-11-12 (H02 Day 1) ✅

### Added

**Connection Management:**
- ✅ `connection.py` con AsyncEngine (asyncpg driver)
- ✅ `session.py` con AsyncSessionLocal session factory
- ✅ `get_db()` async context manager para dependency injection
- ✅ `init_db()` función para crear tablas
- ✅ `close_db()` función para cerrar conexiones
- ✅ `test_connection()` utility en connection.py
- ✅ Connection pooling configuration (NullPool desarrollo)

**Base Models:**
- ✅ `base.py` con DeclarativeBase SQLAlchemy 2.0
- ✅ `BaseModel` con multi-tenant support (tenant_id)
- ✅ Timestamps automáticos (created_at, updated_at)
- ✅ `to_dict()` method en BaseModel
- ✅ `__repr__()` method en BaseModel

**SQLAlchemy Models (7 modelos):**
- ✅ `models/user.py` - Usuario Telegram
  - telegram_id (BigInteger, unique)
  - username, first_name, last_name
  - language_code, timezone
  - is_active (Boolean, indexed)
  - preferences (JSONB)
  - Relationships: events, notes, conversations
- ✅ `models/event.py` - Eventos/Recordatorios
  - title, description (Text)
  - start_datetime, end_datetime (timezone-aware)
  - location, event_type, status (indexed)
  - reminder_minutes (Integer)
  - recurrence_rule (String)
  - external_id (sync integraciones)
  - extra_data (JSONB) - fix metadata reservada
- ✅ `models/note.py` - Notas
  - title, content (Text, not null)
  - category (indexed), priority
  - tags (ARRAY Text)
  - is_pinned (Boolean, indexed)
  - reminder_datetime (timezone-aware)
  - extra_data (JSONB)
- ✅ `models/conversation.py` - Sesiones FSM
  - session_id (unique, indexed)
  - current_state (FSM, indexed)
  - context_data (JSONB)
  - last_message_id
  - is_active (Boolean, indexed)
  - started_at, last_activity (timezone-aware)
- ✅ `models/message_history.py` - Auditoría ML
  - message_id (indexed)
  - user_message, bot_response (Text)
  - intent_detected (indexed)
  - entities_extracted (JSONB)
  - confidence_score (Float)
  - processing_time_ms (Integer)
- ✅ `models/__init__.py` - Exports completos

**Migrations:**
- ✅ Alembic configurado para async
- ✅ `alembic.ini` con timezone UTC, logging
- ✅ `migrations/env.py` con async environment
- ✅ `migrations/versions/e0a17d850507_initial_schema.py` (285 líneas)
  - Crea 5 tablas (users, events, notes, conversations, message_history)
  - 20+ índices de performance
  - Foreign keys con ondelete='CASCADE'
  - Elimina schema antiguo con CASCADE

**Features:**
- ✅ Multi-tenant support (tenant_id en todas las tablas)
- ✅ Timestamps automáticos (created_at, updated_at)
- ✅ Foreign keys con CASCADE delete
- ✅ Índices en columnas frecuentes (tenant_id, user_id, datetime, status, is_active)
- ✅ JSONB para metadata flexible (preferences, extra_data, context_data, entities)
- ✅ ARRAY para tags (PostgreSQL native)
- ✅ Timezone-aware timestamps (DateTime(timezone=True))
- ✅ BigInteger para telegram_id (soporta IDs grandes)

**Database Schema (aplicado exitosamente):**
- ✅ Tabla `users` con 12 columnas + 3 índices
- ✅ Tabla `events` con 15 columnas + 4 índices + FK user_id
- ✅ Tabla `notes` con 12 columnas + 4 índices + FK user_id
- ✅ Tabla `conversations` con 12 columnas + 5 índices + FK user_id + unique session_id
- ✅ Tabla `message_history` con 11 columnas + 4 índices + FK conversation_id
- ✅ 20+ índices totales
- ✅ 5 foreign keys con CASCADE
- ✅ Schema antiguo eliminado (9 tablas obsoletas)

**Configuration:**
- ✅ `.env` actualizado y documentado por hitos
- ✅ DATABASE_URL sin password (trust mode desarrollo)
- ✅ Connection: 127.0.0.1 (fix WinError 64)
- ✅ Driver: asyncpg para async PostgreSQL

**Dependencies:**
- ✅ sqlalchemy==2.0.23
- ✅ asyncpg==0.29.0
- ✅ psycopg2-binary==2.9.9 (Alembic sync)
- ✅ alembic==1.12.1
- ✅ greenlet==3.0.1

**Documentation:**
- ✅ README.md actualizado
- ✅ ROADMAP.md actualizado
- ✅ CHANGELOG.md actualizado (este archivo)
- ✅ STRUCTURE.md actualizado
- ✅ DEPENDENCIES.md actualizado
- ✅ Docstrings completos en todos los modelos
- ✅ Comentarios arquitectónicos en migración

### Changed
- 🔄 Modelo `reminder` → `event` (más genérico, soporta eventos + recordatorios)
- 🔄 Campo `metadata` → `extra_data` (evita palabra reservada SQLAlchemy)
- 🔄 Arquitectura: Basada en archive + adaptaciones S40
- 🔄 Multi-tenant: Añadido tenant_id a todos los modelos (decisión Sesión 5)
- 🔄 Timezone: Todos los DateTime ahora timezone-aware

### Fixed
- 🐛 Fix conexión PostgreSQL WinError 64 (localhost → 127.0.0.1)
- 🐛 Fix pg_hba.conf (modo trust para desarrollo)
- 🐛 Fix DATABASE_URL sin password
- 🐛 Fix palabra reservada `metadata` → `extra_data`
- 🐛 Fix migración CASCADE para eliminar tablas antiguas

### Migration
- ✅ Primera migración `e0a17d850507_initial_schema.py` aplicada exitosamente
- ✅ 5 tablas creadas
- ✅ 20+ índices aplicados
- ✅ Schema antiguo eliminado
- ✅ Rollback disponible (downgrade())

### Tests
- ⏳ test_connection.py (pendiente Día 2)
- ⏳ test_models.py (pendiente Día 2)
- ⏳ test_repositories.py (pendiente Día 2)
- ⏳ test_integration.py (pendiente Día 3)

### Performance
- ✅ Índices en user_id para isolation
- ✅ Índices en datetime para queries temporales
- ✅ Índices en status/is_active para filtros
- ✅ Índices en tenant_id para multi-tenant
- ✅ Foreign keys para integridad referencial
- ✅ CASCADE para deletes eficientes

### Security
- ✅ SQLAlchemy parameterized queries (SQL injection protection)
- ✅ Multi-tenant isolation (tenant_id + índices)
- ✅ Foreign keys para integridad
- ✅ No secrets in code (todo en .env)
- ✅ Connection pooling limits
- ⏳ RLS (H04)
- ⏳ Encryption at rest (H15)

### Session Details (12 Nov 2025)
**Sesión 8: H02 Database Implementation**
- **Horario:** 14:30-16:17 (1h 47min)
- **Tipo:** Implementación PostgreSQL Database Layer
- **Resultado:** H02 Day 1 100% completado ✅
- **Progreso H02:** 50% (Database Layer listo, falta Adapter + Repos)

**Fases:**
1. **Modelos SQLAlchemy (1h):** 7 modelos completos con multi-tenant
2. **Configuración Async (20min):** session.py, connection.py, .env, alembic
3. **Troubleshooting (15min):** Fix conexión PostgreSQL
4. **Migración (12min):** Primera migración generada y aplicada

**Archivos Creados/Modificados:** 16 archivos
- 7 modelos Python
- 4 archivos configuración
- 2 archivos Alembic
- 1 archivo migración (285 líneas)
- 2 archivos documentación

---

## [0.1.0] - 2025-11-03 (H01)

### Added

**Estructura inicial del módulo:**
- Documentación completa:
  - README.md - Overview y quick start
  - ROADMAP.md - Evolución planificada
  - CHANGELOG.md - Este archivo
  - STRUCTURE.md - Estructura detallada por hito
  - DEPENDENCIES.md - Dependencias y setup
- Arquitectura definida (Repository Pattern + SQLAlchemy + Alembic)
- Schema database planificado (6 tablas)
- Patrones seleccionados (async, multi-tenant, user isolation)

**Planning:**
- H02: Database base funcional
- H04: Enterprise features (RLS, soft delete, audit)
- H11: High availability + Kubernetes

---

## Tipos de Cambios

- **Added** - Para nuevas funcionalidades
- **Changed** - Para cambios en funcionalidades existentes
- **Deprecated** - Para funcionalidades que serán eliminadas
- **Removed** - Para funcionalidades eliminadas
- **Fixed** - Para corrección de bugs
- **Security** - Para correcciones de seguridad
- **Migration** - Para cambios en schema database
- **Performance** - Para mejoras de rendimiento

---

## Database Migrations

### Tracking Schema Changes

Cada cambio en schema debe tener:
- Nueva migración Alembic
- Tests para nueva estructura
- Documentación en este CHANGELOG
- Migration guide si breaking change

### [0.2.0] Migration Guide

**From v0.1.0 (planning) to v0.2.0 (implementation)**

No migration needed - v0.1.0 solo tenía documentación.  
Primera implementación real es v0.2.0 (H02 Day 1).

**Setup Steps:**

1. Setup PostgreSQL
docker-compose up -d postgres

2. Configure .env
cp .env.example .env

Edit DATABASE_URL=postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/thea_ia
3. Run migrations
alembic upgrade head

4. Verify
alembic current
psql -U postgres -d thea_ia -c "\dt"

text

**Migración aplicada (12 Nov 16:11):**
INFO [alembic.runtime.migration] Running upgrade -> e0a17d850507, Initial schema with tenant support

text

---

## Future Breaking Changes

### v1.0.0 (TBD)

Posibles breaking changes considerados:
- Rename columns (ej: telegram_id → external_id)
- Change types (ej: tags array → JSONB)
- Remove deprecated fields
- RLS enforcement (queries sin tenant_id fallan)

Se documentará migration guide completo cuando llegue.

---

## Rollback Procedure

Si migración falla:

Ver historial
alembic history

Rollback a versión anterior
alembic downgrade -1

O rollback a versión específica
alembic downgrade <revision_id>

Verificar estado
alembic current

text

**Backup antes de migration:**

Backup database
pg_dump -U postgres thea_ia > backup_$(date +%Y%m%d_%H%M%S).sql

Restore si necesario
psql -U postgres thea_ia < backup_20251112_161000.sql

text

---

## Performance Tracking

### Query Performance Targets:

| Version | Avg Query Time | 95th Percentile | Slow Query Threshold |
|---------|----------------|-----------------|---------------------|
| 0.2.0   | <100ms         | <500ms          | >1000ms             |
| 0.3.0 (H04) | <50ms      | <100ms          | >500ms              |
| 1.0.0 (H11) | <20ms      | <50ms           | >200ms              |

**Current Performance (12 Nov):**
- ✅ Índices aplicados: 20+ índices
- ✅ Foreign keys: 5 FKs con CASCADE
- ✅ Connection pooling: NullPool (desarrollo)
- ⏳ Benchmarks: Pendiente H02 Day 2

---

## Security Fixes

### v0.2.0 Security Features:
- ✅ SQLAlchemy parameterized queries (SQL injection protection)
- ✅ Multi-tenant isolation (tenant_id + FK)
- ✅ Connection pooling limits
- ✅ No secrets in code (all in .env)
- ✅ CASCADE deletes (integridad referencial)
- ⏳ RLS (H04)
- ⏳ Encryption at rest (H15)

---

## Contribuir a este CHANGELOG

Al hacer cambios en database/:
- ✅ Añadir entrada en sección [Unreleased]
- ✅ Usar categoría correcta (Added, Changed, Migration, etc)
- ✅ Si cambio schema: crear migración Alembic
- ✅ Documentar breaking changes
- ✅ Al release, mover [Unreleased] a versión nueva

**Migration Template:**

Crear migración
alembic revision --autogenerate -m "descriptive_name"

Editar archivo generado
- upgrade(): cambios schema
- downgrade(): rollback
Test migration
alembic upgrade head
pytest src/tests/unit/test_database/

Si OK, commit
git add .
git commit -m "database: add column X to table Y"

text

---

**Mantenido por:** Álvaro Fernández Mota  
**Última actualización:** 12 Nov 2025, 16:22 CET  
**Estado:** H02 Day 1 COMPLETADO ✅ | v0.2.0 | Database Layer 50% 🚀