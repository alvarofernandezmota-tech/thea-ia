⚙️ Configuration — THEA IA
Versión: v0.14.0
Última actualización: 2025-11-09 19:17 CET (Sesión 37)
Responsable: Álvaro Fernández Mota (CEO THEA IA)
Estado: ✅ Activo

📋 Propósito
Referencia completa de variables de entorno y configuración para THEA IA.

🔧 Variables de Entorno
App Core
bash
ENVIRONMENT=development|production|staging
LOG_LEVEL=DEBUG|INFO|WARNING|ERROR|CRITICAL
SECRET_KEY=<random-string-64-chars>  # Para sesiones/cookies
DEBUG=false  # Solo dev
Database
bash
# PostgreSQL (recomendado prod)
DATABASE_URL=postgresql://user:password@localhost:5432/theaia

# SQLite (dev/testing)
DATABASE_URL=sqlite:///thea.db

# Parámetros conexión
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
DATABASE_POOL_TIMEOUT=30
DATABASE_POOL_RECYCLE=3600
Authentication & Security
bash
# JWT
JWT_SECRET=<random-string-64-chars>
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600  # segundos (1h)
JWT_REFRESH_EXPIRATION=604800  # 7 días

# OAuth2 (si usas)
OAUTH_GOOGLE_CLIENT_ID=...
OAUTH_GOOGLE_CLIENT_SECRET=...

# CORS
CORS_ORIGINS=["http://localhost:3000","https://yourdomain.com"]

# Rate limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100  # per
RATE_LIMIT_WINDOW=60  # seconds
Telegram Adapter
bash
TELEGRAM_BOT_TOKEN=<your-bot-token>
TELEGRAM_WEBHOOK_URL=https://your-domain.com/adapters/telegram/webhook
TELEGRAM_ALLOWED_USER_IDS=123456,789012  # optional whitelist
ML & NLP
bash
# spaCy
SPACY_MODEL=es_core_news_sm  # Spanish model

# Intent detection
INTENT_CONFIDENCE_THRESHOLD=0.7
ENTITY_CONFIDENCE_THRESHOLD=0.6

# Training data path
TRAINING_DATA_PATH=data/training_data.json
MODEL_PATH=models/
Observability & Monitoring
bash
# Prometheus
PROMETHEUS_ENABLED=true
PROMETHEUS_PORT=9090

# Loki (logs)
LOKI_ENABLED=true
LOKI_URL=http://localhost:3100

# Jaeger (traces)
JAEGER_ENABLED=true
JAEGER_AGENT_HOST=localhost
JAEGER_AGENT_PORT=6831
JAEGER_SAMPLER_TYPE=const  # probabilistic, const, remote
JAEGER_SAMPLER_PARAM=1  # 0.0-1.0 para probabilistic

# OpenTelemetry
OTEL_ENABLED=false
OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
Storage & Caching
bash
# Redis (opcional, para caching/sessions)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0

# S3 (para archivos/backups)
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_S3_BUCKET=thea-ia-files
AWS_S3_REGION=us-east-1
Email (notificaciones)
bash
SMTP_ENABLED=false
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=<app-password>
SMTP_FROM=noreply@thea-ia.com
📝 Archivo .env.example
bash
# =============================================================================
# THEA IA Configuration
# =============================================================================

# App
ENVIRONMENT=development
LOG_LEVEL=INFO
SECRET_KEY=dev-secret-change-in-prod
DEBUG=false

# Database
DATABASE_URL=sqlite:///thea.db
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20

# JWT
JWT_SECRET=dev-jwt-secret-change-in-prod
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Telegram
TELEGRAM_BOT_TOKEN=your-bot-token-here
TELEGRAM_WEBHOOK_URL=http://localhost:8000/adapters/telegram/webhook

# ML
SPACY_MODEL=es_core_news_sm
INTENT_CONFIDENCE_THRESHOLD=0.7

# Monitoring
PROMETHEUS_ENABLED=true
LOKI_ENABLED=true
JAEGER_ENABLED=false

# Redis (opcional)
REDIS_ENABLED=false
REDIS_URL=redis://localhost:6379/0
🔐 Desarrollo vs Producción
Development (.env.development)
bash
ENVIRONMENT=development
DEBUG=true
LOG_LEVEL=DEBUG
DATABASE_URL=sqlite:///thea.db
JWT_SECRET=dev-secret
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
JAEGER_ENABLED=false  # para no saturar
Producción (.env.production)
bash
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://user:secure-pass@prod-db.com:5432/theaia
JWT_SECRET=<use-vault-or-secrets-manager>
CORS_ORIGINS=["https://yourdomain.com"]
JAEGER_ENABLED=true
JAEGER_SAMPLER_PARAM=0.1  # 10% sampling
RATE_LIMIT_ENABLED=true
🔄 Cargar Configuración en Código
Usando Pydantic Settings
python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "sqlite:///thea.db"
    jwt_secret: str
    jwt_expiration: int = 3600
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
Acceder en app
python
from src.theaia.core.config import settings

# En FastAPI
app = FastAPI(
    title="THEA IA",
    debug=settings.DEBUG,
    log_level=settings.LOG_LEVEL
)

# En cualquier lugar
print(f"DB: {settings.database_url}")
print(f"Environment: {settings.environment}")
✅ Validación de Configuración
Script de validación
bash
python -m src.theaia.scripts.validate_config
Checklist pre-deploy
 ENVIRONMENT=production

 DEBUG=false

 JWT_SECRET es único y seguro (64+ chars)

 DATABASE_URL apunta a BD producción

 CORS_ORIGINS solo incluye dominios permitidos

 TELEGRAM_BOT_TOKEN es válido

 JAEGER_ENABLED=true en producción

 Todos los secretos en Kubernetes Secrets o HashiCorp Vault

 .env local NO está commiteado a Git

🔒 Secretos & Vault
Kubernetes Secrets
bash
# Crear secret
kubectl create secret generic thea-secrets \
  --from-literal=JWT_SECRET=<value> \
  --from-literal=DATABASE_PASSWORD=<value> \
  -n thea-ia

# Usar en pod
env:
- name: JWT_SECRET
  valueFrom:
    secretKeyRef:
      name: thea-secrets
      key: JWT_SECRET
HashiCorp Vault
python
import hvac

client = hvac.Client(url='http://vault:8200')
secrets = client.secrets.kv.v2.read_secret_version(path='thea-ia')
jwt_secret = secrets['data']['data']['JWT_SECRET']
📊 Volver a aplicar config en runtime
bash
# Recargar sin restart (graceful reload)
curl -X POST http://localhost:8000/admin/reload-config

# Validar config actual
curl http://localhost:8000/admin/config/validate

# Ver config (secretos enmascarados)
curl http://localhost:8000/admin/config
📌 Meta-información
Campo	Valor
Archivo	docs/guides/configuration.md
Versión	v0.14.0
Última revisión	2025-11-09 19:17 CET (S37)
Responsable	CEO THEA IA
Estado	✅ Activo
Última actualización: 2025-11-09 19:17 CET