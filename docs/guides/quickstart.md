# 🚀 Quickstart — THEA IA

**Versión:** v0.14.0  
**Última actualización:** 2025-10-31 03:22 CET  
**Responsable:** Álvaro Fernández Mota (CEO THEA IA)

---

## 📋 Prerequisitos

- Python 3.10+
- Git
- Docker (opcional, para prod)
- PostgreSQL (opcional, fallback a JSON local)

---

## 1️⃣ Instalación Local

### Clonar repo
git clone https://github.com/thea-ia/thea-ia.git
cd thea-ia

text

### Crear virtual env
python -m venv venv
source venv/bin/activate # Linux/Mac

o
venv\Scripts\activate # Windows

text

### Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt # Para development

text

---

## 2️⃣ Configuración

### .env local
cp .env.example .env

Editar .env con configuración local
text

**Variables principales:**
ENVIRONMENT=development
DATABASE_URL=sqlite:///thea.db # Local (fallback JSON)
TELEGRAM_BOT_TOKEN=your_token
JWT_SECRET=your_secret
LOG_LEVEL=INFO

text

---

## 3️⃣ Tests

### Ejecutar tests unitarios
pytest src/theaia/tests/unit -v

text

### Con cobertura
pytest src/theaia/tests -v --cov=src/theaia --cov-report=html

Abrir htmlcov/index.html
text

### Tests e2e
pytest src/theaia/tests/e2e -v

text

---

## 4️⃣ Ejecutar (Local)

### FastAPI dev server
uvicorn src.theaia.api:app --reload --host 0.0.0.0 --port 8000

text

### Visitar
http://localhost:8000

text

### Swagger docs
http://localhost:8000/docs

text

---

## 5️⃣ Docker (Local)

### Build image
docker build -t thea-ia:dev -f Dockerfile.lite .

text

### Run container
docker run -p 8000:8000 -e ENVIRONMENT=development thea-ia:dev

text

### Docker Compose (con PostgreSQL opcional)
docker-compose up -d

text

---

## 6️⃣ Primeros pasos

### Crear usuario
curl -X POST http://localhost:8000/users
-H "Content-Type: application/json"
-d '{"name":"John","email":"john@example.com"}'

text

### Enviar mensaje
curl -X POST http://localhost:8000/chat/user_123
-H "Content-Type: application/json"
-d '{"message":"quiero agendar cita"}'

text

### Respuesta esperada
{
"response": "¿Qué día prefieres?",
"state": "disambiguation",
"agent": "AgendaAgent"
}

text

---

## 📖 Próximos pasos

- [Deployment](./deployment.md) — Desplegar a producción
- [Troubleshooting](./troubleshooting.md) — Resolver problemas
- [Architecture](../architecture/overview.md) — Entender diseño
- [Roadmap](../roadmap/master.md) — Ver plan completo

---

## 🆘 Ayuda

**Problema:** ImportError con `src.theaia`

**Solución:**
Agregar raíz al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ...

text

---

**Última actualización:** 2025-10-31 03:22 CET
