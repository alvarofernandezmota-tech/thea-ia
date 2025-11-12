Dependencias - src/config/
Módulo: Configuration
Versión actual: 0.1.0 (H01 - Planificación)
Última actualización: 11 Nov 2025

📦 Dependencias Python
H02 (12-16 Nov): Config Base
Producción:
text
# Settings Management
pydantic==2.5.0                 # BaseSettings, validación
pydantic-settings==2.1.0        # BaseSettings desde v2
python-dotenv==1.0.0            # Cargar .env

# Logging
# (stdlib, sin deps externas)

# Paths
pathlib                         # (stdlib) Path handling
Desarrollo:
text
# Testing
pytest==7.4.3
pytest-env==1.1.3               # Variables entorno en tests

# Code Quality
black==23.12.0
pylint==3.0.3
mypy==1.7.1
H04 (20-23 Nov): Config Enterprise
Adicionales Producción:
text
# Error Tracking
sentry-sdk==1.40.0              # Sentry integration (opcional)

# Structured Logging
python-json-logger==2.0.7       # JSON logging format
structlog==23.3.0               # Structured logging (alternativa)

# Secrets Management
hvac==2.1.0                     # HashiCorp Vault client (opcional)
boto3==1.34.0                   # AWS Secrets Manager (opcional)
H11 (Feb 2026): Config Kubernetes
Adicionales Producción:
text
# Kubernetes
kubernetes==28.1.0              # K8s Python client
🔗 Dependencias Internas (THEA IA)
Módulos que usa config/:
python
# NINGUNO - config es el módulo más bajo
# No depende de nadie
Módulos que usan config/:
python
# TODOS los módulos

# main.py
from src.config import get_settings, setup_logging

# src/core/
from src.config import get_settings, get_logger
from src.config.constants import *

# src/database/
from src.config import get_settings

# src/adapters/
from src.config import get_settings, get_logger

# src/agents/
from src.config import get_logger
from src.config.constants import AGENT_TYPES, MAX_*

# src/models/
from src.config.constants import DEFAULT_TIMEZONE

# etc.
🌐 Servicios Externos
H04: Sentry (Error Tracking) [OPCIONAL]
text
Servicio: Sentry
URL: https://sentry.io
Auth: DSN (Data Source Name)
Pricing: Free tier 5K errors/mes
Configuración:

bash
# .env
SENTRY_DSN=https://examplePublicKey@o0.ingest.sentry.io/0
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1  # 10% de transacciones
Uso:

python
import sentry_sdk
from src.config import get_settings

settings = get_settings()

if settings.SENTRY_DSN:
    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        environment=settings.SENTRY_ENVIRONMENT,
        traces_sample_rate=settings.SENTRY_TRACES_SAMPLE_RATE
    )
H04: AWS Secrets Manager [OPCIONAL]
text
Servicio: AWS Secrets Manager
Auth: AWS credentials
Pricing: $0.40/mes por secret
Configuración:

bash
# .env
AWS_REGION=eu-west-1
AWS_SECRETS_PREFIX=thea-ia/production/
Uso:

python
import boto3
from src.config import get_settings

def get_secret(secret_name: str) -> dict:
    settings = get_settings()
    client = boto3.client('secretsmanager', region_name=settings.AWS_REGION)
    response = client.get_secret_value(SecretId=f"{settings.AWS_SECRETS_PREFIX}{secret_name}")
    return json.loads(response['SecretString'])
🔐 Variables de Entorno
Archivo .env.example (config):
bash
# ============================================
# THEA IA - CONFIGURATION
# ============================================

# ----------------
# APP SETTINGS
# ----------------
APP_NAME=THEA IA
VERSION=0.2.0
ENVIRONMENT=development  # development, staging, production
DEBUG=False

# ----------------
# DATABASE
# ----------------
DATABASE_URL=postgresql+asyncpg://thea:password@localhost:5432/thea_ia
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=False  # Log SQL queries (debug only)

# ----------------
# TELEGRAM
# ----------------
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_WEBHOOK_URL=  # Opcional (polling por defecto)
TELEGRAM_WEBHOOK_SECRET=  # Requerido si webhook
TELEGRAM_USE_WEBHOOK=False

