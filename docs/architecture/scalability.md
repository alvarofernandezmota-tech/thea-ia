📈 Scalability Strategy — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-08 17:31 CET (Sesión 36)
Responsable: Architecture Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Estrategia de escalabilidad horizontal de THEA IA: componentes escalables, bottlenecks, métricas.

Audiencia:

Architects planificando crecimiento

DevOps configurando auto-scaling

Developers optimizando performance

🎯 Componentes escalables
FSM Engine
Escalabilidad: Horizontal (stateless)

Límite: <10ms por transición

Escala: 100-1000s requests/min

Bottleneck: BD contexto

Adapters
Escalabilidad: Horizontal (stateless)

Límite: Rate limitado por API externa

Escala: Telegram (1000s msg/s), REST (100s req/s)

Bottleneck: Conexión con API externa

Agents
Escalabilidad: Vertical (CPU intensivo)

Límite: Modelo ML inference

Escala: 50-100 queries/s por replica

Bottleneck: GPU si hay ML heavy compute

Database (PostgreSQL)
Escalabilidad: Vertical + Replicación

Límite: ~1000 queries/s

Escala: Read replicas + caching

Bottleneck: Writes serializados

Cache (Redis)
Escalabilidad: Horizontal (Cluster mode)

Límite: ~100k ops/s

Escala: Sharding automático

Bottleneck: Memory limits

📊 Arquitectura escalada (producción)
text
┌─────────────────────────────────────┐
│  CDN / Load Balancer (Cloudflare)  │
└────────────────┬────────────────────┘
                 ↓
    ┌────────────────────────┐
    │  API Gateway (Kong)    │
    │  Rate Limiting         │
    │  Authentication        │
    └────────────┬───────────┘
                 ↓
    ┌────────────────────────┐
    │  K8s Service Mesh      │
    │  (Istio)               │
    │  Circuit breakers      │
    └────────────┬───────────┘
                 ↓
    ┌──────────────────────────────────────┐
    │  FSM API (Horizontal scaling)        │
    │  ├─ Replica 1 (CPU 500m, RAM 256Mi) │
    │  ├─ Replica 2                       │
    │  └─ Replica N (auto-scale 3-20)     │
    └────────────┬──────────────────────┬──┘
                 ↓                      ↓
    ┌──────────────────┐    ┌──────────────────┐
    │  PostgreSQL      │    │  Redis Cache     │
    │  (Replicación)   │    │  (Cluster)       │
    │  - Primary       │    │  - Shard 1       │
    │  - Read Replica  │    │  - Shard 2       │
    │  - Backup        │    │  - Shard 3       │
    └──────────────────┘    └──────────────────┘
                 ↓
    ┌──────────────────────┐
    │  Object Storage      │
    │  (S3/GCS)            │
    │  Backup + Artifacts  │
    └──────────────────────┘
🔄 Auto-scaling policies
CPU-based
text
hpa:
  targetCPUUtilizationPercentage: 70
  minReplicas: 3
  maxReplicas: 20
Memory-based
text
hpa:
  targetMemoryUtilizationPercentage: 80
  minReplicas: 3
  maxReplicas: 20
Custom metrics (Prometheus)
text
hpa:
  metrics:
    - resource:
        name: cpu
        target:
          averageUtilization: 70
    - resource:
        name: memory
        target:
          averageUtilization: 80
    - pods:
        metric:
          name: http_requests_per_second
          target:
            averageValue: "100"
📊 Métricas de escalabilidad
Componente	Métrica	Target	Escalabilidad
FSM Engine	Req/s	1000+	Horizontal ✅
Adapters	Msg/s	100+	Horizontal ✅
Agents	Query/s	50+	Vertical ⚠️
PostgreSQL	Query/s	1000+	Vertical + replicas
Redis	Ops/s	100k+	Horizontal ✅
🚨 Bottlenecks conocidos
Bottleneck	Causa	Solución
Transacciones BD	Writes serializadas	Sharding (futura)
Inference ML	GPU saturada	Vertical scale + TPU
Memoria agents	Cache contexto	Redis distributed
Rate limiter API	API externa throttle	Queue + retry
🎯 Planificación de capacidad
Hoy (v0.14.0):

3 replicas FSM

2 read replicas PostgreSQL

Redis single instance

Target: 100 usuarios concurrentes

Próximas versiones:

H08: Multi-tenant sharding

H09: Kubernetes clustering

H11: Observabilidad auto-scaling

📌 Meta-información
Campo	Valor
Archivo	docs/architecture/scalability.md
Versión	v0.14.0
Última revisión	2025-11-08 17:31 CET (Sesión 36)
Responsable	Architecture Team / CEO
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/architecture/)

ADR-003 (Docker + K8s) soporta esta estrategia

Validado en sesión 36