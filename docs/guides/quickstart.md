🚀 Quickstart — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:06 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Prerequisitos
Python 3.10+

Git

Docker (opcional, para prod)

PostgreSQL (opcional, fallback a JSON local)

1️⃣ Instalación Local
Clonar repo
bash
git clone https://github.com/thea-ia/thea-ia.git
cd thea-ia
Crear virtual env
bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
Instalar dependencias
bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para development
2️⃣ Configuración
.env local
bash
cp .env.example .env
# Editar .env con configuración local
Variables principales:

bash
ENVIRONMENT=development
DATABASE_URL=sqlite:///thea.db  # Local (fallback JSON)
TELEGRAM_BOT_TOKEN=your_token
JWT_SECRET=your_secret
LOG_LEVEL=INFO
3️⃣ Tests
Ejecutar tests unitarios
bash
pytest src/theaia/tests/unit -v
Con cobertura
bash
pytest src/theaia/tests -v --cov=src/theaia --cov-report=html
# Abrir htmlcov/index.html
Tests e2e
bash
pytest src/theaia/tests/e2e -v
4️⃣ Ejecutar (Local)
FastAPI dev server
bash
uvicorn src.theaia.api:app --reload --host 0.0.0.0 --port 8000
Visitar
text
http://localhost:8000
Swagger docs
text
http://localhost:8000/docs
5️⃣ Docker (Local)
Build image
bash
docker build -t thea-ia:dev -f Dockerfile.lite .
Run container
bash
docker run -p 8000:8000 -e ENVIRONMENT=development thea-ia:dev
Docker Compose (con PostgreSQL opcional)
bash
docker-compose up -d
6️⃣ Primeros pasos
Crear usuario
bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com"}'
Enviar mensaje
bash
curl -X POST http://localhost:8000/chat/user_123 \
  -H "Content-Type: application/json" \
  -d '{"message":"quiero agendar cita"}'
Respuesta esperada
json
{
  "response": "¿Qué día prefieres?",
  "state": "disambiguation",
  "agent": "AgendaAgent"
}
📖 Próximos pasos
Installation Guide — Instalación detallada

Configuration — Configuración avanzada

Deployment — Desplegar a producción

Troubleshooting — Resolver problemas

Architecture — Entender diseño

Roadmap — Ver plan completo

🆘 Ayuda
Problema: ImportError con src.theaia

Solución:

bash
# Agregar raíz al PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest ...
Problema: Docker build falla

Solución:

bash
# Limpiar cache Docker
docker system prune -a
docker build --no-cache -t thea-ia:dev .
Problema: Tests fallan por falta de variables

Solución:

bash
# Crear .env.test
cp .env.example .env.test
# Editar con valores test
pytest --envfile .env.test
📌 Meta-información
Campo	Valor
Archivo	docs/guides/quickstart.md
Versión	v0.14.0
Última revisión	2025-11-09 19:06 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 19:06 CET