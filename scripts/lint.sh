#!/bin/bash
# ==============================================
# THEA IA 2.0 – LINT & FORMATO
# ==============================================

set -e

# Activar entorno virtual
if [ -f "./venv/bin/activate" ]; then
  source venv/bin/activate
fi

echo "🔍 Ejecutando flake8..."
flake8 src/theaia

echo "🎨 Formateando con Black..."
black src/theaia

echo "✅ Lint y formato completados"
