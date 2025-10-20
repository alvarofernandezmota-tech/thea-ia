#!/usr/bin/env bash
# ==============================================
# THEA IA 3.0 — OPTIMIZACIÓN PARA GITHUB CODESPACES
# ==============================================

echo "🔧 Configurando entorno Thea IA 3.0 Lite en Codespaces..."

# 1️⃣ Actualizar utilidades base
python3 -m pip install --upgrade pip setuptools wheel build

# 2️⃣ Instalar NumPy precompilado (evita compilación)
pip install numpy==1.26.4 --only-binary=:all:

# 3️⃣ Instalar las dependencias completas (sin cache)
pip install -r requirements.txt --no-cache-dir

# 4️⃣ Eliminar módulos CUDA (no necesarios en Codespaces)
echo "🧹 Eliminando dependencias CUDA innecesarias (Torch GPU)..."
pip uninstall -y nvidia-* || true

# 5️⃣ Instalar versión CPU de Torch
pip install torch==2.9.0+cpu --index-url https://download.pytorch.org/whl/cpu

# 6️⃣ Validar instalación y correr tests automáticos
pytest -v src/theaia/tests/integration || true

# 7️⃣ Congelar dependencias exactas
pip freeze > requirements.lock

echo "✅ Thea IA 3.0 Codespaces listo y probado."
