# 🧠 Arquitectura General – Thea IA 3.0

Este documento describe la arquitectura, componentes, flujos y buenas prácticas del sistema **Thea IA 3.0**, versión estable y modular lista para despliegue productivo.

---

## 🌐 Visión General

Thea IA 3.0 está diseñada como una plataforma **asíncrona**, **modular** y **persistente**, combinando una **máquina de estados finitos (FSM)** con **agentes inteligentes independientes** que dialogan mediante un **CoreRouter asíncrono** y un **ContextManager persistente**.

Su arquitectura permite comunicación fluida entre NLP, FSM y base de datos sin bloqueos, favoreciendo escalabilidad y carga concurrente en múltiples adaptadores (Telegram, API, Web, etc.).

---

## 🧩 Capas Principales

| Capa | Descripción |
|------|--------------|
| **Core Router (FSM Engine)** | Núcleo de orquestación de estados y mensajes. Dirige intenciones y transiciones entre agentes. |
| **Context Manager** | Sistema de memoria activa que mantiene el histórico de conversación y estado por usuario (usando SQLite o PostgreSQL). |
| **Agentes** | Cada agente representa una lógica autónoma (FSM propia): agenda, notas, hábitos, contexto, evento, etc. |
| **NLP / ML Pipeline** | Modelos spaCy + scikit‑learn para detección de intención y extracción de entidades. |
| **Database Layer** | SQLAlchemy 2 async + Alembic para ORM, migraciones y persistencia de datos. |
| **API REST (FastAPI)** | Endpoints para interacción externa, observabilidad (`/health`, `/metrics`) y webhooks. |
| **Scripts & Automation** | Configuración de entorno, pruebas y deploy automatizado en Codespaces / Actions. |
| **Tests** | Pruebas unitarias (Agents/Core) e integración FSM disponibles en `src/theaia/tests/`. |

---

## 🔄 Flujo General de Interacción

1. **El usuario** envía un mensaje (vía Telegram o REST).  
2. **El Adaptador** transforma y envía la petición al **CoreRouter**.  
3. **NLP/ML** procesa la intención y extrae entidades.  
4. **FSM Engine** determina qué agente debe responder.  
5. **El Agente activo** ejecuta acciones (lógica, DB, memoria).  
6. **ContextManager** actualiza estado y persistencia del usuario.  
7. **El Adaptador** devuelve una respuesta estructurada al canal original.  

---

## 🧭 Diagrama de Arquitectura (Mermaid)

graph TD
A[Usuario o Canal externo] --> B[Adaptador / Endpoint API]
B --> C[CoreRouter / FSM Engine]
C --> D[ContextManager]
C --> E[NLP / ML Pipeline]
E --> C
C --> F[Agente activo]
F --> G[(Base de Datos)]
G --> F
F --> D
D --> B
B --> A

text

---

## 🚀 Ejemplo de Flujo – Creación de Evento

| Paso | Descripción |
|------|--------------|
| **1** | El usuario envía “Reunión con María mañana a las 11”. |
| **2** | Adaptador envía texto al CoreRouter. |
| **3** | NLP detecta intent `create_event` y extrae fecha / contacto. |
| **4** | FSM activa el `event_agent`. |
| **5** | El agente crea la entrada en la base de datos vía ORM. |
| **6** | ContextManager actualiza estado del usuario y respuesta. |
| **7** | El sistema devuelve: “Reunión con María programada para mañana a las 11.” |

---

## 🧱 Diseño Modular y Extensible

- **Agentes independientes:** añadir uno nuevo solo requiere registrarlo en `registry.py`.  
- **Asincronía total:** `asyncpg` y `aiosqlite` para operaciones no bloqueantes.  
- **Plug‑ins de canales:** Telegram, Web, REST → pueden añadirse adaptadores personalizados.  
- **Configuración de entorno única:** `scripts/setup_env.sh` configura todas las dependencias.  
- **CI/CD integrado:** tests y linting automatizados con GitHub Actions.  

---

## 🧬 Estructura Completa del Proyecto

theaia/
├── scripts/
│ ├── setup_env.sh
│ ├── deploy.sh
│ ├── migrate.sh
│ └── lint.sh
├── src/theaia/
│ ├── api/
│ │ ├── main.py
│ │ ├── health.py
│ │ └── metrics.py
│ ├── core/
│ │ ├── router.py
│ │ ├── context_manager.py
│ │ ├── database.py
│ │ ├── fsm/
│ │ │ └── state_machine.py
│ │ └── event_bus.py
│ ├── agents/
│ │ ├── base_agent.py
│ │ ├── agenda_agent.py
│ │ ├── note_agent.py
│ │ ├── event_agent.py
│ │ ├── habit_agent.py
│ │ ├── context_agent.py
│ │ └── registry.py
│ ├── ml/
│ │ ├── intent_detector/
│ │ └── ner_extractor/
│ ├── database/
│ │ ├── connection.py
│ │ └── repositories/
│ ├── utils/
│ │ ├── validators.py
│ │ ├── formatters.py
│ │ └── exceptions.py
│ └── tests/
│ ├── unit/
│ ├── integration/
│ └── e2e/
└── docs/
├── README.md
├── architecture.md
├── api_reference.md
└── deployment.md

text

---

## 🔍 Buenas Prácticas Arquitectónicas

- **Separación de responsabilidades:** Core, Agentes y Persistencia desacoplados.  
- **Documentación constante:** todos los módulos con docstrings y README.  
- **Logs estructurados:** registro FSM → Prometheus.  
- **Monitorización:** endpoints de salud y métricas activas.  
- **Migraciones versionadas:** Alembic gestiona todos los esquemas.

---

## 📊 Stack Tecnológico

| Capa | Tecnología |
|------|-------------|
| **API / Framework** | FastAPI 0.104 + Uvicorn 0.24 |
| **FSM Engine** | Transitions 0.9.3 (extendido con callbacks asíncronos) |
| **ORM / DB** | SQLAlchemy 2 async + Alembic 1.12 / PostgreSQL + SQLite |
| **NLP / ML** | spaCy 3.7 + scikit‑learn 1.3 |
| **Mensajería / Asincronía** | asyncio / aiohttp / asyncpg |
| **Testing** | pytest 8.4 + pytest‑asyncio + coverage |
| **Infraestructura** | Docker / GitHub Actions / Codespaces / Prometheus + Grafana |

---

## ✅ Estado Actual

- FSM v2 operativa y estable  
- Migraciones funcionales (Alembic / SQLite)  
- Agentes registrados (Agenda, Notas, Contexto, Eventos, Hábitos)  
- CI/CD en configuración con Actions  
- Documentación y scripts validados en Codespaces  

---

**Thea IA 3.0 — Arquitectura modular, inteligente y lista para escalar. © 2025 Álvaro Fernández Mota**