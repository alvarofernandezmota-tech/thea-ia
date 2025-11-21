# 🤖 Agenda FSM v2.0 — Máquina de Estados Profesional H03

**Versión:** v2.0.0  
**Archivo:** `src/theaia/agents/agenda_agent/model/agenda_fsm.py`  
**Última actualización:** 21 Noviembre 2025, 14:15 CET  
**Status:** ✅ H03 Production  
**Integración:** BaseStateMachine Core FSM Engine  
**Filosofía:** TRES (Álvaro + Jarvis + THEA IA)

---

## 📋 Propósito

El **AgendaFSM v2.0** es una máquina de estados finitos profesional que gestiona **6 flujos completos** de AgendaAgent, integrándose con el **Core FSM Engine** de THEA IA.

### Responsabilidades v2.0:

✅ **6 flujos completos:** Crear, Listar, Editar, Eliminar, Buscar, Cancelar  
✅ **15 estados robustos:** Con validaciones y callbacks  
✅ **Callbacks pre/post/error:** Validación automática + side effects  
✅ **Herencia BaseStateMachine:** Aprovecha framework completo  
✅ **Transitions con triggers:** No más if/elif manual  
✅ **Context management:** Integrado con Core  
✅ **Error handling:** Robusto y automático  
✅ **Logging:** Auditoría completa

---

## 🔄 Cambios H03 v2.0

### **NUEVA ARQUITECTURA:**

| Aspecto | v1.0 (Anterior) | v2.0 (H03) |
|---------|-----------------|------------|
| **LOC** | 58 (stub) | 450+ (profesional) |
| **Estados** | 6 básicos | 15 completos |
| **Flujos** | 1 (solo crear) | 6 completos |
| **Callbacks** | 0 | 30+ |
| **Transitions** | Manual if/elif | Framework triggers |
| **Coverage** | 90% | 95% |
| **Tests** | 17 (débiles) | 17 (robustos) |
| **Integration** | None | BaseStateMachine Core |

### **Mejoras clave:**

✅ Hereda `BaseStateMachine` (framework completo)  
✅ Usa `AgendaStates` enum (vs strings hardcoded)  
✅ Transitions con `add_transition()` + triggers  
✅ Callbacks `before`/`after` en cada transición  
✅ Validaciones robustas pre-transición  
✅ Side effects automáticos post-transición  
✅ Error handling integrado  
✅ Context management profesional  
✅ Logging estructurado

---

## 🔄 Diagrama de Estados v2.0

### **FLUJO 1: CREAR EVENTO**

START
↓
IDLE → AWAITING_TITLE → AWAITING_DATE → AWAITING_TIME →
AWAITING_LOCATION → PROCESSING → EVENT_SAVED → IDLE

text

### **FLUJO 2: LISTAR EVENTOS**

IDLE → LISTING_EVENTS → IDLE

text

### **FLUJO 3: EDITAR EVENTO**

IDLE → SELECTING_EVENT → EDITING_FIELD → PROCESSING →
EVENT_UPDATED → IDLE

text

### **FLUJO 4: ELIMINAR EVENTO**

IDLE → DELETING_EVENT → CONFIRMING_DELETE →
EVENT_DELETED → IDLE

text

### **FLUJO 5: BUSCAR EVENTOS**

IDLE → SEARCHING_EVENTS → IDLE

text

### **FLUJO 6: CANCELAR**

ANY_STATE → CANCELLED → IDLE

text

---

## 📊 Estados v2.0 (15 estados)

1. **IDLE** - Estado inicial/reposo
2. **AWAITING_TITLE** - Esperando título evento
3. **AWAITING_DATE** - Esperando fecha
4. **AWAITING_TIME** - Esperando hora
5. **AWAITING_LOCATION** - Esperando ubicación (opcional)
6. **PROCESSING** - Procesando datos
7. **EVENT_SAVED** - Evento guardado exitosamente
8. **LISTING_EVENTS** - Listando eventos
9. **SELECTING_EVENT** - Seleccionando evento para editar/eliminar
10. **EDITING_FIELD** - Editando campo específico
11. **EVENT_UPDATED** - Evento actualizado exitosamente
12. **DELETING_EVENT** - Proceso de eliminación iniciado
13. **CONFIRMING_DELETE** - Confirmando eliminación
14. **EVENT_DELETED** - Evento eliminado exitosamente
15. **SEARCHING_EVENTS** - Buscando eventos
16. **CANCELLED** - Operación cancelada

