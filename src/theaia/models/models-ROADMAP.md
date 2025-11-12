Roadmap - src/models/
Módulo: Models (Pydantic Schemas)
Versión actual: 0.1.0 (H01 - Planificación)
Próxima versión: 0.2.0 (H02 - Implementación Base)

📊 Estado Actual (11 Nov 2025 - H01)
Completado ✅
Arquitectura schemas definida (Base/Create/Update/Response/InDB)

Patrón seleccionado (Pydantic BaseModel + validators)

Estructura por módulos planificada

Documentación completa

Dependencias identificadas

Pendiente ⏳
Implementación schemas Python

Validators custom

Tests unitarios validación

🎯 H02 (12-16 Nov 2025): Schemas Base
Objetivo: Pydantic schemas funcionales para MVP

Día 1 (12 Nov):
Base Schemas:

base.py

BaseSchema (config común)

TimestampSchema (created_at, updated_at)

ResponseSchema (success, message, data)

Core Schemas:

user.py

UserBase, UserCreate, UserUpdate, UserResponse, UserInDB

reminder.py

ReminderBase, ReminderCreate, ReminderUpdate, ReminderResponse, ReminderInDB

message.py

MessageIn (normalizado de adapter)

MessageOut (respuesta a adapter)

Tests Día 1:

test_base.py (schemas base)

test_user.py (validación User)

test_reminder.py (validación Reminder)

Criterio Done Día 1:
✅ User + Reminder schemas validan correctamente
✅ MessageIn/Out funcionan con adapters
✅ Tests básicos pasan

Día 2 (13 Nov):
Additional Schemas:

note.py

NoteBase, NoteCreate, NoteUpdate, NoteResponse, NoteInDB

event.py

EventBase, EventCreate, EventUpdate, EventResponse, EventInDB

Custom Validators:

Validator datetime futuro (reminder)

Validator tags normalizados (note)

Validator date range (event)

Tests Día 2:

test_note.py

test_event.py

test_validators.py

Criterio Done Día 2:
✅ Note + Event schemas completos
✅ Validators custom funcionan
✅ Tests >85% coverage

Día 3 (14 Nov):
Complete Schemas:

task.py

TaskBase, TaskCreate, TaskUpdate, TaskResponse, TaskInDB

context.py

ContextBase, ContextCreate, ContextResponse

Integration:

Integración con repositories

Serialización from_orm funciona

Deserialización a dict/JSON funciona

Tests Día 3:

test_task.py

test_context.py

test_serialization.py

Criterio Done Día 3:
✅ Todos los schemas implementados
✅ Integración con database funciona
✅ Tests coverage >90%

Criterios Done H02:
✅ 7 módulos schemas (base, user, reminder, note, event, task, context, message)

✅ ~30 schemas totales (5 per module average)

✅ Validators custom funcionan

✅ Serialización/deserialización OK

✅ from_orm() funciona con SQLAlchemy

✅ Tests >90% coverage

✅ Type hints completos (mypy pass)

✅ Integración con agents funciona

🏢 H04 (20-23 Nov 2025): Enterprise Schemas
Objetivo: Schemas para features enterprise

Nuevos Schemas:
1. Payment Schemas:

payment.py

PaymentBase

PaymentCreate

PaymentResponse

SubscriptionSchema

2. Webhook Schemas:

webhook.py

StripeWebhookEvent

TelegramWebhookUpdate

3. Advanced Validation:

Email validation (pydantic[email])

Phone validation

URL validation

Custom business rules

4. API Schemas (si Web):

api.py

APIRequest

APIResponse

ErrorResponse

PaginatedResponse

Criterios Done H04:
✅ Payment schemas completos

✅ Webhook schemas validan correctamente

✅ Email/phone validation funciona

✅ API schemas (si web implementado)

🔮 H08 (Ene 2026): Web API Schemas [CONDICIONAL]
Si se implementa Web:

REST API Schemas:
Request/Response pairs para cada endpoint

OpenAPI/Swagger auto-generation

Versioning schemas (v1, v2)

WebSocket Schemas:
WS message schemas

Real-time event schemas

📈 Métricas de Éxito
Hito	Schemas	Validators	Tests Coverage	Type Safety
H02	~30	~10	>90%	100% (mypy)
H04	~45	~20	>90%	100%
H08	~60	~30	>95%	100%
🚧 Riesgos y Mitigaciones
Riesgo 1: Validación muy estricta bloquea usuarios
Impacto: MEDIO
Mitigación:

Validación flexible donde posible

Mensajes error claros

Fallbacks razonables

Riesgo 2: Schemas desincronizados con database models
Impacto: ALTO
Mitigación:

Tests integración schemas ↔ models

CI/CD valida consistencia

Documentación clara responsabilidades

Riesgo 3: Performance serialización con muchos objetos
Impacto: BAJO
Mitigación:

Paginación en queries

Lazy loading cuando posible

orjson para JSON rápido

📝 Decisiones Técnicas
¿Por qué Pydantic vs Marshmallow?
Razón:

Type hints nativos Python

Mejor performance

Mejor integración FastAPI (H08)

Auto-validation

Editor autocomplete

¿Por qué patrón Base/Create/Update/Response/InDB?
Razón:

Separación clara responsabilidades

Evita exponer campos internos

Facilita versionado API

Seguridad (no leak passwords, etc)

¿Por qué from_attributes=True (ex orm_mode)?
Razón:

Integración transparente con SQLAlchemy

Evita mapeo manual

Código más limpio

🔄 Proceso de Cambio
Añadir Nuevo Schema:
Crear archivo en src/models/

Implementar Base/Create/Update/Response/InDB

Añadir validators si necesario

Escribir tests

Actualizar __init__.py exports

Documentar en README.md

Actualizar CHANGELOG.md

Cambiar Schema Existente:
Evaluar si breaking change

Si breaking: version bump major

Migration guide si necesario

Tests actualizados

CHANGELOG.md updated

💡 Best Practices
Naming Convention:
python
# Entity + Suffix pattern
UserBase
UserCreate
UserUpdate
UserResponse
UserInDB

# NO usar:
User (confuso con database model)
UserDTO (no necesario, Pydantic ya es DTO)
Field Validation:
python
from pydantic import Field, field_validator

class ReminderCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    
    @field_validator('title')
    def title_not_empty_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be only whitespace')
        return v.strip()
Optional vs Required:
python
# Create: required fields (except defaults)
class ReminderCreate(BaseModel):
    title: str  # Required
    description: str | None = None  # Optional

# Update: all fields optional
class ReminderUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
📞 Feedback y Contribuciones
Issues Reportadas:
Ninguna aún (módulo en planificación)

Feature Requests:
Ninguna aún

Cómo Contribuir:
Review schemas planificados

Suggest validators útiles

Report validation issues en desarrollo

Submit PRs con tests

Última actualización: 11 Nov 2025
Próxima revisión: H02 complete (16 Nov 2025)
Responsable: Álvaro Fernández Mota