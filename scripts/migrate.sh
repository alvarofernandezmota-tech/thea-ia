#!/bin/bash
# ==============================================
# THEA IA 2.0 – EJECUTAR MIGRACIONES
# ==============================================

set -e

# Activar entorno virtual
if [ -f "./venv/bin/activate" ]; then
  source venv/bin/activate
fi

echo "🔄 Aplicando migraciones Alembic..."
alembic upgrade head

echo "✅ Migraciones completadas"
