🧠 Arquitectura General – Thea IA 3.0
Este documento describe la arquitectura, componentes, flujos y mejores prácticas de Thea IA 3.0, versión estable y modular lista para despliegue productivo.

🌐 Visión General
Thea IA está diseñada como una plataforma asíncrona, modular y persistente, con:

Máquina de estados finitos (FSM) colaborativa.

Agentes autónomos e inteligentes conectados por un CoreRouter asíncrono.

ContextManager persistente y escalable.

🧩 Capas Principales
Capa	Descripción
Core Router (FSM)	Orquesta estados y mensajes, delega intents, asegura ciclo conversacional.
Context Manager	Memoria activa, persistencia por usuario (SQLite/PostgreSQL).
Agentes	Lógica autónoma — agenda, notas, hábitos, contexto, eventos, etc.
NLP / ML Pipeline	spaCy, scikit-learn para intents y entidades.
Database Layer	SQLAlchemy 2 async, Alembic, soporte multibase y migraciones versionadas.
API REST (FastAPI)	Endpoints, observabilidad (/health, /metrics), webhooks.
Scripts & Automation	Deploy y setup CI/CD, pruebas automatizadas en Codespaces/Actions.
Tests	Unitarios e integración (Agents/Core/FSM).
🔄 Flujo General de Interacción
El usuario envía un mensaje (Telegram/REST).

El Adaptador envía la petición al CoreRouter.

NLP/ML detecta intención y extrae entidades.

FSM decide agente a despachar.

El agente ejecuta lógica, opera sobre DB, gestiona memoria.

ContextManager actualiza estado usuario, persiste contexto.

Adaptador responde estructurado al canal.

🧭 Diagrama (Mermaid recomendado)
(graph TD ... copiar tu diagrama aquí).

🚀 Ejemplo de Flujo — Creación de Evento
Paso	Descripción
1	Usuario: “Reunión con X mañana a las 11.”
2	Adaptador → CoreRouter
3	NLP: intent create_event, extrae fecha/contacto
4	FSM activa event_agent
5	Agente crea entrada en DB
6	ContextManager actualiza estado y contexto
7	Respuesta final: “Reunión programada para mañana a las 11.”
🧱 Diseño Modular y Extensible
Agentes independientes agregables vía registry.

Asincronía total — operaciones no bloqueantes.

Plug-ins de canales — adaptadores por Telegram, Web, REST...

Configuración y setup único — scripts en /scripts/.

CI/CD y tests automatizados — integración total con Actions.

🧬 Estructura del Proyecto
(copiar tu árbol y subcarpetas reales aquí: scripts/, src/theaia/, ml/, etc.).

📊 Stack Tecnológico
Capa	Tecnología
API/Framework	FastAPI, Uvicorn
FSM Engine	Transitions (callbacks async personalizados)
ORM/DB	SQLAlchemy 2 async, Alembic, PostgreSQL
NLP/ML	spaCy 3, scikit-learn
Tests	pytest, pytest-asyncio, coverage
Infra	Docker, GH Actions, Codespaces, Prometheus
🔍 Buenas Prácticas
Separación de responsabilidades (Core, Agentes, DB).

Documentación modular.

Logs estructurados, métricas y health-checks.

Migraciones versionadas y clear rollback.

Referencia histórica y legacy en archive/.

✅ Estado Actual
FSM, migraciones y agentes validados.

CI/CD y scripts funcionales.

Documentación y diagramas al día.

Para legacy y versiones previas, ver /docs/architecture/archive/.

Thea IA 3.0 — Arquitectura modular, inteligente y lista para escalar. © 2025 Álvaro Fernández Mota