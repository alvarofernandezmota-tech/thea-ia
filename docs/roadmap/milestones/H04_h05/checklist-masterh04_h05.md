✅ CHECKLIST DETALLADO H04-H05 — OPERACIONAL + DATABASE INTEGRADA
Proyecto: THEA IA — Asistente Multi-Agente MVP
Versión: v4.0 — CHECKLIST DETALLADO + DATABASE COMPLETO
Período: 26 NOV – 5 DIC 2025
Responsable: Álvaro Fernández Mota
Status: 🟢 LISTO PARA EJECUTAR AHORA

🎯 OBJETIVO H04-H05
text
INPUT (post-H03):
├─ CoreRouter orquestador con FSM v2
├─ ML Pipeline (Intent Detector 89%, Entity Extractor)
└─ Database multi-tenant (PostgreSQL, 5 modelos base, 65+ tests)

OUTPUT (post-H05):
├─ 5 agentes CORE 100% operativos (handlers + FSM reales + repos)
├─ Database avanzada (9 modelos, 4 repos nuevos, indices optimizados)
├─ EventAgent proactivo (scheduler cada 60s)
├─ Tests exhaustivos (50+, ≥80% coverage)
└─ MVP READY para H06 (ML pipelines) + H07 (QA)
📋 FASE 1 — AUDITORÍA INICIAL (2h - LUN 26 NOV TARDE)
BLOQUE 1.1: Análisis Estado Agentes
✅ TAREA 1.1.1 — Revisar AgendaAgent
text
□ Leer handler.py (268 LOC)
  └─ Ubicación: src/theaia/agents/agenda_agent/handler.py
  └─ Qué buscar: estructura __init__, handle(), métodos create/update/delete
  └─ Registrar: ¿tiene integración ML? ¿qué repos usa?

□ Revisar FSM (¿hereda BaseStateMachine?)
  └─ Ubicación: src/theaia/agents/agenda_agent/fsm.py
  └─ Qué buscar: clase principal, estados definidos, transiciones
  └─ Registrar: ¿heredanza correcta? ¿callbacks on_enter/on_exit?

□ Validar EventRepository connection
  └─ ¿Llama EventRepository? ¿qué métodos?
  └─ ¿Multi-tenant validation? (tenant_id field)

□ Revisar tests existentes
  └─ Ubicación: tests/agents/agenda_agent/test_*.py
  └─ ¿Cuántos tests? ¿Coverage? ¿PASSING?

□ Documentar estado en matriz
  └─ RESULTADO: Fila en tabla estado (ver abajo)
  └─ MICRO-RECOMPENSA: +1 punto
MATRIZ ESTADO AGENTES (ir completando):

text
| Agente | Handler LOC | FSM LOC | BaseStateMachine? | Repo | ML | Tests | Action |
|--------|-------------|---------|-------------------|------|----|----|--------|
| AgendaAgent | 268 | ? | ? | YES | ? | ? | REFACTOR |
| NoteAgent | 15 | ? | ? | NO | NO | NO | CREATE NEW |
| ReminderAgent | 15 | 58 | ? | NO | NO | NO | MERGE→Event |
| QueryAgent | 15 | 68 | ? | NO | NO | NO | REFACTOR |
| ScheduleAgent | 15 | ? | ? | NO | NO | NO | DELETE |
| HelpAgent | 16 | 90 | ? | NO | NO | NO | MERGE→Help |
| EventAgent | 16 | 70 | ? | NO | NO | NO | REUSE+ENHANCE |
| FallbackAgent | 16 | 36 | ? | NO | NO | NO | MERGE→Help |
| MilestoneAgent | 16 | ? | NO | NO | NO | NO | DEFER→H08 |
✅ TAREA 1.1.2 — Revisar NoteAgent
text
□ Leer handler.py (15 LOC stub)
  └─ Verificar: ¿es stub real? ¿tiene lógica?
  └─ Registrar en matriz

□ Revisar FSM (¿real o placeholder?)
  └─ Estados definidos? ¿transiciones?
  └─ Registrar en matriz

□ ¿Existe NoteRepository? (NO)
  └─ Verificar: src/theaia/database/repositories/note_repository.py
  └─ ACCIÓN: Crear en FASE 2

□ ¿Integración ML? (NO)
  └─ Registrar en matriz

□ Documentar: REFACTOR FROM SCRATCH
  └─ Registrar decisión
  └─ MICRO-RECOMPENSA: +1 punto
✅ TAREA 1.1.3 — Revisar ReminderAgent
text
□ Leer handler (15 LOC stub)
  □ Revisar FSM (58 LOC, ¿real?)
  □ ¿Existe ReminderRepository? (NO)
  □ Documentar: MERGE → EventAgent
  □ MICRO-RECOMPENSA: +1 punto
✅ TAREA 1.1.4 — Revisar QueryAgent
text
□ Leer handler (15 LOC stub)
  □ Revisar FSM (68 LOC incomplete)
  □ Cross-domain search capability? (NO)
  □ Cache strategy? (NO)
  □ Documentar: REFACTOR + NEW REPOS
  □ MICRO-RECOMPENSA: +1 punto
✅ TAREA 1.1.5 — Revisar HelpAgent + FallbackAgent
text
□ HelpAgent: 16 LOC handler, 90 LOC FSM
□ FallbackAgent: 16 LOC handler, 36 LOC FSM
□ Documentar: MERGE → Unified Help
□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 1.1.6 — Revisar EventAgent
text
□ 16 LOC handler, 70 LOC FSM
□ Scheduler capability? (NO)
□ TelegramAdapter integration? (NO)
□ Documentar: REUSE + ENHANCE (proactive scheduler)
□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 1.1.7-1.1.8 — Revisar ScheduleAgent + MilestoneAgent
text
□ ScheduleAgent: DELETE (funcionalidad en Agenda+Event)
□ MilestoneAgent: DEFER → H08 (no MVP)
□ MICRO-RECOMPENSA: +2 puntos
BLOQUE 1.1 TOTAL MICRO-RECOMPENSA: ✅ +8 puntos
CRITERIO DONE: Matriz completada, hallazgos documentados
RESULTADO: AUDITORIA_AGENTES_26NOV.md

BLOQUE 1.2: Decisiones Arquitectónicas
✅ TAREA 1.2.1 — Definir plan refactorización
text
□ Crear documento: DECISIONES_H04H05.md

□ Registrar para cada agente:
  ├─ AgendaAgent: REFACTOR (validar FSM herencia, ML integration)
  ├─ NoteAgent: CREATE NEW (handler + FSM + repo from scratch)
  ├─ ReminderAgent: MERGE → EventAgent
  ├─ QueryAgent: REFACTOR (cross-domain, cache)
  ├─ HelpAgent+FallbackAgent: MERGE → Unified Help
  ├─ EventAgent: REUSE + ENHANCE (scheduler proactivo)
  ├─ ScheduleAgent: DELETE
  └─ MilestoneAgent: DEFER

□ MICRO-RECOMPENSA: +3 puntos
✅ TAREA 1.2.2 — Definir nuevos repositorios
text
□ Registrar 4 nuevos repos:
  ├─ NoteRepository (search_by_tags, full_text_search, get_recent, get_by_date_range)
  ├─ ReminderRepository (get_pending, mark_sent, create_batch, cleanup_old)
  ├─ QueryCacheRepository (cache management con TTL)
  └─ UserPreferencesRepository (quiet_hours, reminder_advance, language, timezone)

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 1.2.3 — Definir contratos agentes
text
□ Registrar contrato (input/output) para cada agente:
  ├─ AgendaAgent: create_event, update_event, list_events, delete_event
  ├─ NoteAgent: create_note, list_notes, search_notes, delete_note
  ├─ QueryAgent: search_cross_domain, get_daily_summary, get_weekly_summary
  ├─ HelpAgent: show_help, show_commands, error_recovery, delegate_to_agent
  └─ EventAgent: run_scheduler (proactive, respeta quiet hours)

□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 1.2.4 — Validar CoreRouter routes
text
□ Revisar routing table actual:
  ├─ Intent mappings (schedule/event → Agenda, save note → Notes, etc.)
  ├─ Fallback route (unknown → Help agent)
  └─ Cross-agent delegation (Query → Agenda/Notes if needed)

□ Registrar cambios necesarios

□ MICRO-RECOMPENSA: +1 punto
BLOQUE 1.2 TOTAL MICRO-RECOMPENSA: ✅ +7 puntos
CRITERIO DONE: Todas decisiones documentadas y consensuadas
RESULTADO: DECISIONES_H04H05.md (firmado)

FASE 1 TOTAL: 8 + 7 = ✅ 15 PUNTOS
ESTADO: ⏳ AUDITORÍA COMPLETADA
PRÓXIMO: FASE 2 (Repositorios + Database)

📚 FASE 2 — REPOSITORIOS AVANZADOS + DATABASE (8h - MAR 27-28 NOV)
BLOQUE 2.1: Database Setup + Modelo Reminder
✅ TAREA 2.1.1 — Crear modelo Reminder
text
□ Archivo: src/theaia/database/models/reminder.py

□ Definir modelo SQLAlchemy:
  ├─ class Reminder(Base):
  ├─ Fields:
  │  ├─ id (PK, UUID)
  │  ├─ user_id (FK User, not null)
  │  ├─ event_id (FK Event, nullable)
  │  ├─ trigger_time (TIMESTAMPTZ, not null)
  │  ├─ sent (BOOLEAN, default False)
  │  ├─ created_at (TIMESTAMPTZ, default now())
  │  ├─ updated_at (TIMESTAMPTZ)
  │  └─ tenant_id (para multi-tenant)
  └─ Constraints:
     └─ FK: user_id → User(id)
     └─ FK: event_id → Event(id) ON DELETE SET NULL
     └─ Índices: user_id, trigger_time, sent, tenant_id

□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 2.1.2 — Crear migración Alembic
text
□ Generar migración:
  └─ alembic revision --autogenerate -m "add reminder model"

□ Editar archivo de migración:
  └─ Validar SQL (DDL) correcto
  └─ Añadir índices manualmente si es necesario

□ Ejecutar migración:
  └─ alembic upgrade head

□ Verificar tabla en BD:
  └─ \dt reminders (en psql)
  └─ Columnas correctas
  └─ Índices creados

□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 2.1.3 — Crear modelo QueryCache
text
□ Archivo: src/theaia/database/models/query_cache.py

□ Definir modelo:
  ├─ class QueryCache(Base):
  ├─ Fields:
  │  ├─ id (PK)
  │  ├─ user_id (FK User)
  │  ├─ query_hash (VARCHAR 64, index)
  │  ├─ result (JSONB)
  │  ├─ ttl (INTEGER, segundos)
  │  ├─ created_at (TIMESTAMPTZ)
  │  ├─ expires_at (TIMESTAMPTZ, calculated from ttl + created_at)
  │  └─ tenant_id
  └─ Índices: user_id+query_hash, expires_at

□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 2.1.4 — Crear modelo UserPreferences
text
□ Archivo: src/theaia/database/models/user_preferences.py

□ Definir modelo:
  ├─ class UserPreferences(Base):
  ├─ Fields:
  │  ├─ user_id (FK User, PK)
  │  ├─ quiet_hours_start (TIME, default 23:00)
  │  ├─ quiet_hours_end (TIME, default 07:00)
  │  ├─ reminder_advance_min (INTEGER, default 15)
  │  ├─ language (VARCHAR 10, default 'es')
  │  ├─ timezone (VARCHAR 50, default 'UTC')
  │  ├─ created_at (TIMESTAMPTZ)
  │  ├─ updated_at (TIMESTAMPTZ)
  │  └─ tenant_id
  └─ Constraint: user_id unique

□ MICRO-RECOMPENSA: +1 punto
✅ TAREA 2.1.5 — Migración para QueryCache + UserPreferences
text
□ alembic revision --autogenerate -m "add query_cache and user_preferences models"
□ Validar SQL
□ Ejecutar: alembic upgrade head
□ Verificar tablas en BD

□ MICRO-RECOMPENSA: +1 punto
BLOQUE 2.1 TOTAL MICRO-RECOMPENSA: ✅ +5 puntos
CRITERIO DONE: 3 modelos + migraciones creados, tablas en BD
ESTADO: Database schema actualizado

BLOQUE 2.2: NoteRepository
✅ TAREA 2.2.1 — Crear NoteRepository clase
text
□ Archivo: src/theaia/database/repositories/note_repository.py

□ Estructura:
  ├─ from database.repositories.base_repository import BaseRepository
  ├─ from database.models.note import Note
  ├─ class NoteRepository(BaseRepository[Note]):
  │
  │  Métodos custom:
  │  ├─ async def search_by_tags(user_id, tags: List[str]) → List[Note]
  │  │   └─ Query: WHERE user_id=? AND tag = ANY(tags)
  │  │   └─ Multi-tenant validation
  │  │
  │  ├─ async def full_text_search(user_id, query: str) → List[Note]
  │  │   └─ Query: WHERE user_id=? AND content @@ to_tsquery(query)
  │  │   └─ TSVECTOR índex en content
  │  │
  │  ├─ async def get_recent(user_id, limit=10) → List[Note]
  │  │   └─ ORDER BY created_at DESC LIMIT limit
  │  │
  │  └─ async def get_by_date_range(user_id, start, end) → List[Note]
  │      └─ WHERE created_at BETWEEN start AND end

