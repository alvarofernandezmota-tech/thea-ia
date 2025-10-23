#!/usr/bin/env bash

echo "🔎 Iniciando entorno Thea IA..."
export PYTHONUNBUFFERED=1
export THEA_ENV=development

# Instalar modelo spaCy (asegura compat)
python -m spacy validate || python -m spacy download es_core_news_sm

# Migrar DB (si es necesario)
alembic upgrade head

# Verificar acceso a .env local
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Se ha copiado .env.example a .env"
fi

echo "✅ Entorno Thea IA listo para desarrollo"
