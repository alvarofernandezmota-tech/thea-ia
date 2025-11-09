🧠 FSM Engine v2 — Detalles Técnicos
Versión: v0.14.0
Componente: src/theaia/core/fsm/
Última actualización: 2025-11-08 17:45 CET (Sesión 36)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Propósito
Documentación técnica del FSM Engine v2: detalles de callbacks, estados, integración con CoreRouter y ejemplos de código.

Audiencia:

Developers implementando FSM

Architects diseñando flujos

DevOps monitoreando FSM

🎯 Qué es FSM Engine v2
Finite State Machine mejorada con:

Callbacks pre-transition, post-transition, on-error

Contexto persistente entre estados

Manejo de excepciones granular

Compatible con múltiples agentes

Integración CoreRouter + Manager Universal (H03)

🔄 Estados principales
text
┌─────────┐
│ initial │ (usuario conecta)
└────┬────┘
     │
     ▼
┌────────────┐      ┌──────────────┐
│processing  │─────→│disambiguation│ (aclarar intención)
│(procesa)   │      │(si necesario) │
└────┬───────┘      └──────┬───────┘
     │                      │
     └────────┬─────────────┘
              ▼
     ┌──────────────┐
     │  executing   │ (ejecuta agente)
     └────┬─────────┘
          │
          ▼
     ┌──────────────┐
     │  completion  │ (resultado)
     └────┬─────────┘
          │
          ▼
     ┌──────────────┐
     │    idle      │ (listo para siguiente)
     └──────────────┘

┌─ ON ERROR ─────────────────────────────┐
│ Desde cualquier estado → error handler │
└────────────────────────────────────────┘
Transiciones:

initial → processing (siempre)

processing → disambiguation (si ambigüedad)

processing/disambiguation → executing (intención clara)

executing → completion (éxito)

completion → idle (listo)

ANY → error_handler (excepción)

💾 Callbacks (Hooks)
Pre-transition
Ejecuta antes de cambiar de estado.

Uso: Validación, preparación datos

python
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
Post-transition
Ejecuta después de cambiar de estado.

Uso: Logging, persistencia, triggers

python
@fsm.post_transition('executing')
def log_execution(context):
    """Registrar ejecución en logs"""
    logger.info(
        f"Agent {context['agent']} executed for user {context['user_id']}"
    )
    return context

@fsm.post_transition('completion')
def save_context(context):
    """Guardar contexto en DB"""
    context_manager.save(context['user_id'], context)
    return context
On-error
Ejecuta cuando ocurre excepción.

Uso: Recovery, alertas, limpieza

python
@fsm.on_error()
def handle_error(error, context):
    """Manejar errores globalmente"""
    logger.error(f"FSM Error: {str(error)}")
    # Reset contexto si es necesario
    if error.critical:
        context_manager.clear(context['user_id'])
    return context
🔗 Integración con CoreRouter
FSM Engine se integra así:

python
from src.theaia.core.fsm import FSMEngine
from src.theaia.core.router import CoreRouter

# Inicializar FSM
fsm = FSMEngine()

# CoreRouter usa FSM para orquestar
router = CoreRouter(fsm_engine=fsm)
Flujo:

Router recibe mensaje

FSM determina estado actual

FSM ejecuta pre-callbacks

FSM transiciona a nuevo estado

FSM ejecuta post-callbacks

Router delega a agente

📊 Ejemplo uso completo
Inicializar
python
fsm = FSMEngine()
context = {
    'user_id': 'user_123',
    'message': 'quiero agendar cita',
    'state': 'initial',
    'agent': None
}
Registrar callbacks
python
@fsm.pre_transition('processing')
def validate(ctx):
    assert ctx['message'], "Message required"
    return ctx

@fsm.post_transition('processing')
def log_process(ctx):
    print(f"Processing: {ctx['message']}")
    return ctx
Ejecutar
python
# Pasar a processing
result = fsm.handle('processing', context)
# Output: Processing: quiero agendar cita

# Transicionar a siguiente estado
result = fsm.handle('disambiguation', result)
# Pre-transition se ejecuta
# Cambio de estado
# Post-transition se ejecuta
⏱️ Ciclo completo ejemplo
text
Entrada usuario: "crear evento mañana"
                    ↓
         FSM: initial → processing
                    ↓
         Pre-transition: validate_message
                    ↓
    Post-transition: log_process, NLP
                    ↓
     Intent claro: no necesita disambiguation
                    ↓
         FSM: processing → executing
                    ↓
         Pre-transition: check_agent_availability
                    ↓
    Post-transition: agent_selector (→ EventAgent)
                    ↓
        EventAgent procesa: crear evento
                    ↓
         FSM: executing → completion
                    ↓
    Post-transition: save_context (→ DB)
                    ↓
         FSM: completion → idle
                    ↓
  Output: "Evento creado para mañana ✓"
🎯 Métricas esperadas (H03)
Métrica	Objetivo
Latencia transición	<10ms
Cobertura tests	≥90%
Memory per state	<1MB
Callbacks máx	5 por transición
Error recovery	<500ms
🚨 Manejo de excepciones
Estrategia
python
try:
    fsm.handle('processing', context)
except ValidationError as e:
    logger.warning(f"Validation failed: {e}")
    # Reintentar con correción automática
    context['message'] = auto_correct(context['message'])
    fsm.handle('processing', context)
except AgentNotAvailableError as e:
    logger.error(f"Agent error: {e}")
    # Usar fallback agent
    context['agent'] = 'fallback'
    fsm.handle('executing', context)
except Exception as e:
    logger.critical(f"Unrecoverable error: {e}")
    # Trigger on_error callback
    fsm.on_error()(e, context)
🔗 Relación con hitos
H03 — FSM v2 callbacks avanzados ✅

H04 — Persistencia contexto en DB

H11 — Métricas FSM en Prometheus

📌 Meta-información
Campo	Valor
Archivo	docs/architecture/fsmengine.md
Versión	v0.14.0
Última revisión	2025-11-08 17:45 CET (Sesión 36)
Responsable	Álvaro Fernández Mota (CEO)
Estado	✅ Activo
🔗 Enlaces relacionados
Architecture Overview — Visión general

Diagrams — Flujos visuales

Deployment — Despliegue

Adapters — Integración

Agents — Agentes

🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/architecture/)

Detalles técnicos completos del FSM v2

Ejemplos Python verificados

Validado en sesión 36