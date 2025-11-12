src/config/ - Configuration Module
Módulo de configuración centralizada para THEA IA

📋 Overview
El módulo config/ gestiona toda la configuración de THEA IA de forma centralizada, incluyendo:

⚙️ Settings (variables de entorno)

📝 Logging (configuración logs)

🔢 Constants (valores fijos)

🔐 Secrets (gestión segura)

Patrón: Singleton + Environment-based Configuration

🎯 Propósito
Problema que resuelve:
Sin este módulo:

❌ Configuración dispersa en múltiples archivos

❌ Hardcoded values en código

❌ Difícil cambiar entre development/staging/production

❌ Secrets expuestos en código

❌ Logging inconsistente

Con este módulo:

✅ Configuración centralizada en un solo lugar

✅ Variables de entorno (.env)

✅ Multi-environment support

✅ Secrets seguros

✅ Logging estructurado y consistente

📁 Estructura (H02)
text
src/config/
├── __init__.py                 # Exports principales
├── settings.py                 # Settings con Pydantic
├── logging_config.py           # Setup logging
├── constants.py                # Constantes del proyecto
├── .env.example                # Template variables entorno
├── README.md                   # Este archivo
├── ROADMAP.md                  # Evolución del módulo
├── CHANGELOG.md                # Historial de cambios
├── STRUCTURE.md                # Estructura detallada por hito
└── DEPENDENCIES.md             # Dependencias del módulo
🏗️ Arquitectura
Flujo de Configuración:
text
.env file
    ↓
Settings (Pydantic validation)
    ↓
get_settings() [Singleton]
    ↓
Usado por todos los módulos
Componentes:
1. Settings (settings.py)
Clase Settings que hereda de pydantic.BaseSettings

Carga variables desde .env

Validación automática de tipos

Singleton global accesible vía get_settings()

2. Logging (logging_config.py)
Función setup_logging() para configurar logging

Handlers: console + rotating file

Formato estructurado: timestamp | level | module | message

Niveles configurables por módulo

3. Constants (constants.py)
Valores fijos del proyecto (no en .env)

App constants: VERSION, APP_NAME

Agent types y límites

Error codes

Regex patterns

📦 Dependencias
Python:
text
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
Internas:
text
NINGUNA - config es el módulo más bajo
No depende de otros módulos THEA IA
🚀 Uso
Setup Inicial:
python
# main.py
from src.config import get_settings, setup_logging

def main():
    # 1. Setup logging primero
    setup_logging()
    
    # 2. Cargar settings
    settings = get_settings()
    
    # 3. Usar en toda la app
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
En cualquier módulo:
python
from src.config import get_settings, get_logger
from src.config.constants import AGENT_REMINDER, MAX_REMINDERS_FREE

# Obtener settings (singleton)
settings = get_settings()

# Usar settings
database_url = settings.DATABASE_URL
bot_token = settings.TELEGRAM_BOT_TOKEN
debug_mode = settings.DEBUG

# Obtener logger
logger = get_logger(__name__)
logger.info("Processing reminder")

# Usar constants
if count >= MAX_REMINDERS_FREE:
    logger.warning(f"User reached limit: {MAX_REMINDERS_FREE}")
⚙️ Configuración
1. Crear archivo .env:
bash
# Copiar template
cp .env.example .env

# Editar con tus valores
nano .env
2. Variables Obligatorias (H02):
bash
# Database
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/thea_ia

# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11

# Security
SECRET_KEY=generate_with_openssl_rand_hex_32
3. Generar SECRET_KEY:
bash
python -c "import secrets; print(secrets.token_hex(32))"
🔐 Seguridad
Best Practices:
✅ DO:

Usar .env para todos los secrets

Añadir .env a .gitignore

Usar .env.example sin valores reales

Validar config en startup

Rotar secrets cada 6 meses

❌ DON'T:

Hardcodear tokens/passwords en código

Commitear .env a Git

Compartir .env por email/Slack

Usar mismos secrets en dev/prod

🧪 Testing
Test Settings Loading:
python
# tests/unit/test_config/test_settings.py
import pytest
from src.config import get_settings

def test_settings_loads():
    settings = get_settings()
    assert settings.APP_NAME == "THEA IA"
    assert settings.VERSION is not None
    assert settings.DATABASE_URL is not None

def test_settings_singleton():
    settings1 = get_settings()
    settings2 = get_settings()
    assert settings1 is settings2  # Same instance
Test Logging:
python
# tests/unit/test_config/test_logging.py
import logging
from src.config import setup_logging, get_logger

def test_logging_setup():
    setup_logging()
    logger = get_logger("test")
    
    # Verify logger configured
    assert logger.level == logging.INFO
    assert len(logger.handlers) > 0

def test_logger_writes():
    setup_logging()
    logger = get_logger("test")
    
    # This should not raise
    logger.info("Test message")
    logger.warning("Test warning")
    logger.error("Test error")
Ejecutar tests:
bash
pytest src/tests/unit/test_config/ -v
pytest --cov=src/config --cov-report=html
📊 Estado Actual
H01 (03 Nov 2025):
✅ Estructura definida

✅ Documentación completa

⏳ Sin implementación código

H02 (12-16 Nov 2025):
🎯 Implementar settings.py

🎯 Implementar logging_config.py

🎯 Implementar constants.py

🎯 Crear .env.example

🎯 Tests unitarios

🔮 Próximos Pasos
H04 (20-23 Nov): Enterprise Config
Database config avanzado (pooling, replicas)

Security config (JWT, encryption, rate limiting)

Sentry integration (error tracking)

Multi-environment soporte mejorado

H11 (Feb 2026): Kubernetes Config
ConfigMaps support

Secrets K8s

Multi-environment production-grade

📝 Notas Implementación
Singleton Pattern:
python
# settings.py
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Retorna instancia única de Settings"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
Pydantic Validation:
python
from pydantic import Field, validator

class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str = Field(..., min_length=30)
    LOG_LEVEL: str = Field("INFO", pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    
    @validator('DATABASE_URL')
    def validate_database_url(cls, v):
        if not v.startswith('postgresql'):
            raise ValueError('Database must be PostgreSQL')
        return v
Environment-Specific Config:
python
class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"
    
    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"
🔗 Relaciones con Otros Módulos
Usado por (todos los módulos):
text
src/config/
    ↓
┌───────────────────────────────────────┐
│ main.py                               │
│ src/core/                             │
│ src/agents/                           │
│ src/adapters/                         │
│ src/database/                         │
│ src/models/                           │
│ src/ml/                               │
│ src/services/                         │
│ src/utils/                            │
└───────────────────────────────────────┘
Usa (ninguno):
text
Config es el módulo más bajo en la jerarquía.
No depende de ningún otro módulo THEA IA.
Solo depende de librerías externas (pydantic, dotenv).
📞 Soporte
Issues Comunes:
1. ValidationError al cargar settings

text
Solution: Verificar que todas las variables obligatorias están en .env
2. .env no se carga

text
Solution: Verificar que .env está en root del proyecto
Solution: Verificar que python-dotenv está instalado
3. Logs no aparecen

text
Solution: Llamar setup_logging() antes de cualquier logging
Solution: Verificar permisos carpeta logs/
📚 Recursos
Pydantic Settings Docs

Python Logging Tutorial

12-Factor App Config

👥 Contribuir
Al modificar este módulo:

✅ Actualizar .env.example si añades variables

✅ Añadir validación en Settings si es crítico

✅ Documentar nueva variable en DEPENDENCIES.md

✅ Añadir tests para nueva funcionalidad

✅ Actualizar CHANGELOG.md

Versión: 0.1.0
Estado: Planificación (H01)
Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota