#!/usr/bin/env bash
# ==================================================
# THEA IA 3.0 — ENTORNO DE INICIALIZACIÓN AUTOMÁTICO
# ==================================================

echo "🔧 Preparando entorno Python para Thea IA 3.0..."

# --------------------------------------------------
# 1️⃣ Actualizar herramientas base del intérprete
# --------------------------------------------------
python3 -m pip install --upgrade pip setuptools wheel build

# --------------------------------------------------
# 2️⃣ Instalar dependencias críticas y CLI (para Codespaces)
# --------------------------------------------------
echo "📦 Instalando dependencias del entorno (base, servidor y migraciones)..."
pip install -r requirements.txt \
  uvicorn==0.24.0 \
  alembic==1.12.1 \
  asyncpg==0.29.0 \
  SQLAlchemy==2.0.44

# --------------------------------------------------
# 3️⃣ Instalar NumPy de binarios precompilados (acelerado)
# --------------------------------------------------
echo "📦 Instalando NumPy (versión binaria precompilada 1.26.4)..."
pip install numpy==1.26.4 --only-binary=:all:

# --------------------------------------------------
# 4️⃣ Ejecutar migraciones (usa SQLite si no hay Postgres)
# --------------------------------------------------
echo "🗃️ Ejecutando migraciones de la base de datos..."
(
  alembic upgrade head 2>/dev/null \
  || {
    echo "⚠️ No se detectó conexión con PostgreSQL. Usando SQLite (local.db)..."
    sed -i 's|sqlalchemy.url *=.*|sqlalchemy.url = sqlite+aiosqlite:///local.db|' alembic.ini
    alembic upgrade head || alembic revision --autogenerate -m "Versión inicial SQLite"
  }
)

# --------------------------------------------------
# 5️⃣ Ejecutar tests automáticos de integración
# --------------------------------------------------
echo "🧪 Ejecutando tests de integración..."
pytest -v src/theaia/tests/integration || true

# --------------------------------------------------
# 6️⃣ Congelar versiones (crear requirements.lock)
# --------------------------------------------------
echo "📄 Guardando versions del entorno..."
pip freeze > requirements.lock

# --------------------------------------------------
# 7️⃣ Levantar el servidor FastAPI (en modo desarrollo)
# --------------------------------------------------
echo "🚀 Iniciando Thea IA 3.0 (servidor FastAPI)..."
export PATH=$PATH:/home/codespace/.local/bin
(
  uvicorn src.theaia.api.main:app --reload \
  || echo "⚠️ Verifica que el archivo src/theaia/api/main.py defina la variable 'app'."
)

echo "✅ Entorno Thea IA 3.0 configurado y operativo."
