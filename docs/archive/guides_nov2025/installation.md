📦 Installation — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:16 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Propósito
Guía de instalación paso a paso para THEA IA en diferentes plataformas.

🖥️ Requisitos Previos
Hardware mínimo
CPU: 2 cores (4+ recomendado)

RAM: 4 GB (8+ recomendado)

Disk: 10 GB SSD

Software
Python 3.10+ (verificar: python --version)

Git (verificar: git --version)

pip (verificar: pip --version)

Docker (opcional, pero recomendado)

Permisos
Acceso lectura/escritura carpeta instalación

Si uses PostgreSQL: acceso TCP puerto 5432

1️⃣ Opción A: Instalación Local (Python + venv)
Paso 1: Clonar repositorio
bash
git clone https://github.com/thea-ia/thea-ia.git
cd thea-ia
Paso 2: Crear virtual environment
bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Windows (CMD)
python -m venv venv
venv\Scripts\activate.bat
Verificar activación:

bash
which python  # Linux/Mac: debe mostrar ruta venv
# o
where python  # Windows: debe mostrar ruta venv
Paso 3: Instalar dependencias
bash
# Upgrade pip first
pip install --upgrade pip

# Instalar requirements
pip install -r requirements.txt

# Si develops, instala dev dependencies
pip install -r requirements-dev.txt
Verificar instalación:

bash
python -c "import src.theaia; print('OK')"
Paso 4: Configurar .env
bash
# Copiar ejemplo
cp .env.example .env

# Editar .env
nano .env  # o tu editor favorito
Variables mínimas requeridas:

bash
ENVIRONMENT=development
DATABASE_URL=sqlite:///thea.db
JWT_SECRET=your-random-secret-here
TELEGRAM_BOT_TOKEN=your-bot-token
Paso 5: Ejecutar
bash
# Dev server (con reload automático)
uvicorn src.theaia.api:app --reload --host 0.0.0.0 --port 8000

# Producción (sin reload)
uvicorn src.theaia.api:app --host 0.0.0.0 --port 8000 --workers 4
Verificar funcionamiento:

bash
curl http://localhost:8000/health
2️⃣ Opción B: Instalación Docker
Paso 1: Requisitos
bash
docker --version    # 20.10+
docker-compose --version  # 2.0+
Paso 2: Build image
bash
# Desde raíz proyecto
docker build -t thea-ia:latest .

# O con tag específico
docker build -t thea-ia:v0.14.0 .
Verificar build:

bash
docker images | grep thea-ia
Paso 3: Run container
bash
# Opción A: Con SQLite local (desarrollo)
docker run -d \
  --name thea-ia \
  -p 8000:8000 \
  -e ENVIRONMENT=development \
  -e DATABASE_URL=sqlite:///thea.db \
  -e JWT_SECRET=dev-secret \
  thea-ia:latest

# Opción B: Con PostgreSQL
docker run -d \
  --name thea-ia \
  -p 8000:8000 \
  --network thea-network \
  -e ENVIRONMENT=development \
  -e DATABASE_URL=postgresql://user:pass@postgres:5432/theaia \
  -e JWT_SECRET=dev-secret \
  thea-ia:latest
Verificar container:

bash
docker ps | grep thea-ia
docker logs -f thea-ia
3️⃣ Opción C: Docker Compose (recomendado para dev + prod)
Paso 1: Archivo docker-compose.yml ya existe
bash
ls docker-compose.yml  # Debe existir en raíz
Paso 2: Configurar .env
bash
cp .env.example .env
# Editar variables
Paso 3: Start servicios
bash
# Start en background
docker-compose up -d

# O en foreground (para ver logs)
docker-compose up

# Verificar servicios
docker-compose ps
Servicios levantados:

thea-ia (FastAPI app, puerto 8000)

postgres (PostgreSQL, puerto 5432)

prometheus (Prometheus, puerto 9090)

grafana (Grafana, puerto 3000)

loki (Loki logs, puerto 3100)

promtail (Log scraper)

Paso 4: Verificar
bash
# Health check
curl http://localhost:8000/health

# Acceder app
open http://localhost:8000/docs  # macOS
xdg-open http://localhost:8000/docs  # Linux
start http://localhost:8000/docs  # Windows

# Grafana dashboards
open http://localhost:3000  # usuario: admin, password: admin
Paso 5: Stop/restart
bash
# Parar servicios
docker-compose down

# Reiniciar
docker-compose restart

# Ver logs específico
docker-compose logs -f thea-ia
🔧 Verificación Post-Instalación
1. Health check
bash
curl -s http://localhost:8000/health | jq
# Response:
{
  "status": "healthy",
  "version": "v0.14.0",
  "database": "connected",
  "uptime": 42
}
2. API docs
text
http://localhost:8000/docs (Swagger UI)
http://localhost:8000/redoc (ReDoc)
3. Tests
bash
# Unit tests
pytest src/theaia/tests/unit -v

# Integration tests
pytest src/theaia/tests/integration -v

# E2E tests
pytest src/theaia/tests/e2e -v

# Con coverage
pytest --cov=src/theaia --cov-report=html
open htmlcov/index.html
4. Funcional
bash
# Crear usuario
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com"}'

# Enviar mensaje
curl -X POST http://localhost:8000/chat/test_user \
  -H "Content-Type: application/json" \
  -d '{"message":"Hola, quiero agendar cita"}'
🐛 Troubleshooting Instalación
Problema	Causa	Solución
python: not found	Python no instalado	Instalar Python 3.10+
ModuleNotFoundError	venv no activado	source venv/bin/activate
pip: permission denied	Sin permisos	Usar venv, no sudo
psycopg2 error	PostgreSQL no disponible	docker-compose up -d postgres
port 8000 in use	Puerto ocupado	lsof -i :8000 y liberar
SQLAlchemy error	DB schema no creado	python scripts/init_db.py
Ver guía completa: Troubleshooting

📚 Próximos Pasos
Configuration — Configurar variables avanzadas

Quickstart — Primeros tests y pruebas

Deployment — Desplegar a producción

Troubleshooting — Resolver problemas

📌 Meta-información
Campo	Valor
Archivo	docs/guides/installation.md
Versión	v0.14.0
Última revisión	2025-11-09 19:16 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 19:16 CET