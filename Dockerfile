# ==============================================
# THEA IA 3.0 Enterprise — Dockerfile Optimizado Gratis
# Ejecuta FastAPI + MkDocs en entornos low‑RAM (Fly / Render)
# ==============================================

FROM python:3.12-slim AS base

LABEL maintainer="Álvaro Fernández Mota <alvarofernandezmota@gmail.com>"
LABEL version="3.0.1"
LABEL description="Thea IA 3.0 — Plataforma modular de IA con FastAPI, FSM y Docs integrados"

# Variables de entorno esenciales
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    THEA_ENV=production \
    APP_NAME="thea-ia" \
    APP_VERSION="3.0.1"

WORKDIR /app

# Dependencias base
RUN apt update && apt install -y --no-install-recommends build-essential libpq-dev curl git && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos
COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Descargar modelo NLP español
RUN python -m spacy download es_core_news_sm

# Copiar código fuente y docs
COPY ./src ./src
COPY ./scripts ./scripts
COPY ./docs ./docs
COPY mkdocs.yml .

# Crear carpetas necesarias
RUN mkdir -p /app/logs /app/models /app/uploads && \
    chmod +x ./scripts/setup_env.sh

# Exponer puertos de API (8000) y Docs (8001)
EXPOSE 8000 8001

# Healthcheck para FastAPI
HEALTHCHECK --interval=30s --timeout=10s \
  CMD curl -fsS http://localhost:8000/health || exit 1

# Arranque API
CMD ["uvicorn", "src.theaia.main:app", "--host", "0.0.0.0", "--port", "8000"]
