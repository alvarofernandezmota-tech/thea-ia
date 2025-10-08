#!/bin/bash
# ==============================================
# THEA IA 2.0 – SETUP ENTORNO LOCAL
# ==============================================

set -e

echo "🔧 Creando entorno virtual..."
python3 -m venv venv
source venv/bin/activate

echo "📦 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Entorno listo. Para activarlo ejecuta: source venv/bin/activate"
