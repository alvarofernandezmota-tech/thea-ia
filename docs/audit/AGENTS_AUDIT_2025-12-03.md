# 🔍 AUDITORÍA COMPLETA SISTEMA AGENTES - THEA IA

**Fecha:** 03 Diciembre 2025  
**Versión:** 1.0  
**Auditor:** Equipo THEA IA (Perplexity AI + Lead Developer)  
**Objetivo:** Analizar estado actual de 8 agentes para definir roadmap MVP

---

## 📊 RESUMEN EJECUTIVO

### Agentes Analizados: 8

| Categoría | Cantidad | Agentes |
|-----------|----------|---------|
| **MVP (implementar)** | 5 | AgendaAgent, NoteAgent, ReminderAgent, QueryAgent, HelpFallbackAgent |
| **Eliminar/Merger** | 2 | EventAgent_NEW, ScheduleAgent |
| **Post-MVP** | 1 | MilestoneAgent |

### Decisiones Tomadas: 8

- 🔴 **REFACTOR:** 3 agentes (AgendaAgent, ReminderAgent, QueryAgent)
- 🔴 **CREATE NEW:** 1 agente (NoteAgent)
- 🔵 **MERGE:** 2 agentes (Help+Fallback → HelpFallbackAgent, EventAgent_NEW → AgendaAgent)
- 🟢 **ARCHIVADO:** 1 agente (ScheduleAgent - mantener archivado)
- 🟡 **POST-MVP:** 1 agente (MilestoneAgent)

### Hallazgos Clave

- ⚠️ **92% código muerto** en AgendaAgent y NoteAgent (8% coverage)
- ⚠️ **0% coverage** en 4 FSMs (nunca se ejecutan)
- ❌ **Ningún agente persiste en BD** (todos simulan)
- ⚠️ **Overlap crítico** EventAgent_NEW duplica AgendaAgent 100%
- ✅ **78 tests PASSING** en AgendaAgent (base sólida)

---

## 🎯 MATRIZ DE DECISIONES COMPLETA

| Agente | LOC Handler | LOC FSM | Coverage | Repo | ML | Tests | MVP? | Decisión | Prioridad |
|--------|-------------|---------|----------|------|----|-------|------|----------|-----------|
| **AgendaAgent** | 392 | 85 | 8% / 39% | ❌ NO | ⚠️ Parcial | ✅ 78 | ✅ SÍ | 🔴 REFACTOR | P0 |
| **NoteAgent** | 392 | 85 | 8% / 39% | ✅ SÍ | ⚠️ Parcial | ✅ 47 | ✅ SÍ | 🔴 CREATE NEW | P0 |
| **ReminderAgent** | 40 | 82 | 54% / 39% | ❌ NO | ❌ NO | ✅ 15 | ✅ SÍ | 🔴 REFACTOR | P0 |
| **QueryAgent** | 12 | 26 | 50% / 0% | ❌ NO | ❌ NO | ✅ 19 | ✅ SÍ | 🔴 REFACTOR | P1 |
| **HelpAgent** | 12 | 41 | 50% / 0% | ❌ NO | ❌ NO | ✅ 18 | ✅ SÍ | 🔵 MERGE | P1 |
| **FallbackAgent** | 16 | 36 | 50% / 0% | ❌ NO | ❌ NO | ❓ | ✅ SÍ | 🔵 MERGE | P1 |
| **EventAgent_NEW** | 52 | 210 | 0% / 0% | ❌ NO | ✅ SÍ | ❓ | ❌ NO | 🔴 DELETE | - |
| **ScheduleAgent** | N/A | 140 | ❓ | ❌ NO | ❌ NO | ✅ | ❌ NO | 🟢 ARCHIVADO | - |
| **MilestoneAgent** | N/A | N/A | N/A | N/A | N/A | N/A | ❌ NO | 🟡 POST-MVP | - |

**Leyenda:**
- P0 = Prioridad crítica MVP
- P1 = Prioridad alta MVP
- Coverage = Handler / FSM

---

## 📋 ANÁLISIS DETALLADO POR AGENTE

### 1. AgendaAgent ✅ MVP

**Estado Actual:**
- **LOC:** 392 (handler) + 85 (FSM) = 477 LOC total
- **Coverage:** 8% handler, 39% FSM
- **Código muerto:** 360/392 líneas handler (92%)
- **Tests:** 78/78 PASSING ✅
- **Repository:** ❌ NO conectado (simula guardado)
- **ML Integration:** ⚠️ Parcial (Entity extractors, NO Intent detector)

**Funcionalidad:**
- ✅ FSM conversacional (78 tests lo confirman)
- ✅ ML Entity extraction (fechas, ubicaciones)
- ❌ NO persiste en BD (EventRepository NO usado)
- ❌ Intent detection hardcoded

**Problemas:**
1. 92% código muerto (360 líneas sin ejecutar)
2. NO persiste eventos (solo simula)
3. NO usa EventRepository
4. NO usa Intent Detector ML

**Decisión:** 🔴 **REFACTOR COMPLETO**

**Plan FASE 3:**
Target: 200-250 LOC (vs 392 actual)
class AgendaAgent(BaseAgent):
def init(self):
self.intent_detector = IntentDetector() # ✅ NEW
self.entity_extractor = EntityExtractor()
self.event_repository = EventRepository(session) # ✅ NEW
self.fsm_instances = {}

text
async def handle(self, user_id, message, context):
    # 1. Intent detection ML
    intent = self.intent_detector.detect(message)
    
    # 2. Entity extraction
    entities = self.entity_extractor.extract(message)
    
    # 3. Router ML-driven
    if intent == 'create_event':
        return await self._handle_create_event(...)
    
    # 4. Guardar en BD REAL
    event = await self.event_repository.create({...})
text

**Mantener:**
- ✅ FSM conversacional (funciona)
- ✅ 78 tests (regression suite)
- ✅ ML Entity extraction

**Añadir:**
- ✅ EventRepository connection
- ✅ Intent Detector ML
- ✅ FSM BaseStateMachine herencia
- ✅ 8 tests nuevos (E2E con BD)

**Target:** Coverage 8% → 85%+

---

### 2. NoteAgent ✅ MVP

**Estado Actual:**
- **LOC:** 392 (handler) + 85 (FSM) = 477 LOC total
- **Coverage:** 8% handler, 39% FSM
- **Código muerto:** 360/392 líneas handler (92%)
- **Tests:** 47/47 PASSING ✅
- **Repository:** ✅ SÍ conectado (NoteRepository)
- **ML Integration:** ⚠️ Parcial (Entity extractors, NO Intent detector)

**Funcionalidad:**
- ✅ FSM conversacional
- ✅ ML Entity extraction (personas, ubicaciones)
- ✅ NoteRepository CONECTADO (mejor que AgendaAgent)
- ✅ CRUD completo (create/list/search/edit/delete/pin)
- ❌ Intent detection hardcoded

**Paradoja:**
- ✅ Repository conectado (mejor que Agenda)
- ✅ CRUD completo (mejor que Agenda)
- ⚠️ Pero 92% código NO se ejecuta

**Decisión:** 🔴 **CREATE NEW (reescribir desde cero)**

**Razón:** Aunque tiene Repository, 92% código muerto indica implementación ineficiente.

**Plan FASE 3:**
Target: 200-250 LOC (vs 392 actual)
class NoteAgent(BaseAgent):
def init(self):
self.intent_detector = IntentDetector() # ✅ NEW
self.entity_extractor = EntityExtractor()
self.note_repository = NoteRepository(session) # ✅ MANTENER
self.fsm_instances = {}

text
async def handle(self, user_id, message, context):
    # Intent detection ML (NO hardcoded)
    intent = self.intent_detector.detect(message)
    
    # Router ML-driven
    if intent == 'create_note':
        return await self._handle_create_note(...)
    elif intent == 'search_notes':
        return await self._handle_search_notes(...)
text

**Mantener:**
- ✅ NoteRepository connection
- ✅ CRUD completo
- ✅ 47 tests (regression)

**Añadir:**
- ✅ Intent Detector ML
- ✅ FSM BaseStateMachine
- ✅ Simplificar handler (392 → 200-250 LOC)
- ✅ 8 tests nuevos

**Target:** Coverage 8% → 85%+

---

### 3. ReminderAgent ✅ MVP

**Estado Actual:**
- **LOC:** 40 (handler stub) + 82 (FSM) = 122 LOC total
- **Coverage:** 54% handler, 39% FSM
- **Tests:** 15/15 PASSING ✅
- **Repository:** ❌ NO conectado
- **ML Integration:** ❌ NO

**Funcionalidad:**
- ⚠️ Handler STUB (delega a ConversationManager)
- ✅ FSM 17 estados definidos
- ⚠️ Solo flujo CREATE implementado (60% falta)
- ❌ NO guarda en BD
- ❌ NO usa ML

**Decisión:** 🔴 **REFACTOR COMPLETO**

**Razón:** ReminderAgent SÍ entra en MVP (recordatorios = feature core)

**Plan FASE 3:**
Target: 180-200 LOC
class ReminderAgent(BaseAgent):
def init(self):
self.intent_detector = IntentDetector()
self.entity_extractor = EntityExtractor()
self.reminder_repository = ReminderRepository(session) # ✅ NEW
self.fsm_instances = {}

text
async def handle(self, user_id, message, context):
    intent = self.intent_detector.detect(message)
    
    if intent == 'create_reminder':
        return await self._handle_create_reminder(...)
    elif intent == 'list_reminders':
        return await self._handle_list_reminders(...)
    elif intent == 'complete_reminder':
        return await self._handle_complete_reminder(...)
text

**Implementar:**
- ✅ ReminderRepository connection
- ✅ CRUD completo (create/list/complete/delete)
- ✅ Intent Detector ML
- ✅ FSM BaseStateMachine
- ✅ 8 tests nuevos

**Diferencia vs EventAgent proactivo:**
- **ReminderAgent** = Conversacional (usuario crea/gestiona)
- **EventAgent proactivo (FASE 3)** = Background (envía push notifications)

**Target:** Coverage 54%/39% → 85%+

---

### 4. QueryAgent ✅ MVP

**Estado Actual:**
- **LOC:** 12 (handler stub) + 26 (FSM placeholder) = 38 LOC total
- **Coverage:** 50% handler, 0% FSM ❌
- **Tests:** 19/19 PASSING ✅
- **Repository:** ❌ NO conectado
- **ML Integration:** ❌ NO

**Funcionalidad:**
- ⚠️ Handler STUB (delega a ConversationManager)
- ❌ FSM 0% coverage = NUNCA SE EJECUTA
- ❌ `_process_query()` retorna PLACEHOLDER
- ❌ NO implementa cross-domain search
- ❌ NO implementa cache strategy
- ❌ NO usa repositories

**Estado:** QueryAgent es **ESQUELETO VACÍO**

**Decisión:** 🔴 **REFACTOR COMPLETO (casi CREATE NEW)**

**Plan FASE 3:**
Target: 200-250 LOC
class QueryAgent(BaseAgent):
def init(self):
self.intent_detector = IntentDetector()
self.entity_extractor = EntityExtractor()

text
    # Repositories (cross-domain)
    self.event_repository = EventRepository(session)
    self.note_repository = NoteRepository(session)
    self.query_cache_repository = QueryCacheRepository(session)
    
    self.fsm_instances = {}

async def handle(self, user_id, message, context):
    # 1. Check cache FIRST
    query_hash = sha256(message).hexdigest()
    cached = await self.query_cache_repository.get_cached(user_id, query_hash)
    if cached and not cached.expired:
        return cached.result, "idle", context
    
    # 2. Intent detection
    intent = self.intent_detector.detect(message)
    
    # 3. Cross-domain search
    if intent == 'search_events':
        result = await self._search_events(user_id, entities)
    elif intent == 'search_notes':
        result = await self._search_notes(user_id, entities)
    elif intent == 'cross_domain_search':
        result = await self._search_cross_domain(user_id, message)
    elif intent == 'daily_summary':
        result = await self._generate_daily_summary(user_id)
    
    # 4. Cache result
    await self.query_cache_repository.set_cache(user_id, message, result, ttl=3600)
    
    return result, "idle", context
text

**Implementar desde cero:**
- ✅ Cross-domain search (eventos + notas)
- ✅ Cache strategy (QueryCacheRepository)
- ✅ Daily/weekly summary
- ✅ Full-text search
- ✅ Parallel search (asyncio.gather)
- ✅ 8 tests nuevos

**Target:** Handler 12 → 200-250 LOC, Coverage 0%/50% → 85%+

---

### 5. HelpAgent + FallbackAgent → HelpFallbackAgent ✅ MVP

**Estado Actual HelpAgent:**
- **LOC:** 12 (handler stub) + 41 (FSM) = 53 LOC
- **Coverage:** 50% handler, 0% FSM ❌
- **Tests:** 18/18 PASSING ✅
- **Help topics:** 6 hardcoded

**Estado Actual FallbackAgent:**
- **LOC:** 16 (handler stub) + 36 (FSM) = 52 LOC
- **Coverage:** 50% handler, 0% FSM ❌
- **Funcionalidad:** Respuesta genérica hardcoded

**Problemas:**
- ❌ Help topics hardcoded (no dinámicos)
- ❌ Keyword matching (no ML)
- ❌ Fallback NO sugiere correcciones
- ❌ NO persiste fallbacks (analytics)
- ❌ 0% coverage FSMs

**Decisión:** 🔵 **MERGE → HelpFallbackAgent**

**Plan FASE 3:**
Target: 250-300 LOC total
class HelpFallbackAgent(BaseAgent):
def init(self):
self.intent_detector = IntentDetector()
self.agent_registry = AgentRegistry.get_all()
self.fallback_logger = FallbackLogger() # NEW

text
async def handle(self, user_id, message, context):
    intent = self.intent_detector.detect(message)
    
    if intent == 'help_general':
        return self._generate_general_help()
    
    elif intent == 'help_specific':
        agent_name = self._extract_agent_name(message)
        return self._generate_agent_help(agent_name)
    
    elif intent == 'fallback':
        # Log fallback
        await self.fallback_logger.log({
            'user_id': user_id,
            'message': message,
            'timestamp': datetime.now()
        })
        
        # Fuzzy matching
        suggestions = self._suggest_intents(message)
        
        if suggestions:
            return f"No entendí '{message}'. ¿Quisiste decir?\n{suggestions}"
        else:
            return "No he entendido. Escribe 'ayuda' para ver comandos."

def _generate_general_help(self):
    """Help dinámico desde AgentRegistry."""
    help_text = "**🤖 Thea IA - Ayuda**\n\n"
    
    for agent in self.agent_registry:
        intents = agent.get_supported_intents()
        help_text += f"**{agent.name}:**\n"
        help_text += f"- Comandos: {', '.join(intents[:3])}\n\n"
    
    return help_text

def _suggest_intents(self, message):
    """Fuzzy matching para sugerir intents."""
    all_intents = []
    
    for agent in self.agent_registry:
        for intent in agent.get_supported_intents():
            score = self._fuzzy_score(message, intent)
            if score > 0.5:
                all_intents.append({
                    'intent': intent,
                    'confidence': score
                })
    
    return sorted(all_intents, key=lambda x: x['confidence'], reverse=True)[:3]
text

**Implementar:**
- ✅ Help dinámico (AgentRegistry)
- ✅ Fallback inteligente (fuzzy matching)
- ✅ FallbackLogger (analytics)
- ✅ Intent suggestions (confidence scores)
- ✅ 8 tests nuevos

**Target:** Coverage 50%/0% → 85%+

---

### 6. EventAgent_NEW ❌ NO MVP

**Estado Actual:**
- **LOC:** 52 (handler) + 332 (conversation manager) + 210 (FSM) = 594 LOC
- **Coverage:** 0% TODO ❌
- **Tests:** ❓
- **Repository:** ❌ NO conectado
- **ML Integration:** ✅ SÍ (DateTime + Location extractors)

**Funcionalidad:**
- ✅ ML Integration (mejor que AgendaAgent)
- ✅ Flujo CREATE conversacional
- ⚠️ EventFSM NUNCA SE USA (conversation manager duplica lógica)
- ❌ NO persiste eventos

**Problema CRÍTICO:** 🔴 **OVERLAP 100% con AgendaAgent**

| Funcionalidad | EventAgent_NEW | AgendaAgent | Overlap |
|---------------|----------------|-------------|---------|
| Crear eventos | ✅ | ✅ | 🔴 100% |
| Fecha/hora/ubicación | ✅ | ✅ | 🔴 100% |
| Lista eventos | ❌ | ✅ | - |
| Edita eventos | ❌ | ✅ | - |

**Decisión:** 🔴 **DELETE + MERGE → AgendaAgent**

**Razón:** Mantener 2 agentes que crean eventos = confusión arquitectura

**Plan FASE 3:**
AgendaAgent absorbe intents de EventAgent_NEW
class AgendaAgent:
def get_supported_intents(self):
return [
# Original
"crear_cita",
"agendar",
"agenda",
# FROM EventAgent_NEW
"crear_evento", # NEW
"evento", # NEW
"calendario", # NEW
]

text

**Acción:**
- 🔴 DELETE `src/theaia/agents/event_agent_new/`
- ✅ MERGE intents → AgendaAgent
- ✅ MANTENER ML extractors (ya en Agenda)

**EventAgent FASE 3 = Scheduler proactivo (NO conversacional)**

---

### 7. ScheduleAgent ❌ NO MVP (ARCHIVADO)

**Estado Actual:**
- **Ubicación:** `.archive/schedule_agent/`
- **LOC:** 29 (conversation manager) + 140 (FSM) = 169 LOC
- **Coverage:** ❓
- **Tests:** ✅ Existen
- **Status README:** "✅ Producción" (MENTIRA)

**Funcionalidad:**
- ⚠️ Keyword matching hardcoded
- ❌ TODAS las funciones retornan PLACEHOLDERS fake

**Análisis funcionalidad:**

| Feature | Implementación | Overlap |
|---------|----------------|---------|
| Consultar horario | PLACEHOLDER | AgendaAgent 100% |
| Agregar eventos | PLACEHOLDER | AgendaAgent 100% |
| Eliminar eventos | PLACEHOLDER | AgendaAgent 100% |
| Optimizar agenda | FAKE (texto hardcoded) | Nadie |
| Tiempo libre | FAKE (texto hardcoded) | Nadie |
| Priorizar tareas | FAKE (texto hardcoded) | Nadie |

**Decisión:** 🟢 **MANTENER ARCHIVADO**

**Razón archivo:**
1. Overlap 100% con AgendaAgent (CRUD eventos)
2. Funcionalidad "avanzada" son placeholders fake
3. No justifica agente separado
4. Features "inteligentes" → FASE 4 (IA avanzada)

**Acción:** NO restaurar, mantener en `.archive/`

---

### 8. MilestoneAgent ❌ NO MVP (POST-MVP)

**Estado Actual:**
- **Ubicación:** ❌ NO EXISTE (ni src/ ni .archive/)
- **Status:** POSTPONIDO

**Funcionalidad planeada:**
- Gestión de HITOS a largo plazo
- Tracking de objetivos mensuales/anuales
- Progress tracking
- Analytics avanzado

**Decisión:** 🟡 **POST-MVP (NO implementar ahora)**

**Razón:**
- NO es feature CORE para MVP
- MVP requiere: Agenda, Notas, Recordatorios
- Hitos = funcionalidad avanzada
- Implementar en versión futura

**Acción:** NO implementar en FASE 2/3

---

## 🗺️ ROADMAP IMPLEMENTACIÓN

### FASE 2: Modelos Base de Datos (H04-H05)

**Objetivo:** Crear modelos SQLAlchemy + repositories

**Modelos a crear:**

1. Event (para AgendaAgent)
class Event(Base):
id, user_id, tenant_id
title, start_datetime, end_datetime
location, description
created_at, updated_at

2. Note (para NoteAgent)
class Note(Base):
id, user_id, tenant_id
title, content, category
tags (ARRAY), is_pinned
created_at, updated_at

3. Reminder (para ReminderAgent)
class Reminder(Base):
id, user_id, tenant_id
title, trigger_time
completed, sent
event_id (FK Event, nullable)
created_at, updated_at

4. QueryCache (para QueryAgent)
class QueryCache(Base):
id, user_id, tenant_id
query_hash, query_text
result (JSONB), cached_at
expires_at, hit_count

text

**Repositories a crear:**

class EventRepository(BaseRepository):
async def create(...)
async def get_by_id(...)
async def get_by_user(...)
async def get_by_date_range(...)
async def search(...)
async def update(...)
async def delete(...)

class NoteRepository(BaseRepository):
async def create(...)
async def get_by_id(...)
async def get_by_user(...)
async def search_by_tags(...)
async def full_text_search(...)
async def update(...)
async def delete(...)

class ReminderRepository(BaseRepository):
async def create(...)
async def get_pending(...)
async def mark_completed(...)
async def mark_sent(...)
async def delete(...)

class QueryCacheRepository(BaseRepository):
async def get_cached(...)
async def set_cache(...)
async def invalidate(...)
async def get_hit_stats(...)

text

**Tests:**
- 8 tests por repository (≥85% coverage)
- E2E tests con BD real
- Multi-tenant isolation tests

**Duración estimada:** H04-H05 (2 hitos)

---

### FASE 3: Refactor Agentes (H06-H10)

#### Bloque 3.1: AgendaAgent REFACTOR (H06)

**Tareas:**
1. Conectar EventRepository REAL
2. Implementar Intent Detector ML
3. Refactorizar handler (392 → 200-250 LOC)
4. FSM hereda BaseStateMachine
5. Añadir 8 tests nuevos (E2E con BD)

**Entregables:**
- ✅ Handler refactorizado
- ✅ EventRepository conectado
- ✅ Coverage 8% → 85%+
- ✅ 86 tests PASSING (78 + 8 nuevos)

**Duración:** 1 hito

---

#### Bloque 3.2: NoteAgent CREATE NEW (H07)

**Tareas:**
1. Crear handler NUEVO (200-250 LOC)
2. Conectar NoteRepository
3. Implementar Intent Detector ML
4. FSM BaseStateMachine
5. Añadir 8 tests nuevos

**Entregables:**
- ✅ Handler nuevo simplificado
- ✅ NoteRepository conectado
- ✅ Coverage 8% → 85%+
- ✅ 55 tests PASSING (47 + 8 nuevos)

**Duración:** 1 hito

---

#### Bloque 3.3: ReminderAgent REFACTOR (H08)

**Tareas:**
1. Crear handler completo (180-200 LOC)
2. Conectar ReminderRepository
3. Implementar Intent Detector ML
4. FSM BaseStateMachine
5. CRUD completo
6. Añadir 8 tests nuevos

**Entregables:**
- ✅ Handler completo
- ✅ ReminderRepository conectado
- ✅ Coverage 54%/39% → 85%+
- ✅ 23 tests PASSING (15 + 8 nuevos)

**Duración:** 1 hito

---

#### Bloque 3.4: QueryAgent REFACTOR (H09)

**Tareas:**
1. Crear handler NUEVO (200-250 LOC)
2. Conectar 3 repositories (Event, Note, QueryCache)
3. Implementar cross-domain search
4. Cache strategy
5. Daily/weekly summary
6. Añadir 8 tests nuevos

**Entregables:**
- ✅ Handler funcional completo
- ✅ Cross-domain search operativo
- ✅ Cache strategy implementado
- ✅ Coverage 0%/50% → 85%+
- ✅ 27 tests PASSING (19 + 8 nuevos)

**Duración:** 1 hito

---

#### Bloque 3.5: HelpFallbackAgent MERGE (H10)

**Tareas:**
1. Crear HelpFallbackAgent (250-300 LOC)
2. Help dinámico (AgentRegistry)
3. Fallback inteligente (fuzzy matching)
4. FallbackLogger
5. Añadir 8 tests nuevos

**Entregables:**
- ✅ Macro-agente operativo
- ✅ Help dinámico desde registry
- ✅ Fallback con suggestions
- ✅ Coverage 50%/0% → 85%+
- ✅ 26 tests PASSING (18 + 8 nuevos)

**Duración:** 1 hito

---

#### Bloque 3.6: Cleanup (H10)

**Tareas:**
1. DELETE `src/theaia/agents/event_agent_new/`
2. Verificar ScheduleAgent archivado
3. Actualizar documentación
4. Regression tests (217 tests totales)

**Duración:** Incluido en H10

---

### FASE 4: EventAgent Proactivo (POST-MVP)

**Objetivo:** Scheduler background para notificaciones push

class EventAgent:
"""
Agente proactivo NO conversacional.
Scheduler background para enviar recordatorios.
"""

text
async def run_scheduler(self):
    while True:
        await asyncio.sleep(60)  # Check cada 60s
        await self._check_and_send_reminders()

async def _check_and_send_reminders(self):
    reminders = await reminder_repo.get_pending(
        before_time=now() + timedelta(minutes=15)
    )
    
    for reminder in reminders:
        if not await self._is_quiet_time(user_id):
            await telegram_adapter.send_message(
                user_id,
                f"🔔 Recordatorio: {reminder.title} en 15 min"
            )
            await reminder_repo.mark_sent(reminder.id)
text

**Features:**
- ✅ Scheduler background (asyncio)
- ✅ Push notifications (Telegram)
- ✅ Quiet hours support
- ✅ Snooze functionality
- ✅ Recurrent reminders

**Duración:** POST-MVP

---

## 📈 MÉTRICAS ÉXITO MVP

### Coverage Targets

| Agente | Actual | Target | Delta |
|--------|--------|--------|-------|
| AgendaAgent | 8% / 39% | 85%+ | +77% / +46% |
| NoteAgent | 8% / 39% | 85%+ | +77% / +46% |
| ReminderAgent | 54% / 39% | 85%+ | +31% / +46% |
| QueryAgent | 50% / 0% | 85%+ | +35% / +85% |
| HelpFallbackAgent | 50% / 0% | 85%+ | +35% / +85% |

**Target global:** ≥85% coverage en 5 agentes MVP

---

### Tests Targets

| Agente | Tests Actual | Tests Target | Delta |
|--------|--------------|--------------|-------|
| AgendaAgent | 78 | 86 | +8 |
| NoteAgent | 47 | 55 | +8 |
| ReminderAgent | 15 | 23 | +8 |
| QueryAgent | 19 | 27 | +8 |
| HelpFallbackAgent | 18 | 26 | +8 |
| **TOTAL** | **177** | **217** | **+40** |

**Target global:** 217 tests PASSING

---

### LOC Reduction

| Agente | LOC Actual | LOC Target | Reducción |
|--------|------------|------------|-----------|
| AgendaAgent | 477 | 300-350 | -27% a -37% |
| NoteAgent | 477 | 300-350 | -27% a -37% |
| ReminderAgent | 122 | 180-200 | +48% a +64% |
| QueryAgent | 38 | 200-250 | +426% a +558% |
| HelpFallbackAgent | 105 | 250-300 | +138% a +186% |

**Nota:** Reducción LOC en Agenda/Note = código más eficiente (menos código muerto)

---

## 🎯 CONCLUSIONES

### Hallazgos Críticos

1. **92% código muerto** en 2 agentes principales (Agenda, Note)
   - Requiere reescritura urgente
   - Coverage 8% indica implementación ineficiente

2. **0% coverage en 4 FSMs**
   - FSMs NUNCA SE EJECUTAN
   - ConversationManagers duplican lógica FSM
   - Decisión: Usar FSM REAL o eliminar

3. **Ningún agente persiste en BD**
   - Todos simulan guardado
   - FASE 2 crítica (repositories)

4. **Overlap crítico EventAgent_NEW**
   - Duplica AgendaAgent 100%
   - Requiere DELETE inmediato

5. **Tests sólidos como base**
   - 177 tests PASSING
   - Excelente base para refactor
   - Target +40 tests = 217 total

---

### Arquitectura MVP Final

**5 agentes conversacionales:**

AgendaAgent → Eventos/citas calendario

NoteAgent → Notas rápidas

ReminderAgent → Recordatorios simples

QueryAgent → Búsqueda cross-domain + cache

HelpFallbackAgent → Help dinámico + fallback inteligente

text

**1 agente proactivo (FASE 4):**

EventAgent → Scheduler background (push notifications)

text

---

### Roadmap Resumen

| Fase | Duración | Entregables |
|------|----------|-------------|
| **FASE 2 (BD)** | H04-H05 (2 hitos) | 4 modelos, 4 repositories, tests |
| **FASE 3 (Agentes)** | H06-H10 (5 hitos) | 5 agentes refactorizados, 217 tests |
| **FASE 4 (Proactivo)** | POST-MVP | EventAgent scheduler |

**Total MVP:** 7 hitos (H04-H10)

---

### Próximos Pasos Inmediatos

1. ✅ Aprobar auditoría
2. ✅ Iniciar FASE 2 (H04)
3. ✅ Crear modelos SQLAlchemy
4. ✅ Implementar repositories
5. ✅ Tests E2E con BD real

---

## 📝 APÉNDICES

### A. Definiciones

- **REFACTOR:** Mantener estructura, mejorar implementación
- **CREATE NEW:** Reescribir desde cero
- **MERGE:** Fusionar 2+ agentes en uno
- **DELETE:** Eliminar agente completo
- **ARCHIVADO:** Mover a `.archive/` (mantener histórico)
- **POST-MVP:** Implementar después de MVP

---

### B. Referencias

- Coverage report: `coverage.txt`
- Tests: `src/theaia/tests/`
- Agentes: `src/theaia/agents/`
- Archivo: `.archive/`

---

### C. Equipo

**Auditor:** Perplexity AI + Lead Developer  
**Fecha auditoría:** 03 Diciembre 2025  
**Duración auditoría:** 1 sesión (análisis 8 agentes)  
**Líneas código analizadas:** ~2,500 LOC

---

**FIN AUDITORÍA**

---

*Documento generado automáticamente por sistema de auditoría THEA IA v1.0*
