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

