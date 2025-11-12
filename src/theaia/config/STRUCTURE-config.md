Estructura Planificada - src/config/
Módulo: Configuration (Configuración centralizada)
Propósito: Gestión configuración, settings, constantes y logging
Patrón: Singleton + Settings Management (Pydantic)

📋 Estado Actual (11 Nov 2025 - H01)
text
src/config/
├── __init__.py (placeholder)
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅
Estado: Sin implementación, solo planificación

🎯 H02 (12-16 Nov): Config Base
Estructura Objetivo:
text
src/config/
│
├── __init__.py
│   # Exports: Settings, get_settings, setup_logging
│
├── settings.py ← 🆕 CREAR H02 DÍA 1
│   # Clase Settings(BaseSettings)
│   # Variables de entorno centralizadas
│   # Validación automática con Pydantic
│   # Singleton pattern para config global
│   #
│   # Sections:
│   #   - App settings (nombre, versión, debug)
│   #   - Database settings (PostgreSQL)
│   #   - Telegram settings (bot token, webhook)
│   #   - Logging settings (level, formato)
│   #   - Security settings (secrets)
│
├── logging_config.py ← 🆕 CREAR H02 DÍA 1
│   # Función setup_logging()
│   # Configuración logging estructurado
│   # Handlers: console, file, rotating
│   # Formato: timestamp, level, module, message
│   # Niveles por módulo configurables
│   #
│   # Funciones:
│   #   - setup_logging() -> None
│   #   - get_logger(name: str) -> logging.Logger
│
├── constants.py ← 🆕 CREAR H02 DÍA 1
│   # Constantes del proyecto
│   # No usar variables de entorno aquí
│   #
│   # Categories:
│   #   - App constants (VERSION, APP_NAME)
│   #   - Agent constants (tipos, límites)
│   #   - Error codes
│   #   - Default values
│   #   - Regexes comunes
│
├── .env.example ← 🆕 CREAR H02 DÍA 1
│   # Template variables de entorno
│   # Sin valores reales (ejemplo)
│   # Documentado con comentarios
│
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── STRUCTURE.md (este archivo)
└── DEPENDENCIES.md
Archivos Detallados H02:
settings.py (Día 1):
python
# Estructura planificada (sin código completo)

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Configuración centralizada THEA IA"""
    
    # App
    APP_NAME: str = "THEA IA"
    VERSION: str = "0.2.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Database (PostgreSQL)
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 5
    DATABASE_MAX_OVERFLOW: int = 10
    DATABASE_ECHO: bool = False  # Log SQL queries
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_WEBHOOK_URL: Optional[str] = None
    TELEGRAM_WEBHOOK_SECRET: Optional[str] = None
    TELEGRAM_USE_WEBHOOK: bool = False  # Polling por defecto
    
    # Logging
    LOG_LEVEL: str = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FILE: str = "logs/thea.log"
    LOG_MAX_BYTES: int = 10_485_760  # 10MB
    LOG_BACKUP_COUNT: int = 5
    
    # Security
    SECRET_KEY: str
    
    # Paths
    BASE_DIR: str = "."
    DATA_DIR: str = "data"
    LOGS_DIR: str = "logs"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Singleton
_settings: Optional[Settings] = None

def get_settings() -> Settings:
    """Obtiene instancia única de Settings"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
logging_config.py (Día 1):
python
# Estructura planificada

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

def setup_logging(
    level: str = "INFO",
    log_file: str = "logs/thea.log",
    max_bytes: int = 10_485_760,
    backup_count: int = 5
) -> None:
    """
    Configura logging para toda la aplicación.
    
    Features:
    - Console handler (stdout)
    - File handler (rotating)
    - Formato estructurado
    - Niveles por módulo
    """
    
    # Crear directorio logs si no existe
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # Formato logging
    fmt = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    
    # Root logger
    # Console handler
    # File handler (rotating)
    # Configurar niveles por módulo
    
def get_logger(name: str) -> logging.Logger:
    """Obtiene logger para módulo específico"""
    return logging.getLogger(name)
constants.py (Día 1):
python
# Estructura planificada

# App
APP_NAME = "THEA IA"
VERSION = "0.2.0"
DESCRIPTION = "Asistente Personal con IA"

# Agent Types
AGENT_REMINDER = "reminder"
AGENT_NOTE = "note"
AGENT_EVENT = "event"
AGENT_TASK = "task"
AGENT_AGENDA = "agenda"
AGENT_CONTEXT = "context"
AGENT_CONFIG = "config"
AGENT_QUERY = "query"

AGENT_TYPES = [
    AGENT_REMINDER,
    AGENT_NOTE,
    AGENT_EVENT,
    AGENT_TASK,
    AGENT_AGENDA,
    AGENT_CONTEXT,
    AGENT_CONFIG,
    AGENT_QUERY,
]

# Limits (Free tier)
MAX_REMINDERS_FREE = 10
MAX_NOTES_FREE = 20
MAX_EVENTS_FREE = 10
MAX_TASKS_FREE = 15

# Limits (Pro tier)
MAX_REMINDERS_PRO = -1  # Unlimited
MAX_NOTES_PRO = -1
MAX_EVENTS_PRO = -1
MAX_TASKS_PRO = -1

# Error Codes
ERROR_INVALID_INPUT = "E001"
ERROR_DATABASE = "E002"
ERROR_ADAPTER = "E003"
ERROR_AGENT = "E004"
ERROR_AUTH = "E005"

# Regex
REGEX_DATETIME = r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
REGEX_DATE = r"\d{4}-\d{2}-\d{2}"
REGEX_TIME = r"\d{2}:\d{2}"

# Default values
DEFAULT_TIMEZONE = "Europe/Madrid"
DEFAULT_LANGUAGE = "es"
DEFAULT_REMINDER_ADVANCE = 15  # minutos
.env.example (Día 1):
bash
# ============================================
# THEA IA - Configuration
# ============================================

# Environment
ENVIRONMENT=development  # development, staging, production
DEBUG=False

# Database (PostgreSQL)
DATABASE_URL=postgresql+asyncpg://thea:password@localhost:5432/thea_ia
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO=False

# Telegram
TELEGRAM_BOT_TOKEN=123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11
TELEGRAM_WEBHOOK_URL=  # Opcional (polling por defecto)
TELEGRAM_WEBHOOK_SECRET=  # Requerido si webhook
TELEGRAM_USE_WEBHOOK=False

# Logging
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE=logs/thea.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5

# Security
SECRET_KEY=  # Generar con: openssl rand -hex 32

# Paths
BASE_DIR=.
DATA_DIR=data
LOGS_DIR=logs
🔮 H04 (20-23 Nov): Config Enterprise
Estructura Ampliada:
text
src/config/
├── __init__.py
├── settings.py (extendido)
├── database_config.py ← 🆕 H04
│   # Configuración avanzada database
│   # Connection pooling
│   # Read replicas
│   # RLS (Row Level Security)
│
├── security_config.py ← 🆕 H04
│   # JWT settings
│   # Encryption keys
│   # Rate limiting config
│   # CORS settings
│
├── logging_config.py (extendido)
│   # Sentry integration
│   # ELK stack support
│   # Structured logging
│
├── constants.py (extendido)
│   # Business tier constants
│   # Compliance constants
│
└── ...
⚙️ H11 (Feb 2026): Config Kubernetes
Estructura Cloud-Native:
text
src/config/
├── settings.py (multi-environment)
│   # Soporta env vars Kubernetes
│   # ConfigMaps
│   # Secrets
│
├── k8s/ ← 🆕 H11
│   ├── configmap.yaml
│   ├── secrets.yaml (template)
│   └── env-vars.yaml
│
└── ...
📐 Patrones de Diseño
Singleton:
Settings instancia única global

get_settings() retorna siempre misma instancia

Environment-based Config:
.env para local development

Variables de entorno para staging/production

Validación automática Pydantic

Separation of Concerns:
settings.py: Variables dinámicas (.env)

constants.py: Valores fijos (hardcoded)

logging_config.py: Setup logging

Cada archivo una responsabilidad

🔗 Dependencias Internas
text
src/config/ es usado por:
├── src/main.py (setup inicial)
├── src/core/ (obtiene settings)
├── src/database/ (connection settings)
├── src/adapters/ (bot tokens)
├── src/agents/ (constantes, límites)
└── TODOS los módulos (logging)
text
src/config/ NO depende de nadie
└── Es el módulo más bajo en jerarquía
📊 Métricas Estimadas
H02:
Archivos: 4 archivos Python + 1 .env.example

Líneas código: ~300 LOC

Tests: ~150 LOC

Cobertura objetivo: >90%

H04:
Archivos adicionales: +3

LOC adicional: ~400

Tests adicionales: ~200 LOC

🎯 Criterios de Completitud
H02 Done cuando:
✅ Settings clase implementada

✅ Pydantic valida todas las variables

✅ .env.example completo y documentado

✅ setup_logging() funciona

✅ Console + file logging activos

✅ constants.py con valores necesarios

✅ Tests de settings y logging pasan

✅ Sin secretos en código (todo en .env)

H04 Done cuando:
✅ Database config avanzado

✅ Security config completo

✅ Sentry integrado (opcional)

✅ Multi-environment support

🚀 Uso Planificado
En main.py:
python
from src.config import get_settings, setup_logging

def main():
    # Setup logging primero
    setup_logging()
    
    # Obtener settings
    settings = get_settings()
    
    # Usar en toda la app
    logger.info(f"Starting {settings.APP_NAME} v{settings.VERSION}")
En otros módulos:
python
from src.config import get_settings, get_logger
from src.config.constants import AGENT_REMINDER, MAX_REMINDERS_FREE

settings = get_settings()
logger = get_logger(__name__)

# Usar settings
db_url = settings.DATABASE_URL

# Usar constants
if count >= MAX_REMINDERS_FREE:
    raise LimitExceeded()
📝 Notas Implementación
Seguridad:
❌ NUNCA hardcodear tokens/passwords

✅ Siempre .env para secrets

✅ .env en .gitignore

✅ .env.example sin valores reales

Validación:
Pydantic valida tipos automáticamente

Errores claros si config inválida

Defaults razonables donde posible

Testing:
Tests con .env.test

Mocks de settings en tests

No usar settings reales en tests

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota