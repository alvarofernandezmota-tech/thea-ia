
# Dependencias - src/database/

**Módulo:** Database  
**Versión actual:** 0.2.0 (H02 Day 1 - 50% ✅)  
**Última actualización:** 12 Nov 2025, 16:22 CET

---

## 📦 Dependencias Python

### H02 (12-16 Nov): Database Base ✅

#### Producción (INSTALADAS ✅):

ORM
sqlalchemy==2.0.23 # SQLAlchemy ORM async support
sqlalchemy[asyncio]==2.0.23 # Async extensions

PostgreSQL Drivers
asyncpg==0.29.0 # Async PostgreSQL driver (principal) ✅
psycopg2-binary==2.9.9 # Sync driver (Alembic migrations) ✅

Migrations
alembic==1.12.1 # Database migrations ✅

Async Support
greenlet==3.0.1 # Required for async SQLAlchemy ✅

text

**Estado:** ✅ Todas instaladas y funcionando (12 Nov 16:17)

#### Desarrollo:

Testing
pytest==7.4.3
pytest-asyncio==0.21.1 # Async tests
pytest-postgresql==5.0.0 # PostgreSQL test fixtures

text

**Estado:** ⏳ Pendiente instalar (H02 Day 2)

---

### H04 (20-23 Nov): Database Enterprise

#### Adicionales Producción:

Connection Pooling Avanzado
sqlalchemy-utils==0.41.1 # Utilities (database exists, etc)
pg8000==1.30.3 # Alternative pure-Python driver

Monitoring
sqlalchemy-instrumentation==0.1.0 # SQLAlchemy metrics

text

---

## 🔗 Dependencias Internas (THEA IA)

### Módulos que usa database/:

Obligatorias H02 (ACTIVAS ✅)
from src.config import get_settings, get_logger # Settings y logging
from src.config.constants import * # Constantes

Opcionales (validación) - H02 Day 2
from src.models import * # Schemas Pydantic para validación repos

text

### Módulos que usan database/:

src/agents/ (todos) - H02 Day 2+
from src.database.repositories import (
EventRepository,
NoteRepository,
ConversationRepository,
MessageHistoryRepository
)
from src.database.models import Event, Note, Conversation, MessageHistory

src/adapters/ - H02 Day 2 ✅
from src.database.repositories import UserRepository
from src.database.models import User
from src.database import get_db

src/core/ - H02 Day 2+
from src.database.repositories import ConversationRepository, UserRepository
from src.database import get_db

src/services/ (H05-H06)
from src.database.repositories import *

text

---

## 🌐 Servicios Externos

### PostgreSQL Database

Servicio: PostgreSQL 18 (instalado localmente)
Desarrollo: Instalación nativa Windows ✅
Staging: Railway/Render (próximo)
Producción: AWS RDS / Google Cloud SQL (próximo)

text

#### Desarrollo (Nativo Windows) ✅:

**Instalación actual (12 Nov):**
Versión: PostgreSQL 18
Path: C:\Program Files\PostgreSQL\18
Usuario: postgres
Database: thea_ia
Puerto: 5432
Auth: trust mode (pg_hba.conf)
Estado: ✅ Corriendo (33 procesos activos)

text

**Configuración aplicada:**
- `pg_hba.conf`: trust mode para 127.0.0.1
- `postgresql.conf`: listen_addresses = '*'
- Connection: 127.0.0.1:5432 (evita WinError 64)

#### Docker (Alternativa):

docker-compose.yml
services:
postgres:
image: postgres:16
environment:
POSTGRES_USER: postgres
POSTGRES_PASSWORD: postgres
POSTGRES_DB: thea_ia
ports:
- "5432:5432"
volumes:
- postgres_data:/var/lib/postgresql/data

text

#### Staging/Producción (Próximo):

**Railway:**
URL: postgresql://user:pass@containers-us-west-x.railway.app:port/railway
Pricing: $5/mes + $0.000463/GB-hour
Backup: Automático
SSL: Requerido

text

**AWS RDS:**
URL: postgresql://user:pass@instance.region.rds.amazonaws.com:5432/thea_ia
Instance: db.t3.micro (dev) / db.t3.small (prod)
Pricing: ~$15-30/mes
Backup: Automático 7 días
SSL: Requerido

text

---

## 🔐 Variables de Entorno

### Archivo .env (database) - ACTUALIZADO 12 Nov ✅:

============================================
DATABASE CONFIGURATION - H02
Actualizado: 12 Nov 2025, 16:00 CET
============================================
Connection URL (SIN PASSWORD - trust mode desarrollo)
DATABASE_URL=postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia

Pool Configuration
DATABASE_POOL_SIZE=5 # Connections in pool
DATABASE_MAX_OVERFLOW=10 # Max extra connections
DATABASE_POOL_RECYCLE=3600 # Recycle connections after 1h
DATABASE_POOL_TIMEOUT=30 # Timeout getting connection (seconds)

Debug
DATABASE_ECHO=False # Log all SQL (True solo en debug)

SSL (Producción)
DATABASE_SSL_MODE=disable # disable (dev) / require (prod)
DATABASE_SSL_CA= # Path to CA certificate

text

**Cambios 12 Nov:**
- ✅ URL sin password (`:postgres` eliminado)
- ✅ Host: `127.0.0.1` en lugar de `localhost`
- ✅ Driver: `asyncpg` para async
- ✅ SSL: `disable` en desarrollo

---

## 📊 Tabla Resumen Dependencias

| Hito | Deps Python Prod | Deps Python Dev | Servicios Externos |
|------|------------------|-----------------|-------------------|
| H02  | 6 ✅             | 3 ⏳            | PostgreSQL 18 ✅  |
| H04  | +3               | 0               | PostgreSQL + Monitoring |

---

## 🚀 Instalación Dependencias

### H02 (Setup inicial) - COMPLETADO 12 Nov ✅:

Instalar dependencias producción
pip install sqlalchemy[asyncio]==2.0.23 asyncpg==0.29.0 psycopg2-binary==2.9.9 alembic==1.12.1 greenlet==3.0.1

Instalar dependencias desarrollo (próximo)
pip install pytest==7.4.3 pytest-asyncio==0.21.1 pytest-postgresql==5.0.0

Setup PostgreSQL (ya instalado nativamente)
PostgreSQL 18 corriendo en C:\Program Files\PostgreSQL\18\
Verificar conexión ✅
python -c "
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine

async def test_connection():
engine = create_async_engine('postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia')
async with engine.begin() as conn:
result = await conn.execute('SELECT 1')
print('✅ Connection OK:', result.scalar())
await engine.dispose()

asyncio.run(test_connection())
"

text

**Resultado 12 Nov:** ✅ Conexión exitosa

---

## 🔧 Setup Alembic - COMPLETADO 12 Nov ✅

### Inicialización:

Inicializar Alembic (completado)
alembic init src/database/migrations

Editar alembic.ini (completado)
Cambiado: sqlalchemy.url = postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia
Editar src/database/migrations/env.py (completado)
Añadido:
from src.config import get_settings
from src.database.base import Base
from src.database.models import * # Import all models

config.set_main_option("sqlalchemy.url", "postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia")
target_metadata = Base.metadata

text

### Crear primera migración - COMPLETADO 12 Nov ✅:

Auto-generar migración desde modelos
alembic revision --autogenerate -m "initial schema with tenant support"

Resultado: e0a17d850507_initial_schema.py (285 líneas)
Aplicar migración
alembic upgrade head

Resultado: ✅ 5 tablas creadas (users, events, notes, conversations, message_history)
Verificar
alembic current

Output: e0a17d850507 (head), Initial schema with tenant support
text

**Estado:** ✅ Migración aplicada exitosamente (12 Nov 16:11)

---

## 🧪 Testing Dependencias

### Test PostgreSQL Connection:

tests/unit/test_database/test_connection.py
import pytest
from src.database import engine, get_db

@pytest.mark.asyncio
async def test_engine_connects():
async with engine.begin() as conn:
result = await conn.execute("SELECT 1")
assert result.scalar() == 1

@pytest.mark.asyncio
async def test_session_context_manager():
async with get_db() as session:
result = await session.execute("SELECT 1")
assert result.scalar() == 1

text

### Ejecutar tests (Próximo H02 Day 2):

Solo tests database
pytest src/tests/unit/test_database/ -v

Con coverage
pytest --cov=src/database --cov-report=html

Ver coverage
open htmlcov/index.html

text

---

## ⚠️ Notas Seguridad

### Connection String:

❌ **NUNCA:**
NO hardcodear en código
DATABASE_URL = "postgresql://user:pass@host/db"

text

✅ **SIEMPRE:**
Usar .env
from src.config import get_settings
DATABASE_URL = get_settings().DATABASE_URL

text

### SQL Injection:

✅ **Usar siempre parámetros:**
Correcto (SQLAlchemy protege automáticamente)
result = await session.execute(
select(User).where(User.telegram_id == user_id)
)

❌ NUNCA string formatting
query = f"SELECT * FROM users WHERE telegram_id = {user_id}"
text

### Connection Pooling:

- Limitar pool_size (5-10 para apps pequeñas) ✅
- Configurar max_overflow (2x pool_size) ✅
- Recycle connections regularmente ✅
- Timeout razonable (30 segundos) ✅

**Configuración actual (12 Nov):**
- Pool: NullPool (desarrollo, sin pooling)
- Producción: AsyncSessionLocal con pool_size=5

---

## 🔍 Troubleshooting

### 1. "asyncpg.exceptions.InvalidCatalogNameError: database does not exist"

Crear database manualmente
psql -U postgres
CREATE DATABASE thea_ia;
\q

text

**Estado:** ✅ Resuelto (database thea_ia existe)

### 2. "sqlalchemy.exc.OperationalError: connection refused"

Verificar PostgreSQL corriendo
Get-Process -Name postgres

Verificar puerto
netstat -an | findstr 5432

Verificar .env tiene URL correcta
cat .env | findstr DATABASE_URL

text

**Estado:** ✅ Resuelto (PostgreSQL corriendo, 33 procesos)

### 3. "alembic.util.exc.CommandError: Can't locate revision"

Limpiar historial Alembic
rm -rf src/database/migrations/versions/*.py

Recrear migración
alembic revision --autogenerate -m "initial schema"
alembic upgrade head

text

**Estado:** ✅ Resuelto (migración e0a17d850507 aplicada)

### 4. "asyncio.run() cannot be called from a running event loop"

En Jupyter/IPython usar:
await your_async_function()

NO usar:
asyncio.run(your_async_function()) # Falla en notebook
text

### 5. "ConnectionDoesNotExistError: connection was closed in the middle of operation" (WinError 64)

**Causa:** Problema de red Windows con `localhost`

**Solución aplicada (12 Nov):**
❌ ANTES
DATABASE_URL = "postgresql+asyncpg://postgres@localhost:5432/thea_ia"

✅ DESPUÉS
DATABASE_URL = "postgresql+asyncpg://postgres@127.0.0.1:5432/thea_ia"

text

**Estado:** ✅ Resuelto

### 6. "pg_hba.conf authentication failed"

**Solución aplicada (12 Nov):**

Editar `C:\Program Files\PostgreSQL\18\data\pg_hba.conf`:
Cambiar línea:
host all all 127.0.0.1/32 scram-sha-256

Por:
host all all 127.0.0.1/32 trust

text

Reiniciar PostgreSQL (desde servicios Windows o comando):
Restart-Service postgresql-x64-18

text

**Estado:** ✅ Resuelto

---

## 📈 Performance

### Connection Pool Sizing:

Regla general:
pool_size = (num_cores * 2) + effective_spindle_count
Para app pequeña: 5-10
Para app mediana: 20-50
Para app grande: 100+
THEA IA H02 (actual):
DATABASE_POOL_SIZE = 5
DATABASE_MAX_OVERFLOW = 10

= Max 15 connections simultáneas
text

### Query Optimization:

✅ Eager loading (si necesitas relaciones)
users = await session.execute(
select(User).options(selectinload(User.events))
)

✅ Lazy loading (por defecto, mejor performance)
user = await session.get(User, user_id)

events se cargan solo si accedes: user.events
❌ N+1 problem
users = await session.execute(select(User))
for user in users:
# Esto hace 1 query por user (malo)
print(user.events)

text

**Índices aplicados (12 Nov):**
- ✅ 20+ índices en columnas frecuentes
- ✅ tenant_id (todas las tablas)
- ✅ user_id (foreign keys)
- ✅ datetime fields (start_datetime, reminder_datetime, created_at)
- ✅ status, is_active (filtros comunes)
- ✅ session_id, message_id (lookups únicos)

---

## 📚 Recursos

### Documentación Oficial:
- [SQLAlchemy 2.0 Docs](https://docs.sqlalchemy.org/en/20/)
- [SQLAlchemy Async](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)
- [Alembic Docs](https://alembic.sqlalchemy.org/)
- [asyncpg Docs](https://magicstack.github.io/asyncpg/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/18/)

### Tutoriales:
- [SQLAlchemy 2.0 Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)

---

## 🔄 Actualización Dependencias

### Política:
- **SQLAlchemy:** Actualizar a minor versions (2.0.x → 2.0.y) cada 3 meses
- **asyncpg:** Actualizar a minor/patch cada mes
- **Alembic:** Actualizar a minor versions cada 6 meses
- **PostgreSQL:** Actualizar a versions patch regularmente, major con cuidado

### Comando:

Ver outdated
pip list --outdated | findstr "sqlalchemy asyncpg alembic"

Actualizar específica
pip install --upgrade sqlalchemy

Actualizar todas (con cuidado)
pip install --upgrade -r requirements.txt

Ejecutar tests después
pytest src/tests/unit/test_database/ -v

text

---

## 📦 Requirements.txt Actual

Database H02 (instaladas 12 Nov)
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
psycopg2-binary==2.9.9
alembic==1.12.1
greenlet==3.0.1

Testing (próximo H02 Day 2)
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-postgresql==5.0.0

text

---

**Última actualización:** 12 Nov 2025, 16:22 CET  
**Versión:** 1.1  
**Responsable:** Álvaro Fernández Mota

**Estado:** H02 Day 1 COMPLETADO ✅ | Todas las deps instaladas y funcionando 🚀
