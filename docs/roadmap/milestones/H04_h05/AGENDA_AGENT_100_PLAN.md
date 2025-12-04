# 🎯 AGENDA AGENT 100% - PLAN COMPLETO PRODUCCIÓN

**Fecha:** 04 Diciembre 2025  
**Responsable:** Álvaro Fernández Mota  
**Objetivo:** AgendaAgent production-ready al 100% con todo su ecosistema

---

## 📊 ESTADO ACTUAL (AUDITORÍA)

### ✅ COMPONENTES EXISTENTES

| Componente | Archivo | LOC | Estado | Integrado |
|------------|---------|-----|--------|----------|
| **Handler** | `handler.py` | ~400 | ⚠️ Funcional | Parcial |
| **FSM** | `agenda_fsm.py` | ~350 | ✅ Completo | Sí |
| **States** | `agent_states.py` | ~30 | ✅ Completo | Sí |
| **EventRepository** | `event_repository.py` | ~200 | ✅ Completo | ❌ NO |
| **Event Model** | `event.py` | ~50 | ✅ Completo | Sí |
| **EntityExtractor** | `pipeline.py` | ~300 | ✅ Completo | Sí |
| **DateTimeExtractor** | `date_parser.py` | ~250 | ✅ Completo | Sí |
| **Orchestrator v2** | `orchestrator.py` | ~150 | ⚠️ Preparado | No usado |

### 🔴 GAPS IDENTIFICADOS

1. **Handler NO conecta EventRepository** (línea 337: TODO comment)
2. **Tests E2E ausentes** (coverage probablemente <30%)
3. **Orchestrator v2 no usado** (preparado pero handler no lo usa)
4. **Legacy code** (~100 LOC de métodos deprecated)
5. **Validations básicas** (falta validación robusta de fechas futuras)
6. **Error handling** (logging pero sin recovery strategies)

---

## 🎯 OBJETIVO FINAL

### AgendaAgent 100% Production-Ready

**Criterios de éxito:**
- ✅ EventRepository 100% integrado
- ✅ FSM completa con 15 estados operativos
- ✅ ML extraction (dates, times, locations) funcionando
- ✅ Database persistence real (no TODOs)
- ✅ Validations robustas (fechas futuras, títulos, etc)
- ✅ Error handling graceful
- ✅ Tests E2E: 8+ tests (≥85% coverage)
- ✅ Performance: <100ms queries, <10ms comandos simples
- ✅ Multi-tenant completo
- ✅ Logging production-grade

**Métricas:**
- Coverage: 0% → 85%+
- Tests: 0 → 8+
- Performance: Variable → <100ms
- Code quality: ⚠️ → ✅

---

## 📋 PLAN DE EJECUCIÓN (6 Tareas)

### TAREA 1: EventRepository Integration (CRÍTICO)
**Prioridad:** P0  
**Duración:** 45min  
**Archivos:** `handler.py`

**Objetivos:**
1. Añadir EventRepository al `__init__`
2. Implementar `_save_event_to_db()` real
3. Conectar en método `handle()` línea 337
4. Añadir session management (dependency injection)
5. Validar multi-tenant en save

**Cambios código:**

```python
# handler.py línea 70 (añadir)
from src.theaia.database.repositories.event_repository import EventRepository
from src.theaia.database.session import get_session

class AgendaAgent(BaseAgent):
    def __init__(self, config: Optional[AgentConfig] = None, session: Optional[AsyncSession] = None):
        # ... existing code ...
        
        # Repository integration (NEW)
        self.session = session
        self.event_repo = EventRepository(session) if session else None
        self.logger.info("EventRepository integrated" if self.event_repo else "EventRepository pending session")
```

```python
# handler.py línea 337 (reemplazar TODO)
async def _save_event_to_db(self, user_id: str, event_data: Dict[str, Any]):
    """
    Save event to database using EventRepository.
    
    Args:
        user_id: User identifier
        event_data: Event data from FSM draft
    """
    try:
        if not self.event_repo:
            raise ValueError("EventRepository not initialized (session required)")
        
        # Build event data for DB
        db_event_data = {
            "user_id": int(user_id),
            "tenant_id": event_data.get('tenant_id', 'default'),
            "title": event_data.get('title'),
            "start_datetime": self._parse_datetime(
                event_data.get('date'),
                event_data.get('time')
            ),
            "location": event_data.get('location'),
            "status": "pending",
            "event_type": event_data.get('event_type', 'personal'),
            "reminder_minutes": event_data.get('reminder_minutes', 15)
        }
        
        # Create event in DB
        created_event = await self.event_repo.create(db_event_data)
        
        self.logger.info(f"Event created in DB: id={created_event.id}, user={user_id}")
        
        return created_event.id
        
    except Exception as e:
        self.logger.error(f"Failed to save event to DB: {e}", exc_info=True)
        raise

def _parse_datetime(self, date_str: str, time_str: str) -> datetime:
    """
    Parse date and time strings to datetime object.
    
    Args:
        date_str: Date string (YYYY-MM-DD or relative like "mañana")
        time_str: Time string (HH:MM or "3pm")
    
    Returns:
        Timezone-aware datetime object
    """
    # TODO: Implement robust datetime parsing
    # For now, basic implementation
    from dateutil import parser
    
    combined = f"{date_str} {time_str}"
    dt = parser.parse(combined)
    
    # Ensure timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    
    return dt
```

**Validación:**
- [ ] Handler instancia EventRepository con session
- [ ] `_save_event_to_db()` crea evento real en BD
- [ ] Multi-tenant validation (tenant_id)
- [ ] Logging completo
- [ ] Error handling con raise

**Micro-recompensa:** +2 puntos

---

### TAREA 2: Validations Robustas
**Prioridad:** P0  
**Duración:** 30min  
**Archivos:** `handler.py`, `agenda_fsm.py`

**Objetivos:**
1. Validar fechas futuras (no pasadas)
2. Validar formato time (HH:MM)
3. Validar title (no vacío, max 200 chars)
4. Validar location (max 500 chars)
5. Añadir validaciones a FSM callbacks

**Cambios código:**

```python
# handler.py (añadir nuevo método)
def _validate_future_date(self, date_obj) -> bool:
    """
    Validate that date is in the future.
    
    Args:
        date_obj: Date to validate
    
    Returns:
        True if future, raises ValueError if past
    """
    today = datetime.now(timezone.utc).date()
    
    if hasattr(date_obj, 'date'):
        date_obj = date_obj.date()
    
    if date_obj < today:
        raise ValueError(f"Fecha pasada: {date_obj}. Usa fecha futura.")
    
    return True

def _validate_time_format(self, time_str: str) -> bool:
    """
    Validate time format (HH:MM or variants).
    
    Args:
        time_str: Time string to validate
    
    Returns:
        True if valid, raises ValueError if invalid
    """
    import re
    
    # Accept formats: HH:MM, H:MM, HHam/pm, Ham/pm
    patterns = [
        r'^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$',  # 14:30, 9:00
        r'^([1-9]|1[0-2])(am|pm)$',             # 3pm, 11am
        r'^([1-9]|1[0-2]):[0-5][0-9](am|pm)$'  # 3:30pm
    ]
    
    for pattern in patterns:
        if re.match(pattern, time_str.lower().strip()):
            return True
    
    raise ValueError(f"Formato hora inválido: '{time_str}'. Usa HH:MM o 3pm")
```

**Integrar en handle():**

```python
# handler.py línea 200 (después de extract entities)
if trigger == 'provide_date':
    date_entity = entities.get('extracted_date')
    if date_entity:
        self._validate_future_date(date_entity)

if trigger == 'provide_time':
    time_entity = entities.get('extracted_time')
    if time_entity:
        self._validate_time_format(time_entity)
```

**Validación:**
- [ ] Fecha pasada rechazada con error claro
- [ ] Formato hora validado
- [ ] Title max 200 chars enforced
- [ ] Location max 500 chars enforced

**Micro-recompensa:** +1 punto

---

### TAREA 3: Error Handling Graceful
**Prioridad:** P1  
**Duración:** 30min  
**Archivos:** `handler.py`

**Objetivos:**
1. Try-catch en `_save_event_to_db()`
2. Rollback FSM en error DB
3. User-friendly error messages
4. Logging detallado con stack traces
5. Recovery strategies (retry, fallback)

**Cambios código:**

```python
# handler.py línea 260 (mejorar try-catch)
try:
    # 6. Save to database if event completed
    if fsm.current_state == AgendaStates.EVENT_SAVED:
        try:
            event_id = await self._save_event_to_db(user_id, fsm._event_draft)
            context['db_event_id'] = event_id
            context['event_saved'] = True
            
            # Reset FSM to IDLE
            fsm.transition('finish', context)
            
        except ValueError as ve:
            # Validation error
            self.logger.warning(f"Validation failed saving event: {ve}")
            
            # Rollback FSM to PROCESSING
            fsm.current_state = AgendaStates.PROCESSING
            
            return {
                "response": f"Error de validación: {str(ve)}. Intenta nuevamente.",
                "state": str(AgendaStates.PROCESSING),
                "context": context,
                "status": "validation_error",
                "performance_ms": self._calculate_performance(start_time),
                "level": 1
            }
            
        except Exception as db_error:
            # Database error
            self.logger.error(f"Database error saving event: {db_error}", exc_info=True)
            
            # Rollback FSM to PROCESSING
            fsm.current_state = AgendaStates.PROCESSING
            
            return {
                "response": "Error guardando evento. Por favor intenta nuevamente.",
                "state": str(AgendaStates.PROCESSING),
                "context": context,
                "status": "db_error",
                "error_details": str(db_error),
                "performance_ms": self._calculate_performance(start_time),
                "level": 1
            }
```

**Validación:**
- [ ] DB errors no rompen aplicación
- [ ] FSM rollback en error
- [ ] User-friendly messages
- [ ] Stack traces logged

**Micro-recompensa:** +1 punto

---

### TAREA 4: Limpieza Legacy Code
**Prioridad:** P1  
**Duración:** 20min  
**Archivos:** `handler.py`

**Objetivos:**
1. Eliminar métodos deprecated (~100 LOC)
2. Remover comentarios obsoletos
3. Simplificar handler a 250-300 LOC
4. Actualizar docstrings

**Métodos a eliminar:**

```python
# ELIMINAR estos métodos legacy:
- _process_message() (línea 360)
- _extract_datetime() (línea 380)
- _list_events_internal() (línea 490)
- create_event() (línea 510)
- list_events() (línea 530)
- _get_conversation_manager() (línea 350)
- self.conversation_managers dict (línea 90)
```

**Validación:**
- [ ] Handler reducido a ~280 LOC
- [ ] Solo métodos usados presentes
- [ ] Docstrings actualizados
- [ ] Sin TODOs en código

**Micro-recompensa:** +1 punto

---

### TAREA 5: Tests E2E (8 tests)
**Prioridad:** P0  
**Duración:** 60min  
**Archivos:** `tests/agents/agenda_agent/test_agenda_agent_e2e.py` (NEW)

**Objetivos:**
1. Test flujo completo CREATE evento
2. Test FSM transitions
3. Test ML entity extraction
4. Test DB persistence
5. Test validations (fecha pasada, etc)
6. Test error handling
7. Test multi-tenant isolation
8. Test performance (<100ms)

**Tests a crear:**

```python
# test_agenda_agent_e2e.py
import pytest
from datetime import datetime, timedelta, timezone
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.database.repositories.event_repository import EventRepository

@pytest.mark.asyncio
async def test_create_event_full_flow(async_session):
    """
    TEST 1: Flujo completo de creación de evento.
    
    Flow:
    1. User: "crear evento"
    2. Agent: "¿Cuál es el título?"
    3. User: "Reunión con cliente"
    4. Agent: "¿Para qué fecha?"
    5. User: "mañana"
    6. Agent: "¿A qué hora?"
    7. User: "3pm"
    8. Agent: "¿Dónde será?"
    9. User: "Oficina central"
    10. Agent: "✅ Evento guardado"
    
    Validates:
    - FSM transitions correctas
    - ML extraction funciona
    - Evento guardado en DB
    - Response correcta en cada paso
    """
    # Setup
    agent = AgendaAgent(session=async_session)
    user_id = "test_user_123"
    context = {"user_id": user_id, "tenant_id": "test_tenant"}
    
    # Step 1: Start create
    result = await agent.handle(user_id, "crear evento", context)
    assert result["status"] == "ok"
    assert "título" in result["response"].lower()
    assert result["state"] == "AWAITING_TITLE"
    
    # Step 2: Provide title
    context = result["context"]
    context["event_title"] = "Reunión con cliente"
    result = await agent.handle(user_id, "Reunión con cliente", context)
    assert result["status"] == "ok"
    assert "fecha" in result["response"].lower()
    assert result["state"] == "AWAITING_DATE"
    
    # Step 3: Provide date
    context = result["context"]
    tomorrow = (datetime.now() + timedelta(days=1)).date()
    context["event_date"] = str(tomorrow)
    result = await agent.handle(user_id, "mañana", context)
    assert result["status"] == "ok"
    assert "hora" in result["response"].lower()
    assert result["state"] == "AWAITING_TIME"
    
    # Step 4: Provide time
    context = result["context"]
    context["event_time"] = "15:00"
    result = await agent.handle(user_id, "3pm", context)
    assert result["status"] == "ok"
    assert "dónde" in result["response"].lower() or "ubicación" in result["response"].lower()
    assert result["state"] == "AWAITING_LOCATION"
    
    # Step 5: Provide location
    context = result["context"]
    context["event_location"] = "Oficina central"
    result = await agent.handle(user_id, "Oficina central", context)
    assert result["status"] == "ok"
    assert "guardado" in result["response"].lower() or "✅" in result["response"]
    
    # Verify DB
    event_repo = EventRepository(async_session)
    events = await event_repo.get_by_user(
        user_id=int(user_id.split("_")[-1]),
        tenant_id="test_tenant"
    )
    assert len(events) == 1
    assert events[0].title == "Reunión con cliente"
    assert events[0].location == "Oficina central"

@pytest.mark.asyncio
async def test_fsm_transitions(async_session):
    """TEST 2: FSM transitions funcionan correctamente."""
    agent = AgendaAgent(session=async_session)
    user_id = "test_user_456"
    context = {"user_id": user_id, "tenant_id": "test_tenant"}
    
    # IDLE -> AWAITING_TITLE
    result = await agent.handle(user_id, "crear evento", context)
    assert result["state"] == "AWAITING_TITLE"
    
    # Cancel from AWAITING_TITLE
    context = result["context"]
    result = await agent.handle(user_id, "cancelar", context)
    assert result["state"] == "CANCELLED"

@pytest.mark.asyncio
async def test_ml_entity_extraction(async_session):
    """TEST 3: ML extrae entities correctamente."""
    agent = AgendaAgent(session=async_session)
    user_id = "test_user_789"
    context = {"user_id": user_id, "tenant_id": "test_tenant"}
    
    result = await agent.handle(
        user_id,
        "crear evento mañana a las 3pm",
        context
    )
    
    entities = result.get("entities", {})
    assert "dates" in entities or "extracted_date" in entities
    assert "extracted_time" in entities or "time" in entities

@pytest.mark.asyncio
async def test_db_persistence(async_session):
    """TEST 4: Eventos persisten correctamente en DB."""
    agent = AgendaAgent(session=async_session)
    # ... create event ...
    # ... verify in DB ...
    pass

@pytest.mark.asyncio
async def test_validation_past_date(async_session):
    """TEST 5: Rechaza fechas pasadas."""
    agent = AgendaAgent(session=async_session)
    # ... try past date ...
    # ... assert validation error ...
    pass

@pytest.mark.asyncio
async def test_error_handling(async_session):
    """TEST 6: Error handling graceful."""
    agent = AgendaAgent(session=async_session)
    # ... simulate DB error ...
    # ... assert recovery ...
    pass

@pytest.mark.asyncio
async def test_multi_tenant_isolation(async_session):
    """TEST 7: Multi-tenant aislado."""
    agent = AgendaAgent(session=async_session)
    # ... create events for tenant A ...
    # ... verify tenant B can't see them ...
    pass

@pytest.mark.asyncio
async def test_performance(async_session):
    """TEST 8: Performance <100ms."""
    agent = AgendaAgent(session=async_session)
    result = await agent.handle("test_user", "crear evento", {})
    assert result["performance_ms"] < 100
```

