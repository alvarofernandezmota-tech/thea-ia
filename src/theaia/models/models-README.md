src/models/ - Models Module (Pydantic Schemas)
Módulo de validación y serialización con Pydantic

📋 Overview
El módulo models/ contiene Pydantic schemas para validación, serialización y deserialización de datos en THEA IA.

NO confundir con database/models/:

database/models/ = SQLAlchemy ORM (persistencia PostgreSQL)

src/models/ = Pydantic schemas (validación + API contracts)

🎯 Propósito
¿Por qué Pydantic Schemas?
✅ Validación automática: Types, constraints, custom validators

✅ Serialización: Python objects ↔ JSON/dict

✅ Documentation: Auto-generate API docs (FastAPI)

✅ Type safety: IDE autocomplete + mypy validation

✅ Parsing: String → datetime, int, etc automático

Uso en THEA IA:
python
# Agents validan input con Pydantic
reminder_data = ReminderCreate(
    title="Reunión",
    description="Team meeting",
    reminder_datetime="2025-11-15 15:00"  # String → datetime auto
)

# Adapters serializan output
response = ReminderResponse.from_orm(reminder_db_model)
# Devuelve JSON limpio al usuario
📁 Estructura (H02)
text
src/models/
│
├── __init__.py                    # Exports: todos los schemas
│
├── base.py ← 🆕 DÍA 1 H02
│   # Base schemas comunes
│   # Classes:
│   #   - BaseSchema (base para todos)
│   #   - TimestampSchema (created_at, updated_at)
│   #   - ResponseSchema (success, message, data)
│
├── user.py ← 🆕 DÍA 1 H02
│   # Schemas User
│   # Classes:
│   #   - UserBase (campos comunes)
│   #   - UserCreate (para crear)
│   #   - UserUpdate (para actualizar)
│   #   - UserResponse (para devolver)
│   #   - UserInDB (con fields internos)
│
├── reminder.py ← 🆕 DÍA 1 H02
│   # Schemas Reminder
│   # Classes:
│   #   - ReminderBase
│   #   - ReminderCreate
│   #   - ReminderUpdate
│   #   - ReminderResponse
│   #   - ReminderInDB
│
├── note.py ← 🆕 DÍA 2 H02
│   # Schemas Note
│   # Classes:
│   #   - NoteBase
│   #   - NoteCreate
│   #   - NoteUpdate
│   #   - NoteResponse
│   #   - NoteInDB
│
├── event.py ← 🆕 DÍA 2 H02
│   # Schemas Event
│   # Classes:
│   #   - EventBase
│   #   - EventCreate
│   #   - EventUpdate
│   #   - EventResponse
│   #   - EventInDB
│
├── task.py ← 🆕 DÍA 3 H02
│   # Schemas Task
│   # Classes:
│   #   - TaskBase
│   #   - TaskCreate
│   #   - TaskUpdate
│   #   - TaskResponse
│   #   - TaskInDB
│
├── context.py ← 🆕 DÍA 3 H02
│   # Schemas Context (historial)
│   # Classes:
│   #   - ContextBase
│   #   - ContextCreate
│   #   - ContextResponse
│
├── message.py ← 🆕 DÍA 2 H02
│   # Schemas mensajes (entre adapters y core)
│   # Classes:
│   #   - MessageIn (mensaje entrante normalizado)
│   #   - MessageOut (respuesta saliente)
│   #   - MessageMetadata
│
└── README.md                      # Este archivo
🏗️ Arquitectura Schemas
Patrón Base/Create/Update/Response/InDB:
python
# reminder.py

class ReminderBase(BaseModel):
    """Campos comunes a todas las operaciones"""
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    reminder_datetime: datetime
    advance_minutes: int = Field(default=15, ge=0, le=1440)

class ReminderCreate(ReminderBase):
    """Para crear (sin id, sin user_id - se añade en repo)"""
    pass

class ReminderUpdate(BaseModel):
    """Para actualizar (todos fields opcionales)"""
    title: str | None = None
    description: str | None = None
    reminder_datetime: datetime | None = None
    advance_minutes: int | None = None
    completed: bool | None = None

class ReminderResponse(ReminderBase):
    """Para devolver al usuario (con id, sin internals)"""
    id: int
    completed: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True  # Para from_orm()

class ReminderInDB(ReminderResponse):
    """Representación completa en DB (con user_id, etc)"""
    user_id: int
    completed_at: datetime | None = None
Beneficio: Separación clara entre lo que se recibe, se guarda, y se devuelve.

📦 Dependencias
Python:
text
pydantic==2.5.0
pydantic[email]==2.5.0        # Para email validation (H04)
python-dateutil==2.8.2        # Parseo flexible fechas
Internas:
python
from src.config.constants import *  # Constantes (ej: DEFAULT_TIMEZONE)
Usado por:
python
# src/agents/ (todos)
from src.models import ReminderCreate, ReminderResponse, ...

# src/adapters/
from src.models import MessageIn, MessageOut

# src/database/repositories/
from src.models import ReminderCreate, ReminderUpdate, ...
🚀 Implementación por Día (H02)
Día 1 (12 Nov):
Prioridad ALTA (necesarios para primera conversación):

python
# base.py
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        str_strip_whitespace = True
        
class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
    
class ResponseSchema(BaseModel):
    success: bool
    message: str
    data: dict | None = None

# user.py
class UserBase, UserCreate, UserUpdate, UserResponse, UserInDB
# Completos

# reminder.py
class ReminderBase, ReminderCreate, ReminderUpdate, ReminderResponse, ReminderInDB
# Completos

# message.py
class MessageIn:  # Mensaje normalizado de adapter
    user_id: int
    text: str
    timestamp: datetime
    metadata: dict = {}
    
class MessageOut:  # Respuesta a enviar
    text: str
    buttons: list | None = None
    metadata: dict = {}
Resultado Día 1:
✅ User + Reminder schemas funcionan
✅ Primera conversación validada

Día 2 (13 Nov):
Prioridad MEDIA:

python
# note.py
class NoteBase, NoteCreate, NoteUpdate, NoteResponse, NoteInDB
# Completos

# event.py
class EventBase, EventCreate, EventUpdate, EventResponse, EventInDB
# Completos
Resultado Día 2:
✅ Note + Event schemas listos
✅ Validación notas y eventos funciona

Día 3 (14 Nov):
Completar resto:

python
# task.py
class TaskBase, TaskCreate, TaskUpdate, TaskResponse, TaskInDB
# Completos

# context.py
class ContextBase, ContextCreate, ContextResponse
# Completos (no Update, no se edita historial)
Resultado Día 3:
✅ Todos los schemas implementados
✅ Validación completa sistema

💡 Ejemplos de Uso
1. Validación Input Agent:
python
# reminder_agent.py
from src.models import ReminderCreate
from pydantic import ValidationError

async def create_reminder(self, data: dict):
    try:
        # Pydantic valida automáticamente
        reminder_data = ReminderCreate(**data)
        
        # Si llega aquí, data es válido
        reminder = await self.reminder_repo.create(
            user_id=self.user_id,
            **reminder_data.model_dump()
        )
        
        return ReminderResponse.from_orm(reminder)
        
    except ValidationError as e:
        # Errores específicos de validación
        return {"error": "Invalid data", "details": e.errors()}
2. Serialización Response:
python
# reminder_repository.py
async def create(self, **data) -> Reminder:
    reminder = Reminder(**data)
    self.session.add(reminder)
    await self.session.flush()
    
    # Devolver SQLAlchemy model
    return reminder

# reminder_agent.py
reminder_db = await repo.create(...)

# Convertir a Pydantic para respuesta
reminder_response = ReminderResponse.from_orm(reminder_db)

# Serializar a dict/JSON
return reminder_response.model_dump()
# O
return reminder_response.model_dump_json()
3. Parseo Flexible:
python
# Pydantic parsea automáticamente
reminder = ReminderCreate(
    title="Reunión",
    reminder_datetime="2025-11-15 15:00"  # String
)

