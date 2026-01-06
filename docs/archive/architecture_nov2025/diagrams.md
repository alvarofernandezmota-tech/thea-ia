📐 Diagramas de Arquitectura — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-08 17:40 CET (Sesión 36)
Responsable: Architecture Team / Álvaro Fernández Mota (CEO)
Estado: ✅ Activo

📋 Propósito
Recopilación de diagramas técnicos y visuales de todos los flujos clave del ecosistema THEA IA, con leyendas claras y enlaces cruzados a documentos relevantes.

Audiencia:

Arquitectos visualizando flujos

Developers entendiendo interacciones

Onboarding nuevos team members

📑 Índice de diagramas
Diagrama general de arquitectura

Flujo conversacional (FSM)

Orquestación multi-agente

Integración de adapters

Estructura de persistencia

Escalabilidad y deployment

1. Diagrama general de arquitectura
text
┌──────────────────────────────────────────────────────────────┐
│                    THEA IA Ecosystem v0.14.0                 │
├──────────────────────────────────────────────────────────────┤
│
│  ENTRADA (Adapters)
│  ├─ Telegram Bot
│  ├─ REST API
│  ├─ Web Client
│  └─ WhatsApp (futuro)
│
│  ↓
│
│  CoreRouter (Normalización)
│  ├─ Validación entrada
│  ├─ Rate limiting
│  └─ Auth/RBAC
│
│  ↓
│
│  FSM Engine v2 (Orquestación)
│  ├─ State machine (pre/post callbacks)
│  ├─ Context manager
│  └─ Intent classification
│
│  ↓
│
│  ML/NLP Pipeline
│  ├─ Intent Detector (spaCy)
│  └─ Entity Extractor
│
│  ↓
│
│  Agent Selector (BotFactory)
│  ├─ Router → Agenda Agent
│  ├─ Router → Notes Agent
│  ├─ Router → Events Agent
│  ├─ Router → Query Agent
│  └─ Router → Fallback Agent
│
│  ↓
│
│  Persistencia
│  ├─ PostgreSQL (prod)
│  ├─ JSON Fallback (local)
│  └─ Redis Cache
│
│  ↓
│
│  Observabilidad (H11)
│  ├─ Prometheus (métricas)
│  ├─ Grafana (dashboards)
│  ├─ Loki (logs)
│  └─ Jaeger (tracing)
│
│  ↓
│
│  SALIDA (Adapters)
│  ├─ Respuesta a Telegram
│  ├─ JSON a REST API
│  ├─ Actualizar Web Client
│  └─ Mensaje WhatsApp
│
└──────────────────────────────────────────────────────────────┘
Referencias:

Architecture Overview

ADRs

2. Flujo conversacional (FSM)
text
┌─────────────────────────────────────┐
│  Usuario envía mensaje (Telegram)   │
└────────────┬────────────────────────┘
             ↓
    ┌────────────────────┐
    │ Adapter (normalize)│
    │ input → JSON       │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ FSM.pre_callbacks()│
    │ (validación, auth)│
    └────────┬───────────┘
             ↓
    ┌────────────────────────────────┐
    │ Intent Detector + Entity Ex.   │
    │ (spaCy: intent + entities)     │
    └────────┬───────────────────────┘
             ↓
    ┌────────────────────┐
    │ Agent Selector     │
    │ (¿Agenda? Notes?)  │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Agent Handler      │
    │ (ejecuta lógica)   │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Database           │
    │ (persist contexto) │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ FSM.post_callbacks()
    │ (notificaciones)   │
    └────────┬───────────┘
             ↓
    ┌────────────────────┐
    │ Adapter (format)   │
    │ JSON → Telegram    │
    └────────┬───────────┘
             ↓
┌─────────────────────────────────────┐
│  Usuario recibe respuesta           │
└─────────────────────────────────────┘
Latencia esperada: <500ms
Estados FSM: ready → processing → persisting → responding
Callbacks: pre_transition, post_transition, on_error

3. Orquestación multi-agente
text
┌──────────────────────────┐
│ FSM Engine (Orquestador) │
└────────────┬─────────────┘
             ↓
   ┌─────────────────────┐
   │ BotFactory (Registry)│
   │ agent_type → Agent  │
   └────────┬────────────┘
            ↓
   ┌────────────────────────────────────────┐
   │ Intent: "crear evento mañana"         │
   │ → Agente: EventAgent                  │
   └────────┬─────────────────────────────┘
            ↓
   ┌────────────────────────────────────────┐
   │ EventAgent.process()                  │
   │ ├─ Extraer fecha (NLP)                │
   │ ├─ Consultar Calendar API             │
   │ ├─ Crear evento                       │
   │ └─ Persistir en DB                    │
   └────────┬─────────────────────────────┘
            ↓
   ┌────────────────────────────────────────┐
   │ Contexto guardado:                    │
   │ {user, event_id, timestamp, ...}      │
   └────────┬─────────────────────────────┘
            ↓
   ┌────────────────────────────────────────┐
   │ Callback: Notificar usuario           │
   │ ├─ Telegram: "Evento creado ✓"       │
   │ └─ Email: "Reunión mañana"            │
   └────────────────────────────────────────┘
Agentes disponibles:

AgendaAgent (eventos calendarios)

NotesAgent (notas y tags)

EventAgent (procesamiento eventos)

QueryAgent (búsqueda)

FallbackAgent (comandos desconocidos)

4. Integración de adapters
text
┌────────────────────┐     ┌────────────────────┐
│  Telegram Adapter  │     │  REST API Adapter  │
│  (Bot API)         │     │  (FastAPI)         │
└────────┬───────────┘     └────────┬───────────┘
         ↓                          ↓
┌────────────────────┐     ┌────────────────────┐
│ normalize_input()  │     │ normalize_input()  │
│ raw → standard     │     │ payload → standard │
└────────┬───────────┘     └────────┬───────────┘
         └────────────┬─────────────┘
                      ↓
            ┌─────────────────────┐
            │   CoreRouter        │
            │ (FSM Engine)        │
            └────────┬────────────┘
                     ↓
        ┌────────────────────────┐
        │ format_output()        │
        │ response → channel fmt │
        └────────┬───────────────┘
                 ↓
        ┌────────────────────┐     ┌────────────────────┐
        │ Telegram enviar    │     │ REST responder     │
        │ (message.reply())  │     │ (JSON response)    │
        └────────────────────┘     └────────────────────┘
Adapters soportados:

Telegram (webhook + polling)

REST API (HTTP)

Slack (events API)

Discord (gateway)

WhatsApp (futuro)

5. Estructura de persistencia
text
┌──────────────────────────────────────┐
│ Application Layer                    │
│ (FSM, Agents, Context)              │
└────────────────┬─────────────────────┘
                 ↓
        ┌────────────────┐
        │ Repository     │
        │ Pattern        │
        │ (abstraction)  │
        └────────┬───────┘
                 ↓
    ┌────────────────────────┐
    │ Adapter Pattern        │
    │ ├─ PostgreSQL Impl     │
    │ └─ JSON Impl (fallback)│
    └────────┬───────────────┘
             ↓
    ┌───────────────────────────────────┐
    │ PostgreSQL (Producción)           │
    │ ├─ Users (id, name, email)        │
    │ ├─ Sessions (user_id, context)    │
    │ ├─ Events (user_id, event_data)   │
    │ ├─ Notes (user_id, note_content)  │
    │ └─ Audit Log (all operations)     │
    │                                   │
    │ + Redis Cache (session context)   │
    │ + JSON Fallback (local dev)       │
    └───────────────────────────────────┘
Modelos principales:

User (autenticación, preferencias)

Session (contexto conversacional)

Event (eventos calendarios)

Note (notas con tags)

AuditLog (compliance)

6. Escalabilidad y deployment
text
┌──────────────────────────────────────┐
│  Cloud Provider (AWS/GCP/Azure)      │
├──────────────────────────────────────┤
│
│  CDN / Load Balancer
│  └─ Distribución geográfica
│
│  ↓
│
│  Kubernetes Cluster (H09)
│  ├─ Service Mesh (Istio)
│  ├─ API Gateway (Kong)
│  └─ Pod Autoscaler (HPA)
│
│  ├─ Deployment: FSM API (3-20 replicas)
│  ├─ StatefulSet: PostgreSQL (HA)
│  ├─ DaemonSet: Prometheus/Loki (logging)
│  └─ Ingress: HTTP routing
│
│  ↓
│
│  Storage
│  ├─ PostgreSQL RDS (managed)
│  ├─ Redis Cluster (cache)
│  └─ S3/GCS (backups + artifacts)
│
└──────────────────────────────────────┘
Scaling policies:

CPU: target 70%

Memory: target 80%

Throughput: 1000+ req/s

📌 Meta-información
Campo	Valor
Archivo	docs/architecture/diagrams.md
Versión	v0.14.0
Última revisión	2025-11-08 17:40 CET (Sesión 36)
Responsable	Architecture Team / CEO
Estado	✅ Activo
🔗 Enlaces relacionados
Overview — Visión general

Decisiones — ADRs

Deployment — CI/CD

Scalability — Escalado

Adapters — Sistema adapters

Agents — Sistema multi-agente

🛡️ Auditoría y cumplimiento
Parte del Hito 36.1 (docs/architecture/)

Diagramas ASCII para reproducibilidad

Validado en sesión 36