# ----------------
# LOGGING
# ----------------
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/thea.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Logging avanzado (H04)
LOG_FORMAT=json  # text, json
SENTRY_DSN=  # Opcional
SENTRY_ENVIRONMENT=development
SENTRY_TRACES_SAMPLE_RATE=0.1

# ----------------
# SECURITY
# ----------------
SECRET_KEY=  # Generar con: openssl rand -hex 32

# JWT (H04)
JWT_SECRET_KEY=  # Generar con: openssl rand -hex 32
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=1440

# ----------------
# PATHS
# ----------------
BASE_DIR=.
DATA_DIR=data
LOGS_DIR=logs

# ----------------
# AWS (H04 - Opcional)
# ----------------
AWS_REGION=eu-west-1
AWS_SECRETS_PREFIX=thea-ia/production/

# ----------------
# MONITORING (H12)
# ----------------
PROMETHEUS_PORT=9090
GRAFANA_API_KEY=
📊 Tabla Resumen Dependencias por Hito
Hito	Deps Python Prod	Deps Python Dev	Servicios Externos	Variables .env
H02	3	4	0	15 vars
H04	+4 (opcionales)	0	2 (Sentry, AWS)	+10 vars
H11	+1	0	1 (Kubernetes)	+5 vars
Total	8	4	3	30 vars
🚀 Instalación Dependencias
H02 (Setup inicial):
bash
# Instalar dependencias producción
pip install pydantic==2.5.0 pydantic-settings==2.1.0 python-dotenv==1.0.0

# Instalar dependencias desarrollo
pip install pytest==7.4.3 pytest-env==1.1.3 black==23.12.0 pylint==3.0.3 mypy==1.7.1

# Crear .env desde template
cp .env.example .env
# Editar .env con tus valores reales

# Verificar instalación
python -c "from src.config import get_settings; print('OK')"
Generar SECRET_KEY:
bash
# Generar secret key seguro
python -c "import secrets; print(secrets.token_hex(32))"

# Añadir a .env
echo "SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')" >> .env
🧪 Testing Dependencias
Test settings loading:
bash
# Verificar que .env se carga correctamente
python -c "
from src.config import get_settings
settings = get_settings()
print(f'App: {settings.APP_NAME}')
print(f'DB: {settings.DATABASE_URL}')
print(f'Token: {settings.TELEGRAM_BOT_TOKEN[:10]}...')
"
Test logging:
bash
# Verificar logging funciona
python -c "
from src.config import setup_logging, get_logger
setup_logging()
logger = get_logger('test')
logger.info('Test log message')
"
# Verificar que aparece en console y logs/thea.log
⚠️ Notas Seguridad
Secrets Management:
❌ NUNCA commitear .env a Git

✅ Siempre usar .env.example sin valores reales

✅ Añadir .env a .gitignore

✅ Usar secrets manager (Vault, AWS) en producción (H04)

✅ Rotar secrets cada 6 meses

Validación:
✅ Pydantic valida tipos y formatos automáticamente

✅ Errores claros si config inválida

✅ Usar Field() para validaciones custom

python
from pydantic import Field

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., min_length=30)
    LOG_LEVEL: str = Field("INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
📝 Best Practices
1. Environment-specific config:
bash
# Development
.env

# Staging
.env.staging

# Production
.env.production  # O variables entorno K8s
2. Secrets en producción:
python
# Cargar desde Vault/AWS en producción
if settings.ENVIRONMENT == "production":
    secrets = load_from_vault()
    settings.DATABASE_PASSWORD = secrets['db_password']
3. Config validation en startup:
python
# main.py
def main():
    try:
        settings = get_settings()
    except ValidationError as e:
        logger.critical(f"Invalid configuration: {e}")
        sys.exit(1)
📞 Recursos
Documentación Oficial:
Pydantic Settings: https://docs.pydantic.dev/latest/concepts/pydantic_settings/

Python Logging: https://docs.python.org/3/library/logging.html

Python Dotenv: https://pypi.org/project/python-dotenv/

Sentry Python: https://docs.sentry.io/platforms/python/

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota