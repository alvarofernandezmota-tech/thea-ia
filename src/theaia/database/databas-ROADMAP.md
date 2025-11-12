# Roadmap - src/database/

**Módulo:** Database  
**Versión actual:** 0.2.0 (H02 - Database Layer 50% ✅)  
**Próxima versión:** 0.3.0 (H02 - TelegramAdapter + Repos 100%)  

---

## 📊 Estado Actual (12 Nov 2025 - H02 Day 1)

### Completado ✅

**H02 Day 1 (12 Nov, 14:30-16:17, 1h 47min):**
- ✅ **7 Modelos SQLAlchemy** implementados con multi-tenant
  - base.py (BaseModel con tenant_id)
  - user.py (Usuario Telegram con relationships)
  - event.py (Eventos/recordatorios con recurrencia)
  - note.py (Notas con tags ARRAY)
  - conversation.py (Sesiones FSM con context JSONB)
  - message_history.py (Auditoría ML con intent/entities)
  - __init__.py (Exports completos)
- ✅ **Async Configuration** completa
  - session.py (AsyncSessionLocal, get_db, init_db, close_db)
  - connection.py (AsyncEngine, test_connection)
  - __init__.py database (Exports session + models + connection)
- ✅ **Alembic Migrations** funcionando
  - alembic.ini configurado (async, timezone UTC)
  - env.py con async environment
  - Primera migración e0a17d850507_initial_schema.py (285 líneas)
- ✅ **PostgreSQL Operativo**
  - 5 tablas creadas (users, events, notes, conversations, message_history)
  - 20+ índices aplicados
  - Foreign keys CASCADE configuradas
  - Schema antiguo eliminado
- ✅ **Multi-tenant Support**
  - tenant_id en todas las tablas
  - Índices en tenant_id
- ✅ **Troubleshooting Resuelto**
  - Fix conexión WinError 64 (localhost → 127.0.0.1)
  - Fix pg_hba.conf (trust mode)
  - Fix DATABASE_URL sin password

**Decisiones Técnicas (12 Nov):**
- Driver: `asyncpg` para PostgreSQL async
- Auth: Sin password (desarrollo trust mode)
- Metadata: Cambio `metadata` → `extra_data` (palabra reservada)
- JSONB: preferences, extra_data, context_data, entities_extracted
- Timestamps: timezone-aware (DateTime con timezone=True)
- Cascade: DELETE orphans automático
- Arquitectura: Basada en archive + adaptaciones S40

### Pendiente ⏳

**H02 Day 2 (13 Nov):**
- ⏳ TelegramAdapter con database integration
- ⏳ UserRepository CRUD completo
- ⏳ EventRepository + NoteRepository base
- ⏳ ConversationRepository + MessageHistoryRepository
- ⏳ Integration tests bot + database
- ⏳ Primera conversación funcional con persistencia
- ⏳ Documentación H02 completa

---

## 🎯 H02 (12-16 Nov 2025): Database Base + Adapter

**Objetivo:** Sistema funcional end-to-end (PostgreSQL + TelegramAdapter)

### ✅ Día 1 (12 Nov) - COMPLETADO 100%

**Infrastructure:**
- ✅ connection.py (AsyncEngine + sessions async)
- ✅ base.py (BaseModel + tenant_id + timestamps)
- ✅ session.py (AsyncSessionLocal, get_db)
- ✅ models/user.py (telegram_id, preferences, relationships)
- ✅ models/event.py (recordatorios, recurrencia, external_id)
- ✅ models/note.py (tags ARRAY, categories, priority)
- ✅ models/conversation.py (FSM state, context JSONB)
- ✅ models/message_history.py (auditoría ML)
- ✅ Alembic init + primera migración
- ✅ Migración aplicada exitosamente

**Tests:**
- ⏳ test_connection.py (próximo)
- ⏳ test_models.py (User, Event, Note, Conversation, MessageHistory)

**Criterio Done Día 1:** ✅ COMPLETADO
- ✅ PostgreSQL conecta
- ✅ 5 tablas creadas (users, events, notes, conversations, message_history)
- ✅ Índices aplicados
- ✅ Multi-tenant operativo

### ⏳ Día 2 (13 Nov) - PENDIENTE

**Repositories:**
- ⏳ repositories/base_repository.py
- ⏳ repositories/user_repository.py
- ⏳ repositories/event_repository.py (ex reminder)
- ⏳ repositories/note_repository.py
- ⏳ repositories/conversation_repository.py
- ⏳ repositories/message_history_repository.py

**TelegramAdapter:**
- ⏳ adapters/telegram_adapter.py con database integration
- ⏳ Handlers conectados con repositories
- ⏳ CRUD básico funcionando (crear user, eventos, notas)

**Tests:**
- ⏳ test_repositories.py (User, Event, Note CRUD)
- ⏳ test_integration_bot_database.py

**Criterio Done Día 2:**
- ✅ CRUD User funciona
- ✅ CRUD Event funciona
- ✅ CRUD Note funciona
- ✅ TelegramAdapter guarda en PostgreSQL
- ✅ tenant_id isolation verificado
- ✅ Tests repositories >80% coverage

### ⏳ Día 3 (14 Nov) - OBJETIVO FINAL

**Integration:**
- ⏳ Primera conversación completa (Telegram → DB → respuesta)
- ⏳ Conversation + MessageHistory guardados
- ⏳ Context recovery funciona
- ⏳ Multi-turn conversation persistente

