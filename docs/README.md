# Thea IA 2.0

🤖 **Agente conversacional inteligente** con máquina de estados finitos (FSM) y procesamiento de lenguaje natural (NLP) para gestión automatizada de eventos, notas y recordatorios.

---

## 🎯 Visión del proyecto

Thea IA es un asistente personal conversacional diseñado para transformar la gestión de eventos y tareas a través de inteligencia artificial. Combina FSM avanzada, NLP y arquitectura modular para ofrecer una experiencia de usuario natural e intuitiva.
Sección 2: Características y estructura abreviada
text
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
│ ├── core/
│ ├── adapters/
│ ├── services/
│ ├── models/
│ ├── database/
│ ├── ml/
│ ├── agents/
│ ├── utils/
│ └── api/
├── src/theaia/tests/
├── scripts/
├── docs/
└── deployment/
Sección 3: Instalación rápida
text
---
### FSM – Orquestación y Desambiguación

En la versión **2.1.0** se ha incorporado el submódulo **core/fsm** que aporta:

- **Desambiguación Inteligente** entre nota, cita y recordatorio  
- **Orquestación Global** de flujos conversacionales  
- **Gestión de estados finitos** (FSM) con timeouts y reintentos  
- **Delegación a agentes** de forma centralizada  

Componentes clave en `src/theaia/core/fsm/`:

- **conversation_manager.py**: `ConversationManager`, corazón del FSM global.  
- **state_machine.py**: Clase base (`BaseStateMachine`) y `ConversationStateMachine`.  
- **states/global_states.py**: Enumeración `GlobalState`, validación y descripciones.  
- **states/disambiguation_state.py**: Lógica de desambiguación y plantillas.  
- **states/agent_states.py**: Mapeo de intents a `AgentType` y estados iniciales.  
- **transitions.py**: Reglas de transición, condiciones y callbacks de logging.  

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
undefined
Sección 4: Comandos útiles
text
---

### Comandos útiles
- `make test`       : Ejecutar tests  
- `make lint`       : Linting y formato de código  
- `make format`     : Formatear código con Black  
- `make migrate`    : Ejecutar migraciones de BD  
- `make logs`       : Ver logs de la aplicación  
- `make clean`      : Limpiar archivos temporales  
Sección 5: Guía de contribución
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
- **Testing:** Incluir tests para nueva funcionalidad  
- **Logging:** Usar niveles adecuados  
Sección 6: Stack tecnológico
text
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
Sección 7: Testing & Calidad
text
---

## 🧪 Testing & Calidad

- **Ejecutar tests unitarios:**  
pytest -v src/theaia/tests/unit

text
- **Ejecutar tests E2E:**  
pytest -v src/theaia/tests/e2e

text
- **Generar reporte de cobertura:**  
pytest --cov=src/theaia --cov-report=html

text
undefined
Sección 8: Estado Auditoría – Fase 1
text
---

## 📋 Estado Auditoría – Fase 1 (13/10/2025 16:05 CEST)

- **src/theaia/utils/**: Documentación (`README.md`) y guía de testing (`TESTING.md`) añadidas  
- **scripts/**: Scripts de automatización (`setup.sh`, `deploy.sh`, `migrate.sh`, `lint.sh`, `backup.sh`, `entrypoint.sh`, `test_runner.sh`) y `README.md` completado  
- **src/theaia/tests/**: Estructura de 10 subcarpetas creada y `README.md` global  
Sección 9: Licencia y Contacto
text
---

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Puedes copiar, modificar y usar libremente el código respetando las condiciones.

---

## 📬 Contacto

- **Autor principal**: Alvaro Fernandez Mota ([alvarofernandezmota-tech](https://github.com/alvarofernandezmota-tech))


