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

### Fase 1 – Fundamentos  
| Tarea                                        | Estado        | Estimación |
|----------------------------------------------|---------------|------------|
| Carpeta y archivos de configuración base     | ✅ Completada  | 0.5 días   |
| Entorno local y scripts de setup             | ✅ Completada  | 0.5 días   |
| Convenciones de código (PEP8, Black)         | ✅ Completada  | 1 día      |

---

### Fase 2 – Core (FSM & Context)  
**Punto actual: 40% completado**  
| Tarea                                                                                                   | Estado         | Estimación |
|---------------------------------------------------------------------------------------------------------|----------------|------------|
| Integrar router en adaptadores                                                                          | ✅ Completada   | 1 día      |
| Conectar intent_detector al router                                                                      | ✅ Completada   | 2 días     |
| Conectar entity_extractor al router                                                                     | ✅ Completada   | 1 día      |
| Persistir contexto de usuario (DB/Redis)                                                                | ⬜ Pendiente    | 2 días     |
| Pruebas end-to-end (simulaciones sintéticas y reales)                                                   | ⬜ Pendiente    | 3 días     |
| Validación arquitectural (diagramas UML, análisis estático)                                             | ⬜ Pendiente    | 2 días     |
| **Reforzar registry.py:** Validación de INTENT único                                                    | ⬜ Pendiente    | 1 día      |
| **Reforzar registry.py:** Ranking de intenciones y umbral de confianza                                  | ⬜ Pendiente    | 1 día      |
| **Reforzar registry.py:** Fallback dinámico y logging de no entendidos                                  | ⬜ Pendiente    | 1 día      |
| **Reforzar registry.py:** Hot-reload de agentes                                                         | ⬜ Pendiente    | 1 día      |
| **Reforzar registry.py:** Métricas de despacho y alertas                                                | ⬜ Pendiente    | 1 día      |

---

### 🤖 Fase 2.5 – TheaScaler Agent (Escalador de Desarrollo)  
**⭐ ACTIVACIÓN: Inmediatamente después de completar Fase 2**  
| Tarea                                                                                  | Estado         | Estimación |
|----------------------------------------------------------------------------------------|----------------|------------|
| **Análisis Repository:** Auditoría completa del estado actual vs roadmap               | ⬜ Planificada  | 1 día      |
| **GitHub API Integration:** Conexión con repositorio para lectura/escritura           | ⬜ Planificada  | 1 día      |
| **Code Generation Engine:** Motor de generación de código inteligente                 | ⬜ Planificada  | 2 días     |
| **Automated Commits/PRs:** Sistema de commits y pull requests automáticos             | ⬜ Planificada  | 1 día      |
| **Progress Tracking:** Dashboard de progreso tiempo real                              | ⬜ Planificada  | 1 día      |
| **Quality Gates:** Validación automática antes de commits                             | ⬜ Planificada  | 1 día      |
| **Integration Testing:** Pruebas de integración del agente con el proyecto            | ⬜ Planificada  | 1 día      |

---

### Fase 3 – Adaptadores **🚀 ACELERADA POR THEASCALER**  
| Tarea                                      | Estado        | Estimación | Con TS  |
|--------------------------------------------|---------------|------------|---------|
| Telegram adapter: integración con router   | ⬜ Planificada  | 1 día      | 0.5 días |
| Webhook handler: integración con router    | ⬜ Planificada  | 1 día      | 0.5 días |
| Validar payloads con Pydantic              | ⬜ Planificada  | 1 día      | 0.5 días |
| Agent Validation (Dialogflow CX)           | ⬜ Planificada  | 1 día      | 0.5 días |
| Pruebas de integración canal ↔ Core        | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 4 – Services (Lógica de negocio) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                    | Estado        | Estimación | Con TS  |
|------------------------------------------|---------------|------------|---------|
| event_service, note_service, scheduler_service | ⬜ Planificada  | 2 días     | 1 día    |
| Validar inputs/outputs con Pydantic      | ⬜ Planificada  | 1 día      | 0.5 días |
| Tests unitarios con mocks de repositorios | ⬜ Planificada  | 2 días     | 1 día    |
| Pruebas de regresión de lógica de negocio | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 5 – Persistencia (Base de datos) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                            | Estado        | Estimación | Con TS  |
|--------------------------------------------------|---------------|------------|---------|
| Modelos SQLAlchemy y migraciones Alembic         | ⬜ Planificada  | 1 día      | 0.5 días |
| Validación de integridad relacional y constraints | ⬜ Planificada  | 1 día      | 0.5 días |
| Pruebas de migraciones en staging                | ⬜ Planificada  | 2 días     | 1 día    |

---

### Fase 6 – ML/NLP (Core & Agentes) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                                       | Estado        | Estimación | Con TS  |
|-------------------------------------------------------------|---------------|------------|---------|
| Estructura ml/intent_detector y ml/ner_extractor            | ⬜ Planificada  | 1 día      | 0.5 días |
| Entrenamiento spaCy v3 (TextCategorizer + EntityRuler)      | ⬜ Planificada  | 2 días     | 1.5 días |
| fastText como alternativa ligera                            | ⬜ Planificada  | 1 día      | 0.5 días |
| Integración Transformer + AdapterHub para embeddings         | ⬜ Planificada  | 2 días     | 1.5 días |
| Métodos ABMS: muestreo de sesiones y validación empírica    | ⬜ Planificada  | 2 días     | 1.5 días |
| Pruebas de precisión, recall y latencia                     | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 7 – API (Endpoints) **🚀 ACELERADA POR THEASCALER**  
| Tarea                             | Estado        | Estimación | Con TS  |
|-----------------------------------|---------------|------------|---------|
| Implementar /health y /metrics    | ⬜ Planificada  | 1 día      | 0.5 días |
| Documentación OpenAPI y validación de esquemas | ⬜ Planificada | 1 día      | 0.5 días |
| Pruebas de contrato (mock server) | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 8 – Testing (Calidad) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                                           | Estado        | Estimación | Con TS  |
|-----------------------------------------------------------------|---------------|------------|---------|
| Unit tests (core, agents, services)                             | ⬜ Planificada  | 2 días     | 1 día    |
| Integration/E2E tests                                           | ⬜ Planificada  | 2 días     | 1 día    |
| Pruebas de estrés y carga                                       | ⬜ Planificada  | 1 día      | 0.5 días |
| Human-in-the-Loop: revisión manual de fallos de baja confianza  | ⬜ Planificada  | 1 día      | 1 día    |

---

### Fase 9 – Infraestructura (Despliegue) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                      | Estado        | Estimación | Con TS  |
|--------------------------------------------|---------------|------------|---------|
| Dockerización y multi-stage builds         | ⬜ Planificada  | 1 día      | 0.5 días |
| Kubernetes manifests y HPA/VPA             | ⬜ Planificada  | 1 día      | 0.5 días |
| CI/CD (GitHub Actions)                     | ⬜ Planificada  | 1 día      | 0.5 días |
| Monitorización Prometheus/Grafana          | ⬜ Planificada  | 1 día      | 0.5 días |
| Validar políticas de autoscaling en staging | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 10 – Documentación (Docs finales) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                             | Estado        | Estimación | Con TS  |
|---------------------------------------------------|---------------|------------|---------|
| Diagramas detallados (ARCHITECTURE.md)            | ⬜ Planificada  | 1 día      | 0.5 días |
| ADRs para decisiones críticas                     | ⬜ Planificada  | 1 día      | 0.5 días |
| Guía de despliegue y playbooks DR                 | ⬜ Planificada  | 1 día      | 0.5 días |
| Changelog diario en `docs/README-diario.md`       | ⬜ Planificada  | 1 día      | 0.5 días |

---

### Fase 11 – MLOps (Operaciones & ML Pipelines) **🚀 ACELERADA POR THEASCALER**  
| Tarea                                      | Estado        | Estimación | Con TS  |
|--------------------------------------------|---------------|------------|---------|
| Pipeline ML automatizado (CI/CD GPU)       | ⬜ Planificada  | 1 día      | 0.5 días |
| Versionado de artefactos (MLflow/S3)       | ⬜ Planificada  | 1 día      | 0.5 días |
| Drift detection y alertas de degradación   | ⬜ Planificada  | 1 día      | 0.5 días |
| Rollback y pruebas de rollback             | ⬜ Planificada  | 2 días     | 1 día    |

---

### 🧠 Fase 12 – Self-Evolution Core (Auto-mejora Integrada)  
| Tarea                                      | Estado        | Estimación |
|--------------------------------------------|---------------|------------|
| Performance Monitor                        | ⬜ Planificada  | 1 día      |
| Feedback Loop System                       | ⬜ Planificada  | 2 días     |
| Meta-learning Engine                       | ⬜ Planificada  | 2 días     |
| Dynamic Code Modification                  | ⬜ Planificada  | 2 días     |
| Self-updating Mechanisms                   | ⬜ Planificada  | 1 día      |
| Safety Constraints                         | ⬜ Planificada  | 1 día      |
| Rollback Capabilities                      | ⬜ Planificada  | 1 día      |

---

### 🌐 Fase 13 – Agent Ecosystem (Ecosistema de Agentes)  
| Tarea                                      | Estado        | Estimación |
|--------------------------------------------|---------------|------------|
| Individual Agent Evolution                 | ⬜ Planificada  | 2 días     |
| Cross-agent Learning                       | ⬜ Planificada  | 2 días     |
| Collaborative Improvement                  | ⬜ Planificada  | 1 día      |
| Ecosystem Orchestration                    | ⬜ Planificada  | 2 días     |
| Knowledge Sharing Protocol                 | ⬜ Planificada  | 1 día      |
| Distributed Learning                       | ⬜ Planificada  | 2 días     |
| Emergence Detection                        | ⬜ Planificada  | 1 día      |

---

## 📊 Cronograma optimizado  
- **Duración total sin TheaScaler:** 8–10 semanas  
- **Duración total con TheaScaler:** 6–7 semanas  
- **Ahorro de tiempo:** 30-40%

---

🚀 **Resultado final:** Thea IA 2.0 completamente funcional, auto-escalable y con capacidades de mejora continua en **6-7 semanas**.  



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

---

**¡Únete al proyecto Thea IA y revoluciona la gestión de eventos con inteligencia artificial!** 🚀

