✅ CHECKLIST EJECUTABLE H03 + H04 + H05 (ACTUALIZADO v3.4)
Proyecto: THEA IA — Asistente Multi-Agente MVP
Versión: v3.4 EJECUTABLE (Actualizado 04 Dic 2025, 23:13 CET)
Formato: Checklist secuencial para seguir paso a paso
Status: 🟢 EN PROGRESO - H04 PHASE 2 COMPLETADO ✅

🎯 CÓMO USAR ESTE CHECKLIST
text
☑ Marca cuando esté en progreso/completo
✅ Marca HITO completo cuando termines todas sus tareas
Ejemplo:

☑ Tarea 1.1.2 ← En progreso/completo

✅ HITO 1 COMPLETO ← Hito entero terminado

📊 PROGRESO GENERAL
Fase	Hitos	Estado	Progreso	Última Actualización
H03	1-6	⏳ En Progreso	15%	-
H04	7-9	🔄 En Progreso	75%	04 Dic 2025, 23:10 CET
H05	10-12	⏸️ Pendiente	0%	-
Última actualización: 04 Diciembre 2025, 23:13 CET - H04 PHASE 2 EXTENDED ✅

🆕 NUEVO: H04 PHASE 2 EXTENDED - AgendaAgent Tests E2E + CRUD
✅ COMPLETADO (04 Dic 2025, 16:00-23:10 CET)
Problemas Resueltos:

✅ Event loop issues (Windows + asyncpg)

✅ Foreign key violations (fixture automático scope='session')

✅ BaseRepository.create() TypeError

✅ Validation errors (event status enum)

✅ EventTools datetime compatibility (v1.3)

✅ pytest-asyncio timeout issues (fixture síncrono)

✅ pytest-timeout plugin instalado (v2.4.0)

Tests E2E Suite 1 (test_agenda_integration.py):

✅ 10/10 tests PASSING

✅ Handler → Service → Repository → Database validado

✅ PostgreSQL real en tests

✅ Coverage: event_service 65%, event_tools 24%, agent_states 89%

Tests CRUD Suite 2 (test_agenda_crud.py) ✨ NUEVO:

✅ 6/6 tests PASSING

✅ Router → Agent → Service → Repository validado

✅ test_create_event (crear evento vía router)

✅ test_update_event (actualizar título)

✅ test_query_events (consultar eventos)

✅ test_delete_event (eliminar evento)

✅ test_mark_complete (marcar completado)

✅ test_unknown_intent (fallback handling)

Métricas Totales:

✅ 16/16 tests PASSING (10 E2E + 6 CRUD)

✅ Cobertura: 5% → 19% (+14%)

✅ Router coverage: 38% → 59% (+21%)

✅ Orchestrator coverage: 31% → 84% (+53%)

✅ NLP Engine coverage: 13% → 72% (+59%)

✅ Handler coverage: 14% → 41% (+27%)

Archivos Actualizados:

✅ src/theaia/tests/conftest.py (WindowsSelectorEventLoopPolicy)

✅ src/theaia/tests/agents/agenda_agent/test_agenda_integration.py (10 tests)

✅ src/theaia/tests/integration/test_agenda_crud.py ✨ NUEVO (6 tests)

✅ src/theaia/database/repositories/base_repository.py (**kwargs)

✅ src/theaia/agents/agenda_agent/tools/event_tools.py ✨ v1.3 (Union[datetime, str])

Herramientas Instaladas:

✅ pytest-timeout (v2.4.0)

Pendiente para AgendaAgent:

⏳ Integración con Core Router (H04 Phase 3)

⏳ FSM testing completo

⏳ Telegram integration tests

⏳ Features avanzadas (recordatorios, eventos recurrentes)

📋 H03: AGENTES + COREROUTER (HITO 1-6)
🎯 HITO 1: EVENTAGENT COMPLETO + COREROUTER
BLOQUE 1.1: Event Model + EventRepository
☑ 1.1.1 — Crear archivo src/theaia/database/models/event.py
☑ 1.1.2 — Definir class Event(Base)
☑ 1.1.3 — Agregar fields (id, user_id, title, description, date, time, participants, created_at, updated_at, tenant_id)
☑ 1.1.4 — Agregar relationships (user, reminders)
☑ 1.1.5 — Implementar repr
☑ 1.1.6 — Crear migración: alembic revision --autogenerate -m "add event model"
☑ 1.1.7 — Editar migración: agregar índices (user_id, date, tenant_id)
☑ 1.1.8 — Ejecutar migración: alembic upgrade head
☑ 1.1.9 — Verificar tabla en BD: \dt events
☑ 1.1.10 — Crear archivo src/theaia/database/repositories/event_repository.py
☑ 1.1.11 — Implementar EventRepository(BaseRepository[Event])
☑ 1.1.12 — Método create_event(user_id, title, date, time, participants, description, tenant_id)
☑ 1.1.13 — Método get_events(user_id, date=None, tenant_id=None)
☑ 1.1.14 — Método search_events(user_id, keyword, tenant_id=None)
☑ 1.1.15 — Método update_event(event_id, changes)
☑ 1.1.16 — Método delete_event(event_id)
☑ 1.1.17 — Agregar docstrings con ejemplos en cada método
☑ 1.1.18 — Agregar logging (logger.info/error)
☑ 1.1.19 — Verificar todos los métodos son async
☑ 1.1.20 — Verificar multi-tenant validation en todos

✅ BLOQUE 1.1 COMPLETO

BLOQUE 1.2: Reminder Model + ReminderRepository
☑ 1.2.1 — Crear archivo src/theaia/database/models/reminder.py
☑ 1.2.2 — Definir class Reminder(Base)
☑ 1.2.3 — Agregar fields (id, user_id, event_id, trigger_time, minutes_before, sent, created_at, updated_at, tenant_id)
☑ 1.2.4 — Agregar relationships (user, event)
☑ 1.2.5 — Implementar repr
☑ 1.2.6 — Crear migración: alembic revision --autogenerate -m "add reminder model"
☑ 1.2.7 — Editar migración: agregar índices (user_id, trigger_time, sent, tenant_id, user_id+trigger_time+sent composite)
☑ 1.2.8 — Ejecutar migración: alembic upgrade head
☑ 1.2.9 — Verificar tabla en BD: \dt reminders
☑ 1.2.10 — Crear archivo src/theaia/database/repositories/reminder_repository.py
☑ 1.2.11 — Implementar ReminderRepository(BaseRepository[Reminder])
☑ 1.2.12 — Método get_pending(before_time, user_id=None, tenant_id=None)
☑ 1.2.13 — Método mark_sent(reminder_id)
☑ 1.2.14 — Método create_batch(reminders: List[dict])
☑ 1.2.15 — Método cleanup_old(older_than: datetime, tenant_id=None)
☑ 1.2.16 — Agregar docstrings con ejemplos
☑ 1.2.17 — Agregar logging
☑ 1.2.18 — Verificar todos async
☑ 1.2.19 — Verificar multi-tenant validation

✅ BLOQUE 1.2 COMPLETO

BLOQUE 1.3: EventAgent Handler + CoreRouter Integration
☑ 1.3.1 — Crear archivo src/theaia/agents/event_agent/handler.py
☑ 1.3.2 — Definir class EventAgentHandler
☑ 1.3.3 — Método init(event_repo, reminder_repo, intent_detector, entity_extractor)
☑ 1.3.4 — Método async def handle(user_id, message, context) → router
☑ 1.3.5 — Método async def create_event_handler(user_id, message, context)
☑ Extract entities (date, time, title)
☑ Validar fecha futura, hora válida
☑ event_repo.create_event(...)
☑ Crear automáticamente 2 recordatorios:
☑ Recordatorio 1: trigger_time = event.time - 15 min, minutes_before=15
☑ Recordatorio 2: trigger_time = event.time exacto, minutes_before=0
☑ reminder_repo.create_batch([...])
☑ Return response success
☑ 1.3.6 — Método async def update_event_handler(user_id, message, context)
☑ Extract entities
☑ event_repo.update_event(...)
☑ Return response
☑ 1.3.7 — Método async def cancel_event_handler(user_id, message, context)
☑ Extract event_id
☑ event_repo.delete_event(...) ← Reminders CASCADE delete automáticos
☑ Return response
☑ 1.3.8 — Agregar intent mapping (crear_evento, modificar_evento, cancelar_evento)
☑ 1.3.9 — Agregar logging
☑ 1.3.10 — Agregar docstrings
☑ 1.3.11 — Verificar todos async
☑ 1.3.12 — Target LOC: 300-350
□ 1.3.13 — Modificar src/theaia/core/router.py
□ 1.3.14 — Importar EventAgentHandler en CoreRouter
□ 1.3.15 — Actualizar agent_registry:

text
"crear_evento": EventAgentHandler,
"modificar_evento": EventAgentHandler,
"cancelar_evento": EventAgentHandler,
□ 1.3.16 — Verificar CoreRouter.route() instancia agent correctamente
□ 1.3.17 — Verificar CoreRouter.route() llama agent.handle()
□ 1.3.18 — Verificar CoreRouter retorna response del agente
□ 1.3.19 — Agregar fallback: si intent NOT in registry → "Intención no reconocida"

⏳ BLOQUE 1.3 EN PROGRESO (80%)

BLOQUE 1.4: EventAgent FSM + Tests E2E
☑ 1.4.1 — Crear archivo src/theaia/agents/event_agent/fsm.py
☑ 1.4.2 — Definir class EventFSM(BaseStateMachine)
☑ 1.4.3 — Estados: IDLE, ASKING_DATE, ASKING_TIME, ASKING_TITLE, CONFIRMED, ERROR
☑ 1.4.4 — Transiciones definidas y completas
☑ 1.4.5 — async def transition(trigger) → str
☑ 1.4.6 — Draft storage en context['event_draft']
☑ 1.4.7 — Validaciones en transiciones
☑ 1.4.8 — Docstrings
☑ 1.4.9 — Target LOC: 150-200
☑ 1.4.10 — Crear archivo tests/agents/event_agent/test_event_agent.py
☑ 1.4.11 — Fixture: event_repo
☑ 1.4.12 — Fixture: reminder_repo
☑ 1.4.13 — Fixture: intent_detector
☑ 1.4.14 — Fixture: entity_extractor
☑ 1.4.15 — Fixture: test_user
☑ 1.4.16 — Test 1: FSM transition IDLE → ASKING_DATE
☑ 1.4.17 — Test 2: FSM full chain IDLE → CONFIRMED
☑ 1.4.18 — Test 3: FSM error handling
☑ 1.4.19 — Test 4: create_event_handler E2E
☑ 1.4.20 — Test 5: Verificar 2 recordatorios creados (15 min + exacto)
☑ 1.4.21 — Test 6: update_event_handler E2E
☑ 1.4.22 — Test 7: cancel_event_handler E2E (reminders CASCADE deleted)
☑ 1.4.23 — Test 8: Multi-tenant isolation
☑ 1.4.24 — Test 9: Performance (<100ms)
□ 1.4.25 — Test 10: ⭐ CoreRouter integration E2E
□ message → CoreRouter.route()
□ CoreRouter detecta "crear_evento"
□ CoreRouter instancia EventAgentHandler
□ CoreRouter llama handler.handle()
□ Retorna response correcto
□ 1.4.26 — Test 11: CoreRouter routing (create, update, cancel)
□ 1.4.27 — Test 12: CoreRouter fallback (unknown intent)
☑ 1.4.28 — pytest tests/agents/event_agent/ -v --cov
☑ 1.4.29 — Verificar tests PASSING
☑ 1.4.30 — Verificar coverage ≥85%

⏳ BLOQUE 1.4 EN PROGRESO (85%)

BLOQUE 1.5: Git Commit Sprint 1
□ 1.5.1 — git add src/theaia/database/models/event.py
□ 1.5.2 — git add src/theaia/database/models/reminder.py
□ 1.5.3 — git add src/theaia/database/repositories/event_repository.py
□ 1.5.4 — git add src/theaia/database/repositories/reminder_repository.py
□ 1.5.5 — git add src/theaia/agents/event_agent/handler.py
□ 1.5.6 — git add src/theaia/agents/event_agent/fsm.py
□ 1.5.7 — git add src/theaia/core/router.py
□ 1.5.8 — git add tests/agents/event_agent/
□ 1.5.9 — git add alembic/versions/
□ 1.5.10 — git commit -m "Sprint 1: EventAgent COMPLETO + CoreRouter Integration..."
□ 1.5.11 — git log -1 --stat (verificar)

⏸️ BLOQUE 1.5 PENDIENTE

⏳ HITO 1: EVENTAGENT EN PROGRESO (70%)

🎯 HITO 2: NOTEAGENT COMPLETO + COREROUTER
□ 2.1.1 — Crear archivo src/theaia/database/models/note.py
□ 2.1.2 — Definir class Note(Base)
□ 2.1.3 — Agregar fields (id, user_id, text, tags, created_at, updated_at, tenant_id)
□ 2.1.4 — Crear migración: alembic revision --autogenerate -m "add note model"
□ 2.1.5 — Ejecutar migración: alembic upgrade head
□ 2.1.6 — Crear archivo src/theaia/database/repositories/note_repository.py
□ 2.1.7 — Implementar NoteRepository(BaseRepository[Note])
□ 2.1.8 — Método create_note(user_id, text, tags, tenant_id)
□ 2.1.9 — Método get_recent(user_id, limit=10, tenant_id=None)
□ 2.1.10 — Método search_by_tags(user_id, tags: List[str], tenant_id=None)
□ 2.1.11 — Método full_text_search(user_id, keyword, tenant_id=None)
□ 2.1.12 — Método update_note(note_id, changes)
□ 2.1.13 — Método delete_note(note_id)

□ 2.2.1 — Crear archivo src/theaia/agents/note_agent/handler.py
□ 2.2.2 — Definir class NoteAgentHandler
□ 2.2.3 — Método init(note_repo, intent_detector, entity_extractor)
□ 2.2.4 — Método async def handle(user_id, message, context)
□ 2.2.5 — Método async def create_note_handler(user_id, message, context)
□ 2.2.6 — Método async def update_note_handler(user_id, message, context)
□ 2.2.7 — Método async def delete_note_handler(user_id, message, context)
□ 2.2.8 — Agregar intent mapping (crear_nota, modificar_nota, borrar_nota)

□ 2.3.1 — Crear archivo src/theaia/agents/note_agent/fsm.py
□ 2.3.2 — Definir class NoteFSM(BaseStateMachine)
□ 2.3.3 — Estados: IDLE, ASKING_TEXT, ASKING_TAGS, CONFIRMED, ERROR
□ 2.3.4 — Transiciones completas
□ 2.3.5 — async def transition(trigger)

□ 2.4.1 — Modificar src/theaia/core/router.py (actualizar agent_registry)
□ 2.4.2 — Agregar intents NoteAgent:

text
"crear_nota": NoteAgentHandler,
"modificar_nota": NoteAgentHandler,
"borrar_nota": NoteAgentHandler,
□ 2.4.3 — Verificar CoreRouter enruta correctamente

□ 2.5.1 — Crear tests/agents/note_agent/test_note_agent.py
□ 2.5.2 — Tests FSM transitions (3 tests)
□ 2.5.3 — Tests handlers E2E (3 tests)
□ 2.5.4 — Tests multi-tenant (1 test)
□ 2.5.5 — Tests performance (1 test)
□ 2.5.6 — ⭐ Tests CoreRouter integration E2E (2 tests)
□ 2.5.7 — pytest tests/agents/note_agent/ -v --cov
□ 2.5.8 — Verificar 10 tests PASSING
□ 2.5.9 — Verificar coverage ≥85%

□ 2.6.1 — git add y commit Sprint 2

⏸️ HITO 2: NOTEAGENT PENDIENTE (0%)

🎯 HITO 3: QUERYAGENT COMPLETO + COREROUTER
□ 3.1.1 — Crear archivo src/theaia/database/models/query_cache.py
□ 3.1.2 — Definir class QueryCache(Base)
□ 3.1.3 — Agregar fields (id, user_id, query_hash, result, ttl, created_at, expires_at, tenant_id)
□ 3.1.4 — Crear migración: alembic revision --autogenerate -m "add query_cache model"
□ 3.1.5 — Ejecutar migración

□ 3.2.1 — Crear archivo src/theaia/database/repositories/query_cache_repository.py
□ 3.2.2 — Implementar QueryCacheRepository(BaseRepository[QueryCache])
□ 3.2.3 — Método get_cached(user_id, query_hash, tenant_id=None)
□ 3.2.4 — Método set_cache(user_id, query, result, ttl, tenant_id=None)
□ 3.2.5 — Método cleanup_expired(tenant_id=None)

□ 3.3.1 — Crear archivo src/theaia/agents/query_agent/handler.py
□ 3.3.2 — Definir class QueryAgentHandler
□ 3.3.3 — Método init(event_repo, note_repo, query_cache_repo)
□ 3.3.4 — Método async def handle(user_id, message, context)
□ 3.3.5 — Método async def list_events_handler(user_id, message, context)
□ 3.3.6 — Método async def search_events_handler(user_id, message, context)
□ 3.3.7 — Método async def list_notes_handler(user_id, message, context)
□ 3.3.8 — Método async def search_notes_handler(user_id, message, context)
□ 3.3.9 — Método async def daily_summary_handler(user_id, message, context)
□ 3.3.10 — Método async def weekly_summary_handler(user_id, message, context)
□ 3.3.11 — Método async def list_reminders_handler(user_id, message, context)
□ 3.3.12 — Agregar cache logic (query_cache_repo.get_cached, set_cache)
□ 3.3.13 — Agregar intent mapping (listar_eventos, buscar_evento, listar_notas, buscar_nota, resumen_hoy, resumen_semana, listar_recordatorios)

□ 3.4.1 — Crear archivo src/theaia/agents/query_agent/fsm.py
□ 3.4.2 — Definir class QueryFSM(BaseStateMachine)
□ 3.4.3 — Estados: IDLE, SEARCHING, RETURNING_RESULTS, ERROR
□ 3.4.4 — Transiciones con cache hit/miss logic

□ 3.5.1 — Modificar src/theaia/core/router.py (actualizar agent_registry)
□ 3.5.2 — Agregar intents QueryAgent (7 intents)

□ 3.6.1 — Crear tests/agents/query_agent/test_query_agent.py
□ 3.6.2 — Tests FSM (2 tests)
□ 3.6.3 — Tests handlers (7 tests)
□ 3.6.4 — Tests cache logic (3 tests)
□ 3.6.5 — Tests multi-tenant (1 test)
□ 3.6.6 — ⭐ Tests CoreRouter integration (3 tests)
□ 3.6.7 — pytest tests/agents/query_agent/ -v --cov
□ 3.6.8 — Verificar 16 tests PASSING
□ 3.6.9 — Verificar coverage ≥85%

□ 3.7.1 — git add y commit Sprint 3

⏸️ HITO 3: QUERYAGENT PENDIENTE (0%)

🎯 HITO 4: HELPAGENT + FULL COREROUTER INTEGRATION
□ 4.1.1 — Crear archivo src/theaia/agents/help_agent/handler.py
□ 4.1.2 — Definir class HelpAgentHandler
□ 4.1.3 — Método init(core_router, intent_detector)
□ 4.1.4 — Método async def handle(user_id, message, context)
□ 4.1.5 — Método async def show_help_handler(user_id, message, context)
□ Return menú principal con 4 agentes
□ 4.1.6 — Método async def show_commands_handler(user_id, message, context)
□ Return lista de todos los comandos
□ 4.1.7 — Método async def handle_unknown_intent(user_id, message, context) ← FALLBACK
□ Sugerencias basadas en palabras clave
□ Log para mejorar ML
□ 4.1.8 — Método async def error_recovery_handler(user_id, message, context, error)
□ Message: "Hubo un error. ¿Puedo ayudarte?"
□ Log error
□ 4.1.9 — Agregar intent mapping (ayuda, comandos, unknown)

□ 4.2.1 — Crear archivo src/theaia/agents/help_agent/fsm.py
□ 4.2.2 — Definir class HelpFSM(BaseStateMachine)
□ 4.2.3 — Estados: IDLE, SHOWING_HELP, SHOWING_COMMANDS, AWAITING_CLARIFICATION, ERROR
□ 4.2.4 — Transiciones con fallback logic

□ 4.3.1 — Modificar src/theaia/core/router.py (actualizar agent_registry COMPLETO)
□ 4.3.2 — Agregar HelpAgent intents:

text
"ayuda": HelpAgentHandler,
"comandos": HelpAgentHandler,
"unknown": HelpAgentHandler, # Fallback
□ 4.3.3 — Verificar CoreRouter.route() implementa fallback correctamente
□ Si intent NOT in registry → intent = "unknown" → HelpAgent
□ 4.3.4 — Verificar CoreRouter.route() logging completo

□ 4.4.1 — Crear tests/integration/test_corerouter_e2e.py
□ 4.4.2 — ⭐ Test E2E: message → CoreRouter → EventAgent (create) → DB + response
□ 4.4.3 — ⭐ Test E2E: message → CoreRouter → NoteAgent (create) → DB + response
□ 4.4.4 — ⭐ Test E2E: message → CoreRouter → QueryAgent (list) → cache + response
□ 4.4.5 — ⭐ Test E2E: unknown intent → CoreRouter → HelpAgent (fallback)
□ 4.4.6 — ⭐ Test E2E: "ayuda" → CoreRouter → HelpAgent (show_help)
□ 4.4.7 — ⭐ Test E2E: 4 agentes juntos en flujo completo
□ 4.4.8 — pytest tests/integration/test_corerouter_e2e.py -v --cov
□ 4.4.9 — Verificar 6 tests PASSING

□ 4.5.1 — git add y commit Sprint 4

⏸️ HITO 4: HELPAGENT PENDIENTE (0%)

🎯 HITO 5: EVENTSCHEDULER BACKGROUND TASK
□ 5.1.1 — Crear archivo src/theaia/agents/event_agent/scheduler.py
□ 5.1.2 — Definir class EventScheduler
□ 5.1.3 — Método init(reminder_repo, event_repo, telegram_adapter, user_prefs_repo)
□ 5.1.4 — Método async def run_scheduler()
□ while True loop
□ await asyncio.sleep(60)
□ get pending reminders
□ check quiet hours
□ send via Telegram
□ mark as sent
□ 5.1.5 — Método async def _fetch_pending_reminders(before_time, user_id=None)
□ 5.1.6 — Método async def _send_reminder(reminder, event)
□ Check quiet hours
□ Format mensaje
□ Enviar Telegram
□ 5.1.7 — Método async def _mark_sent(reminder_id)
□ 5.1.8 — Método async def _is_quiet_time(user_id, current_time)

□ 5.2.1 — Crear modelo UserPreferences (si no existe)
□ quiet_hours_start, quiet_hours_end
□ reminder_advance_min
□ 5.2.2 — Crear UserPreferencesRepository (si no existe)
□ get_or_create_default
□ is_quiet_time

□ 5.3.1 — Crear tests/integration/test_scheduler_e2e.py
□ 5.3.2 — Test: Scheduler fetch pending reminders
□ 5.3.3 — Test: Scheduler respeta quiet hours
□ 5.3.4 — Test: Scheduler send reminder + mark sent
□ 5.3.5 — Test: Scheduler cleanup old reminders
□ 5.3.6 — pytest tests/integration/test_scheduler_e2e.py -v --cov
□ 5.3.7 — Verificar 4 tests PASSING

□ 5.4.1 — git add y commit Sprint 5

⏸️ HITO 5: EVENTSCHEDULER PENDIENTE (0%)

🎯 HITO 6: MAIN.PY + DOCS + RELEASE V1.0-MVP
□ 6.1.1 — Modificar src/theaia/main.py
□ 6.1.2 — Agregar on_startup():
□ Initialize repositories
□ Initialize EventScheduler
□ asyncio.create_task(scheduler.run_scheduler())
□ Log "Scheduler started"
□ 6.1.3 — Agregar on_shutdown():
□ Cancel scheduler task
□ Close DB connections
□ Log "Scheduler stopped"
□ 6.1.4 — Verificar FastAPI app instancia correctamente

□ 6.2.1 — Crear docs/agents/EVENT_AGENT.md
□ Purpose, responsibilities
□ Intents soportados
□ Methods públicos
□ FSM states & transitions
□ Examples
□ 6.2.2 — Crear docs/agents/NOTE_AGENT.md
□ 6.2.3 — Crear docs/agents/QUERY_AGENT.md
□ 6.2.4 — Crear docs/agents/HELP_AGENT.md
□ 6.2.5 — Crear docs/COREROUTER.md
□ Intent detection
□ Routing table
□ Fallback mechanism
□ 6.2.6 — Crear docs/ARCHITECTURE.md (overview)
□ 6.2.7 — Crear docs/DATABASE.md (models + repositories)
□ 6.2.8 — Crear docs/TESTING.md

□ 6.3.1 — pytest --cov=src/theaia --cov-report=html
□ 6.3.2 — Verificar coverage >85%
□ 6.3.3 — Revisar coverage report
□ 6.3.4 — Crear CHANGELOG.md (cambios H03)

□ 6.4.1 — Clean commits (revisión final)
□ 6.4.2 — git add docs/
□ 6.4.3 — git add CHANGELOG.md
□ 6.4.4 — git commit -m "Sprint 6: Main.py + Documentation + Release v1.0-mvp"
□ 6.4.5 — git tag -a v1.0-mvp -m "H03 COMPLETE: 4 agentes operativos, CoreRouter, EventScheduler"
□ 6.4.6 — git push origin main --tags

□ 6.5.1 — Crear documento HITO_H03_CIERRE.md
□ Summary de sprints 1-6
□ Logros principales
□ Tests totales (40+)
□ Coverage final
□ Release notes

⏸️ HITO 6: MAIN + DOCS PENDIENTE (0%)

⏳⏳⏳ H03 EN PROGRESO (25%) ⏳⏳⏳

📋 H04: NLP REFINEMENT (HITO 7-9)
🆕 ACTUALIZADO: H04 PHASE 1 & 2 - AgendaAgent Implementation
✅ PHASE 1: Core Implementation (COMPLETADO)
☑ AgendaAgent Handler implementado
☑ EventService implementado
☑ EventTools (CrewAI) implementado
☑ Intent parser implementado
☑ DateTime parser implementado
☑ NLP Engine integrado
☑ Response formatter implementado

✅ PHASE 2: Testing (COMPLETADO 04 Dic 2025)
Suite 1: Tests E2E (test_agenda_integration.py)
☑ test_handler_initialization
☑ test_service_create_event
☑ test_service_get_event
☑ test_tools_create_event
☑ test_tools_list_upcoming_events
☑ test_tools_update_event
☑ test_tools_mark_completed
☑ test_service_get_upcoming_events
☑ test_service_delete_event
☑ test_full_integration_flow
✅ 10/10 tests PASSING

Suite 2: Tests CRUD via Router (test_agenda_crud.py) ✨ NUEVO
☑ test_create_event (router.handle → agent → DB)
☑ test_update_event (actualizar título)
☑ test_query_events (consultar eventos)
☑ test_delete_event (eliminar evento)
☑ test_mark_complete (marcar completado)
☑ test_unknown_intent (fallback)
✅ 6/6 tests PASSING

Fixes Implementados:
☑ Event loop issues (Windows + asyncpg)
☑ Foreign key violations (fixture scope='session')
☑ BaseRepository.create() TypeError (**kwargs)
☑ EventTools datetime compatibility (Union[datetime, str])
☑ pytest-asyncio timeout (fixture síncrono + asyncio.run())
☑ pytest-timeout plugin instalado (v2.4.0)

Cobertura Mejorada:
☑ Router: 38% → 59% (+21%)
☑ Orchestrator: 31% → 84% (+53%)
☑ NLP Engine: 13% → 72% (+59%)
☑ Handler: 14% → 41% (+27%)
☑ Total: 5% → 19% (+14%)

✅ PHASE 2 COMPLETADO AL 100%

⏸️ PHASE 3: Integration (PENDIENTE)
□ 3.1 — Registrar AgendaAgent en Core Router
□ 3.2 — Mapear intents específicos a AgendaAgent
□ 3.3 — Tests de routing completo
□ 3.4 — Intent classification refinement

Progreso Phase 3: 0%

⏸️ PHASE 4: Advanced Features (PENDIENTE)
□ 4.1 — Recordatorios automáticos
□ 4.2 — Eventos recurrentes
□ 4.3 — Integración con Google Calendar
□ 4.4 — Notificaciones push

Progreso Phase 4: 0%

🔄 H04 PROGRESO TOTAL: 75% (Phase 1 + Phase 2 completadas)

🎯 HITO 7: INTENT DETECTOR REFINEMENT
□ 7.1.1 — Analizar errores Intent Detection actual (~80% accuracy)
□ 7.1.2 — Crear log de misclassified intents
□ 7.1.3 — Identificar patrones de error

□ 7.2.1 — Feature engineering mejoras
□ 7.2.2 — Mejorar preprocessing (tokenization, stemming)
□ 7.2.3 — Agregar features lingüísticas adicionales
□ 7.2.4 — Balancear dataset de entrenamiento

□ 7.3.1 — Reentrenar Intent Detector modelo
□ 7.3.2 — Usar nuevas features
□ 7.3.3 — Aumentar data de entrenamiento (si posible)
□ 7.3.4 — Validar accuracy >92%

□ 7.4.1 — Crear tests/ml/test_intent_detector.py
□ 7.4.2 — Test accuracy benchmark (>92%)
□ 7.4.3 — Test confusion matrix
□ 7.4.4 — Test performance (<50ms)
□ 7.4.5 — Test edge cases (typos, abbreviations, etc)
□ 7.4.6 — pytest tests/ml/ -v --cov
□ 7.4.7 — Verificar 15+ tests PASSING

□ 7.5.1 — git add y commit Sprint 7

⏸️ HITO 7: INTENT DETECTOR PENDIENTE (0%)

🎯 HITO 8: ENTITY EXTRACTOR + CONTEXT REFINEMENT
□ 8.1.1 — Analizar errores Entity Extraction (~75% accuracy)
□ 8.1.2 — Crear log de extraction failures

□ 8.2.1 — Mejorar Entity Extractor modelo
□ 8.2.2 — Agregar NER mejoras
□ 8.2.3 — Mejorar date/time parsing
□ 8.2.4 — Mejorar people name extraction
□ 8.2.5 — Validar accuracy >90%

□ 8.3.1 — Mejorar Context Manager
□ 8.3.2 — Implementar sliding window (últimos 5 mensajes)
□ 8.3.3 — Agregar context embeddings
□ 8.3.4 — Mejorar context relevance scoring

□ 8.4.1 — Crear tests/ml/test_entity_extractor.py
□ 8.4.2 — Test accuracy benchmark (>90%)
□ 8.4.3 — Test date extraction (múltiples formatos)
□ 8.4.4 — Test time extraction
□ 8.4.5 — Test name extraction
□ 8.4.6 — Test performance (<100ms)
□ 8.4.7 — pytest tests/ml/ -v --cov
□ 8.4.8 — Verificar 12+ tests PASSING

□ 8.5.1 — git add y commit Sprint 8

⏸️ HITO 8: ENTITY EXTRACTOR PENDIENTE (0%)

🎯 HITO 9: ML PIPELINE INTEGRATION + RELEASE V1.1-ML
□ 9.1.1 — Integrar refined Intent Detector en CoreRouter
□ 9.1.2 — Integrar refined Entity Extractor en handlers
□ 9.1.3 — Integrar improved Context Manager

□ 9.2.1 — Crear A/B testing framework
□ 9.2.2 — Setup old vs new model comparison
□ 9.2.3 — Log metrics de ambos

□ 9.3.1 — Performance benchmarking
□ 9.3.2 — Intent detection latency (<50ms)
□ 9.3.3 — Entity extraction latency (<100ms)
□ 9.3.4 — End-to-end latency (<200ms)

□ 9.4.1 — Crear tests/ml/test_ml_pipeline_integration.py
□ 9.4.2 — Test: refined models improve accuracy
□ 9.4.3 — Test: performance within budgets
□ 9.4.4 — pytest tests/ml/ -v --cov

□ 9.5.1 — pytest --cov=src/theaia --cov-report=html
□ 9.5.2 — Verificar coverage ≥85%

□ 9.6.1 — Crear CHANGELOG.md (cambios H04)
□ 9.6.2 — git add y commit Sprint 9
□ 9.6.3 — git tag -a v1.1-ml -m "H04 COMPLETE: Intent >92%, Entity >90%"
□ 9.6.4 — git push origin main --tags

□ 9.7.1 — Crear documento HITO_H04_CIERRE.md

⏸️ HITO 9: ML PIPELINE PENDIENTE (0%)

🔄🔄🔄 H04 EN PROGRESO (75%) 🔄🔄🔄

📋 H05: TESTING + QA (HITO 10-12)
🎯 HITO 10: UNIT + INTEGRATION TESTING
□ 10.1.1 — Analizar coverage actual (~19%)
□ 10.1.2 — Identificar áreas sin cobertura

□ 10.2.1 — Crear tests faltantes (target >90%)
□ 10.2.2 — Unit tests para cada método
□ 10.2.3 — Integration tests para workflows completos
□ 10.2.4 — Mock improvements
□ 10.2.5 — Fixture improvements

□ 10.3.1 — Crear tests/units/
□ test_event_repository.py (si no existe)
□ test_note_repository.py (si no existe)
□ test_reminder_repository.py (si no existe)
□ test_query_cache_repository.py (si no existe)

□ 10.4.1 — Crear tests/integration/
□ test_event_agent_full_workflow.py
□ test_note_agent_full_workflow.py
□ test_query_agent_full_workflow.py
□ test_multi_agent_workflows.py

□ 10.5.1 — pytest --cov=src/theaia --cov-report=html
□ 10.5.2 — Verificar coverage >90%
□ 10.5.3 — Revisar coverage report

□ 10.6.1 — pytest tests/ -v (run ALL tests)
□ 10.6.2 — Verificar 30+ NEW tests PASSING
□ 10.6.3 — TOTAL tests: 70+

□ 10.7.1 — git add y commit Sprint 10

⏸️ HITO 10: COVERAGE PENDIENTE (0%)

🎯 HITO 11: LOAD TESTING + STRESS TESTING
□ 11.1.1 — Crear tests/load/ directorio
□ 11.1.2 — Setup load testing framework (locust, pytest-benchmark)

□ 11.2.1 — Load test: 100 concurrent users
□ 11.2.2 — Load test: 500 concurrent users
□ 11.2.3 — Load test: 1000 concurrent users
□ 11.2.4 — Medir: latency, throughput, error rate

□ 11.3.1 — Performance profiling
□ 11.3.2 — Database query optimization (si necesario)
□ 11.3.3 — Caching optimization
□ 11.3.4 — Connection pooling verification

□ 11.4.1 — Memory leak detection
□ 11.4.2 — Profile memory usage long-running
□ 11.4.3 — Fix leaks (si encontradas)

□ 11.5.1 — pytest tests/load/ -v
□ 11.5.2 — Verificar 10+ stress scenarios PASSING
□ 11.5.3 — Documentar resultados (latency SLA, throughput)

□ 11.6.1 — git add y commit Sprint 11

⏸️ HITO 11: LOAD TESTING PENDIENTE (0%)

🎯 HITO 12: ERROR SCENARIOS + EDGE CASES + RELEASE V1.2-STABLE
□ 12.1.1 — Crear tests/edge_cases/ directorio

□ 12.2.1 — Error recovery tests
□ 12.2.2 — Test: DB connection fail
□ 12.2.3 — Test: Telegram API fail
□ 12.2.4 — Test: Intent detector timeout
□ 12.2.5 — Test: Entity extraction fail
□ 12.2.6 — Test: Graceful degradation

□ 12.3.1 — Edge case tests
□ 12.3.2 — Test: null inputs
□ 12.3.3 — Test: empty strings
□ 12.3.4 — Test: special characters
□ 12.3.5 — Test: very long messages
□ 12.3.6 — Test: Unicode/emojis
□ 12.3.7 — Test: SQL injection attempts (basic)

□ 12.4.1 — Multi-tenant isolation verification
□ 12.4.2 — Test: data leak between tenants (NO leak)
□ 12.4.3 — Test: quota isolation

□ 12.5.1 — Security basics testing
□ 12.5.2 — Test: authentication (basic)
□ 12.5.3 — Test: authorization (basic)
□ 12.5.4 — Test: SQL injection (basic)

□ 12.6.1 — pytest tests/edge_cases/ -v
□ 12.6.2 — Verificar 15+ edge case tests PASSING
□ 12.6.3 — TOTAL tests ahora: 85+

□ 12.7.1 — pytest --cov=src/theaia --cov-report=html (final)
□ 12.7.2 — Verificar coverage >90% (final)

□ 12.8.1 — Crear CHANGELOG.md (cambios H05)
□ 12.8.2 — Crear documento HITO_H05_CIERRE.md
□ 12.8.3 — Crear documento FINAL_REPORT.md
□ Architecture overview
□ Agentes implementados
□ Database schema
□ Testing results
□ Performance metrics
□ Known limitations

□ 12.9.1 — git add y commit Sprint 12
□ 12.9.2 — git tag -a v1.2-stable -m "H05 COMPLETE: Coverage >90%, All tests passing, Production-ready"
□ 12.9.3 — git push origin main --tags

□ 12.10.1 — Crear README.md (Quick start guide)

⏸️ HITO 12: EDGE CASES PENDIENTE (0%)

⏸️⏸️⏸️ H05 PENDIENTE (0%) ⏸️⏸️⏸️

═════════════════════════════════════════════

📊 ESTADO FINAL DEL PROYECTO
Última Actualización: 04 Diciembre 2025, 23:13 CET

Hitos Completados: ✅
H04 PHASE 1 - AgendaAgent Core Implementation (100%)

H04 PHASE 2 - AgendaAgent Tests E2E + CRUD (100%)

16/16 tests PASSING

Cobertura: 5% → 19% (+14%)

Router: 38% → 59% (+21%)

Orchestrator: 31% → 84% (+53%)

NLP Engine: 13% → 72% (+59%)

En Progreso: ⏳
H03 - Agentes + CoreRouter (25% completado)

HITO 1: EventAgent (70% completado)

H04 - NLP Refinement (75% completado)

Phase 1: ✅ 100%

Phase 2: ✅ 100%

Phase 3: ⏸️ 0%

Phase 4: ⏸️ 0%

Pendientes: ⏸️
H03 HITO 2-6 - NoteAgent, QueryAgent, HelpAgent, Scheduler, Docs

H04 HITO 7-9 - Intent Detector, Entity Extractor, ML Pipeline

H05 - Testing + QA (0% completado)

Próximos Pasos Inmediatos:
H04 Phase 3: Registrar AgendaAgent en Core Router

H04 Phase 3: Mapear intents específicos a AgendaAgent

H04 Phase 3: Tests de routing E2E completo

H03 HITO 1: Completar CoreRouter integration tests

Métricas Actuales:
Tests totales: 16 (10 E2E + 6 CRUD)

Tests passing: 16/16 (100%)

Cobertura código: 19%

Archivos test: 2 suites principales

═════════════════════════════════════════════
✅✅✅ CHECKLIST MASTER ACTUALIZADO v3.4 ✅✅✅
═════════════════════════════════════════════