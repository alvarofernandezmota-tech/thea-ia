# 🧠 FSM Engine v2 — Detalles Técnicos

**Versión:** v0.14.0  
**Componente:** `src/theaia/core/fsm/`  
**Última actualización:** 2025-10-31 03:16 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 🎯 Qué es FSM Engine v2

**Finite State Machine** mejorada con:
- Callbacks pre-transition, post-transition, on-error
- Contexto persistente entre estados
- Manejo de excepciones granular
- Compatible con múltiples agentes
- Integración CoreRouter + Manager Universal (H03)

---

## 🔄 Estados principales

┌─────────┐
│ initial │ (usuario conecta)
└────┬────┘
│
▼
┌────────────┐ ┌─────────────┐
│processing │─────→│ disamb... │ (aclarar intención)
│(procesa) │ │(si necesario)│
└────┬───────┘ └──────┬──────┘
│ │
└────────┬───────────┘
▼
┌──────────────┐
│ executing │ (ejecuta agente)
└────┬─────────┘
│
▼
┌──────────────┐
│ completion │ (resultado)
└────┬─────────┘
│
▼
┌──────────────┐
│ idle │ (listo para siguiente)
└──────────────┘

┌─ ON ERROR ─────────────────────────────┐
│ Desde cualquier estado → error handler │
└────────────────────────────────────────┘

text

---

## 💾 Callbacks (Hooks)

### Pre-transition
Ejecuta **antes** de cambiar de estado.

**Uso:** Validación, preparación datos

@fsm.pre_transition('processing')
def validate_message(context):
"""Validar que el mensaje no esté vacío"""
if not context.get('message'):
raise ValueError('Mensaje vacío')
return context

@fsm.pre_transition('executing')
def check_agent_availability(context):
"""Verificar que el agente está disponible"""
agent = context.get('agent')
if not agent:
raise ValueError('Agente no seleccionado')
return context

text

### Post-transition
Ejecuta **después** de cambiar de estado.

**Uso:** Logging, persistencia, triggers

@fsm.post_transition('executing')
def log_execution(context):
"""Registrar ejecución en logs"""
logger.info(f"Agent {context['agent']} executed for user {context['user_id']}")
return context

@fsm.post_transition('completion')
def save_context(context):
"""Guardar contexto en DB"""
context_manager.save(context['user_id'], context)
return context

text

### On-error
Ejecuta cuando ocurre **excepción**.

**Uso:** Recovery, alertas, limpieza

@fsm.on_error()
def handle_error(error, context):
"""Manejar errores globalmente"""
logger.error(f"FSM Error: {str(error)}")
# Reset contexto si es necesario
if error.critical:
context_manager.clear(context['user_id'])
return context

text

---

## 🔗 Integración con CoreRouter

FSM Engine se integra así:

from src.theaia.core.fsm import FSMEngine
from src.theaia.core.router import CoreRouter

Inicializar FSM
fsm = FSMEngine()

CoreRouter usa FSM para orquestar
router = CoreRouter(fsm_engine=fsm)

Flujo:
1. Router recibe mensaje
2. FSM determina estado actual
3. FSM ejecuta pre-callbacks
4. FSM transiciona a nuevo estado
5. FSM ejecuta post-callbacks
6. Router delega a agente
text

---

## 📊 Ejemplo uso completo

Inicializar
fsm = FSMEngine()
context = {
'user_id': 'user_123',
'message': 'quiero agendar cita',
'state': 'initial',
'agent': None
}

Registrar callbacks
@fsm.pre_transition('processing')
def validate(ctx):
assert ctx['message'], "Message required"
return ctx

@fsm.post_transition('processing')
def log_process(ctx):
print(f"Processing: {ctx['message']}")
return ctx

Ejecutar
result = fsm.handle('processing', context)

Output: Processing: quiero agendar cita
Transicionar a siguiente estado
result = fsm.handle('disambiguation', result)

Callback pre-transition se ejecuta
Cambio de estado
Callback post-transition se ejecuta
text

---

## 🎯 Métricas esperadas (H03)

| Métrica | Objetivo |
|---------|----------|
| Latencia transición | <10ms |
| Cobertura tests | ≥90% |
| Memory per state | <1MB |
| Callbacks máx | 5 por transición |

---

## 🔗 Relación con hitos

- **H03** — FSM v2 callbacks avanzados
- **H04** — Persistencia contexto en DB
- **H11** — Métricas FSM en Prometheus

---

## 📖 Documentación relacionada

- [Architecture Overview](./overview.md)
- [Decisiones arquitectónicas](./decisions.md)
- [H03 - FSM Avanzado](../roadmap/milestones/H03_17.md)

---

**Última actualización:** 2025-10-31 03:16 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)