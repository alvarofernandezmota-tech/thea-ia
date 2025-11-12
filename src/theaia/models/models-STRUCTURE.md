Estructura Planificada - src/models/
Módulo: Models (Pydantic Schemas)
Propósito: Validación y serialización de datos
Patrón: Base/Create/Update/Response/InDB

📋 Estado Actual (11 Nov 2025 - H01)
text
src/models/
├── __init__.py (placeholder)
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅
Estado: Sin implementación, solo planificación

🎯 H02 (12-16 Nov): Schemas Base
Estructura Objetivo:
text
src/models/
│
├── __init__.py
│   # Exports: todos los schemas
│   from .base import BaseSchema, TimestampSchema, ResponseSchema
│   from .user import UserCreate, UserUpdate, UserResponse
│   from .reminder import ReminderCreate, ReminderUpdate, ReminderResponse
│   from .note import NoteCreate, NoteUpdate, NoteResponse
│   from .event import EventCreate, EventUpdate, EventResponse
│   from .task import TaskCreate, TaskUpdate, TaskResponse
│   from .context import ContextCreate, ContextResponse
│   from .message import MessageIn, MessageOut
│
├── base.py ← 🆕 DÍA 1
│   # Base schemas comunes
│   #
│   # class BaseSchema(BaseModel):
│   #     """Base para todos los schemas"""
│   #     class Config:
│   #         from_attributes = True
│   #         str_strip_whitespace = True
│   #         json_encoders = {datetime: lambda v: v.isoformat()}
│   #
│   # class TimestampSchema(BaseModel):
│   #     """Mixin timestamps"""
│   #     created_at: datetime
│   #     updated_at: datetime
│   #
│   # class ResponseSchema(BaseModel):
│   #     """Schema respuesta genérica"""
│   #     success: bool
│   #     message: str
│   #     data: dict | None = None
│
├── user.py ← 🆕 DÍA 1
│   # Schemas User
│   #
│   # class UserBase(BaseModel):
│   #     """Campos comunes User"""
│   #     username: str | None = None
│   #     first_name: str | None = None
│   #     last_name: str | None = None
│   #     language_code: str = "es"
│   #     timezone: str = "Europe/Madrid"
│   #
│   # class UserCreate(UserBase):
│   #     """Crear user"""
│   #     telegram_user_id: int
│   #
│   # class UserUpdate(BaseModel):
│   #     """Actualizar user (todos opcionales)"""
│   #     username: str | None = None
│   #     first_name: str | None = None
│   #     last_name: str | None = None
│   #     language_code: str | None = None
│   #     timezone: str | None = None
│   #
│   # class UserResponse(UserBase, TimestampSchema):
│   #     """User para devolver"""
│   #     id: int
│   #     subscription_tier: str
│   #     is_active: bool
│   #
│   #     class Config:
│   #         from_attributes = True
│   #
│   # class UserInDB(UserResponse):
│   #     """User completo en DB"""
│   #     telegram_user_id: int
│   #     subscription_expires: datetime | None = None
│
├── reminder.py ← 🆕 DÍA 1
│   # Schemas Reminder
│   #
│   # class ReminderBase(BaseModel):
│   #     """Campos comunes Reminder"""
│   #     title: str = Field(..., min_length=1, max_length=200)
│   #     description: str | None = None
│   #     reminder_datetime: datetime
│   #     advance_minutes: int = Field(default=15, ge=0, le=1440)
│   #
│   #     @field_validator('reminder_datetime')
│   #     def datetime_must_be_future(cls, v):
│   #         if v <= datetime.now():
│   #             raise ValueError('Reminder must be in future')
│   #         return v
│   #
│   # class ReminderCreate(ReminderBase):
│   #     """Crear reminder"""
│   #     pass
│   #
│   # class ReminderUpdate(BaseModel):
│   #     """Actualizar reminder"""
│   #     title: str | None = None
│   #     description: str | None = None
│   #     reminder_datetime: datetime | None = None
│   #     advance_minutes: int | None = None
│   #     completed: bool | None = None
│   #
│   # class ReminderResponse(ReminderBase, TimestampSchema):
│   #     """Reminder para devolver"""
│   #     id: int
│   #     completed: bool
│   #     completed_at: datetime | None = None
│   #
│   #     class Config:
│   #         from_attributes = True
│   #
│   # class ReminderInDB(ReminderResponse):
│   #     """Reminder completo DB"""
│   #     user_id: int
│
├── note.py ← 🆕 DÍA 2
│   # Schemas Note
│   #
│   # class NoteBase(BaseModel):
│   #     title: str | None = None
│   #     content: str = Field(..., min_length=1)
│   #     tags: list[str] | None = None
│   #     is_pinned: bool = False
│   #
│   #     @field_validator('tags')
│   #     def normalize_tags(cls, v):
│   #         if v is None:
│   #             return []
│   #         return list(set(tag.lower().strip() for tag in v))
│   #
│   # class NoteCreate(NoteBase):
│   #     pass
│   #
│   # class NoteUpdate(BaseModel):
│   #     title: str | None = None
│   #     content: str | None = None
│   #     tags: list[str] | None = None
│   #     is_pinned: bool | None = None
│   #
│   # class NoteResponse(NoteBase, TimestampSchema):
│   #     id: int
│   #     class Config:
│   #         from_attributes = True
│   #
│   # class NoteInDB(NoteResponse):
│   #     user_id: int
│
├── event.py ← 🆕 DÍA 2
│   # Schemas Event
│   #
│   # class EventBase(BaseModel):
│   #     title: str = Field(..., min_length=1, max_length=200)
│   #     description: str | None = None
│   #     start_datetime: datetime
│   #     end_datetime: datetime | None = None
│   #     location: str | None = None
│   #     is_all_day: bool = False
│   #
│   #     @field_validator('end_datetime')
│   #     def end_after_start(cls, v, info):
│   #         if v and info.data.get('start_datetime'):
│   #             if v <= info.data['start_datetime']:
│   #                 raise ValueError('End must be after start')
│   #         return v
│   #
│   # class EventCreate(EventBase):
│   #     pass
│   #
│   # class EventUpdate(BaseModel):
│   #     title: str | None = None
│   #     description: str | None = None
│   #     start_datetime: datetime | None = None
│   #     end_datetime: datetime | None = None
│   #     location: str | None = None
│   #     is_all_day: bool | None = None
│   #
│   # class EventResponse(EventBase, TimestampSchema):
│   #     id: int
│   #     class Config:
│   #         from_attributes = True
│   #
│   # class EventInDB(EventResponse):
│   #     user_id: int
│
├── task.py ← 🆕 DÍA 3
│   # Schemas Task
│   #
│   # class TaskBase(BaseModel):
│   #     title: str = Field(..., min_length=1, max_length=200)
│   #     description: str | None = None
│   #     due_date: date | None = None
│   #     priority: str = Field(default="medium", pattern="^(low|medium|high)$")
│   #
│   # class TaskCreate(TaskBase):
│   #     pass
│   #
│   # class TaskUpdate(BaseModel):
│   #     title: str | None = None
│   #     description: str | None = None
│   #     due_date: date | None = None
│   #     priority: str | None = None
│   #     completed: bool | None = None
│   #
│   # class TaskResponse(TaskBase, TimestampSchema):
│   #     id: int
│   #     completed: bool
│   #     completed_at: datetime | None = None
│   #     class Config:
│   #         from_attributes = True
│   #
│   # class TaskInDB(TaskResponse):
│   #     user_id: int
│
├── context.py ← 🆕 DÍA 3
│   # Schemas Context (historial)
│   #
│   # class ContextBase(BaseModel):
│   #     message_type: str = Field(..., pattern="^(user|assistant)$")
│   #     content: str = Field(..., min_length=1)
│   #     metadata: dict = {}
│   #
│   # class ContextCreate(ContextBase):
│   #     pass
│   #
│   # class ContextResponse(ContextBase):
│   #     id: int
│   #     created_at: datetime
│   #     class Config:
│   #         from_attributes = True
│
├── message.py ← 🆕 DÍA 2
│   # Schemas mensajes (adapters ↔ core)
│   #
│   # class MessageIn(BaseModel):
│   #     """Mensaje entrante normalizado"""
│   #     user_id: int
│   #     text: str
│   #     timestamp: datetime = Field(default_factory=datetime.now)
│   #     metadata: dict = {}
│   #
│   # class MessageOut(BaseModel):
│   #     """Respuesta saliente"""
│   #     text: str
│   #     buttons: list[dict] | None = None
│   #     metadata: dict = {}
│
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── STRUCTURE.md (este archivo)
└── DEPENDENCIES.md
📐 Patrones Implementados
Base/Create/Update/Response/InDB:
text
UserBase → Campos comunes
    ↓
UserCreate → Para crear (+ campos required)
UserUpdate → Para actualizar (todos opcional)
UserResponse → Para devolver al user (+ id, timestamps)
UserInDB → Completo en DB (+ user_id, internal fields)
Beneficios:

Separación clara responsabilidades

Security (no exponer internals en Response)

Flexibility (Update permite partial updates)

Type safety (cada operación su schema)

🔗 Dependencias Internas
text
src/models/ depende de:
├── src/config.constants (DEFAULT_TIMEZONE, etc)
└── [Ninguna otra dependencia interna]
text
src/models/ es usado por:
├── src/agents/ (validación input/output)
├── src/adapters/ (MessageIn/Out)
├── src/database/repositories/ (Create/Update schemas)
└── src/api/ (H08 - request/response)
📊 Métricas Estimadas
H02:
Archivos: 8 archivos Python

Schemas: ~30 classes

Fields: ~150 total

Validators: ~10 custom

LOC: ~800

Tests LOC: ~600

Coverage: >90%

🎯 Criterios Completitud
H02 Done cuando:
✅ 8 archivos implementados

✅ ~30 schemas funcionan

✅ Validators custom validan correctamente

✅ from_attributes=True funciona con SQLAlchemy

✅ Serialización JSON funciona

✅ Deserialización con validación funciona

✅ Tests >90% coverage

✅ mypy type checking pasa

✅ Integración con agents OK

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota