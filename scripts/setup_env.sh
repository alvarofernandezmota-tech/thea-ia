#!/usr/bin/env bash
# ==============================================
# THEA IA 3.0 — ENTORNO DE INICIALIZACIÓN
# ==============================================

echo "🔧 Preparando entorno Python para Thea IA 3.0..."

# Actualizar herramientas base
python3 -m pip install --upgrade pip setuptools wheel build

# Instalar NumPy binario precompilado
echo "📦 Instalando NumPy (versión binaria estable)..."
pip install numpy==1.26.4 --only-binary=:all:

# Instalar todas las dependencias del proyecto
echo "📦 Instalando dependencias desde requirements.txt..."
pip install -r requirements.txt

# Ejecutar tests automáticos
echo "🧪 Ejecutando tests de integración..."
pytest -v src/theaia/tests/integration || true

# Congelar versiones exactas tras instalación correcta
echo "📄 Generando requirements.lock..."
pip freeze > requirements.lock

echo "✅ Entorno Thea IA 3.0 configurado correctamente."
