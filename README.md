# 🤖 THEA-IA
**Sistema Conversacional Inteligente Multi-IA con Arquitectura Escalable**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-En%20Desarrollo-orange.svg)]()

## 📋 Descripción

THEA-IA es un sistema conversacional avanzado que integra múltiples modelos de inteligencia artificial para proporcionar respuestas contextuales, precisas y personalizadas. Diseñado con arquitectura modular y escalable, permite la integración de diferentes proveedores de IA (OpenAI, Anthropic, Google, etc.) bajo una API unificada.

### ✨ Características Principales

- **Multi-Modelo**: Integración con OpenAI (GPT-4, GPT-3.5), Anthropic (Claude), Google (Gemini) y más
- **API REST**: Interfaz FastAPI con documentación automática (Swagger/OpenAPI)
- **Gestión de Contexto**: Mantenimiento de historial conversacional con memoria persistente
- **Streaming en Tiempo Real**: Respuestas generadas progresivamente para mejor UX
- **Sistema de Agentes**: Arquitectura basada en agentes especializados para diferentes tareas
- **Validación Robusta**: Pydantic para validación automática de datos
- **Despliegue Flexible**: Compatible con Docker, Kubernetes y servicios cloud
- **Seguridad**: Autenticación JWT, rate limiting y gestión segura de API keys

## 🏗️ Arquitectura

thea-ia/
├── app/
│ ├── main.py # Punto de entrada FastAPI
│ ├── config.py # Configuración y variables de entorno
│ ├── models/ # Modelos Pydantic
│ │ ├── request.py
│ │ └── response.py
│ ├── services/ # Lógica de negocio
│ │ ├── ai_service.py # Integración con modelos IA
│ │ ├── context_manager.py # Gestión de contexto
│ │ └── agent_system.py # Sistema de agentes
│ ├── api/ # Endpoints API
│ │ └── routes/
│ │ ├── chat.py
│ │ └── health.py
│ └── utils/ # Utilidades
│ ├── logger.py
│ └── validators.py
├── tests/ # Tests unitarios e integración
├── docs/ # Documentación adicional
├── docker/ # Configuración Docker
├── .env.example # Variables de entorno ejemplo
├── requirements.txt # Dependencias Python
├── Dockerfile
├── docker-compose.yml
└── README.md

text

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.11 o superior
- pip o Poetry
- Docker (opcional)
- Cuenta en OpenAI/Anthropic/Google (para API keys)

### Instalación Local

```bash
# Clonar el repositorio
git clone https://github.com/alvarofernandezmota-tech/thea-ia.git
cd thea-ia

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys
Variables de Entorno
Crea un archivo .env con:

text
# API Keys
OPENAI_API_KEY=tu_clave_openai
ANTHROPIC_API_KEY=tu_clave_anthropic
GOOGLE_API_KEY=tu_clave_google

# Configuración FastAPI
APP_ENV=development
APP_HOST=0.0.0.0
APP_PORT=8000
DEBUG=True

# Base de datos (opcional)
DATABASE_URL=postgresql://user:pass@localhost:5432/thea_ia

# Seguridad
SECRET_KEY=tu_clave_secreta_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Ejecución
bash
# Modo desarrollo
uvicorn app.main:app --reload --port 8000

# Modo producción
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
Despliegue con Docker
bash
# Construir imagen
docker build -t thea-ia:latest .

# Ejecutar contenedor
docker run -d -p 8000:8000 --env-file .env thea-ia:latest

# Con Docker Compose
docker-compose up -d
📚 Uso de la API
Documentación Interactiva
Una vez ejecutado el servidor, accede a:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

Ejemplos de Peticiones
Chat Básico
bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Explícame qué es la inteligencia artificial",
    "model": "gpt-4",
    "temperature": 0.7
  }'
Chat con Contexto
bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Y cómo se relaciona con el machine learning?",
    "conversation_id": "uuid-conversation",
    "model": "gpt-4"
  }'
Streaming
bash
curl -X POST "http://localhost:8000/api/v1/chat/stream" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Genera un poema sobre la tecnología",
    "stream": true
  }'
Respuesta Ejemplo
json
{
  "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
  "message": "La inteligencia artificial (IA) es...",
  "model": "gpt-4",
  "tokens_used": 150,
  "timestamp": "2026-01-11T22:55:00Z"
}
🧪 Testing
bash
# Ejecutar todos los tests
pytest

# Con cobertura
pytest --cov=app --cov-report=html

# Tests específicos
pytest tests/test_api.py -v
🛠️ Tecnologías Utilizadas
FastAPI: Framework web asíncrono

Pydantic: Validación de datos

Uvicorn: Servidor ASGI de alto rendimiento

OpenAI SDK: Cliente oficial OpenAI

LangChain: Orquestación de LLMs

SQLAlchemy: ORM para persistencia

Redis: Caché y gestión de sesiones

Docker: Containerización

Pytest: Framework de testing

🗺️ Roadmap
 API REST básica con FastAPI

 Integración con OpenAI GPT-4

 Sistema de gestión de contexto

 Integración con Claude (Anthropic)

 Integración con Gemini (Google)

 Sistema de agentes especializados

 RAG (Retrieval-Augmented Generation)

 Interfaz web React/Next.js

 Despliegue en AWS/GCP

 Métricas y observabilidad (Prometheus/Grafana)

 Sistema de evaluación de respuestas

🤝 Contribución
Las contribuciones son bienvenidas. Por favor:

Fork el proyecto

Crea una rama (git checkout -b feature/nueva-funcionalidad)

Commit tus cambios (git commit -m 'Añade nueva funcionalidad')

Push a la rama (git push origin feature/nueva-funcionalidad)

Abre un Pull Request

📄 Licencia
Este proyecto está bajo la Licencia MIT. Ver el archivo LICENSE para más detalles.

👤 Autor
Álvaro Fernández Mota

GitHub: @alvarofernandezmota-tech

LinkedIn: Álvaro Fernández Mota

📧 Contacto
Para preguntas, sugerencias o colaboraciones:

Email: contacto@alvarofernandezmota.tech

Issues: GitHub Issues

🙏 Agradecimientos
Comunidad de FastAPI

OpenAI por su API

Contribuidores del proyecto

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub

Última actualización: 11 de enero de 2026

