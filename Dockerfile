# ==============================================
# THEA IA 3.0 — DOCKERFILE ENTERPRISE EDITION
# ==============================================

# --------- Etapa 1: Build de Dependencias ---------
FROM python:3.12-slim AS builder

LABEL maintainer="Álvaro Fernández Mota <alvarofernandezmota@gmail.com>"
LABEL version="3.0.1"
LABEL description="Thea IA 3.0 — Plataforma modular de IA con FastAPI, FSM y Docs integrados"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/home/theaia/.local/bin:$PATH"

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crear usuario seguro
RUN useradd -m -r -s /bin/bash theaia

WORKDIR /app

# Copiar requerimientos
COPY requirements.txt .

# Actualizar pip & herramientas
RUN pip install --upgrade pip setuptools wheel build

# Instalar dependencias Python en entorno temporal
RUN pip install --prefix=/install -r requirements.txt
RUN pip install --prefix=/install numpy==1.26.4 mkdocs mkdocs-material
# Instalar dependencias de Python (debe contener la versión fija de spaCy + pydantic)
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelo spaCy (ahora sí funcionará)
RUN python -m spacy download es_core_news_sm

# --------- Etapa 2: Runtime (API + Docs) ---------
FROM python:3.12-slim

# Variables de runtime
ENV PATH="/home/theaia/.local/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    THEA_ENV=production \
    APP_NAME="thea-ia" \
    APP_VERSION="3.0.1"

# Crear usuario sin privilegios
RUN useradd -m -r -s /bin/bash theaia

# Copiar dependencias desde builder
COPY --from=builder /install /usr/local

# Directorio de trabajo
WORKDIR /app

# Copiar scripts, código fuente y documentación
COPY --chown=theaia:theaia ./src ./src
COPY --chown=theaia:theaia ./scripts ./scripts
COPY --chown=theaia:theaia ./docs ./docs
COPY --chown=theaia:theaia mkdocs.yml .

# Crear directorios adicionales
RUN mkdir -p /app/logs /app/models /app/uploads /app/site && \
    chown -R theaia:theaia /app

# Descargar modelo nlp base (idioma español)
RUN python -m spacy download es_core_news_sm

# Permitir ejecución del script principal
RUN chmod +x ./scripts/setup_env.sh

USER theaia

# Exponer puertos
EXPOSE 8000 8001

# Healthcheck API
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8000/health || exit 1

# --------- Targets de build ---------
# Target API (predeterminado)
CMD ["uvicorn", "src.theaia.api.main:app", "--host", "0.0.0.0", "--port", "8000"]

# --------- Target de Documentación (mkdocs) ---------
# Para servir el portal docs.theaia.com:
# docker build -t thea-docs --target=docs .
# docker run -p 8001:8001 thea-docs

FROM python:3.12-slim AS docs
COPY --from=builder /install /usr/local
COPY mkdocs.yml .
COPY docs ./docs
EXPOSE 8001
CMD ["mkdocs", "serve", "-a", "0.0.0.0:8001"]
