# ==============================================
# THEA IA 2.0 - DOCKERFILE
# ==============================================

# Usar imagen Python oficial optimizada
FROM python:3.11-slim

# Metadatos de la imagen
LABEL maintainer="Alvaro Fernandez Mota <alvarofernandezmota@gmail.com>"
LABEL version="2.0.0"
LABEL description="Thea IA - Agente conversacional inteligente"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VENV_IN_PROJECT=1

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear usuario no-root para seguridad
RUN groupadd -r theaia && useradd -r -g theaia theaia

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt requirements-dev.txt ./

# Instalar dependencias Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Descargar modelo de spaCy
RUN python -m spacy download es_core_news_sm

# Crear directorios necesarios
RUN mkdir -p /app/logs /app/models /app/uploads && \
    chown -R theaia:theaia /app

# Copiar código fuente
COPY --chown=theaia:theaia ./src /app/src
COPY --chown=theaia:theaia ./alembic /app/alembic
COPY --chown=theaia:theaia ./alembic.ini /app/
COPY --chown=theaia:theaia ./scripts /app/scripts

# Hacer scripts ejecutables
RUN chmod +x /app/scripts/*.sh

# Cambiar a usuario no-root
USER theaia

# Exponer puerto
EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Punto de entrada
ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# Comando por defecto
CMD ["uvicorn", "theaia.main:app", "--host", "0.0.0.0", "--port", "8000"]
