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

## 🏗️ Arquitectura modular

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    ┌──────────────┐
│   Usuario   │────│   Adapters   │────│      Core       │────│   Services   │
│             │    │  (Telegram,  │    │   (FSM, Bot     │    │  (Event,     │
│             │    │  Webhooks)   │    │   Factory,      │    │   User,      │
│             │    │              │    │   Context)      │    │   Scheduler) │
└─────────────┘    └──────────────┘    └─────────────────┘    └──────────────┘
                                                │
                                                ▼
                                       ┌─────────────────┐
                                       │   Repositories  │
                                       │   & Database    │
                                       │   (PostgreSQL)  │
                                       └─────────────────┘
                                                │
                                                ▼
                                       ┌─────────────────┐
                                       │    ML/NLP       │
                                       │  (Intent &      │
                                       │   Entity        │
                                       │  Detection)     │
                                       └─────────────────┘
```

---

## 📂 Estructura del proyecto

```
theaia/
├── README.md                          # Documentación principal
├── .env.example                       # Variables de entorno ejemplo
├── .gitignore                         # Exclusiones Git
├── pyproject.toml                     # Configuración proyecto Python
├── requirements.txt                   # Dependencias producción
├── requirements-dev.txt               # Dependencias desarrollo
├── docker-compose.yml                 # Orquestación contenedores
├── Dockerfile                         # Imagen Docker aplicación
├── Makefile                          # Comandos automatizados
├── src/
│   └── theaia/
│       ├── __init__.py
│       ├── main.py                    # Punto de entrada aplicación
│       ├── config/
│       │   ├── settings.py           # Configuración por entorno
│       │   └── logging_config.py     # Configuración logging
│       ├── core/
│       │   ├── state_machine.py      # FSM principal
│       │   ├── callbacks.py          # Callbacks estados/transiciones
│       │   ├── context_manager.py    # Gestión estado usuario
│       │   └── bot_factory.py        # Creación instancias bot
│       ├── adapters/
│       │   ├── telegram_adapter.py   # Conexión Telegram
│       │   └── webhook_handler.py    # Endpoint webhooks
│       ├── services/
│       │   ├── event_service.py      # Lógica eventos
│       │   ├── note_service.py       # Lógica notas
│       │   ├── user_service.py       # Lógica usuarios
│       │   └── scheduler_service.py  # Lógica recordatorios
│       ├── models/
│       │   ├── user.py              # Modelo usuario
│       │   ├── event.py             # Modelo evento
│       │   ├── note.py              # Modelo nota
│       │   └── context.py           # Modelo contexto
│       ├── database/
│       │   ├── connection.py        # Conexión BD
│       │   └── repositories/
│       │       ├── base.py          # Clase base repositories
│       │       ├── user_repository.py
│       │       ├── event_repository.py
│       │       └── note_repository.py
│       ├── ml/
│       │   ├── intent_detector.py   # Detección intenciones NLP
│       │   └── entity_extractor.py  # Extracción entidades
│       ├── utils/
│       │   ├── validators.py        # Validadores
│       │   ├── formatters.py        # Formateadores
│       │   └── exceptions.py        # Excepciones personalizadas
│       └── api/
│           ├── health.py            # Endpoint salud
│           └── metrics.py           # Endpoint métricas
├── tests/
│   ├── unit/                        # Tests unitarios
│   ├── integration/                 # Tests integración
│   ├── e2e/                        # Tests end-to-end
│   └── fixtures/                   # Datos prueba
├── docs/
│   ├── ARCHITECTURE.md             # Diagrama modular detallado
│   ├── DEPLOYMENT.md              # Guía despliegue
│   ├── API.md                     # Especificaciones endpoints
│   ├── adr/                       # Architecture Decision Records
│   ├── diagrams/                  # Diagramas técnicos
│   └── retros/                    # Retrospectivas desarrollo
├── scripts/
│   ├── setup.sh                   # Script instalación local
│   ├── deploy.sh                  # Script despliegue
│   ├── migrate.sh                 # Script migraciones BD
│   └── lint.sh                    # Script linting/formato
├── alembic/
│   ├── alembic.ini               # Configuración migraciones
│   ├── env.py                    # Entorno migraciones
│   └── versions/                 # Versiones migraciones BD
├── .github/
│   ├── workflows/
│   │   ├── ci.yml               # CI/CD básico
│   │   ├── cd.yml               # Despliegue continuo
│   │   └── security.yml         # Análisis seguridad
│   └── ISSUE_TEMPLATE/          # Plantillas issues
├── monitoring/
│   ├── grafana/                 # Dashboards
│   ├── prometheus/              # Métricas
│   └── alerts/                  # Configuración alertas
└── deployment/
    ├── k8s/                     # Manifiestos Kubernetes
    ├── helm/                    # Charts Helm
    └── terraform/               # Infraestructura como código
```

---

## 🛣️ Roadmap de desarrollo

### Matriz de fases y entregables

| Fase | Componente | Tareas clave | Estado | Estimación | Responsable |
|------|------------|-------------|---------|------------|-------------|
| **1. Fundamentos** | Estructura base | ✅ Carpetas, archivos config, entorno | ✅ Completado | 2 días | DevOps/Backend |
| **2. Core** | FSM & Context | 🔄 State machine, callbacks, gestión contexto | ⏳ En progreso | 5 días | Backend |
| **3. Adapters** | Conectores | 🔄 Telegram, webhooks, handlers | ⏳ Planificado | 4 días | Integración |
| **4. Services** | Lógica negocio | 🔄 Eventos, usuarios, notas, scheduler | ⏳ Planificado | 6 días | Backend |
| **5. Persistencia** | Base datos | 🔄 Modelos, repositories, migraciones | ⏳ Planificado | 4 días | Backend/DB |
| **6. ML/NLP** | Inteligencia | 🔄 Intent detection, entity extraction | ⏳ Planificado | 7 días | IA/ML |
| **7. API** | Endpoints | 🔄 Health, metrics, documentación | ⏳ Planificado | 3 días | Backend |
| **8. Testing** | Calidad | 🔄 Unit, integration, E2E tests | ⏳ Planificado | 5 días | QA |
| **9. Infraestructura** | Despliegue | 🔄 Docker, CI/CD, monitoring | ⏳ Planificado | 4 días | DevOps |
| **10. Documentación** | Docs finales | 🔄 Diagramas, guías, ADRs | ⏳ Planificado | 3 días | Docs/All |

### Cronograma estimado
- **Duración total:** 6-8 semanas
- **Hitos principales:**
  - ✅ **Semana 1:** Estructura y configuración base
  - 🎯 **Semana 2-3:** Core FSM y servicios fundamentales
  - 🎯 **Semana 4-5:** Integración ML/NLP y persistencia
  - 🎯 **Semana 6:** Testing, optimización y documentación
  - 🎯 **Semana 7-8:** Despliegue y monitoreo

---

## 📈 Estado actual y próximos hitos

### 🔄 Estado actual: **Fundamentos completados - Migración en progreso**

#### ✅ Completado:
- Estructura de carpetas modular y profesional
- Archivos de configuración base (pyproject.toml, requirements, docker-compose)
- Documentación inicial y roadmap detallado

#### ⏳ En progreso:
- Migración código existente a nueva estructura
- Configuración entorno desarrollo

#### 🎯 Próximos hitos:
1. **Milestone 1:** FSM funcional con callbacks básicos (Semana 2)
2. **Milestone 2:** Primer demo E2E Telegram bot (Semana 3)
3. **Milestone 3:** Integración ML/NLP funcional (Semana 5)
4. **Milestone 4:** Deploy staging automatizado (Semana 6)

---

## ⚡ Instalación rápida

### Prerrequisitos
- Python 3.11+
- PostgreSQL 14+
- Docker & Docker Compose
- Git

### Configuración desarrollo

1. **Clonar repositorio:**
   ```bash
   git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
   cd thea-ia
   ```

2. **Configurar entorno:**
   ```bash
   make setup
   cp .env.example .env
   # Editar .env con tus configuraciones
   ```

3. **Levantar servicios:**
   ```bash
   docker-compose up -d
   make migrate
   ```

4. **Ejecutar aplicación:**
   ```bash
   make run
   ```

### Comandos útiles

```bash
make test          # Ejecutar tests
make lint          # Linting y formato código
make format        # Formatear código con Black
make migrate       # Ejecutar migraciones BD
make logs          # Ver logs aplicación
make clean         # Limpiar archivos temporales
```

---

## 🤝 Guía de contribución

### Flujo de trabajo

1. **Fork del repositorio** y crea tu rama:
   ```bash
   git checkout -b feature/descripcion-cambio
   ```

2. **Sigue convenciones:**
   - Commits: [Conventional Commits](https://www.conventionalcommits.org/)
   - Código: PEP 8 + Black formatting
   - Tests: Cobertura mínima 80%

3. **Antes del PR:**
   ```bash
   make test && make lint
   ```

4. **Crea PR** con descripción clara y referencia issues relacionados

### Normas código
- **Tipado:** Usar type hints en funciones públicas
- **Docstrings:** Documentar clases y métodos complejos
- **Testing:** Tests para nueva funcionalidad
- **Logging:** Usar logging apropiado por niveles

Para más detalles: [CONTRIBUTING.md](docs/CONTRIBUTING.md)

---

## 🛠️ Stack tecnológico

### Backend & Core
- **Python 3.11+** - Lenguaje principal
- **FastAPI** - Framework API REST
- **Transitions** - Máquina de estados finitos
- **SQLAlchemy** - ORM y gestión BD
- **Alembic** - Migraciones base datos
- **Pydantic** - Validación datos y serialización

### Base de datos & Caché
- **PostgreSQL 14+** - Base datos principal
- **Redis** - Caché y sessions (opcional)

### ML/NLP & IA
- **spaCy** / **NLTK** - Procesamiento lenguaje natural
- **scikit-learn** - Algoritmos machine learning
- **Transformers** (opcional) - Modelos pre-entrenados

### Integración & Comunicación
- **aiogram** - SDK Telegram Bot API
- **aiohttp** - Cliente HTTP asíncrono
- **WebSockets** - Comunicación tiempo real

### Desarrollo & Testing
- **pytest** - Framework testing
- **Black** - Formateo código
- **flake8** / **mypy** - Linting y tipado
- **pre-commit** - Hooks Git

### DevOps & Infraestructura
- **Docker** & **Docker Compose** - Containerización
- **Kubernetes** - Orquestación (producción)
- **GitHub Actions** - CI/CD
- **Prometheus** + **Grafana** - Monitoreo
- **Terraform** - Infraestructura como código

---

## 📊 Arquitectura técnica detallada

### Patrón FSM (Finite State Machine)
```python
Estados principales:
- IDLE: Usuario inactivo
- LISTENING: Esperando comando
- PROCESSING: Procesando solicitud
- CONFIRMING: Esperando confirmación
- EXECUTING: Ejecutando acción
```

### Flujo típico conversación
```
Usuario → Adapter → FSM → Context Manager → Services → Repository → DB
     ←          ←     ←                  ←          ←            ←
```

### Casos de uso principales
1. **Crear evento:** "Recordarme reunión mañana 15:00"
2. **Consultar agenda:** "¿Qué tengo programado hoy?"
3. **Modificar evento:** "Cambiar reunión a las 16:00"
4. **Cancelar evento:** "Cancelar reunión de mañana"
5. **Nota rápida:** "Apunta: comprar leche"

---

## 📚 Documentación técnica

### Documentación principal
- [**ARCHITECTURE.md**](docs/ARCHITECTURE.md) - Diseño detallado y decisiones técnicas
- [**API.md**](docs/API.md) - Especificaciones endpoints y contratos
- [**DEPLOYMENT.md**](docs/DEPLOYMENT.md) - Guías despliegue local y cloud
- [**CONTRIBUTING.md**](docs/CONTRIBUTING.md) - Normas contribución y desarrollo

### Diagramas y recursos
- [**Diagramas arquitectura**](docs/diagrams/) - Visualizaciones técnicas
- [**ADRs**](docs/adr/) - Architecture Decision Records
- [**Retrospectivas**](docs/retros/) - Aprendizajes y mejoras

---

## 🔍 Monitoreo y observabilidad

### Métricas clave
- **Disponibilidad:** Uptime y health checks
- **Performance:** Latencia respuestas, throughput
- **Errores:** Rate errores, excepciones no manejadas
- **Negocio:** Eventos creados, usuarios activos, conversaciones

### Endpoints salud
```
GET /health              # Estado general aplicación
GET /health/detailed     # Estado detallado componentes
GET /metrics            # Métricas Prometheus
```

---

## 🚀 Roadmap futuro (post v1.0)

### Funcionalidades avanzadas
- 🔄 **Integración Google Calendar** - Sincronización bidireccional
- 📱 **App móvil nativa** - iOS y Android
- 🌍 **Multi-idioma** - Soporte i18n
- 🤖 **IA conversacional avanzada** - GPT integration
- 📊 **Analytics predictivos** - ML para sugerencias
- 🔗 **API pública** - Terceros desarrolladores
- ⚡ **Real-time notifications** - Push notifications
- 🎨 **Dashboard web** - Interfaz gestión visual

### Escalabilidad técnica
- **Microservicios:** Descomposición arquitectura
- **Event sourcing:** Historial completo eventos
- **CQRS:** Separación comandos y consultas
- **Multi-tenancy:** Soporte múltiples organizaciones

---

## 👏 Reconocimientos y créditos

### Equipo desarrollo
- **Alvaro Fernandez Mota** - Arquitecto principal y desarrollador
- **Comunidad Open Source** - Contribuciones e inspiración

### Tecnologías y librerías
Agradecimiento especial a los mantenedores de:
- FastAPI, SQLAlchemy, Transitions
- pytest, Black, Docker
- PostgreSQL, Redis, Prometheus
- GitHub, Python Software Foundation

### Inspiración
- Proyectos open source de conversational AI
- Comunidad Python y mejores prácticas
- Feedback usuarios y casos uso reales

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

## 📞 Contacto y soporte

- **GitHub:** [thea-ia repository](https://github.com/alvarofernandezmota-tech/thea-ia)
- **Issues:** Reportar bugs y solicitar features via GitHub Issues
- **Discusiones:** GitHub Discussions para preguntas generales
- **Email:** [Contacto directo](mailto:alvarofernandezmota@gmail.com)

---

**¡Únete al proyecto Thea IA y revoluciona la gestión de eventos con inteligencia artificial!** 🚀