□ Validations en todos:
  └─ tenant_id check (multi-tenant)
  └─ user_id check (authorization)

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 2.2.2 — Tests NoteRepository
text
□ Archivo: tests/database/test_note_repository.py

□ Test 1: create_note (básico)
  └─ assert nota guardada en BD

□ Test 2: search_by_tags (1 tag)
  └─ Create nota con tags=['urgent'], search por 'urgent'
  └─ assert encontrada

□ Test 3: search_by_tags (multiple tags, no match)
  └─ Create nota con tags=['urgent'], search por 'low_priority'
  └─ assert lista vacía

□ Test 4: full_text_search (match)
  └─ Create nota con content="Python es genial"
  └─ Search "Python", assert encontrada

□ Test 5: full_text_search (no match)
  └─ Search "Rust", assert vacío

□ Test 6: get_recent (ordering)
  └─ Create 5 notas
  └─ get_recent(limit=3)
  └─ assert orden DESC por created_at

□ Test 7: get_by_date_range (inclusive)
  └─ Create notas on varios días
  └─ get_by_date_range(start, end)
  └─ assert solo notas en rango

□ Test 8: Multi-tenant isolation
  └─ Create notas con different tenant_id
  └─ assert no leak entre tenants

□ Test 9: Performance (<100ms)
  └─ Medir tiempo query
  └─ assert query_time < 100ms

□ Test 10: Edge case (null tags)
  └─ search_by_tags(tags=None)
  └─ assert sin error

□ Run: pytest tests/database/test_note_repository.py -v --cov
□ Target coverage: ≥85%

□ MICRO-RECOMPENSA: +1 punto (all 10 PASSING)
BLOQUE 2.2 TOTAL MICRO-RECOMPENSA: ✅ +3 puntos
CRITERIO DONE: Todos 10 tests PASSING, coverage ≥85%

BLOQUE 2.3: ReminderRepository
✅ TAREA 2.3.1 — Crear ReminderRepository clase
text
□ Archivo: src/theaia/database/repositories/reminder_repository.py

□ Métodos custom:
  ├─ async def get_pending(user_id, before_time) → List[Reminder]
  │   └─ WHERE sent=False AND trigger_time <= before_time
  │   └─ ORDER BY trigger_time ASC
  │
  ├─ async def mark_sent(reminder_id, sent_time) → None
  │   └─ UPDATE reminders SET sent=True, updated_at=sent_time WHERE id=reminder_id
  │
  ├─ async def create_batch(reminders: List[dict]) → List[Reminder]
  │   └─ INSERT multiple reminders
  │   └─ RETURN list of created
  │
  └─ async def cleanup_old(older_than: datetime) → int
      └─ DELETE FROM reminders WHERE created_at < older_than AND sent=True
      └─ RETURN count deleted

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 2.3.2 — Tests ReminderRepository
text
□ Test 1: create_reminder
□ Test 2: get_pending (found)
□ Test 3: get_pending (empty)
□ Test 4: mark_sent (BD updated)
□ Test 5: create_batch
□ Test 6: cleanup_old
□ Test 7: Multi-tenant
□ Test 8: Performance (<100ms)
□ Coverage: ≥85%

□ Run: pytest tests/database/test_reminder_repository.py -v --cov
□ MICRO-RECOMPENSA: +1 punto (all 8 PASSING)
BLOQUE 2.3 TOTAL MICRO-RECOMPENSA: ✅ +3 puntos

BLOQUE 2.4: QueryCacheRepository
✅ TAREA 2.4.1 — Crear QueryCacheRepository clase
text
□ Archivo: src/theaia/database/repositories/query_cache_repository.py

□ Métodos:
  ├─ async def get_cached(user_id, query_hash) → Optional[QueryCache]
  │   └─ SELECT * WHERE user_id=? AND query_hash=? AND expires_at > now()
  │   └─ If expired: return None (no delete yet)
  │
  ├─ async def set_cache(user_id, query, result, ttl) → QueryCache
  │   └─ query_hash = sha256(query).hexdigest()
  │   └─ expires_at = now() + ttl seconds
  │   └─ INSERT OR REPLACE
  │
  └─ async def cleanup_expired() → int
      └─ DELETE FROM query_cache WHERE expires_at <= now()
      └─ RETURN count deleted

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 2.4.2 — Tests QueryCacheRepository
text
□ Test 1: set_cache
□ Test 2: get_cached (hit, not expired)
□ Test 3: get_cached (expired, return None)
□ Test 4: cleanup_expired
□ Test 5: Multi-tenant
□ Test 6: TTL calculation
□ Coverage: ≥85%

□ MICRO-RECOMPENSA: +1 punto (all 6 PASSING)
BLOQUE 2.4 TOTAL MICRO-RECOMPENSA: ✅ +3 puntos

BLOQUE 2.5: UserPreferencesRepository
✅ TAREA 2.5.1 — Crear UserPreferencesRepository clase
text
□ Archivo: src/theaia/database/repositories/user_preferences_repository.py

□ Métodos:
  ├─ async def get_or_create_default(user_id) → UserPreferences
  │   └─ Si exists: SELECT * WHERE user_id=?
  │   └─ Si not exists: INSERT defaults
  │
  ├─ async def update_quiet_hours(user_id, start: TIME, end: TIME) → None
  │   └─ UPDATE quiet_hours_start=start, quiet_hours_end=end WHERE user_id=?
  │
  ├─ async def is_quiet_time(user_id, current_time) → bool
  │   └─ SELECT quiet_hours_start, quiet_hours_end WHERE user_id=?
  │   └─ Lógica: if start < end: (current < start or current > end)
  │           else: (current < start and current > end)  # wraps midnight
  │
  └─ async def get_reminder_advance_min(user_id) → int
      └─ SELECT reminder_advance_min WHERE user_id=?

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 2.5.2 — Tests UserPreferencesRepository
text
□ Test 1: get_or_create_default (new user)
□ Test 2: get_or_create_default (existing)
□ Test 3: update_quiet_hours
□ Test 4: is_quiet_time (inside: 14:00 between 23:00-07:00) → False
□ Test 5: is_quiet_time (outside: 02:00 between 23:00-07:00) → True
□ Test 6: Timezone handling
□ Test 7: Language preference
□ Test 8: Multi-tenant
□ Test 9: Edge case (22:59 vs 23:00)
□ Test 10: get_reminder_advance_min
□ Coverage: ≥85%

□ MICRO-RECOMPENSA: +1 punto (all 10 PASSING)
BLOQUE 2.5 TOTAL MICRO-RECOMPENSA: ✅ +3 puntos

FASE 2 TOTAL: 5 + 3 + 3 + 3 + 3 = ✅ 17 PUNTOS
CRITERIO DONE: 4 repos + 3 modelos + 34 tests (all PASSING), coverage ≥85%
ESTADO: Database avanzada operativa

🤖 FASE 3 — AGENTES CORE (20h - MAR 27 – JUE 29 NOV)
BLOQUE 3.1: AgendaAgent (REFACTOR)
✅ TAREA 3.1.1 — Refactor handler.py
text
□ Archivo: src/theaia/agents/agenda_agent/handler.py

□ Revisar estructura actual:
  └─ ¿Tiene class AgendaAgentHandler o AgendaAgent?
  └─ ¿Tiene method handle()?

□ Mejorar:
  ├─ Integrar Intent Detector ML
  │   └─ detect_intent(message) → intent_name
  │   └─ Intents: "create_event", "update_event", "list_events", "delete_event"
  │
  ├─ Integrar Entity Extractor ML
  │   └─ extract_entities(message) → {dates, times, people, title}
  │
  ├─ Context passing a FSM
  │   └─ context = {intent, entities, user_input, ...}
  │
  ├─ Métodos handlers:
  │   ├─ async def create_event_handler(context) → response
  │   ├─ async def update_event_handler(context) → response
  │   ├─ async def list_events_handler(context) → response
  │   └─ async def delete_event_handler(context) → response
  │
  └─ EventRepository calls:
      └─ event_repo.create_event(user_id, data)
      └─ event_repo.update_event(event_id, data)
      └─ event_repo.get_events(user_id)
      └─ event_repo.delete_event(event_id)

□ Validations:
  └─ date_in_future(date) → bool
  └─ valid_time_format(time) → bool
  └─ tenant_id present → True or raise