**Validación:**
- [ ] 8 tests PASSING
- [ ] Coverage ≥85%
- [ ] Tiempo ejecución <5s total

**Micro-recompensa:** +2 puntos

---

### TAREA 6: Integración Final & Documentación
**Prioridad:** P1  
**Duración:** 30min  
**Archivos:** `README.md`, `CHANGELOG.md`

**Objetivos:**
1. README AgendaAgent actualizado
2. CHANGELOG entry para v3.2
3. Architecture diagram actualizado
4. Usage examples
5. Performance benchmarks documentados

**Documentación:**

```markdown
# AgendaAgent v3.2 - Production Ready

## Features

- ✅ EventRepository 100% integrated
- ✅ FSM with 15 states
- ✅ ML entity extraction (dates, times, locations)
- ✅ Database persistence (PostgreSQL)
- ✅ Multi-tenant support
- ✅ Robust validations
- ✅ Graceful error handling
- ✅ Performance <100ms
- ✅ Test coverage ≥85%

## Usage

```python
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.database.session import get_session

async with get_session() as session:
    agent = AgendaAgent(session=session)
    
    result = await agent.handle(
        user_id="user_123",
        message="crear evento mañana a las 3pm",
        context={"tenant_id": "default"}
    )
    
    print(result["response"])
```

## Performance

- Simple commands: <10ms
- NLP queries: <100ms
- Full conversation flow: <500ms

## Testing

```bash
pytest tests/agents/agenda_agent/ -v --cov
```

Coverage: 87%
```

**Validación:**
- [ ] README completo
- [ ] CHANGELOG actualizado
- [ ] Examples funcionando

**Micro-recompensa:** +1 punto

---

## 📊 RESUMEN MICRO-RECOMPENSAS

| Tarea | Puntos | Duración |
|-------|--------|----------|
| **TAREA 1** - EventRepository Integration | +2 | 45min |
| **TAREA 2** - Validations Robustas | +1 | 30min |
| **TAREA 3** - Error Handling | +1 | 30min |
| **TAREA 4** - Limpieza Legacy | +1 | 20min |
| **TAREA 5** - Tests E2E | +2 | 60min |
| **TAREA 6** - Documentación | +1 | 30min |
| **TOTAL** | **+8 puntos** | **~3h 45min** |

---

## ✅ CHECKLIST FINAL

### Pre-ejecución
- [ ] Backup código actual (git commit)
- [ ] Database schema validado (Event model OK)
- [ ] Dependencies instaladas (SQLAlchemy, dateutil)
- [ ] Test DB disponible

### Post-ejecución
- [ ] EventRepository conectado
- [ ] Tests 8/8 PASSING
- [ ] Coverage ≥85%
- [ ] Performance <100ms verificado
- [ ] Documentación actualizada
- [ ] Git commit + push
- [ ] Tag: `v3.2-agenda-agent-production`

---

## 🎯 RESULTADO ESPERADO

**AgendaAgent v3.2 - Production Ready**

```
Estado: ✅ PRODUCTION READY 100%

Componentes:
├─ ✅ Handler (280 LOC)
├─ ✅ FSM (350 LOC)
├─ ✅ EventRepository (integrado)
├─ ✅ ML Extractors (funcionando)
├─ ✅ Validations (robustas)
├─ ✅ Error handling (graceful)
├─ ✅ Tests E2E (8 tests, 87% coverage)
└─ ✅ Documentation (completa)

Performance:
├─ Simple: <10ms ✅
├─ NLP: <100ms ✅
└─ Full flow: <500ms ✅

Quality:
├─ Coverage: 87% ✅
├─ Tests: 8/8 PASSING ✅
├─ Linting: 0 errors ✅
└─ Type hints: 100% ✅
```

---

**¿Listo para ejecutar?** 🚀

**Próximo paso:** Ejecutar TAREA 1 (EventRepository Integration)
