⚡ Agent: Event — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: Agents Team
Estado: ✅ Activo
Prioridad: 🔴 Alta (Core)

📋 Propósito
El Agente Event procesa eventos del sistema internos: transiciones FSM, eventos async, callbacks, webhooks y mensajería interna entre componentes.

Audiencia:

Desarrolladores integrando event-driven architecture

DevOps monitoreando eventos del sistema

Arquitectos diseñando flujos asíncronos

🎯 Responsabilidades
Funcionalidad	Descripción
Procesar eventos	Recibir y procesar eventos del sistema
Enrutamiento	Ruta eventos a handlers apropiados
Event queue	Cola de eventos para procesamiento async
Webhooks	Recibir webhooks externos
Pub/Sub	Sistema publicación/suscripción
Event logging	Registro completo de eventos
🔧 Configuración
text
agent:
  name: "Event"
  version: "1.0"
  enabled: true
  timeout: 15

capabilities:
  - process_event
  - route_event
  - queue_event
  - handle_webhook
  - publish_event
  - subscribe_event

queue:
  engine: "redis"  # o RabbitMQ
  max_size: 10000
  retry_policy: exponential_backoff

logging:
  level: "info"
  retention_days: 30
📥 Entrada - Eventos del sistema
python
{
  "event_type": "fsm_transition",
  "source": "fsm_engine",
  "timestamp": "2025-11-08T16:53:00Z",
  "data": {
    "from_state": "idle",
    "to_state": "processing",
    "context": {...}
  }
}
🔄 Flujo
text
Evento generado (FSM, Adapter, otro agente)
     ↓
Event Agent recibe
     ↓
Validar y parsear
     ↓
Enrutar a handler específico
     ↓
Procesar (sync o async)
     ↓
Registrar en log
     ↓
Emitir eventos derivados (si aplica)
📊 Métricas
Métrica	Actual	Target
Event throughput	500/s	> 400/s
Processing latency	25ms	< 50ms
Queue depth	150	< 1000
📌 Meta
Campo	Valor
Archivo	docs/agents/agent_event.md
Estado	✅ Activo