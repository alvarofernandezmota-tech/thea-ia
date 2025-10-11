# Thea IA 2.0

🤖 **Agente conversacional inteligente** con máquina de estados finitos (FSM) y procesamiento de lenguaje natural (NLP) para gestión automatizada de eventos, notas y recordatorios.

---

## 🎯 Visión del proyecto

Thea IA es un asistente personal conversacional diseñado para transformar la gestión de eventos y tareas a través de inteligencia artificial. Combina FSM avanzada, NLP y arquitectura modular para ofrecer una experiencia de usuario natural e intuitiva.

### Características principales
- 🧠 **FSM inteligente** para gestión de estados conversacionales
- 🔗 **Adaptadores multi-plataforma** (Telegram, webhooks, API REST)
- 📊 **ML/NLP** para detección de intenciones y extracción de entidades
- 🗄️ **Persistencia robusta** con PostgreSQL y migraciones Alembic
- 🐳 **Containerización** completa con Docker y orquestación
- 🔍 **Monitoreo** integrado con métricas y alertas
- ⚡ **API escalable** con FastAPI y endpoints profesionales

---

## 📂 Estructura del proyecto

theaia/
├── README.md # Documentación principal
├── .env.example # Variables de entorno ejemplo
├── .gitignore # Exclusiones Git
├── pyproject.toml # Configuración proyecto Python
├── requirements.txt # Dependencias producción
├── requirements-dev.txt # Dependencias desarrollo
├── docker-compose.yml # Orquestación contenedores
├── Dockerfile # Imagen Docker aplicación
├── Makefile # Comandos automatizados
├── src/
│ └── theaia/
│ ├── init.py
│ ├── main.py # Punto de entrada aplicación
│ ├── config/
│ │ ├── settings.py # Configuración por entorno
│ │ └── logging_config.py # Configuración logging
│ ├── core/
│ │ ├── state_machine.py # FSM principal
│ │ ├── callbacks.py # Callbacks estados/transiciones
│ │ ├── context_manager.py # Gestión estado usuario
│ │ ├── router.py # Enrutamiento a agentes
│ │ └── bot_factory.py # Creación instancias bot
│ ├── adapters/
│ │ ├── telegram_adapter.py # Conexión Telegram
│ │ └── webhook_handler.py # Endpoint webhooks
│ ├── services/
│ │ ├── event_service.py # Lógica eventos
│ │ ├── note_service.py # Lógica notas
│ │ ├── user_service.py # Lógica usuarios
│ │ └── scheduler_service.py # Lógica recordatorios
│ ├── models/
│ │ ├── user.py # Modelo usuario
│ │ ├── event.py # Modelo evento
│ │ ├── note.py # Modelo nota
│ │ └── context.py # Modelo contexto
│ ├── database/
│ │ ├── connection.py # Conexión BD
│ │ └── repositories/
│ │ ├── base.py # Clase base repositorios
│ │ ├── user_repository.py
│ │ ├── event_repository.py
│ │ └── note_repository.py
│ ├── ml/
│ │ ├── intent_detector/ # Modelos intent detection del Core
│ │ │ ├── train.py # Script entrenamiento
│ │ │ ├── dataset/ # Datos anotados
│ │ │ ├── models/ # Modelos exportados
│ │ │ └── vocab.json # Vocabulario inicial
│ │ └── ner_extractor/ # Modelo NER del Core
│ │ ├── train.py
│ │ ├── dataset/
│ │ ├── models/
│ │ └── config.json
│ ├── agents/
│ │ ├── init.py
│ │ ├── base_agent.py # Interfaz BaseAgent
│ │ ├── registry.py # Registro dinámico de agentes
│ │ ├── event_agent/ # Sub-agente eventos
│ │ ├── note_agent/ # Sub-agente notas
│ │ ├── query_agent/ # Sub-agente consultas
│ │ ├── help_agent/ # Sub-agente ayuda
│ │ └── scheduler_agent/ # Sub-agente recordatorios
│ ├── utils/
│ │ ├── validators.py # Validadores
│ │ ├── formatters.py # Formateadores
│ │ └── exceptions.py # Excepciones personalizadas
│ └── api/
│ ├── health.py # Endpoint salud
│ └── metrics.py # Endpoint métricas
├── tests/
│ ├── unit/ # Tests unitarios
│ ├── integration/ # Tests integración
│ ├── e2e/ # Tests end-to-end
│ └── fixtures/ # Datos prueba
├── docs/
│ ├── ARCHITECTURE.md # Diagrama modular detallado
│ ├── DEPLOYMENT.md # Guía despliegue
│ ├── API.md # Especificaciones endpoints
│ ├── adr/ # Architecture Decision Records
│ ├── diagrams/ # Diagramas técnicos
│ └── retros/ # Retrospectivas desarrollo
├── scripts/
│ ├── setup.sh # Script instalación local
│ ├── deploy.sh # Script despliegue
│ ├── migrate.sh # Script migraciones BD
│ └── lint.sh # Script linting/formato
├── alembic/
│ ├── alembic.ini # Config migraciones
│ ├── env.py # Entorno migraciones
│ └── versions/ # Versiones migraciones BD
├── .github/
│ ├── workflows/
│ │ ├── ci.yml # CI básico
│ │ ├── cd.yml # Despliegue continuo
│ │ └── security.yml # Análisis seguridad
│ └── ISSUE_TEMPLATE/ # Plantillas issues
├── monitoring/
│ ├── grafana/ # Dashboards
│ ├── prometheus/ # Métricas
│ └── alerts/ # Configuración alertas
└── deployment/
├── k8s/ # Manifiestos Kubernetes
├── helm/ # Charts Helm
└── terraform/ # Infraestructura como código

text

---
## 🛣️ Roadmap de desarrollo
en pagina aparte docs/roadmap.md

## ⚡ Instalación rápida

### Prerrequisitos
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose
- Git

### Configuración desarrollo

1. **Clonar repositorio:**
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia

text

2. **Configurar entorno:**
make setup
cp .env.example .env

Editar .env con tus configuraciones
text

3. **Levantar servicios:**
docker-compose up -d
make migrate

text

4. **Ejecutar aplicación:**
make run

text

---

### Comandos útiles

make test # Ejecutar tests
make lint # Linting y formato código
make format # Formatear código con Black
make migrate # Ejecutar migraciones BD
make logs # Ver logs aplicación
make clean # Limpiar archivos temporales

text

---

## 🤝 Guía de contribución

### Flujo de trabajo

1. **Fork del repositorio** y crea tu rama:
git checkout -b feature/descripcion-cambio

text

2. **Sigue convenciones:**
- Commits: Conventional Commits  
- Código: PEP8 + Black  
- Tests: Cobertura mínima 80%

3. **Antes del PR:**
make test && make lint

text

4. **Crea PR** con descripción clara y referencia issues.

### Normas de código
- **Tipado:** Usar type hints en funciones públicas  
- **Docstrings:** Documentar clases y métodos complejos  
- **Testing:** Tests para nueva funcionalidad  
- **Logging:** Usar niveles adecuados  

---

## 🛠️ Stack tecnológico

### Backend & Core
- Python 3.11+, FastAPI, Transitions, SQLAlchemy, Alembic, Pydantic

### Base de datos & Caché
- PostgreSQL 14+, Redis

### ML/NLP & IA
- spaCy, scikit-learn, Transformers (opcional)

### Integración & Comunicación
- aiogram, aiohttp, WebSockets

### DevOps & Infraestructura
- Docker, Kubernetes, GitHub Actions, Prometheus, Grafana, Terraform

---Abre docs/README-complete.md
Agrega este bloque actualizado al final o en la sección de testing/documentación:

text
## Resultados de tests y cobertura

- **Tests unitarios agentes:** 19/19 en verde ✅
- **Cobertura generada con pytest-cov**  
  Ejecución:
$env:PYTHONPATH = "src"
pytest --cov=src/theaia --cov-report=html src\theaia\agents\agenda_agent\tests\ src\theaia\agents\scheduler_agent\tests\ src\theaia\agents\event_agent\tests\ src\theaia\agents\note_agent\tests\ src\theaia\agents\query_agent\tests\ src\theaia\agents\help_agent\tests\ src\theaia\agents\fallback_agent\tests\

text
- **Visualización:**  
Abre `htmlcov/index.html` para ver el reporte visual de cobertura.

---

### 2. Prepara y ejecuta el test E2E del Core

1. **Crea el archivo:**
mkdir src\theaia\tests\e2e
notepad src\theaia\tests\e2e\test_core_flow.py

text

2. **Pega este ejemplo de test E2E:**

from theaia.core.router import CoreRouter

def test_e2e_agenda_flow():
router = CoreRouter()
uid = "u1"
state = "initial"
context = {}

text
# Inicia proceso de agenda
resp, state, context = router.handle(uid, "quiero agendar cita", state, context)
assert "fecha" in resp.lower()
assert state == "awaiting_datetime"

resp, state, context = router.handle(uid, "2025-10-10 09:00", state, context)
assert "confirmas" in resp.lower()
assert state == "awaiting_confirmation"

resp, state, context = router.handle(uid, "sí", state, context)
assert "confirmada" in resp.lower()
assert state == "completed"
text

3. **Lanza el test:**
pytest src\theaia\tests\e2e\

text

---

Cuando esto pase verde y quede reflejado en cobertura, puedes actualizar el README de nuevo con los resultados E2E.

¿Quieres que prepare más flujos E2E (por ejemplo scheduler, event, fallback, etc.)? ¿Copias y pegas la parte del README y luego continuamos, o prefieres primero revisar el test e2e? ¡Avísame qué prefieres!

**¡Únete al proyecto Thea IA y revoluciona la gestión de eventos con inteligencia artificial!** 🚀

------------------------------------------------------------------------------------
-----------------------------------------------------------------
------------------------------------------
---------------------
---------------------


README NUEVO 10/10/25


# Thea IA 2.0 – README

## 🚀 Visión & Propósito

**Thea IA 2.0** es una plataforma modular, escalable y extensible para la orquestación inteligente de agentes conversacionales y de procesos automáticos (ML/NLP, servicios, adaptadores y APIs). Su diseño flexible permite incorporar nuevos agentes, adaptar la lógica según el canal y añadir mejoras evolutivas (TheaScaler, AutoML, Ecosistema de agentes).

---

## 🌟 Objetivos Principales

- Integrar agentes nativos: agenda, evento, nota, scheduler, consultas, ayuda, fallback.
- Orquestar flujos conversacionales E2E robustos, testables y verificables.
- Facilitar la integración multiplataforma (Telegram/webhook/API).
- Permitir la monitorización, métrica y mejora continua del sistema.
- Preparar la arquitectura para autoescalado y evolución entre agentes.

---

## 🏗️ Arquitectura Modular

El proyecto está organizado en carpetas claramente separadas por función:

- **src/theaia/agents/**: Cada agente con su lógica, FSM y tests unitarios.
- **src/theaia/core/**: Router y registro central, gestión del flujo de intenciones y estados.
- **src/theaia/adapters/**: Integraciones Telegram, webhook y otros canales.
- **src/theaia/database/**: Modelado, repositorios y migraciones (SQLAlchemy/Alembic).
- **src/theaia/ml/**: Modelos ML/NLP para intents y entidades, pipelines de entrenamiento.
- **src/theaia/services/**: Lógica de negocio y servicios de backend.
- **src/theaia/api/**: Endpoints, validaciones Pydantic y documentación API.
- **src/theaia/config/**: Configuración central (.env, settings, schemas).
- **src/theaia/tests/**: Unitarios, E2E y mocks.
- **docs/**: Documentación técnica y de producto, esquemas, diccionarios y roadmaps.
- **scripts/**: Scripts de automatización, setup, despliegue y testeo.
- **tests/**: Pruebas del proyecto.

---

## ✅ Principales Funcionalidades

- Agentes conversacionales core, integrados y extensibles.
- Orquestación FSM robusta y validada.
- Soporte multicanal (adaptadores).
- Motor NLP configurable (spaCy, fastText, Transformers).
- APIs RESTful seguras y tipadas.
- Cobertura completa de tests unitarios y E2E.
- Monitoreo y alertas.
- Instalación, despliegue y CI/CD listos para producción.

---parte 2

## ⚙️ Instalación y Primeros Pasos

1. **Clona el repositorio**
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia

text

2. **Configura el entorno**
- Renombra y edita `.env.example` a `.env` con tus credenciales y rutas.

3. **Instala las dependencias**
pip install -r requirements.txt

O para desarrollo:
pip install -r requirements-dev.txt

text

4. **Configura la base de datos**
(Ajusta DATABASE_URL en tu .env)
alembic upgrade head

text

5. **Lanza la aplicación**
Para desarrollo
uvicorn src.theaia.api.main:app --reload

O usando Docker Compose
docker-compose up --build

text

---

## 🔎 Estructura del Proyecto

La estructura real incluye:

- **/src/theaia/agents/** *(agentes FSM, diálogo y lógica conversacional, tests)*
- **/src/theaia/adapters/** *(integraciones canales externos y webhooks)*
- **/src/theaia/ml/** *(modelos de IA, entrenamiento, clasificación, embeddings)*
- **/src/theaia/services/** *(negocio, APIs, backend)*
- **/src/theaia/database/** *(modelos ORM, repos, migraciones)*
- **/src/theaia/tests/** *(unitarios y E2E, mocks, pruebas integrales)*
- **/src/theaia/utils/** *(utilidades, helpers, diccionarios, vocabularios)*
- **/docs/** *(roadmaps, evolución, diccionario variables, bases de datos)*
- **/scripts/** *(automatizaciones: deploy, setup, migrate, lint, entrypoint)*
- **Ficheros raíz:** `.env.example`, `Dockerfile`, `Makefile`, `docker-compose.yml`, `requirements.txt`, `pyproject.toml`, `pytest.ini`

---

## 📦 Dependencias Principales

- **Python 3.9+**
- **FastAPI, Uvicorn** (API REST)
- **SQLAlchemy, Alembic** (ORM y migraciones)
- **Pydantic** (Validación)
- **spaCy, scikit-learn, fastText** (NLP/ML)
- **pytest, coverage, httpx, pytest-asyncio** (Testing auto)
- **Docker, Docker Compose** (Despliegue)
- **Telegram Bot API** (Integración canal externo)
- **Prometheus, Grafana** (Monitoreo - opcional)

--parte 3

---

## 🕹️ Ejemplo de Uso

**Consulta rápida del API REST**
curl -X POST "http://localhost:8000/api/v1/agents/agenda"
-H "accept: application/json"
-d '{"datetime": "2025-10-10T16:00:00", "title": "Cita Dentista"}'

text

**Agente Telegram**
- Ejecuta el script Telegram adapter y accede con tu bot.
- Mensaje de usuario: “Agendar cita médica mañana 12:00”
- Respuesta Thea IA: “¿Quieres confirmar la cita médica para mañana a las 12:00?”

---

## 🧪 Testing & Calidad

- Ejecución de tests unitarios
pytest -v src/theaia/tests/unit

text
- Ejecución de tests E2E
pytest -v src/theaia/tests/e2e

text
- Generación de reporte de cobertura
pytest --cov=src/theaia --cov-report=html

text

- Pruebas de estrés, mocks y migración de BDs listas para CI/CD

---

## ⚡ Notas para Desarrolladores

- Estructura modular por agentes y adaptadores, siguiendo separación de responsabilidades.
- Variables de entorno en `.env`, nunca directo en código.
- API REST documentada en `/docs` y vía OpenAPI/Swagger.
- Seguridad y validación exhaustiva por Pydantic en todos los endpoints.
- Tests auto y manuales, todos con reporte de cobertura.
- Scripts listos para setup, linting, migración y despliegue.
- Documentación técnica y de negocio en `/docs` (roadmap, diccionario, evolución, esquemas).
- Facilidad para añadir agentes, modelos ML y nuevos canales vía adaptadores.

---

## 📑 Documentación Técnica Adicional

- [docs/README-complete.md]: Usos avanzados, notas internas y tips.
- [docs/DICCIONARIO-VARIABLES.md]: Diccionario actualizado de variables y ejemplos
- [docs/ROADMAP.md]: Roadmap real y actualizado, con estimaciones y fechas reales
- [docs/EVOLUCION-PROCESO.md]: Evolución por fases y estados del desarrollo

---

*Para contribuciones, sugerencias o reportes de errores, abre un issue o contacta al equipo de Alvaro Fernandez Mota (alvarofernandezmota-tech).*

-- parte 4 

---

## 🗂️ Diccionario de Variables de Entorno (Resumen)

| Variable                   | Uso                                                  | Ejemplo/Valor por defecto                          |
|----------------------------|-----------------------------------------------------|----------------------------------------------------|
| DATABASE_URL               | URL de conexión a PostgreSQL                        | postgresql://user:pass@localhost:5432/theaia_db    |
| REDIS_HOST/PORT/DB/PASS    | Config redis                                        | localhost / 6379 / 0 / redis_password              |
| ENABLE_E2E                 | Activa modo pruebas E2E                             | true                                               |
| CONTEXT_DB_PATH            | DB temporal E2E                                     | /tmp/theaia_context.db                             |
| TELEGRAM_BOT_TOKEN         | Token Telegram bot                                  | your_token                                         |
| API_HOST/API_PORT          | Bind del servidor FastAPI                           | 0.0.0.0 / 8000                                     |
| SECRET_KEY                 | Clave secreta para API y JWT                        | ...                                                |
| GITHUB_TOKEN/GITHUB_REPO   | Autenticación para TheaScaler                       | ghp_xxx / owner/theaia                             |
| PAYLOAD_SCHEMA_PATH        | Esquema Pydantic de payloads                        | schemas/payloads.yaml                              |
| SPACY_MODEL                | Modelo spaCy usado                                  | es_core_news_sm                                    |
| INTENT_MODEL_PATH          | Modelo intents ML                                   | models/intent_classifier.pkl                       |
| ENTITY_MODEL_PATH          | Modelo entidades ML                                 | models/entity_extractor.pkl                        |
| LOG_FILE_PATH              | Ubicación log principal                             | logs/theaia.log                                    |
| PROMETHEUS_PORT            | Puerto Prometheus para métricas                     | 9090                                               |
| GOOGLE_CALENDAR_CREDENTIALS_PATH | Claves Google Calendar (opcional)             | credentials/google_calendar.json                   |
| EMAIL_SMTP_HOST/PORT/USER/PASS | SMTP para notificaciones                        | smtp.gmail.com / 587 / ...                         |

---

## 📋 Diccionario de Variables y Estados del Sistema (Agentes y Core)

- **pending_intent** (`str`): última intención detectada.
- **pending_datetime** (`str/datetime`): fecha/hora pendiente de confirmar.
- **last_event** (`dict`): resumen del último evento registrado.
- **last_note** (`dict`): última nota/crud.
- **fsm_state** (`str`): estado FSM actual.
- **context** (`dict`): almacén de contexto global para el usuario.
- **user_id / chat_id** (`str/int`): identificador de usuario en cada canal.

---

## 📜 Diccionarios Estandarizados

Variables, transiciones, intenciones y respuestas están documentadas a fondo en `docs/DICCIONARIO-VARIABLES.md` y en el propio código fuente siguiendo la convención [VARIABLE]: descripción, tipo, ejemplo/valor posible.

---

## 📕 Referencia Rápida

- Toda nueva variable o diccionario debe documentarse en su módulo y en `docs/DICCIONARIO-VARIABLES.md`
- Las rutas E2E usan contexto y DB temporal controlada por `ENABLE_E2E`
- ML/NLP configurable y swap-friendly entre modelos
- Seguridad actualizable: consistentemente usar variables de entorno y nunca hardcodear claves
- Consultar `/src/theaia/agents/` para ejemplos de uso y definición de variables contextuales
- Adapters y scripts implementan validación estricta de schema y tipos para evitar bugs en flujos cross-service

--- parte 5

---

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor, sigue estos pasos:

1. **Haz un fork** del repositorio.
2. **Crea una rama** con tu cambio:
git checkout -b feature/nombre-rama

text
3. **Ejecuta los tests**:
pytest

text
4. **Haz tu commit y push**:
git commit -m "Descripción"
git push origin feature/nombre-rama

text
5. **Haz un pull request**: explica claramente el objetivo y el impacto de tu cambio.

- Todo PR será revisado por el equipo y debe incluir tests relevantes.
- Revisa el [docs/ROADMAP.md] para alineación con la fase y criterios.
- Da preferencia a la limpieza y coherencia de diccionarios y documentación.

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes copiar, modificar y usar libremente el código respetando las condiciones.

---

## 📬 Contacto

- **Autor principal**: Alvaro Fernandez Mota ([alvarofernandezmota-tech](https://github.com/alvarofernandezmota-tech))
- Para dudas técnicas, usa Issues o contacta por email si lo deseas.

---

### ⏳ Roadmap y versiones

Consulta el roadmap [docs/ROADMAP.md] y el historial de evolución [docs/EVOLUCION-PROCESO.md] para los hitos actuales y próximos.

---

**¡Gracias por contribuir y ayudar a evolucionar Thea IA 2.0!**

Nota sobre tests en archivos ML globales:
Los archivos feature_engineering.py, training.py, inference.py, evaluation.py y la subcarpeta models/ actualmente no cuentan con pruebas unitarias específicas, ya que su complejidad funcional es mínima o solo gestionan archivo. Los tests correspondientes serán implementados en cuanto la lógica, dependencias o evolución del proyecto lo requieran, siguiendo buenas prácticas de ingeniería y auditoría.