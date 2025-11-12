Dependencias - src/models/
Módulo: Models (Pydantic Schemas)
Versión actual: 0.1.0 (H01 - Planificación)
Última actualización: 11 Nov 2025

📦 Dependencias Python
H02 (12-16 Nov): Schemas Base
Producción:
text
# Validation
pydantic==2.5.0                 # Schemas y validación
pydantic-core==2.14.5           # Core (instalado automáticamente)

# Date/Time
python-dateutil==2.8.2          # Parseo fechas flexible
Desarrollo:
text
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1

# Type Checking
mypy==1.7.1                     # Type checking estático
H04 (20-23 Nov): Enterprise Validation
Adicionales Producción:
text
# Advanced Validation
pydantic[email]==2.5.0          # Email validation
phonenumbers==8.13.26           # Phone validation
validators==0.22.0              # URL, IP, etc validation
H08 (Ene 2026): API Schemas [CONDICIONAL]
Adicionales Producción:
text
# API
fastapi==0.108.0                # FastAPI integration (auto OpenAPI)
🔗 Dependencias Internas (THEA IA)
Módulos que usa models/:
python
# Mínimas dependencias internas
from src.config.constants import (
    DEFAULT_TIMEZONE,
    DEFAULT_LANGUAGE,
    DEFAULT_REMINDER_ADVANCE
)
Módulos que usan models/:
python
# src/agents/ (TODOS)
from src.models import (
    ReminderCreate, ReminderUpdate, ReminderResponse,
    NoteCreate, NoteUpdate, NoteResponse,
    EventCreate, EventUpdate, EventResponse,
    TaskCreate, TaskUpdate, TaskResponse,
    ContextCreate, ContextResponse
)

# src/adapters/
from src.models import MessageIn, MessageOut, UserCreate

# src/database/repositories/
from src.models import (
    ReminderCreate, ReminderUpdate,
    # ... para validación antes de guardar
)

# src/api/ (H08)
from src.models import *  # Para request/response FastAPI
🔐 Variables de Entorno
Ninguna - Este módulo no usa variables de entorno directamente.

Obtiene defaults de src/config/constants.py.

📊 Tabla Resumen Dependencias
Hito	Deps Producción	Deps Desarrollo	Dependencias Internas
H02	2 (pydantic, dateutil)	2 (pytest, mypy)	1 (config.constants)
H04	+3 (email, phone, validators)	0	0
H08	+1 (fastapi)	0	0
Total	6	2	1
🚀 Instalación Dependencias
H02 (Setup inicial):
bash
# Instalar producción
pip install pydantic==2.5.0 python-dateutil==2.8.2

# Instalar desarrollo
pip install pytest==7.4.3 mypy==1.7.1

# Verificar instalación
python -c "import pydantic; print(pydantic.__version__)"
python -c "from pydantic import BaseModel; print('OK')"
🧪 Testing Schemas
Test Validation:
python
# tests/unit/test_models/test_reminder.py
import pytest
from pydantic import ValidationError
from src.models import ReminderCreate

def test_reminder_create_valid():
    """Schema válido debe funcionar"""
    from datetime import datetime, timedelta
    
    reminder = ReminderCreate(
        title="Test",
        reminder_datetime=datetime.now() + timedelta(hours=1)
    )
    
    assert reminder.title == "Test"
    assert isinstance(reminder.reminder_datetime, datetime)

def test_reminder_create_invalid_title():
    """Title vacío debe fallar"""
    with pytest.raises(ValidationError) as exc:
        ReminderCreate(
            title="",
            reminder_datetime=datetime.now()
        )
    assert "title" in str(exc.value).lower()

def test_reminder_datetime_past_fails():
    """Datetime pasado debe fallar"""
    with pytest.raises(ValidationError) as exc:
        ReminderCreate(
            title="Test",
            reminder_datetime=datetime.now() - timedelta(hours=1)
        )
    assert "future" in str(exc.value).lower()
Test Serialization:
python
def test_reminder_serialization():
    """from_orm debe funcionar"""
    from src.database.models import Reminder
    from src.models import ReminderResponse
    
    # Mock SQLAlchemy model
    reminder_db = Reminder(
        id=1,
        title="Test",
        reminder_datetime=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now(),
        completed=False
    )
    
    # Convertir a Pydantic
    reminder_schema = ReminderResponse.from_orm(reminder_db)
    
    assert reminder_schema.id == 1
    assert reminder_schema.title == "Test"
    
    # Serializar a dict
    data = reminder_schema.model_dump()
    assert isinstance(data, dict)
    assert data['id'] == 1
Ejecutar tests:
bash
# Todos los tests models
pytest src/tests/unit/test_models/ -v

# Con coverage
pytest --cov=src/models --cov-report=html

# Solo un archivo
pytest src/tests/unit/test_models/test_reminder.py -v

# Verbose con output
pytest -vv -s
🔧 Type Checking (mypy)
Configuración mypy:
text
# mypy.ini
[mypy]
python_version = 3.11
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
plugins = pydantic.mypy

[mypy-tests.*]
disallow_untyped_defs = False
Ejecutar mypy:
bash
# Check todo el proyecto
mypy src/

# Solo models
mypy src/models/

# Strict mode
mypy --strict src/models/

# Ver errores con contexto
mypy --show-error-codes src/models/
⚠️ Troubleshooting
1. ValidationError sin detalles claros
python
# Problema: Error genérico
try:
    reminder = ReminderCreate(**data)
except ValidationError as e:
    print(e)  # Poco claro

# Solución: Ver detalles
except ValidationError as e:
    print(e.json())  # JSON con todos los errores
    print(e.errors())  # Lista de dicts con errores
2. from_orm() no funciona
python
# Problema
class UserResponse(BaseModel):
    id: int
    username: str

user_schema = UserResponse.from_orm(user_db)
# AttributeError: 'UserResponse' has no attribute 'from_orm'

# Solución: Añadir Config
class UserResponse(BaseModel):
    id: int
    username: str
    
    class Config:
        from_attributes = True  # Pydantic v2
        # orm_mode = True  # Pydantic v1 (deprecated)
3. Datetime timezone issues
python
# Problema: Datetime sin timezone
reminder_datetime: datetime  # Puede ser naive o aware

# Solución: Forzar timezone aware
from pydantic import field_validator
import pytz

class ReminderCreate(BaseModel):
    reminder_datetime: datetime
    
    @field_validator('reminder_datetime')
    def make_aware(cls, v):
        if v.tzinfo is None:
            # Asumir Europe/Madrid si naive
            tz = pytz.timezone('Europe/Madrid')
            v = tz.localize(v)
        return v
4. Circular imports
python
# Problema
# models/user.py
from src.models.reminder import ReminderResponse
# models/reminder.py
from src.models.user import UserResponse
# → Circular import error

# Solución: TYPE_CHECKING
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.reminder import ReminderResponse

class UserResponse(BaseModel):
    reminders: list['ReminderResponse'] = []  # Forward ref
📈 Performance
Validation Performance:
python
# Benchmark
import timeit

# Pydantic v2 es ~5-50x más rápido que v1
schema = ReminderCreate(title="Test", reminder_datetime=datetime.now())

# ~50,000 validaciones/segundo (Pydantic v2)
# ~1,000 validaciones/segundo (Pydantic v1)
Optimization Tips:
python
# 1. Usar model_validate() en vez de __init__ si ya validado
data = {"title": "Test", ...}
# Lento (valida siempre)
reminder = ReminderCreate(**data)
# Rápido (skip validation si trusted)
reminder = ReminderCreate.model_construct(**data)  # ⚠️ Usar con cuidado

# 2. Serialization rápida con orjson
from pydantic import ConfigDict
import orjson

class FastSchema(BaseModel):
    model_config = ConfigDict(
        json_loads=orjson.loads,
        json_dumps=lambda v, *, default: orjson.dumps(v, default=default).decode()
    )
📚 Recursos
Documentación Oficial:
Pydantic Docs

Pydantic Validators

Pydantic Performance

Pydantic Migration v1→v2

Tutoriales:
Pydantic Tutorial

Custom Validators

🔄 Actualización Dependencias
Política:
Pydantic: Major versions con cuidado (breaking changes), minor cada 3-6 meses

python-dateutil: Actualizar cada 6 meses

pytest: Actualizar cada 3 meses

Comando:
bash
# Ver outdated
pip list --outdated | grep pydantic

# Actualizar
pip install --upgrade pydantic

# Verificar no rompe nada
pytest src/tests/unit/test_models/ -v
mypy src/models/
🎯 Checklist Producción
Antes de H02 release:

 Todas las deps instaladas

 Tests pasan (>90% coverage)

 mypy type checking pasa

 No ValidationError inesperados

 from_orm() funciona con database models

 Serialización JSON funciona

 Performance aceptable (>10,000 validaciones/seg)

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota