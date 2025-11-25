📋 CHECKLIST MASTER H04-H05 — BLOQUE B FASE 2 (REVISADO)
Proyecto: THEA-IA
Última actualización: 25 Noviembre 2025, 16:55 CET
Responsable: Álvaro Fernández Mota (CEO THEA-IA)
Status: ⏳ PRÓXIMO - Inicio 26 NOV 2025

🎯 INFORMACIÓN GENERAL
text
╔════════════════════════════════════════════════════════════════╗
║   BLOQUE B: AGENT INTELLIGENCE & DATABASE OPTIMIZATION        ║
╠════════════════════════════════════════════════════════════════╣
║ Hitos:              H04 + H05 (Consolidados)                  ║
║ Fase:               2 / 4 (Multi-agente & Adapters)           ║
║ Período:            26 NOV - 17 DIC 2025 (FLEXIBLE)           ║
║ Duración ESTIMADA:  105 horas (orientativo, no rígido)        ║
║ Tests Target:       80 tests                                  ║
║ Coverage Target:    ≥85%                                      ║
║ Status:             ⏳ 0% - Listo para iniciar                ║
╚════════════════════════════════════════════════════════════════╝
⚠️ CLARIFICACIONES IMPORTANTES
1. Agentes a Implementar
YA TENEMOS de H03 (8 agentes del sistema):

text
✅ HelpAgent (sistema)
✅ ResetAgent (sistema)
✅ StartAgent (sistema)
✅ EventAgent (básico)
✅ NoteAgent (básico)
✅ AgendaAgent (básico v1)
✅ ConversationAgent (sistema)
✅ DefaultAgent (fallback)
NUEVOS en H04-H05 (4 agentes VERTICALES v2 - MEJORADOS):

text
⏳ AgendaAgent v2 (mejora del AgendaAgent v1)
   - Arquitectura híbrida 3 niveles
   - NLP + LLM
   - Detección conflictos avanzada

⏳ NotesAgent v2 (mejora del NoteAgent v1)
   - Búsqueda inteligente
   - Búsqueda semántica
   - Auto-categorización

⏳ EventsAgent (nuevo, más robusto que EventAgent básico)
   - Gestión avanzada eventos
   - Eventos recurrentes
   - Optimización horarios LLM

⏳ QueryAgent v2 (nuevo)
   - Consultas multi-agente
   - Búsqueda cross-domain
   - Analytics básico
TOTAL AL COMPLETAR H04-H05: 12 agentes (8 sistema + 4 verticales v2)

2. Database Completa
YA TENEMOS de H02:

text
✅ 5 Modelos base
   - User
   - Event
   - Note
   - Conversation
   - MessageHistory

✅ 5 Repositories async
✅ Migraciones Alembic base
✅ Multi-tenant architecture
NUEVOS en H04-H05 (optimizaciones + posibles modelos):

text
⏳ Modelos adicionales (SI NECESARIOS según agentes v2)
   - Reminder (si AgendaAgent v2 lo requiere)
   - Task (si EventsAgent lo requiere)
   - Category (si NotesAgent v2 lo requiere)

⏳ Optimizaciones
   - Full-text search (PostgreSQL tsvector)
   - Índices compuestos
   - Connection pooling optimizado
   - Query analyzer

⏳ Backup/Restore
   - JSON export completo
   - JSON import con validación
   - Disaster recovery
3. Sin Timeline Rígido
IMPORTANTE: Las horas son ESTIMADAS y ORIENTATIVAS, no compromisos estrictos.

✅ Usamos horas como guía de esfuerzo

✅ Nos adaptamos a ritmo real de trabajo

✅ Priorizamos CALIDAD sobre VELOCIDAD

✅ Sesiones flexibles según disponibilidad

📊 RESUMEN EJECUTIVO
Estado Global
Métrica	Valor	Target	Status
Progreso Total	0%	100%	⏳
Fases completadas	0/4	4/4	⏳
Tests PASSING	0	80	⏳
Coverage	0%	≥85%	⏳
Agentes v2 completos	0/4	4/4	⏳
Optimizaciones DB	0/3	3/3	⏳
🏗️ ESTRUCTURA DEL BLOQUE
text
BLOQUE B (105h estimadas)
│
├─ FASE 1: Agentes Verticales v2 (45h est.)
│  ├─ AgendaAgent v2 (mejora v1)
│  ├─ NotesAgent v2 (mejora NoteAgent)
│  ├─ EventsAgent (nuevo robusto)
│  └─ QueryAgent v2 (nuevo)
│
├─ FASE 2: Database Optimization (25h est.)
│  ├─ Análisis + modelos adicionales (si necesarios)
│  ├─ Query optimization (full-text + índices)
│  └─ JSON backup/restore
│
├─ FASE 3: ML/NLP Integration (20h est.)
│  ├─ Intent Detector spaCy
│  ├─ Entity Extractor advanced
│  └─ LLM integration simple
│
└─ FASE 4: Testing & QA (15h est.)
   ├─ E2E tests
   ├─ Coverage ≥85%
   └─ Performance benchmarks
🎯 FASE 1: AGENTES VERTICALES V2 (45h est.)
Objetivo: Mejorar agentes existentes + nuevos agentes especializados

✅ TAREA 1.1: AgendaAgent v2 - MEJORA DE v1
Relación con H03: Mejora del AgendaAgent básico existente

¿Qué Mejoramos?
text
AgendaAgent v1 (H03) → AgendaAgent v2 (H04-H05)
──────────────────────────────────────────────────
Comandos básicos     → + Arquitectura híbrida 3 niveles
FSM simple           → + NLP intent detection
CRUD eventos         → + LLM para queries complejas
Sin optimización     → + Detección conflictos inteligente
                     → + Sugerencias automáticas horarios
Subtareas
#	Subtarea	Tests	Prioridad
1.1.1	Estructura AgendaAgent v2 (extiende v1)	2	Alta
1.1.2	NIVEL 1: Comandos simples (mantener v1)	3	Alta
1.1.3	NIVEL 2: NLP queries (NUEVO)	5	Alta
1.1.4	NIVEL 3: LLM fallback (NUEVO)	3	Media
1.1.5	Database integration optimizada	2	Alta
TOTAL		15	
Criterios DONE 1.1
text
□ Estructura AgendaAgent v2 creada
  ├─ src/theaia/agents/agenda_agent_v2/__init__.py
  ├─ src/theaia/agents/agenda_agent_v2/handler.py
  ├─ src/theaia/agents/agenda_agent_v2/manager.py
  └─ Extiende funcionalidad de AgendaAgent v1

□ NIVEL 1 implementado (mantiene v1)
  ├─ /agenda_today funcional
  ├─ /agenda_week funcional
  ├─ /agenda_month funcional
  └─ Respuesta <10ms

□ NIVEL 2 implementado (NUEVO)
  ├─ Intent detection: "Qué tengo mañana"
  ├─ Entity extraction: fechas
  ├─ Respuesta <100ms
  └─ Integrado con spaCy básico

□ NIVEL 3 implementado (NUEVO)
  ├─ LLM fallback para queries complejas
  ├─ Cache implementado
  ├─ "Reorganiza mi agenda" funcional
  └─ Respuesta <2s

□ Database integration
  ├─ Usa EventRepository existente
  ├─ Queries optimizadas
  └─ Multi-tenant verificado

□ 15/15 tests PASSING
□ Compatible con CoreRouter existente
□ Documentation completa
Archivos a Crear 1.1
text
src/theaia/agents/agenda_agent_v2/
├── __init__.py
├── handler.py                     # Entry point
├── manager.py                     # Orchestrator
└── model/
    └── fsm.py                     # FSM states

tests/agents/agenda_agent_v2/
├── __init__.py
├── test_handler.py                # 5 tests
├── test_manager.py                # 8 tests
└── test_performance.py            # 2 tests
Progreso 1.1
text
□ Estructura base creada
□ NIVEL 1 completo (comandos simples)
□ NIVEL 2 completo (NLP queries)
□ NIVEL 3 completo (LLM fallback)
□ Database integration OK
□ 15/15 tests PASSING
□ Documentation completa

STATUS: ⏳ 0% → 100%
✅ TAREA 1.2: NotesAgent v2 - MEJORA DE NoteAgent
Relación con H03: Mejora del NoteAgent básico existente

¿Qué Mejoramos?
text
NoteAgent v1 (H03)   → NotesAgent v2 (H04-H05)
──────────────────────────────────────────────────
CRUD básico          → + Arquitectura híbrida 3 niveles
Búsqueda simple      → + Búsqueda NLP inteligente
Tags manuales        → + Búsqueda semántica LLM
                     → + Auto-categorización
                     → + Full-text search optimizado
Subtareas
#	Subtarea	Tests	Prioridad
1.2.1	Estructura NotesAgent v2 (extiende v1)	2	Alta
1.2.2	NIVEL 1: CRUD mejorado	3	Alta
1.2.3	NIVEL 2: Búsqueda NLP (NUEVO)	5	Alta
1.2.4	NIVEL 3: Búsqueda semántica LLM (NUEVO)	3	Media
1.2.5	Auto-categorization (NUEVO)	2	Media
TOTAL		15	
Criterios DONE 1.2
text
□ Estructura NotesAgent v2 creada
  ├─ src/theaia/agents/notes_agent_v2/__init__.py
  ├─ Extiende funcionalidad de NoteAgent v1
  └─ Compatible con NoteRepository existente

□ NIVEL 1: CRUD mejorado
  ├─ create_note() (mantiene v1)
  ├─ edit_note() (mantiene v1)
  ├─ delete_note() (mantiene v1)
  └─ + pin_note() (NUEVO)

□ NIVEL 2: Búsqueda NLP (NUEVO)
  ├─ Búsqueda por contenido (NLP)
  ├─ Búsqueda por tags (mejorada)
  ├─ Búsqueda por fecha
  └─ Full-text search PostgreSQL

□ NIVEL 3: Búsqueda semántica (NUEVO)
  ├─ Embeddings con LLM
  ├─ Similarity search
  ├─ Cache resultados
  └─ "Ideas sobre marketing" funcional

□ Auto-categorization (NUEVO)
  ├─ Sugerencia automática tags
  ├─ ML model básico
  └─ Confidence score

□ 15/15 tests PASSING
□ Compatible con CoreRouter
□ Documentation completa
Archivos a Crear 1.2
text
src/theaia/agents/notes_agent_v2/
├── __init__.py
├── handler.py
├── manager.py
├── model/
│   └── fsm.py
└── search/
    ├── nlp_search.py              # Búsqueda NLP
    └── semantic_search.py         # Búsqueda semántica

tests/agents/notes_agent_v2/
├── __init__.py
├── test_handler.py                # 5 tests
├── test_manager.py                # 8 tests
└── test_search.py                 # 2 tests
Progreso 1.2
text
□ Estructura base creada
□ NIVEL 1 CRUD completo
□ NIVEL 2 búsqueda NLP completo
□ NIVEL 3 búsqueda semántica completo
□ Auto-categorization completo
□ 15/15 tests PASSING
□ Documentation completa

STATUS: ⏳ 0% → 100%
✅ TAREA 1.3: EventsAgent - NUEVO ROBUSTO
Relación con H03: Reemplazo del EventAgent básico con versión robusta

¿Qué es Diferente?
text
EventAgent v1 (H03)  → EventsAgent (H04-H05)
──────────────────────────────────────────────────
CRUD básico          → + Arquitectura híbrida 3 niveles
Sin conflictos       → + Detección automática conflictos
Sin recurrencia      → + Eventos recurrentes (DAILY/WEEKLY/MONTHLY)
Sin optimización     → + Optimización horarios LLM
                     → + Sugerencias inteligentes
                     → + Gestión participantes
Subtareas
#	Subtarea	Tests	Prioridad
1.3.1	Estructura EventsAgent (nuevo)	2	Alta
1.3.2	NIVEL 1: CRUD completo	3	Alta
1.3.3	NIVEL 2: Detección conflictos (NUEVO)	5	Alta
1.3.4	NIVEL 3: Optimización LLM (NUEVO)	3	Media
1.3.5	Eventos recurrentes (NUEVO)	2	Alta
TOTAL		15	
Criterios DONE 1.3
text
□ Estructura EventsAgent creada
  ├─ src/theaia/agents/events_agent/__init__.py
  ├─ Reemplaza EventAgent v1 (más robusto)
  └─ Compatible con EventRepository

□ NIVEL 1: CRUD completo
  ├─ create_event()
  ├─ edit_event()
  ├─ delete_event()
  └─ add_participant() (NUEVO)

□ NIVEL 2: Detección conflictos (NUEVO)
  ├─ detect_conflicts() automático
  ├─ suggest_alternatives()
  ├─ Validación al crear evento
  └─ Notificación conflictos

□ NIVEL 3: Optimización LLM (NUEVO)
  ├─ suggest_optimal_time()
  ├─ Análisis patrones usuario
  ├─ Recomendaciones personalizadas
  └─ "Mejor horario para reunión" funcional

□ Eventos recurrentes (NUEVO)
  ├─ DAILY support
  ├─ WEEKLY support
  ├─ MONTHLY support
  ├─ RRULE parsing básico
  └─ Generación instancias automática

□ 15/15 tests PASSING
□ Compatible con CoreRouter
□ Documentation completa
Archivos a Crear 1.3
text
src/theaia/agents/events_agent/
├── __init__.py
├── handler.py
├── manager.py
├── model/
│   └── fsm.py
├── conflicts/
│   └── detector.py                # Detección conflictos
└── recurrence/
    └── handler.py                 # Eventos recurrentes

tests/agents/events_agent/
├── __init__.py
├── test_handler.py                # 5 tests
├── test_conflicts.py              # 5 tests
└── test_recurrence.py             # 5 tests
Progreso 1.3
text
□ Estructura base creada
□ NIVEL 1 CRUD completo
□ NIVEL 2 detección conflictos completo
□ NIVEL 3 optimización LLM completo
□ Eventos recurrentes completo
□ 15/15 tests PASSING
□ Documentation completa

STATUS: ⏳ 0% → 100%
✅ TAREA 1.4: QueryAgent v2 - NUEVO
Relación con H03: Agente COMPLETAMENTE NUEVO (no existía en H03)

¿Qué Hace?
text
NO EXISTÍA en H03    → QueryAgent v2 (H04-H05)
──────────────────────────────────────────────────
                     → Consultas multi-agente
                     → Búsqueda cross-domain
                     → FAQs sistema
                     → Analytics básico
                     → "Resume mi semana"
                     → Routing inteligente a otros agentes
Subtareas
#	Subtarea	Tests	Prioridad
1.4.1	Estructura QueryAgent (nuevo)	2	Alta
1.4.2	NIVEL 1: FAQs predefinidas	3	Alta
1.4.3	NIVEL 2: Búsqueda estructurada	5	Alta
1.4.4	NIVEL 3: Conversación libre LLM	3	Media
1.4.5	Multi-agent routing	2	Alta
TOTAL		15	
Criterios DONE 1.4
text
□ Estructura QueryAgent v2 creada
  ├─ src/theaia/agents/query_agent_v2/__init__.py
  ├─ Agente NUEVO (no existía en H03)
  └─ Compatible con CoreRouter

□ NIVEL 1: FAQs implementado
  ├─ Lista FAQs comunes
  ├─ "¿Qué puedo hacer?"
  ├─ "¿Cómo creo una nota?"
  └─ Respuestas instantáneas

□ NIVEL 2: Búsqueda estructurada
  ├─ Búsqueda en notas
  ├─ Búsqueda en eventos
  ├─ Búsqueda en conversaciones
  ├─ Resultado unificado
  └─ "Busca 'proyecto X'" funcional

□ NIVEL 3: Conversación libre
  ├─ LLM para queries complejas
  ├─ "Resume mi semana" funcional
  ├─ Analytics básico
  └─ Respuestas contextuales

□ Multi-agent routing
  ├─ route_to_agents()
  ├─ Determina agentes necesarios
  ├─ Combina respuestas
  └─ Delegación inteligente

□ 15/15 tests PASSING
□ Compatible con CoreRouter
□ Documentation completa
Archivos a Crear 1.4
text
src/theaia/agents/query_agent_v2/
├── __init__.py
├── handler.py
├── manager.py
├── model/
│   └── fsm.py
└── routing/
    └── agent_router.py            # Multi-agent routing

tests/agents/query_agent_v2/
├── __init__.py
├── test_handler.py                # 5 tests
├── test_routing.py                # 5 tests
└── test_llm.py                    # 5 tests
Progreso 1.4
text
□ Estructura base creada
□ NIVEL 1 FAQs completo
□ NIVEL 2 búsqueda estructurada completo
□ NIVEL 3 conversación libre completo
□ Multi-agent routing completo
□ 15/15 tests PASSING
□ Documentation completa

STATUS: ⏳ 0% → 100%
📊 CHECKPOINT FASE 1
text
╔════════════════════════════════════════════════════════════════╗
║   CHECKPOINT FASE 1: Agentes Verticales v2                    ║
╠════════════════════════════════════════════════════════════════╣
║ □ AgendaAgent v2 (mejora v1) - 15 tests ✅                    ║
║ □ NotesAgent v2 (mejora NoteAgent) - 15 tests ✅              ║
║ □ EventsAgent (nuevo robusto) - 15 tests ✅                   ║
║ □ QueryAgent v2 (nuevo) - 15 tests ✅                         ║
║                                                                ║
║ □ Tests FASE 1: 60/60 PASSING (100%)                          ║
║ □ Coverage FASE 1: ≥80%                                       ║
║ □ Todos con arquitectura híbrida (3 niveles)                  ║
║ □ Compatibles con CoreRouter de H03                           ║
║                                                                ║
║ TOTAL AGENTES AL COMPLETAR:                                   ║
║ - Sistema (H03): 8 agentes ✅                                 ║
║ - Verticales v2 (H04-H05): 4 agentes ⏳                       ║
║ = TOTAL: 12 agentes                                           ║
║                                                                ║
║ SI TODOS ✓ → CONTINUAR A FASE 2                               ║
║ SI ALGUNO ✗ → REVISAR ANTES DE CONTINUAR                      ║
╚════════════════════════════════════════════════════════════════╝
🗄️ FASE 2: DATABASE OPTIMIZATION (25h est.)
Objetivo: Optimizar database + añadir modelos SI NECESARIOS

✅ TAREA 2.1: Análisis + Modelos Adicionales
Importante: SOLO implementar modelos SI los agentes v2 los requieren

Subtareas
#	Subtarea	Tests	Prioridad
2.1.1	Analizar requisitos agentes FASE 1	0	Alta
2.1.2	Reminder model (SI NECESARIO)	4	Media
2.1.3	Task model (SI NECESARIO)	4	Media
2.1.4	Category model (SI NECESARIO)	0	Baja
2.1.5	Migraciones Alembic	0	Alta
TOTAL		8	
Criterios DONE 2.1
text
□ Análisis requisitos completado
  ├─ AgendaAgent v2: ¿necesita Reminder separado?
  ├─ NotesAgent v2: ¿necesita Category model?
  ├─ EventsAgent: ¿necesita Task model?
  ├─ QueryAgent v2: ¿necesita Analytics model?
  └─ DECISIÓN DOCUMENTADA (sí/no + razón)

□ Modelos implementados (SOLO SI NECESARIOS)
  ├─ src/theaia/database/models/reminder.py (si aplica)
  ├─ src/theaia/database/models/task.py (si aplica)
  ├─ src/theaia/database/models/category.py (si aplica)
  └─ Todos con multi-tenant enforcement

□ Repositories correspondientes (si aplica)
  ├─ ReminderRepository (si modelo creado)
  ├─ TaskRepository (si modelo creado)
  └─ CategoryRepository (si modelo creado)

□ Migraciones Alembic
  ├─ alembic/versions/XXX_add_new_models.py
  ├─ Up/Down testeado
  └─ Rollback verificado

□ Tests (SI aplica - 8 máximo)
  ├─ test_model_creation
  ├─ test_relationships
  ├─ test_multi_tenant_isolation
  └─ test_crud_operations

□ Documentation
  ├─ DECISION.md (análisis + decisión)
  └─ README actualizado (si modelos añadidos)
Archivos a Crear 2.1
text
docs/decisions/
└── H04-05_DATABASE_MODELS_DECISION.md  # Análisis + decisión

# SI SE CREAN MODELOS:
src/theaia/database/models/
├── reminder.py (condicional)
├── task.py (condicional)
└── category.py (condicional)

src/theaia/database/repositories/
├── reminder_repository.py (condicional)
├── task_repository.py (condicional)
└── category_repository.py (condicional)

alembic/versions/
└── XXX_add_new_models.py (si aplica)

tests/database/
├── test_reminder_model.py (si aplica)
└── test_task_model.py (si aplica)
Progreso 2.1
text
□ Análisis requisitos completado
□ Decisión documentada
□ Modelos creados (si necesarios)
□ Repositories creados (si necesarios)
□ Migraciones aplicadas
□ Tests PASSING
□ Documentation completa

STATUS: ⏳ 0% → 100%
✅ TAREA 2.2: Query Optimization
Objetivo: Optimizar queries que se identificaron como lentas

Subtareas
#	Subtarea	Tests	Prioridad
2.2.1	Full-text search PostgreSQL	2	Alta
2.2.2	Índices compuestos	2	Alta
2.2.3	Connection pooling tuning	2	Alta
2.2.4	Query analysis tools	2	Media
2.2.5	Subqueries optimization	2	Media
TOTAL		10	
Criterios DONE 2.2
text
□ Full-text search PostgreSQL
  ├─ tsvector column añadido a notes table
  ├─ GIN index creado
  ├─ Trigger automático actualización
  ├─ NoteRepository.full_text_search() implementado
  └─ Performance <50ms validado

□ Índices compuestos
  ├─ idx_events_tenant_date_range creado
  ├─ idx_notes_tenant_tags creado
  ├─ idx_events_tenant_location creado (si aplica)
  ├─ EXPLAIN ANALYZE ejecutado
  └─ Improvement documentado

□ Connection pooling optimizado
  ├─ pool_size = 20 (antes 5)
  ├─ max_overflow = 40 (antes 10)
  ├─ pool_recycle = 3600s
  ├─ pool_pre_ping = True
  └─ Performance bajo carga validado

□ Query analysis tools
  ├─ QueryAnalyzer class creada
  ├─ explain_query() method
  ├─ log_slow_queries() configurado
  └─ Threshold 100ms

□ Subqueries optimization
  ├─ N+1 problems identificados y eliminados
  ├─ JOINs en vez de múltiples queries
  ├─ Bulk operations implementadas
  └─ get_events_with_conflicts() optimizado

□ 10/10 tests PASSING
□ Performance ANTES vs DESPUÉS documentado
□ Improvement % calculado
Archivos a Crear/Modificar 2.2
text
alembic/versions/
├── XXX_add_fulltext_search.py
└── XXX_add_composite_indexes.py

src/theaia/database/
├── session.py (modificar - pooling)
└── optimization/
    ├── __init__.py
    ├── query_analyzer.py
    └── performance_monitor.py

src/theaia/database/repositories/
├── note_repository.py (añadir full_text_search)
└── event_repository.py (optimizar queries)

tests/database/
├── test_fulltext_search.py         # 2 tests
├── test_indexes.py                 # 2 tests
├── test_connection_pool.py         # 2 tests
├── test_query_analyzer.py          # 2 tests
└── test_optimization.py            # 2 tests

docs/
└── PERFORMANCE_IMPROVEMENTS.md     # ANTES vs DESPUÉS
Progreso 2.2
text
□ Full-text search implementado y validado
□ Índices compuestos creados y verificados
□ Connection pooling optimizado
□ Query analysis tools creados
□ Subqueries optimizadas
□ 10/10 tests PASSING
□ Performance documentado (ANTES vs DESPUÉS)

STATUS: ⏳ 0% → 100%
✅ TAREA 2.3: JSON Backup/Restore
Objetivo: Sistema disaster recovery completo

Subtareas
#	Subtarea	Tests	Prioridad
2.3.1	JSONExporter class	3	Alta
2.3.2	JSONImporter class	3	Alta
2.3.3	CLI commands	1	Media
TOTAL		7	
Criterios DONE 2.3
text
□ JSONExporter implementado
  ├─ export_full(output_path)
  ├─ export_incremental(since, output_path)
  ├─ export_tenant(tenant_id, output_path)
  ├─ Compresión gzip opcional
  └─ Progress bar para exports grandes

□ JSONImporter implementado
  ├─ import_full(backup_path)
  ├─ import_tenant(backup_path, tenant_id)
  ├─ validate_backup(backup_path) antes de importar
  ├─ Rollback automático si error
  └─ Verificación integridad post-import

□ CLI commands
  ├─ python -m theaia.backup export --full
  ├─ python -m theaia.backup export --tenant=X
  ├─ python -m theaia.backup import --file=backup.json.gz
  ├─ python -m theaia.backup validate --file=backup.json.gz
  └─ --help documentation completa

□ 7/7 tests PASSING
  ├─ test_export_full()
  ├─ test_export_incremental()
  ├─ test_export_tenant()
  ├─ test_import_full_restore()
  ├─ test_import_validation()
  ├─ test_tenant_isolation()
  └─ test_disaster_recovery_complete()

□ Documentation
  ├─ BACKUP_GUIDE.md creado
  ├─ Recovery procedures paso a paso
  └─ Best practices documentadas
Archivos a Crear 2.3
text
src/theaia/database/backup/
├── __init__.py
├── json_exporter.py
├── json_importer.py
└── cli.py

docs/
└── BACKUP_GUIDE.md

tests/database/backup/
├── __init__.py
├── test_exporter.py                # 3 tests
├── test_importer.py                # 3 tests
└── test_cli.py                     # 1 test
Progreso 2.3
text
□ JSONExporter completo
□ JSONImporter completo
□ CLI commands funcionales
□ 7/7 tests PASSING
□ BACKUP_GUIDE.md completo
□ Disaster recovery validado

STATUS: ⏳ 0% → 100%
📊 CHECKPOINT FASE 2
text
╔════════════════════════════════════════════════════════════════╗
║   CHECKPOINT FASE 2: Database Optimization                     ║
╠════════════════════════════════════════════════════════════════╣
║ □ Análisis modelos + decisión documentada ✅                  ║
║ □ Modelos adicionales (si necesarios) ✅                      ║
║ □ Full-text search (<50ms) ✅                                 ║
║ □ Índices compuestos validados ✅                             ║
║ □ Connection pooling (20/40) ✅                               ║
║ □ Query analyzer operativo ✅                                 ║
║ □ Backup/restore completo ✅                                  ║
║                                                                ║
║ □ Tests FASE 2: 25/25 PASSING (100%)                          ║
║ □ Coverage FASE 2: ≥85%                                       ║
║                                                                ║
║ MÉTRICAS VALIDADAS:                                            ║
║ □ Full-text search: <50ms                                     ║
║ □ Búsquedas con índices: <20ms                                ║
║ □ Backup 10,000 registros: <30s                               ║
║ □ Performance improvement: documentado                         ║
║                                                                ║
║ SI TODOS ✓ → CONTINUAR A FASE 3                               ║
╚════════════════════════════════════════════════════════════════╝
🤖 FASE 3: ML/NLP INTEGRATION (20h est.)
Objetivo: Inteligencia básica para agentes

✅ TAREA 3.1: Intent Detector spaCy
Criterios DONE 3.1
text
□ IntentDetectorProduction implementado
□ Custom training con datos H03
□ Confidence thresholds configurados
□ Fallback automático a LLM
□ 8/8 tests PASSING
□ Accuracy ≥92% validada
□ Latency <100ms validada
Progreso 3.1
text
□ IntentDetector completo
□ Training pipeline funcional
□ Thresholds configurados
□ 8/8 tests PASSING
□ Accuracy ≥92%
□ Performance validado

STATUS: ⏳ 0% → 100%
✅ TAREA 3.2: Entity Extractor Advanced
Criterios DONE 3.2
text
□ AdvancedEntityExtractor implementado
□ DateTime extraction (fuzzy matching)
□ Location extraction (ciudades ES)
□ Person extraction (nombres)
□ 7/7 tests PASSING
□ Accuracy ≥90% validada
□ Latency <50ms validada
Progreso 3.2
text
□ AdvancedEntityExtractor completo
□ DateTime fuzzy matching OK
□ Location extraction OK
□ Person extraction OK
□ 7/7 tests PASSING
□ Accuracy ≥90%
□ Performance validado

STATUS: ⏳ 0% → 100%
✅ TAREA 3.3: LLM Integration Simple
Criterios DONE 3.3
text
□ LLMService implementado
□ Cache layer (Redis)
□ Fallback & error handling
□ 5/5 tests PASSING
□ Cache reduciendo costos 30-50%
□ Rate limiting funcional
Progreso 3.3
text
□ LLMService completo
□ Cache layer funcional
□ Fallback implementado
□ 5/5 tests PASSING
□ Cost reduction validado

STATUS: ⏳ 0% → 100%
📊 CHECKPOINT FASE 3
text
╔════════════════════════════════════════════════════════════════╗
║   CHECKPOINT FASE 3: ML/NLP Integration                        ║
╠════════════════════════════════════════════════════════════════╣
║ □ Intent Detector (≥92% accuracy) ✅                          ║
║ □ Entity Extractor (≥90% accuracy) ✅                         ║
║ □ LLM integration (30-50% cost reduction) ✅                  ║
║                                                                ║
║ □ Tests FASE 3: 20/20 PASSING (100%)                          ║
║ □ Coverage FASE 3: ≥85%                                       ║
║                                                                ║
║ MÉTRICAS VALIDADAS:                                            ║
║ □ Intent detection: <100ms                                     ║
║ □ Entity extraction: <50ms                                     ║
║ □ LLM cached: <20ms                                            ║
║ □ LLM uncached: <2s                                            ║
║                                                                ║
║ SI TODOS ✓ → CONTINUAR A FASE 4                               ║
╚════════════════════════════════════════════════════════════════╝
✅ FASE 4: TESTING & QA (15h est.)
Objetivo: Coverage ≥85% y performance validado

✅ TAREA 4.1: E2E Tests
Criterios DONE 4.1
text
□ E2E AgendaAgent v2 (5 tests)
□ E2E NotesAgent v2 (5 tests)
□ E2E EventsAgent (5 tests)
□ E2E QueryAgent v2 (5 tests)
□ 20/20 tests PASSING
□ Todos los flujos validados
Progreso 4.1
text
□ E2E AgendaAgent v2 completo
□ E2E NotesAgent v2 completo
□ E2E EventsAgent completo
□ E2E QueryAgent v2 completo
□ 20/20 tests PASSING

STATUS: ⏳ 0% → 100%
✅ TAREA 4.2: Coverage ≥85%
Criterios DONE 4.2
text
□ Coverage analysis completado
□ Gaps identificados y llenados
□ Coverage ≥85% en TODOS los módulos:
  ├─ agenda_agent_v2/ ≥85%
  ├─ notes_agent_v2/ ≥85%
  ├─ events_agent/ ≥85%
  ├─ query_agent_v2/ ≥85%
  ├─ database/ ≥85%
  └─ ml/ ≥85%
□ 10/10 tests adicionales PASSING
□ Coverage report HTML generado
Progreso 4.2
text
□ Coverage analysis OK
□ Gaps llenados
□ Coverage ≥85% alcanzado
□ 10/10 tests adicionales PASSING
□ Report generado

STATUS: ⏳ 0% → 100%
✅ TAREA 4.3: Performance Benchmarks
Criterios DONE 4.3
text
□ Benchmarks por nivel validados:
  ├─ NIVEL 1: <10ms ✅
  ├─ NIVEL 2: <100ms ✅
  └─ NIVEL 3: <2s ✅
□ Database queries: <50ms ✅
□ Concurrent load (100 req): <5s ✅
□ 5/5 tests PASSING
□ Benchmark report generado
Progreso 4.3
text
□ Benchmarks niveles validados
□ DB performance validado
□ Concurrent load validado
□ 5/5 tests PASSING
□ Report generado

STATUS: ⏳ 0% → 100%
📊 CHECKPOINT FINAL BLOQUE B
text
╔════════════════════════════════════════════════════════════════╗
║   ✨ CHECKPOINT FINAL: BLOQUE B COMPLETADO ✨                 ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║ FASE 1: Agentes Verticales v2                                 ║
║ □ AgendaAgent v2 (15 tests) ✅                                ║
║ □ NotesAgent v2 (15 tests) ✅                                 ║
║ □ EventsAgent (15 tests) ✅                                   ║
║ □ QueryAgent v2 (15 tests) ✅                                 ║
║                                                                ║
║ FASE 2: Database Optimization                                 ║
║ □ Modelos (si necesarios) + decisión ✅                       ║
║ □ Query optimization (10 tests) ✅                            ║
║ □ Backup/restore (7 tests) ✅                                 ║
║                                                                ║
║ FASE 3: ML/NLP Integration                                    ║
║ □ Intent Detector (8 tests) ✅                                ║
║ □ Entity Extractor (7 tests) ✅                               ║
║ □ LLM integration (5 tests) ✅                                ║
║                                                                ║
║ FASE 4: Testing & QA                                          ║
║ □ E2E tests (20 tests) ✅                                     ║
║ □ Coverage ≥85% (10 tests) ✅                                 ║
║ □ Performance benchmarks (5 tests) ✅                         ║
║                                                                ║
╠════════════════════════════════════════════════════════════════╣
║                    TOTALES FINALES                             ║
╠════════════════════════════════════════════════════════════════╣
║ □ Tests PASSING: 80/80 (100%)                                 ║
║ □ Coverage global: ≥85%                                       ║
║ □ Performance validado                                         ║
║ □ Documentation completa                                       ║
║                                                                ║
║ AGENTES TOTALES:                                               ║
║ - Sistema (H03): 8 agentes ✅                                 ║
║ - Verticales v2 (H04-H05): 4 agentes ✅                       ║
║ = TOTAL: 12 agentes funcionales                               ║
║                                                                ║
║ SI TODOS ✓ → BLOQUE B COMPLETADO ✅                           ║
║ PRÓXIMO: BLOQUE C (H06+H07) - Cuando iniciemos               ║
╚════════════════════════════════════════════════════════════════╝
🎊 ENTREGABLES FINALES
text
✅ 4 Agentes Verticales v2 (nuevos/mejorados)
   ├─ AgendaAgent v2 (mejora v1)
   ├─ NotesAgent v2 (mejora NoteAgent)
   ├─ EventsAgent (nuevo robusto)
   └─ QueryAgent v2 (nuevo)

✅ Database Optimizada
   ├─ Modelos adicionales (si necesarios)
   ├─ Full-text search PostgreSQL
   ├─ Índices compuestos
   ├─ Connection pooling optimizado
   └─ Backup/restore completo

✅ ML/NLP Básico
   ├─ Intent Detector (≥92%)
   ├─ Entity Extractor (≥90%)
   └─ LLM integration + cache

✅ Testing Completo
   ├─ 80 tests PASSING
   ├─ Coverage ≥85%
   ├─ E2E validado
   └─ Performance benchmarked

✅ Documentation
   ├─ README por agente
   ├─ DECISION.md (modelos DB)
   ├─ BACKUP_GUIDE.md
   └─ PERFORMANCE_IMPROVEMENTS.md
NOTAS FINALES:

✅ Agentes completos: 12 total (8 sistema H03 + 4 verticales v2 H04-H05)

✅ Database completa: Base H02 + optimizaciones H04-H05

✅ Sin timeline rígido: Horas son orientativas, trabajamos a ritmo flexible

✅ Checklist flexible: Marcamos según completemos, sin presión horaria

✅ Calidad > Velocidad: Priorizamos hacer bien vs. hacer rápido

Última actualización: 25 Noviembre 2025, 16:55 CET
Versión: v2.0.0 REVISADO (sin timeline rígido)
Status: ✅ READY TO START - Cuando estés listo