□ Logging:
  └─ logger.info(f"Creating event for user {user_id}")
  └─ logger.error(f"Error creating event: {error}")

□ Target LOC: 250-300
□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 3.1.2 — Refactor FSM.py
text
□ Archivo: src/theaia/agents/agenda_agent/fsm.py

□ Verificar herencia:
  └─ from agents.base_state_machine import BaseStateMachine
  └─ class AgendaFSM(BaseStateMachine):

□ Estados:
  ├─ IDLE (inicial)
  ├─ ASKING_TITLE
  ├─ ASKING_DATE
  ├─ ASKING_TIME
  ├─ ASKING_PARTICIPANTS
  ├─ CONFIRMED
  └─ ERROR

□ Transiciones:
  ├─ IDLE → ASKING_TITLE (on_enter: "Dime el título del evento")
  ├─ ASKING_TITLE → ASKING_DATE (on_enter: "¿Qué día?")
  ├─ ASKING_DATE → ASKING_TIME (on_enter: "¿A qué hora?")
  ├─ ASKING_TIME → CONFIRMED (on_enter: "Evento creado!")
  └─ Any → ERROR (on error)

□ Callbacks:
  ├─ on_enter_ASKING_TITLE(): generate prompt
  ├─ on_exit_ASKING_TITLE(): validate input
  └─ on_enter_CONFIRMED(): save to DB

□ Draft storage:
  └─ context['event_draft'] = {title, date, time, participants}

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 3.1.3 — Connect EventRepository + Tests
text
□ Handler llama repo:
  └─ event_repo.create_event(user_id=?, data=?, tenant_id=?)
  └─ Result: Event object o error

□ Multi-tenant validation:
  └─ assert tenant_id present
  └─ repo checks tenant_id ownership

□ Performance:
  └─ assert <100ms create_event

□ Tests (8 tests):
  ├─ Test 1: FSM transition IDLE → ASKING_TITLE
  ├─ Test 2: FSM transition ASKING_TITLE → ASKING_DATE
  ├─ Test 3: FSM full chain (IDLE → CONFIRMED)
  ├─ Test 4: Intent detection ML (detect "crear evento")
  ├─ Test 5: Entity extraction (extract date "mañana" → tomorrow)
  ├─ Test 6: create_event E2E (message → handler → DB)
  ├─ Test 7: Error handling (invalid date "hace 5 días")
  ├─ Test 8: Multi-tenant isolation
  └─ Coverage: ≥85%

□ Run: pytest tests/agents/agenda_agent/test_*.py -v --cov
□ MICRO-RECOMPENSA: +2 puntos (all 8 PASSING)
BLOQUE 3.1 TOTAL MICRO-RECOMPENSA: ✅ +6 puntos
CRITERIO DONE: Handler refactorizado, FSM real, 8 tests PASSING
ESTADO: AgendaAgent operativo

BLOQUE 3.2: NoteAgent (CREATE NEW)
✅ TAREA 3.2.1 — Create handler.py from scratch
text
□ Archivo: src/theaia/agents/note_agent/handler.py (NEW)

□ Estructura:
  ├─ class NoteAgentHandler:
  ├─ __init__(note_repo, intent_detector, entity_extractor)
  ├─ async def handle(user_id, message, context) → response
  │
  ├─ Intents: "create_note", "list_notes", "search_notes", "delete_note"
  │
  ├─ Methods:
  │   ├─ async def create_note_handler(context) → response
  │   │   └─ note_repo.create_note(user_id, text, tags)
  │   │
  │   ├─ async def list_notes_handler(context) → response
  │   │   └─ note_repo.get_recent(user_id, limit=10)
  │   │
  │   ├─ async def search_handler(context) → response
  │   │   └─ entities = extract_entities(message) → {keywords, tags}
  │   │   └─ if tags: note_repo.search_by_tags(user_id, tags)
  │   │   └─ else: note_repo.full_text_search(user_id, query)
  │   │
  │   └─ async def delete_handler(context) → response
  │       └─ note_repo.delete_note(note_id)
  │
  └─ Target LOC: 200-250

□ ML Integration:
  └─ detect_intent(message) → intent
  └─ extract_entities(message) → {keywords, tags}

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 3.2.2 — Create FSM.py from scratch
text
□ Archivo: src/theaia/agents/note_agent/fsm.py (NEW)

□ Heredar BaseStateMachine

