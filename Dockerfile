# ==============================================
# THEA IA 3.0 — DOCKERFILE OFICIAL
# ==============================================

# Imagen base: Python 3.12 slim (optimizada para producción)
FROM python:3.12-slim

# Metadatos
LABEL maintainer="Álvaro Fernández Mota <alvarofernandezmota@gmail.com>"
LABEL version="3.0.0"
LABEL description="Thea IA 3.0 — Agente conversacional inteligente con FSM y persistencia avanzada"

# Variables de entorno
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    THEA_ENV=production

# Instala dependencias del sistema necesarias
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Crea usuario seguro sin privilegios root
RUN groupadd -r theaia && useradd -r -g theaia theaia

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar dependencias y setup script
COPY requirements.txt ./requirements.txt
COPY scripts/setup_env.sh ./scripts/setup_env.sh

# Asignar permisos
RUN chmod +x ./scripts/setup_env.sh

# Actualizar pip y herramientas build
RUN python -m pip install --upgrade pip setuptools wheel build

# Instalar NumPy binario para evitar compilación
RUN pip install numpy==1.26.4 --only-binary=:all:

# Instalar todas las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Descargar modelo básico de spaCy (español)
RUN python -m spacy download es_core_news_sm

# Crear carpetas de logs, modelos, etc.
RUN mkdir -p /app/logs /app/models /app/uploads \
    && chown -R theaia:theaia /app

# Copiar código fuente (usando propiedad del usuario no root)
COPY --chown=theaia:theaia ./src /app/src
COPY --chown=theaia:theaia ./scripts /app/scripts

# Cambiar al usuario no-root
USER theaia

# Exponer puerto principal
EXPOSE 8000

# Healthcheck opcional
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Entrypoint y comando por defecto
ENTRYPOINT ["bash", "scripts/setup_env.sh"]
CMD ["uvicorn", "src.theaia.main:app", "--host", "0.0.0.0", "--port", "8000"]