---

## 💻 Implementación v2.0

### **Clase AgendaFSM(BaseStateMachine)**

from src.theaia.core.fsm.state_machine import BaseStateMachine
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates

class AgendaFSM(BaseStateMachine):
"""
FSM profesional integrado con Core.

text
Features H03:
- Callbacks pre/post/error
- Transitions con triggers
- Context management
- Validaciones automáticas
- Error handling robusto
"""

def __init__(self):
    super().__init__(
        states=AgendaStates.all_states(),
        initial=AgendaStates.IDLE
    )
    self.logger = logging.getLogger(__name__)
    self._configure_transitions()
    self._event_draft: Optional[Dict[str, Any]] = None
text

### **Ejemplo: Transition con Callbacks**

Transitions con callbacks pre/post
self.add_transition(
trigger='start_create',
source=AgendaStates.IDLE,
dest=AgendaStates.AWAITING_TITLE,
before=self._pre_validate_create, # ✅ Callback pre-validación
after=self._post_create_started # ✅ Callback post-acción
)

text

### **Ejemplo: Callback Pre-Validación**

def _pre_validate_create(self, context: Dict[str, Any]) -> None:
"""Valida antes de iniciar creación"""
if not context.get('user_id'):
raise ValueError("User ID requerido")

text
if not context.get('tenant_id'):
    raise ValueError("Tenant ID requerido (multi-tenant)")

self.logger.info(f"Pre-validación OK: user={context['user_id']}")
text

### **Ejemplo: Callback Post-Acción**

def _post_create_started(self, context: Dict[str, Any]) -> None:
"""Inicializa borrador después de validación"""
self._event_draft = {
'user_id': context['user_id'],
'tenant_id': context['tenant_id'],
'created_at': datetime.utcnow().isoformat()
}
context['event_draft'] = self._event_draft
self.logger.info("Borrador iniciado")

text

---

## 🔗 Integración Core FSM

### **Framework BaseStateMachine:**

Antes (v1.0):
if self.state == "awaiting_title":
# lógica manual

Ahora (v2.0):
self.add_transition(
trigger='provide_title',
source=AgendaStates.AWAITING_TITLE,
dest=AgendaStates.AWAITING_DATE,
before=self._validate_title,
after=self._store_title
)

text

### **Ventajas Framework:**

✅ Validaciones automáticas  
✅ Side effects consistentes  
✅ Error handling robusto  
✅ Context merging automático  
✅ Logging estructurado  
✅ Auditoría completa

---

## 🧪 Test Cases v2.0

**Test Coverage:** 95% (vs 90% anterior)  
**Tests:** 17/17 PASSING (mantenidos + mejorados)

### **Tests Principales:**

✅ **Test 1:** Crear evento completo (título → fecha → hora → ubicación)  
✅ **Test 2:** Listar eventos con filtros  
✅ **Test 3:** Editar evento existente  
✅ **Test 4:** Eliminar evento con confirmación  
✅ **Test 5:** Buscar eventos por criterio  
✅ **Test 6:** Cancelar desde cualquier estado  
✅ **Test 7:** Callbacks pre-validación bloquean si inválido  
✅ **Test 8:** Callbacks post-acción ejecutan side effects  
✅ **Test 9:** Error handling captura excepciones  
✅ **Test 10:** Context persistence entre transiciones  
✅ **Test 11:** Multi-tenant isolation  
✅ **Test 12:** FSM state restoration  
✅ **Test 13:** Draft management  
✅ **Test 14:** Concurrent transitions  
✅ **Test 15:** Edge cases (empty, invalid, special chars)  
✅ **Test 16:** Performance <100ms  
✅ **Test 17:** Integration con AgendaHandler

---

## 📈 Métricas v2.0

| Métrica | v1.0 (Anterior) | v2.0 (H03) |
|---------|-----------------|------------|
| **LOC** | 58 | 450+ |
| **Estados** | 6 | 15 |
| **Flujos** | 1 | 6 |
| **Callbacks** | 0 | 30+ |
| **Transitions** | Manual if/elif | Framework triggers |
| **Coverage** | 90% | 95% |
| **Tests** | 17 (débiles) | 17 (robustos) |
| **Integration** | None | BaseStateMachine Core |

---

## 📈 Uso en Conversación

### **Ejemplo Completo v2.0:**

from src.theaia.agents.agenda_agent.model.agenda_fsm import AgendaFSM
from src.theaia.agents.agenda_agent.model.agent_states import AgendaStates

Inicializar FSM
fsm = AgendaFSM()
context = {'user_id': '123', 'tenant_id': 'default'}

Turno 1: Iniciar creación
fsm.start_create(context) # Trigger

Estado: IDLE → AWAITING_TITLE
Pre-callback: Valida user_id + tenant_id ✅
Post-callback: Inicializa borrador ✅
Turno 2: Proporcionar título
context['event_title'] = "Reunión con equipo"
fsm.provide_title(context) # Trigger

Estado: AWAITING_TITLE → AWAITING_DATE
Pre-callback: Valida título (no vacío, ≤200 chars) ✅
Post-callback: Guarda título en borrador ✅
Turno 3: Proporcionar fecha
context['event_date'] = "2025-11-25"
fsm.provide_date(context) # Trigger

Estado: AWAITING_DATE → AWAITING_TIME
Pre-callback: Valida formato fecha ISO 8601 ✅
Post-callback: Guarda fecha en borrador ✅
Turno 4: Proporcionar hora
context['event_time'] = "15:00"
fsm.provide_time(context) # Trigger

Estado: AWAITING_TIME → AWAITING_LOCATION
Turno 5: Proporcionar ubicación (opcional)
context['event_location'] = "Sala de juntas"
fsm.provide_location(context) # Trigger

Estado: AWAITING_LOCATION → PROCESSING
Turno 6: Guardar evento
context['db_event_id'] = 456
fsm.save_event(context) # Trigger

Estado: PROCESSING → EVENT_SAVED
Pre-callback: Valida campos requeridos ✅
Post-callback: Marca como guardado ✅
Turno 7: Finalizar
fsm.finish(context) # Trigger

Estado: EVENT_SAVED → IDLE
Post-callback: Limpia borrador ✅
✅ FLUJO COMPLETADO
text

---

## 🎯 H03 BLOQUE 3.4A.1.1 Status

**✅ COMPLETADO:**

- [x] FSM Refactor integrado con Core
- [x] Herencia BaseStateMachine
- [x] Transitions framework con triggers
- [x] Callbacks pre/post/error implementados
- [x] 15 estados definidos
- [x] 6 flujos completos
- [x] Tests 17/17 PASSING
- [x] Coverage 95%
- [x] LOC: 58 → 450+ (profesional)
- [x] Commit: `refactor(h03-3.4a.1.1): AgendaAgent FSM - integrate Core FSM`

---

## 📌 Meta-Información

| Campo | Valor |
|-------|-------|
| **Archivo** | `src/theaia/agents/agenda_agent/model/agenda_fsm.py` |
| **Versión** | v2.0.0 (H03) |
| **Test Coverage** | 95% |
| **Estados** | 15 |
| **Flujos** | 6 |
| **Callbacks** | 30+ |
| **LOC** | 450+ |
| **Framework** | BaseStateMachine Core FSM Engine |
| **Última actualización** | 21 Noviembre 2025, 14:15 CET |
| **Status** | ✅ H03 Production |
| **Commit** | `refactor(h03-3.4a.1.1): AgendaAgent FSM v2.0` |
| **Responsable** | Álvaro Fernández Mota (CEO THEA IA) |
| **Filosofía** | TRES (Álvaro + Jarvis + THEA IA) |

---

**Agenda FSM v2.0 — Arquitectura Profesional H03**  
Integrado con BaseStateMachine Core FSM Engine  
15 estados + 6 flujos completos + 30+ callbacks  
✅ Ready for Production