□ Estados:
  ├─ IDLE
  ├─ ASKING_TEXT
  ├─ ASKING_TAGS
  ├─ CONFIRMING
  ├─ COMPLETED
  └─ ERROR

□ Draft storage:
  └─ context['note_draft'] = {text, tags}

□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 3.2.3 — Tests NoteAgent
text
□ 8 tests:
  ├─ Test 1: FSM transitions
  ├─ Test 2: Intent detection (create vs search)
  ├─ Test 3: Entity extraction (tags)
  ├─ Test 4: create_note E2E
  ├─ Test 5: list_notes (pagination)
  ├─ Test 6: search_notes (full-text)
  ├─ Test 7: delete_note
  ├─ Test 8: Error (empty text)
  └─ Coverage: ≥85%

□ MICRO-RECOMPENSA: +2 puntos (all 8 PASSING)
BLOQUE 3.2 TOTAL MICRO-RECOMPENSA: ✅ +6 puntos

BLOQUE 3.3: EventAgent (MERGE ReminderAgent + ENHANCE)
✅ TAREA 3.3.1-3.3.2 — Create EventAgent service
text
□ Archivo: src/theaia/agents/event_agent/service.py (NEW)

□ Clase:
  ├─ class EventAgent:
  ├─ __init__(reminder_repo, telegram_adapter, user_prefs_repo)
  │
  ├─ async def run_scheduler() → while True loop
  │   ├─ while True:
  │   │   ├─ await asyncio.sleep(60)  # 60 segundos
  │   │   ├─ await self._check_and_send_reminders()
  │   │   └─ except and log errors
  │   │
  │   └─ Este método corre en background (on_startup de main.py)
  │
  ├─ async def _fetch_pending_reminders(user_id, before_time) → List[Reminder]
  │   └─ reminder_repo.get_pending(user_id, before_time)
  │
  ├─ async def _send_reminder(reminder, user_id) → bool
  │   ├─ Check quiet hours: is_quiet_time(user_id)?
  │   ├─ If quiet: skip, return False
  │   ├─ Else: telegram_adapter.send_message(user_id, "🔔 {evento} en 15 min")
  │   └─ Return True if sent
  │
  ├─ async def _mark_sent(reminder_id, sent_time) → None
  │   └─ reminder_repo.mark_sent(reminder_id, sent_time)
  │
  └─ async def _is_quiet_time(user_id) → bool
      └─ user_prefs = await user_prefs_repo.get_or_create_default(user_id)
      └─ return user_prefs_repo.is_quiet_time(user_id, now())

□ Target LOC: 250-300
□ MICRO-RECOMPENSA: +2 puntos
✅ TAREA 3.3.3 — Tests EventAgent
text
□ 7 tests:
  ├─ Test 1: run_scheduler loop logic (mock sleep)
  ├─ Test 2: _fetch_pending_reminders (found)
  ├─ Test 3: _fetch_pending_reminders (empty)
  ├─ Test 4: _send_reminder (mock Telegram, verify message)
  ├─ Test 5: _mark_sent (BD updated)
  ├─ Test 6: _is_quiet_time (at 2am) → True
  ├─ Test 7: _is_quiet_time (at 2pm) → False
  └─ Coverage: ≥85%

□ MICRO-RECOMPENSA: +2 puntos (all 7 PASSING)
BLOQUE 3.3 TOTAL MICRO-RECOMPENSA: ✅ +6 puntos

BLOQUE 3.4: QueryAgent (REFACTOR)
✅ TAREA 3.4.1-3.4.2 — Refactor + Tests
text
□ Handler:
  ├─ Intents: search_notes, search_events, summary_today, summary_week
  ├─ Cross-domain search logic
  ├─ Cache strategy (QueryCacheRepository)
  └─ Target LOC: 250-300

□ FSM:
  ├─ States: IDLE, ASKING_QUERY, EXECUTING, RETURNING_RESULTS, ERROR
  ├─ Cache hit logic
  └─ Pagination

□ 8 tests:
  ├─ Test 1: Search notes (full-text)
  ├─ Test 2: Search events (date range)
  ├─ Test 3: Cache hit
  ├─ Test 4: Cache miss
  ├─ Test 5: Cross-domain merge
  ├─ Test 6: Summary today
  ├─ Test 7: Summary week
  ├─ Test 8: Error (no results)
  └─ Coverage: ≥85%

