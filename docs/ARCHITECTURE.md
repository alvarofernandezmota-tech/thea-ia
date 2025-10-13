# Arquitectura General – Thea IA 2.0

Este documento describe la arquitectura, flujos y componentes principales del sistema Thea IA 2.0.

---

## 🌐 Visión de alto nivel

Thea IA 2.0 está basada en una arquitectura **modular**, **desacoplada** y **escalable**. Cada agente implementa su propia lógica, y la orquestación central (FSM/Router) coordina los estados y rutas, permitiendo una integración sencilla de nuevos módulos y adaptadores.

---

## 🏗️ Componentes principales

- **Agentes (src/theaia/agents/):** FSM y lógica para agenda, notas, consultas, ayuda y fallback.  
- **Adaptadores (src/theaia/adapters/):** Conectores para Telegram, webhooks y API REST.  
- **Core/Router (src/theaia/core/):** Orquestador central, máquina de estados finitos y gestor de contexto.  
- **ML/NLP (src/theaia/ml/):** Modelos y pipelines para detección de intenciones y extracción de entidades.  
- **Database/Repositories (src/theaia/database/):** Modelos ORM SQLAlchemy y repositorios de acceso a datos.  
- **Servicios (src/theaia/services/):** Lógica de negocio para eventos, notas, usuarios y programación de recordatorios.  
- **API REST (src/theaia/api/):** Endpoints FastAPI para interacción externa y monitoreo.  
- **Utilidades (src/theaia/utils/):** Validadores, formateadores y excepciones personalizadas.  
- **Pruebas (src/theaia/tests/):** Estructura para tests unitarios, integración y E2E.  
- **Automatización (scripts/):** Scripts para setup, despliegue, migraciones, linting, backups y ejecución de tests.

---

## 🔄 Flujo típico de interacción

1. El usuario envía un mensaje (Telegram, API u otro canal).  
2. El adaptador recibe la petición y la envía al Core/Router.  
3. El sistema detecta la intención, estado y entidades usando ML/NLP.  
4. El Router/FSM decide qué agente activar y define la respuesta.  
5. El agente procesa contexto y datos; si es necesario, interactúa con la base de datos.  
6. Se devuelve la respuesta formateada al canal original y se actualizan logs y contexto.

---

## 🧬 Diagrama simplificado

Usuario → Adaptador → Core/Router/FSM → Agente → DB/ML/NLP → Respuesta → Canal

text

---

## 🚀 Ejemplo de flujo: creación de evento

1. **Usuario:** “Agendar cita médica mañana a las 12”  
2. **Telegram Adapter** → Core/Router  
3. **FSM** detecta intent `create_event`, extrae fecha/hora y entidad  
4. **Agenda Agent** crea el evento en la base de datos  
5. **Respuesta:** “Cita médica agendada para mañana a las 12”  

---

## 🧱 Diseño modular y escalabilidad

- **Cada módulo es independiente:** agregar un nuevo agente solo requiere implementar su FSM y registrarlo en el Router.  
- **Modelos intercambiables:** se pueden sustituir o ampliar los pipelines ML/NLP sin afectar otros componentes.  
- **Adaptadores legibles:** añadir nuevos canales (Slack, WhatsApp, SMS) con mínima configuración.  
- **Scripts de automatización:** facilitan despliegue y mantenimiento en CI/CD y entornos de producción.

---

## 🔍 Buenas prácticas arquitectónicas

- **Separation of Concerns:** lógica de negocio, datos y presentación desacoplados.  
- **Documentación constante:** interfaces, variables y flujos documentados en código y en `docs/`.  
- **Health checks y métricas:** endpoints `/health` y `/metrics` para monitoreo continuo.  
- **Logging estructurado:** trazabilidad de transiciones FSM y acciones de agentes.  
- **Versionado de migraciones:** Alembic para gestionar cambios en la base de datos.

## 📂 Estructura de Carpetas y Archivos

theaia/
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── docker-compose.yml
├── Dockerfile
├── Makefile
├── src/
│ └── theaia/
│ ├── main.py
│ ├── config/
│ │ ├── settings.py
│ │ └── logging_config.py
│ ├── core/
│ │ ├── state_machine.py
│ │ ├── callbacks.py
│ │ ├── context_manager.py
│ │ ├── router.py
│ │ └── bot_factory.py
│ ├── adapters/
│ │ ├── telegram_adapter.py
│ │ └── webhook_handler.py
│ ├── services/
│ │ ├── event_service.py
│ │ ├── note_service.py
│ │ ├── user_service.py
│ │ └── scheduler_service.py
│ ├── models/
│ │ ├── user.py
│ │ ├── event.py
│ │ ├── note.py
│ │ └── context.py
│ ├── database/
│ │ ├── connection.py
│ │ └── repositories/
│ │ ├── base.py
│ │ ├── user_repository.py
│ │ ├── event_repository.py
│ │ └── note_repository.py
│ ├── ml/
│ │ ├── intent_detector/
│ │ └── ner_extractor/
│ ├── agents/
│ │ ├── base_agent.py
│ │ ├── registry.py
│ │ └── event_agent/…
│ ├── utils/
│ │ ├── validators.py
│ │ ├── formatters.py
│ │ └── exceptions.py
│ └── api/
│ ├── health.py
│ └── metrics.py
├── src/theaia/tests/
│ ├── agents/
│ ├── core/
│ ├── database/
│ ├── services/
│ ├── ml/
│ ├── utils/
│ ├── fixtures/
│ ├── e2e/
│ ├── unit/
│ └── integration/
├── scripts/
│ ├── setup.sh
│ ├── deploy.sh
│ ├── migrate.sh
│ ├── lint.sh
│ ├── backup.sh
│ ├── entrypoint.sh
│ ├── test_runner.sh
│ └── README.md
├── docs/
│ ├── ARCHITECTURE.md
│ ├── DEPLOYMENT.md
│ ├── API.md
│ ├── adr/
│ ├── diagrams/
│ └── retros/
├── alembic/
│ ├── alembic.ini
│ ├── env.py
│ └── versions/
├── .github/
│ └── workflows/
├── monitoring/
│ ├── grafana/
│ ├── prometheus/
│ └── alerts/
└── deployment/
├── k8s/
├── helm/
└── terraform/

text

---

## Apéndice: Auditoría Fase 1 (13/10/2025)

Durante la Fase 1 se validaron y completaron los siguientes módulos y carpetas:

- **src/theaia/utils/**  
  - `README.md` (documentación de utilidades)  
  - `TESTING.md` (guía de testing de utilidades)  
- **scripts/**  
  - Scripts de automatización:  
    - `setup.sh`, `deploy.sh`, `migrate.sh`, `lint.sh`, `backup.sh`, `entrypoint.sh`, `test_runner.sh`  
  - `README.md` (documentación de uso)  
- **src/theaia/tests/**  
  - Estructura de carpetas para tests:  
    - `agents/`, `core/`, `database/`, `services/`, `ml/`, `utils/`, `fixtures/`, `e2e/`, `unit/`, `integration/`  
  - `README.md` (guía global de testing)  

---

Con este esquema, el documento mostrará de manera clara y completa la organización actual de Thea IA 2.0 antes de la auditoría.

## Apéndice: Auditoría Fase 1 (13/10/2025)

Durante la Fase 1 se validaron y completaron los siguientes módulos y carpetas:

- **src/theaia/utils/**  
  - `README.md` (documentación de utilidades)  
  - `TESTING.md` (guía de testing de utilidades)  
- **scripts/**  
  - Scripts de automatización:  
    - `setup.sh`, `deploy.sh`, `migrate.sh`, `lint.sh`, `backup.sh`, `entrypoint.sh`, `test_runner.sh`  
  - `README.md` (documentación de uso)  
- **src/theaia/tests/**  
  - Estructura de carpetas para tests:  
    - `agents/`, `core/`, `database/`, `services/`, `ml/`, `utils/`, `fixtures/`, `e2e/`, `unit/`, `integration/`  
  - `README.md` (guía global de testing)  