**Tests:**
- ⏳ test_integration_complete.py
- ⏳ test_conversation_persistence.py

**Criterio Done Día 3:**
- ✅ Todas las tablas operativas
- ✅ Todos los repositories funcionan
- ✅ Primera conversación completa funcional
- ✅ Tests >85% coverage

---

## ✅ Criterios Done H02 (Target 16 Nov)

- ✅ 5 tablas PostgreSQL (users, events, notes, conversations, message_history) **COMPLETADO**
- ✅ Alembic migrations funcionan **COMPLETADO**
- ✅ AsyncIO en todo **COMPLETADO**
- ✅ Multi-tenant funciona (tenant_id) **COMPLETADO**
- ✅ Timestamps automáticos **COMPLETADO**
- ✅ JSONB metadata flexible **COMPLETADO**
- ✅ CASCADE relationships **COMPLETADO**
- ⏳ 5 repositories CRUD
- ⏳ TelegramAdapter integrado
- ⏳ Tests >85% coverage
- ⏳ Sin SQL injection vulnerabilities
- ⏳ Connection pooling configurado
- ⏳ Primera conversación funcional

**Progreso H02:** 50% ✅ (Database Layer completo, falta Adapter + Repos)

---

## 🏢 H04 (20-23 Nov 2025): Database Enterprise

**Objetivo:** Features enterprise production-ready

### Nuevas Features:

**1. Soft Delete:**
- SoftDeleteMixin en base.py
- deleted_at, is_deleted en todos los modelos
- Queries automáticamente filtran deleted

**2. Row Level Security:**
- security.py con RLS policies
- PostgreSQL policies por tabla
- Garantía a nivel database de tenant isolation

**3. Audit Logging:**
- AuditMixin (who, when, what)
- audit_logs table
- Track cambios automáticamente

**4. Advanced Pooling:**
- Read replicas support
- Connection retry logic
- Health checks

**5. Performance:**
- Query optimization
- Additional indexes
- EXPLAIN ANALYZE queries lentas

### Criterios Done H04:
- ✅ Soft delete en todo
- ✅ RLS policies activas
- ✅ Audit logging funciona
- ✅ Read replicas configuradas
- ✅ Connection retry works
- ✅ All queries <100ms (95 percentile)

---

## ☁️ H11 (Feb 2026): Database Kubernetes

**Objetivo:** High availability + auto-scaling

### Nuevas Features:

**1. High Availability:**
- Primary + 2 replicas
- Automatic failover
- Load balancing

**2. Backup Automation:**
- Daily backups
- Point-in-time recovery
- Backup retention 30 días

**3. Monitoring:**
- Prometheus metrics export
- Grafana dashboards
- Alerts (connection pool, slow queries)

**4. Scaling:**
- Horizontal read scaling
- Vertical write scaling
- Sharding preparado (H15+)

---

## 🔮 Futuro (Post-MVP)

### H15 (Abr 2026): Compliance
- GDPR data export/delete
- Encryption at rest
- Compliance logs

### H17+ (Jun 2026): Scale
- Sharding by tenant_id
- Multi-region
- Cache layer (Redis)

---

## 📈 Métricas de Éxito

| Hito | Tables | Repositories | Tests Coverage | Performance |
|------|--------|--------------|----------------|-------------|
| H02  | 5 ✅   | 5 ⏳         | >85% ⏳        | <500ms      |
| H04  | 5+     | 5+           | >90%           | <100ms      |
| H11  | 6+     | 6+           | >95%           | <50ms       |

---

## 🚧 Riesgos y Mitigaciones

### Riesgo 1: Data loss
**Mitigación:**
- Backups automáticos daily
- Point-in-time recovery
- Migrations testeadas en staging

### Riesgo 2: Performance degradation
**Mitigación:**
- Indexes en columnas frecuentes
- Connection pooling
- Query optimization continua
- Monitoring + alerts

### Riesgo 3: Migration failures
**Mitigación:**
- Dry-run migrations en staging
- Rollback plan siempre
- Blue-green deployments (H11)

---

## 📝 Decisiones Técnicas

### ¿Por qué PostgreSQL vs MySQL?
**Razón:** Features avanzadas (JSONB, array, GIN indexes, RLS, timezone-aware timestamps)

### ¿Por qué asyncpg vs psycopg2?
**Razón:** Performance (3-5x más rápido), native async, mejor para high-throughput

### ¿Por qué Repository Pattern?
**Razón:** Testeable, reutilizable, maintainable, separa lógica negocio de persistencia

### ¿Por qué Alembic vs Django ORM?
**Razón:** SQLAlchemy-native, más control, mejor para non-Django projects, async support

### ¿Por qué Multi-tenant (tenant_id)?
**Razón:** Escalabilidad futura (B2B), aislamiento datos, compliance, una BD compartida eficiente

### ¿Por qué Sin Password en desarrollo?
**Razón:** Simplifica setup local, trust mode en pg_hba.conf, producción usará credentials seguras

---

**Última actualización:** 12 Nov 2025, 16:22 CET  
**Próxima revisión:** H02 complete (16 Nov 2025)  
**Responsable:** Álvaro Fernández Mota

**Estado:** H02 Day 1 COMPLETADO ✅ | Database Layer 50% | TelegramAdapter próximo 🚀