□ MICRO-RECOMPENSA: +4 puntos (refactor + tests)
BLOQUE 3.4 TOTAL MICRO-RECOMPENSA: ✅ +4 puntos

BLOQUE 3.5: HelpAgent (MERGE + UNIFIED)
✅ TAREA 3.5.1-3.5.2 — Create unified Help + Tests
text
□ Handler:
  ├─ Merge HelpAgent + FallbackAgent
  ├─ Purpose: Help + Fallback unified
  ├─ Intents: help, commands, unknown_command
  └─ Target LOC: 200-250

□ FSM:
  ├─ States: IDLE, SHOWING_HELP, AWAITING_COMMAND, REDIRECTING, ERROR
  └─ Fallback transitions

□ 9 tests:
  ├─ Test 1: Show help menu
  ├─ Test 2: Show commands
  ├─ Test 3: Fallback scenario
  ├─ Test 4: Error recovery
  ├─ Test 5: Command delegation
  ├─ Test 6: Context preservation
  ├─ Test 7: Language preference
  ├─ Test 8: Edge case
  ├─ Test 9: Multi-tenant
  └─ Coverage: ≥85%

□ MICRO-RECOMPENSA: +4 puntos (create + tests)
BLOQUE 3.5 TOTAL MICRO-RECOMPENSA: ✅ +4 puntos

FASE 3 TOTAL: 6 + 6 + 6 + 4 + 4 = ✅ 26 PUNTOS

🔗 FASE 4 — INTEGRACIÓN (8h - VIE 30 NOV)
BLOQUE 4.1: CoreRouter + Validación
text
□ Actualizar routing table
□ Tests CoreRouter (6 tests, ≥80% coverage)
□ MICRO-RECOMPENSA: +3 puntos
BLOQUE 4.2: EventAgent on_startup
text
□ Actualizar main.py (on_startup, on_shutdown)
□ E2E test scheduler
□ MICRO-RECOMPENSA: +2 puntos
BLOQUE 4.3: Full-stack Validation
text
□ Checklist validación (12 items)
□ MICRO-RECOMPENSA: +2 puntos
FASE 4 TOTAL: ✅ +7 PUNTOS

📚 FASE 5 — DOCUMENTACIÓN & CIERRE (6h - VIE 30 NOV)
text
□ Documentación por agente (READMEs)
□ ARCHITECTURE.md global
□ Coverage report + CHANGELOG
□ Clean commits (11 commits)
□ Git push + tags
□ HITO_H04H05_CIERRE.md

FASE 5 TOTAL: ✅ +6 PUNTOS
🎯 RESUMEN MICRO-RECOMPENSAS H04-H05
text
Fase 1: Auditoría                    = 15 puntos
Fase 2: Repos + Database             = 17 puntos
Fase 3: 5 Agentes CORE               = 26 puntos
Fase 4: Integración                  = 7 puntos
Fase 5: Documentación & Cierre        = 6 puntos
─────────────────────────────────────
TOTAL H04-H05:                        ✅ 71 PUNTOS 🎯
✅ ESTADO MVP FINAL (post-H05)
text
✅ 5 AGENTES CORE OPERATIVOS:
  ✓ AgendaAgent (refactorizado)
  ✓ NoteAgent (nuevo)
  ✓ QueryAgent (refactorizado)
  ✓ HelpAgent (unified merged)
  ✓ EventAgent (proactive scheduler)

✅ DATABASE AVANZADA:
  ✓ 9 modelos (5 base + 3 nuevos: Reminder, QueryCache, UserPreferences)
  ✓ 4 repositorios nuevos (Note, Reminder, QueryCache, UserPreferences)
  ✓ 34 tests database (all PASSING, ≥85% coverage)
  ✓ Índices optimizados
  ✓ Multi-tenant aislada

✅ CALIDAD:
  ✓ 50+ tests NEW (TODOS PASSING)
  ✓ Coverage ≥80% por módulo
  ✓ Performance <100ms
  ✓ Error handling graceful

✅ INTEGRACIÓN COMPLETA:
  ✓ CoreRouter + 5 agentes orquestados
  ✓ EventAgent scheduler en background (on_startup)
  ✓ Database ↔ Agentes ↔ Telegram
  ✓ E2E full-cycle operativo

🚀 READY FOR H06 + H07
Versión: v4.0 — CHECKLIST DETALLADO + DATABASE INTEGRADA
Fecha: 26 Noviembre 2025
Status: 🟢 LISTO PARA EJECUTAR AHORA