# reminder.reminder_datetime es datetime object
assert isinstance(reminder.reminder_datetime, datetime)
✅ Validaciones Custom
Example: Validar datetime futuro:
python
from pydantic import field_validator

class ReminderCreate(ReminderBase):
    @field_validator('reminder_datetime')
    def datetime_must_be_future(cls, v):
        if v <= datetime.now():
            raise ValueError('Reminder must be in the future')
        return v
Example: Normalizar tags:
python
class NoteCreate(NoteBase):
    tags: list[str] | None = None
    
    @field_validator('tags')
    def normalize_tags(cls, v):
        if v is None:
            return []
        # Lowercase, sin duplicados
        return list(set(tag.lower().strip() for tag in v))
🧪 Testing
Test Schema Validation:
python
# tests/unit/test_models/test_reminder.py
import pytest
from pydantic import ValidationError
from src.models import ReminderCreate

def test_reminder_create_valid():
    data = {
        "title": "Test",
        "reminder_datetime": datetime.now() + timedelta(hours=1)
    }
    reminder = ReminderCreate(**data)
    assert reminder.title == "Test"

def test_reminder_create_invalid_title():
    with pytest.raises(ValidationError) as exc:
        ReminderCreate(
            title="",  # Empty not allowed
            reminder_datetime=datetime.now()
        )
    assert "title" in str(exc.value)

def test_reminder_create_past_datetime():
    with pytest.raises(ValidationError) as exc:
        ReminderCreate(
            title="Test",
            reminder_datetime=datetime.now() - timedelta(hours=1)
        )
    assert "future" in str(exc.value).lower()
📊 Schemas por Hito
Hito	Schemas	Campos Total	Validators
H02	7 módulos × 4-5 classes = ~30 schemas	~150 fields	~15 validators
H04	+3 módulos (payments, subscriptions)	+30 fields	+10 validators
🔒 Seguridad
Sensitive Data:
python
# ❌ NO exponer passwords, tokens
class UserResponse(BaseModel):
    id: int
    username: str
    # NO incluir: password_hash, api_token, etc

# ✅ Schemas separados para internals
class UserInDB(UserResponse):
    password_hash: str  # Solo usado internamente
    api_token: str | None
Input Sanitization:
python
from pydantic import field_validator

class NoteCreate(BaseModel):
    content: str
    
    @field_validator('content')
    def sanitize_content(cls, v):
        # Strip HTML tags, etc
        return sanitize(v)
📈 Performance
Config Optimization:
python
class BaseSchema(BaseModel):
    class Config:
        # Validar solo una vez
        validate_assignment = False
        
        # Usar slots (menos memoria)
        # slots = True  # Pydantic v2
        
        # JSON parsing rápido
        json_loads = orjson.loads
        json_dumps = orjson.dumps
🔮 Próximos Pasos
H04: Enterprise Schemas
Payment schemas (Stripe)

Subscription schemas

Webhook schemas

Email validation

Phone validation

H08: API Schemas (si Web)
Request/Response pairs para REST API

OpenAPI/Swagger auto-generation

📝 Comandos Útiles
bash
# Validar schemas sin ejecutar
python -c "from src.models import *; print('All schemas OK')"

# Tests
pytest src/tests/unit/test_models/ -v

# Ver schema JSON
python -c "from src.models import ReminderCreate; print(ReminderCreate.model_json_schema())"
📚 Recursos
Pydantic Docs

Pydantic Validators

Pydantic Settings

🎯 Checklist Implementación
Día 1 H02:
 base.py (BaseSchema, TimestampSchema, ResponseSchema)

 user.py (5 classes)

 reminder.py (5 classes)

 message.py (2 classes)

 Tests básicos

 Integración con ReminderAgent

Día 2 H02:
 note.py (5 classes)

 event.py (5 classes)

 Tests note + event

 Integración con NoteAgent + EventAgent

Día 3 H02:
 task.py (5 classes)

 context.py (3 classes)

 Tests task + context

 Integración con TaskAgent + ContextAgent

 Tests coverage >85%

Versión: 0.1.0
Estado: Planificación (H01)
Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota