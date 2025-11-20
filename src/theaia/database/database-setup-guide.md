🗄️ Database Setup Guide — THEA IA
Guía completa paso a paso para configurar PostgreSQL desde cero en cualquier sistema operativo.

📋 Requisitos Previos
PostgreSQL 14+ (recomendado 16 o 18)

Python 3.11+

Paquetes Python: asyncpg, alembic, sqlalchemy[asyncio]

Permisos: Administrador (Windows) o sudo (Linux/macOS)

1️⃣ Instalación PostgreSQL
Windows
Método 1: Instalador Oficial (Recomendado)

Descargar desde postgresql.org/download/windows

Ejecutar instalador .exe (PostgreSQL-16-windows-x64.exe o superior)

Durante instalación:

Directorio: C:\Program Files\PostgreSQL\16 (default)

Puerto: 5432 (default)

Superuser: postgres

Password: Anotar bien (usarás este password)

Locale: Spanish / UTF8

Componentes: pgAdmin 4, Stack Builder (opcional)

Añadir a PATH (opcional):

text
setx PATH "%PATH%;C:\Program Files\PostgreSQL\16\bin"
Verificar instalación:

text
psql --version
Output esperado: psql (PostgreSQL) 16.x

Método 2: Chocolatey

powershell
# Instalar Chocolatey primero si no lo tienes
choco install postgresql16

# Verificar
psql --version
macOS
Método 1: Homebrew (Recomendado)

bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar PostgreSQL
brew install postgresql@16

# Iniciar servicio automáticamente
brew services start postgresql@16

# Verificar
psql --version
Método 2: Postgres.app

Descargar desde postgresapp.com

Arrastrar a Applications

Abrir Postgres.app

Hacer clic en "Initialize" para crear cluster

Linux (Ubuntu/Debian)
bash
# Actualizar repositorios
sudo apt update

# Instalar PostgreSQL
sudo apt install postgresql-16 postgresql-contrib

# Iniciar servicio
sudo systemctl start postgresql

# Habilitar inicio automático
sudo systemctl enable postgresql

# Verificar estado
sudo systemctl status postgresql

# Verificar versión
psql --version
Linux (Fedora/RHEL/CentOS)
bash
# Instalar repositorio PostgreSQL
sudo dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/F-37-x86_64/pgdg-fedora-repo-latest.noarch.rpm

# Instalar PostgreSQL
sudo dnf install -y postgresql16-server

# Inicializar cluster
sudo /usr/pgsql-16/bin/postgresql-16-setup initdb

# Iniciar servicio
sudo systemctl start postgresql-16
sudo systemctl enable postgresql-16
2️⃣ Crear Base de Datos y Usuario
Conectar como superuser postgres
Windows:

text
psql -U postgres
macOS (Homebrew):

bash
psql postgres
Linux:

bash
sudo -u postgres psql
Crear database y user (ejecutar dentro de psql)
sql
-- Crear base de datos
CREATE DATABASE theaia
    WITH 
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.UTF-8'
    LC_CTYPE = 'en_US.UTF-8'
    TEMPLATE = template0;

-- Crear usuario
CREATE USER theaia_user WITH PASSWORD 'tu_password_seguro_2025';

-- Dar permisos al usuario
GRANT ALL PRIVILEGES ON DATABASE theaia TO theaia_user;

-- PostgreSQL 15+ requiere estos permisos adicionales
\c theaia
GRANT ALL ON SCHEMA public TO theaia_user;
GRANT CREATE ON SCHEMA public TO theaia_user;

-- Verificar
\l          -- Listar databases
\du         -- Listar usuarios

-- Salir
\q
Verificar database creada
bash
# Conectar como theaia_user
psql -U theaia_user -d theaia -h 127.0.0.1

# Dentro de psql:
SELECT version();
Output esperado: PostgreSQL 16.x on ...

3️⃣ Configurar Autenticación (Desarrollo)
Ubicación pg_hba.conf
Sistema Operativo	Ruta del archivo
Windows	C:\Program Files\PostgreSQL\16\data\pg_hba.conf
macOS (Homebrew)	/opt/homebrew/var/postgresql@16/pg_hba.conf
macOS (Postgres.app)	~/Library/Application Support/Postgres/var-16/pg_hba.conf
Linux (Ubuntu)	/etc/postgresql/16/main/pg_hba.conf
Linux (Fedora)	/var/lib/pgsql/16/data/pg_hba.conf
Editar pg_hba.conf
Para desarrollo local, cambiar autenticación a trust (sin password):

Abrir pg_hba.conf con editor de texto (como Administrador/sudo)

Buscar la sección # IPv4 local connections:

Modificar/añadir esta línea:

text
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# DESARROLLO: trust mode (sin password) - SOLO LOCAL
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust

# PRODUCCIÓN: usar md5 o scram-sha-256
# host    all             all             127.0.0.1/32            md5
Guardar archivo

⚠️ IMPORTANTE:

trust mode SOLO para desarrollo local

En producción usar md5 o scram-sha-256

127.0.0.1/32 limita a localhost únicamente

Reiniciar PostgreSQL
Windows:

text
# Como Administrador
net stop postgresql-x64-16
net start postgresql-x64-16

# O desde Services:
# Win+R → services.msc → Buscar "postgresql" → Restart
macOS (Homebrew):

bash
brew services restart postgresql@16
macOS (Postgres.app):

Cerrar y volver a abrir Postgres.app

Linux (Ubuntu/Debian):

bash
sudo systemctl restart postgresql
Linux (Fedora/RHEL):

bash
sudo systemctl restart postgresql-16
Verificar autenticación
bash
# Debe conectar SIN pedir password (si configuraste trust)
psql -U theaia_user -d theaia -h 127.0.0.1

# Si funciona, verás:
# theaia=>
4️⃣ Configurar Variables de Entorno
Crear archivo .env en raíz del proyecto
text
# ================================
# DATABASE CONFIGURATION
# ================================

# Connection URL (formato asyncpg para SQLAlchemy 2.0)
DATABASE_URL=postgresql+asyncpg://theaia_user:tu_password@127.0.0.1:5432/theaia

# Connection Pooling
DATABASE_POOL_SIZE=5
DATABASE_MAX_OVERFLOW=10
DATABASE_POOL_RECYCLE=3600
DATABASE_POOL_TIMEOUT=30

# Logging
DATABASE_ECHO=False  # True para debug SQL queries

# SSL (producción)
DATABASE_SSL_MODE=prefer  # prefer, require, verify-ca, verify-full

# ⚠️ CRÍTICO: Usar 127.0.0.1 (NO localhost) en Windows
# localhost causa WinError 64 en algunos sistemas
Validar .env
bash
# Desde raíz del proyecto
cat .env | grep DATABASE_URL

# Windows:
type .env | findstr DATABASE_URL
Proteger .env
Asegurar que .env está en .gitignore:

bash
# Verificar
cat .gitignore | grep .env

# Si no está, añadir:
echo ".env" >> .gitignore
5️⃣ Instalar Dependencias Python
Activar entorno virtual
bash
# Crear venv si no existe
python -m venv .venv

# Activar
# Linux/macOS:
source .venv/bin/activate

# Windows:
.venv\Scripts\activate

# Verificar activación
which python  # Linux/macOS
where python  # Windows
Instalar dependencias
bash
# Instalar todas las dependencias
pip install -r requirements.txt

# O instalar manualmente las necesarias para database:
pip install sqlalchemy[asyncio]==2.0.23
pip install asyncpg==0.29.0
pip install alembic==1.12.1
pip install psycopg2-binary==2.9.9
pip install python-dotenv==1.0.0
Verificar instalación
python
# Ejecutar en Python:
python -c "import asyncpg; print('✅ asyncpg:', asyncpg.__version__)"
python -c "import alembic; print('✅ alembic:', alembic.__version__)"
python -c "import sqlalchemy; print('✅ sqlalchemy:', sqlalchemy.__version__)"
Output esperado:

text
✅ asyncpg: 0.29.0
✅ alembic: 1.12.1
✅ sqlalchemy: 2.0.23
6️⃣ Aplicar Migraciones Alembic
Ver estado actual
bash
# Desde raíz del proyecto
alembic current
Output si es primera vez: (empty) o (no branches)

Ver historial de migraciones disponibles
bash
alembic history
Output esperado:

text
<base> -> e0a17d850507 (head), Initial schema with tenant support
Aplicar TODAS las migraciones
bash
alembic upgrade head
Output esperado:

text
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> e0a17d850507, Initial schema with tenant support
Verificar estado después de migración
bash
alembic current
Output esperado:

text
e0a17d850507 (head)
Verificar tablas creadas en PostgreSQL
bash
psql -U theaia_user -d theaia -h 127.0.0.1 -c "\dt"
Deberías ver 6 tablas:

text
          List of relations
 Schema |       Name        | Type  |    Owner
--------+-------------------+-------+--------------
 public | alembic_version   | table | theaia_user
 public | conversations     | table | theaia_user
 public | events            | table | theaia_user
 public | message_history   | table | theaia_user
 public | notes             | table | theaia_user
 public | users             | table | theaia_user
(6 rows)
Ver estructura de una tabla (ejemplo: users)
bash
psql -U theaia_user -d theaia -h 127.0.0.1 -c "\d users"
7️⃣ Verificar Conexión
Utility check_database.py
Desde raíz del proyecto:

bash
python src/theaia/database/check_database.py
Output esperado:

text
✅ Conexión a base de datos exitosa
PostgreSQL version: PostgreSQL 16.3 on ...
Tablas encontradas: 5
  - users
  - events
  - notes
  - conversations
  - message_history

✅ Database setup completo!
Test programático Python
python
from src.theaia.database.config.connection import test_connection
import asyncio

# Ejecutar test
asyncio.run(test_connection())
Output esperado:

text
✅ Database connection successful!
PostgreSQL version: PostgreSQL 16.3 on ...
Test con psql interactivo
bash
# Conectar
psql -U theaia_user -d theaia -h 127.0.0.1

# Dentro de psql, ejecutar:
SELECT tablename FROM pg_tables WHERE schemaname = 'public';
8️⃣ Ejecutar Tests
Tests específicos de database
bash
# Tests unitarios
pytest src/theaia/tests/database/test_database.py -v

# Tests de repositories
pytest src/theaia/tests/database/test_repositories.py -v

# Todos los tests database
pytest src/theaia/tests/database/ -v
Output esperado: 12/12 tests passed ✅

Con coverage
bash
# Coverage de database module
pytest src/theaia/tests/database/ \
    --cov=src/theaia/database \
    --cov-report=html \
    --cov-report=term

# Ver reporte en navegador
open htmlcov/index.html  # macOS
start htmlcov/index.html  # Windows
xdg-open htmlcov/index.html  # Linux
🐛 Troubleshooting Común
1. WinError 64: Connection refused (Windows)
Problema:

text
OSError: [WinError 64] The specified network name is no longer available
Causa: Windows no resuelve localhost correctamente con asyncpg

Solución:

text
# ❌ No funciona en Windows
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/theaia

# ✅ Usar IP explícita
DATABASE_URL=postgresql+asyncpg://user:pass@127.0.0.1:5432/theaia
2. psql: FATAL: authentication failed
Problema:

text
psql: error: FATAL: password authentication failed for user "theaia_user"
Causas posibles:

Password incorrecto

pg_hba.conf no configurado correctamente

PostgreSQL no reiniciado después de cambiar pg_hba.conf

Soluciones:

Opción A: Usar trust mode (desarrollo)

Editar pg_hba.conf (ver sección 3)

Cambiar método a trust

Reiniciar PostgreSQL

Actualizar .env sin password:

text
DATABASE_URL=postgresql+asyncpg://theaia_user@127.0.0.1:5432/theaia
Opción B: Resetear password

sql
-- Conectar como postgres
psql -U postgres

-- Cambiar password
ALTER USER theaia_user WITH PASSWORD 'nuevo_password_2025';
\q
Actualizar .env con nuevo password.

3. relation "table_name" does not exist
Problema:

text
sqlalchemy.exc.ProgrammingError: (asyncpg.exceptions.UndefinedTableError)
relation "users" does not exist
Causa: Migraciones no aplicadas

Solución:

bash
# Verificar estado
alembic current

# Si dice (empty), aplicar migraciones
alembic upgrade head

# Verificar tablas
psql -U theaia_user -d theaia -h 127.0.0.1 -c "\dt"
4. Port 5432 already in use
Problema:

text
FATAL: could not bind IPv4 address "127.0.0.1": Address already in use
HINT: Is another postmaster already running on port 5432?
Causa: Otra instancia PostgreSQL corriendo en puerto 5432

Solución:

Windows:

text
# Ver qué proceso usa puerto 5432
netstat -ano | findstr :5432

# Matar proceso (reemplazar PID)
taskkill /PID <PID> /F

# O cambiar puerto en postgresql.conf
Linux/macOS:

bash
# Ver proceso
lsof -i :5432

# Matar proceso
kill -9 <PID>

# O cambiar puerto
sudo nano /etc/postgresql/16/main/postgresql.conf
# Cambiar: port = 5433
5. RuntimeError: Working outside of async context
Problema:

python
RuntimeError: Working outside of async context
Causa: Usar repository sin async context manager

Solución:

python
# ❌ INCORRECTO
repo = UserRepository()
users = await repo.get_all(tenant_id="default")

# ✅ CORRECTO
from src.theaia.database.config.session import AsyncSessionLocal

async with AsyncSessionLocal() as session:
    repo = UserRepository(session)
    users = await repo.get_all(tenant_id="default")
6. ImportError: cannot import name 'asyncpg'
Problema:

python
ImportError: cannot import name 'asyncpg' from 'sqlalchemy.dialects'
Causa: Dependencias desactualizadas o mal instaladas

Solución:

bash
# Reinstalar dependencias
pip uninstall sqlalchemy asyncpg alembic -y
pip install sqlalchemy[asyncio]==2.0.23 asyncpg==0.29.0 alembic==1.12.1

# Verificar
python -c "from sqlalchemy.ext.asyncio import create_async_engine; print('OK')"
7. database "theaia" does not exist
Problema:

text
psql: error: FATAL: database "theaia" does not exist
Causa: Database no creada

Solución:

bash
# Conectar como postgres
psql -U postgres

# Crear database
CREATE DATABASE theaia ENCODING 'UTF8';
GRANT ALL PRIVILEGES ON DATABASE theaia TO theaia_user;
\q
8. Permission denied for schema public
Problema (PostgreSQL 15+):

text
sqlalchemy.exc.ProgrammingError: permission denied for schema public
Causa: PostgreSQL 15+ cambió permisos de schema public

Solución:

sql
-- Conectar como postgres
psql -U postgres -d theaia

-- Dar permisos explícitos
GRANT ALL ON SCHEMA public TO theaia_user;
GRANT CREATE ON SCHEMA public TO theaia_user;

-- Verificar
\dn+
🔐 Configuración Producción
Cambiar a autenticación segura
1. Editar pg_hba.conf:

text
# PRODUCCIÓN: password requerido
host    all    all    0.0.0.0/0    scram-sha-256
2. Establecer password fuerte:

sql
ALTER USER theaia_user WITH PASSWORD 'P4ssw0rd!VerySecure2025#';
3. Actualizar .env:

text
DATABASE_URL=postgresql+asyncpg://theaia_user:P4ssw0rd!VerySecure2025#@127.0.0.1:5432/theaia
DATABASE_SSL_MODE=require
4. Configurar SSL (producción remota):

En postgresql.conf:

text
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
5. Firewall: Solo permitir IPs específicas

6. Reiniciar PostgreSQL

Backup automatizado
bash
# Script backup diario (Linux/macOS)
#!/bin/bash
BACKUP_DIR="/backup/postgres"
DATE=$(date +%Y%m%d_%H%M%S)

pg_dump -U theaia_user -d theaia -h 127.0.0.1 \
    -F c -b -v \
    -f "$BACKUP_DIR/theaia_backup_$DATE.dump"

# Retener solo últimos 7 días
find $BACKUP_DIR -name "*.dump" -mtime +7 -delete
Restaurar backup
bash
# Restaurar dump
pg_restore -U theaia_user -d theaia -h 127.0.0.1 \
    -v backup_20251114.dump

# O crear nueva database desde backup
createdb -U postgres theaia_restored
pg_restore -U theaia_user -d theaia_restored backup.dump
✅ Checklist Final
Antes de considerar setup completo, verificar:

 PostgreSQL instalado y corriendo

 Servicio PostgreSQL iniciado automáticamente

 Base de datos theaia creada

 Usuario theaia_user con permisos completos

 pg_hba.conf configurado (trust para dev, md5/scram para prod)

 PostgreSQL reiniciado después de cambios

 Archivo .env creado con DATABASE_URL correcto

 .env añadido a .gitignore

 Entorno virtual Python activado

 Dependencias instaladas (asyncpg, alembic, sqlalchemy)

 Migraciones aplicadas (alembic upgrade head)

 6 tablas verificadas en database (users, events, notes, conversations, message_history, alembic_version)

 check_database.py ejecuta sin errores

 Tests database 12/12 pasando (pytest src/theaia/tests/database/ -v)

 Conexión desde Python funcional

 Backups configurados (producción)

📚 Recursos Adicionales
Documentación Oficial
PostgreSQL Official Docs

SQLAlchemy 2.0 Async

asyncpg Documentation

Alembic Tutorial

Documentación THEA IA
Database Module README

Database Tests

H02 Milestone

Herramientas útiles
pgAdmin 4 - GUI para PostgreSQL

DBeaver - Cliente database universal

TablePlus - GUI moderna (macOS/Windows)

📞 Soporte
Problemas no resueltos:

Revisar Database README Troubleshooting

Abrir issue en GitHub: github.com/alvarofernandezmota-tech/thea-ia/issues

Contacto: alvarofernandezmota@gmail.com

Última actualización: 14 nov 2025
Versión Database Layer: v0.3.0
Responsable: Álvaro Fernández Mota
Estado: H02 Database Layer 100% COMPLETO ✅