Changelog - src/models/
Todos los cambios notables en el módulo models/ serán documentados aquí.

El formato está basado en Keep a Changelog,
y este proyecto adhiere a Semantic Versioning.

[Unreleased]
Planificado para H04 (20-23 Nov 2025)
Payment schemas (Stripe integration)

Webhook schemas (Stripe, Telegram)

Email validation (pydantic[email])

Phone validation

API schemas (si Web implementado)

Planificado para H08 (Ene 2026) [CONDICIONAL]
REST API request/response schemas

WebSocket message schemas

Schema versioning (v1, v2)

[0.2.0] - 2025-11-16 (H02 Target)
Added
Base Schemas:

base.py con BaseSchema, TimestampSchema, ResponseSchema

Core Schemas:

user.py con 5 schemas (Base, Create, Update, Response, InDB)

reminder.py con 5 schemas

note.py con 5 schemas

event.py con 5 schemas

task.py con 5 schemas

context.py con 3 schemas (Base, Create, Response)

message.py con 2 schemas (MessageIn, MessageOut)

Validators Custom:

Validator datetime futuro (reminder)

Validator tags normalizados (note)

Validator date range (event)

Validator priority enum (task)

Features:

from_attributes=True (ex orm_mode) para SQLAlchemy integration

Type hints completos (mypy compatible)

Field constraints (min_length, max_length, ge, le)

Default values razonables

Serialización JSON automática

Deserialización con validación

Tests:

test_base.py

test_user.py

test_reminder.py

test_note.py

test_event.py

test_task.py

test_context.py

test_message.py

test_validators.py

test_serialization.py

Coverage >90%

Schemas Totales
7 módulos de schemas

~30 schemas individuales

~150 fields validados

~10 validators custom

Dependencies
pydantic==2.5.0

python-dateutil==2.8.2

[0.1.0] - 2025-11-03 (H01)
Added
Estructura inicial del módulo

Documentación completa:

README.md - Overview, uso, ejemplos

ROADMAP.md - Evolución planificada

CHANGELOG.md - Este archivo

STRUCTURE.md - Estructura detallada por hito

DEPENDENCIES.md - Dependencias

Arquitectura schemas definida (Base/Create/Update/Response/InDB)

Patrón seleccionado (Pydantic BaseModel)

Planning
H02: Schemas base funcionales (7 módulos)

H04: Payment + webhook schemas

H08: API schemas (si web)

Tipos de Cambios
Added - Para nuevas funcionalidades

Changed - Para cambios en funcionalidades existentes

Deprecated - Para funcionalidades que serán eliminadas

Removed - Para funcionalidades eliminadas

Fixed - Para corrección de bugs

Security - Para correcciones de seguridad

Validation - Para cambios en validación

Versioning
Este módulo sigue Semantic Versioning:

MAJOR (X.0.0): Breaking changes (campos renombrados, tipos cambiados, validación más estricta)

MINOR (0.X.0): Nuevos schemas, nuevos campos opcionales (compatible)

PATCH (0.0.X): Bug fixes validación, mejoras mensajes error (compatible)

Ejemplos Breaking Changes:
0.2.0 → 1.0.0 (MAJOR):

Rename field: telegram_user_id → external_id

Change type: tags: list[str] → tags: dict

Remove field: is_active eliminado

Stricter validation: title ahora min_length=5 (antes 1)

0.2.0 → 0.3.0 (MINOR):

Add new schema: PaymentSchema

Add optional field: user.phone_number

Add new validator: email format

0.2.0 → 0.2.1 (PATCH):

Fix validator bug: datetime timezone aware

Improve error message: "Invalid email" → "Email must be valid format (example@domain.com)"

Migration Guides
Migración a v0.2.0 (desde v0.1.0)
No migration needed - v0.1.0 solo tenía documentación.

Primera implementación real es v0.2.0 (H02).

Usage Example:
python
# Crear reminder
from src.models import ReminderCreate

reminder_data = ReminderCreate(
    title="Reunión",
    reminder_datetime="2025-11-15 15:00"  # Auto-parse to datetime
)

# Validación automática
assert isinstance(reminder_data.reminder_datetime, datetime)
Migración a v1.0.0 (futuro - TBD)
Se documentará cuando llegue.

Si hay breaking changes, se proveerá:

Lista completa de campos renombrados/eliminados

Script migración datos

Tests validación migración

Timeline deprecation (1-2 versiones minor warning)

Schema Evolution Best Practices
Añadir Nuevo Campo:
python
# ✅ BUENO: Opcional con default
class UserUpdate(BaseModel):
    phone_number: str | None = None  # Nuevo campo opcional

# ❌ MALO: Required (breaking change)
class UserUpdate(BaseModel):
    phone_number: str  # Rompe código existente
Cambiar Validación:
python
# ✅ BUENO: Más permisivo
class ReminderCreate(BaseModel):
    title: str = Field(min_length=1)  # Antes min_length=5

# ❌ MALO: Más estricto (breaking)
class ReminderCreate(BaseModel):
    title: str = Field(min_length=10)  # Rompe reminders existentes
Deprecar Campo:
python
from pydantic import Field, model_validator
import warnings

class UserUpdate(BaseModel):
    old_field: str | None = Field(None, deprecated=True)
    new_field: str | None = None
    
    @model_validator(mode='after')
    def warn_deprecated(self):
        if self.old_field is not None:
            warnings.warn(
                "old_field is deprecated, use new_field instead",
                DeprecationWarning
            )
        return self
Testing Changes
Test Backward Compatibility:
python
def test_old_schema_still_works():
    # Asegurar que código viejo funciona con nuevo schema
    old_data = {"title": "Test", "datetime": "2025-11-15"}
    reminder = ReminderCreate(**old_data)
    assert reminder.title == "Test"
Test Validation:
python
def test_validation_catches_invalid():
    with pytest.raises(ValidationError):
        ReminderCreate(title="", datetime="invalid")
Performance Tracking
Serialization Benchmarks:
Version	Objects/sec	Memory (1000 objects)
0.2.0	~50,000	~15MB
0.3.0 (target)	~75,000	~12MB
Security Considerations
v0.2.0 Security Features:
✅ No sensitive data in Response schemas (passwords, tokens)

✅ Input sanitization (strip whitespace)

✅ Type validation prevents injection

✅ Field constraints prevent overflow

⏳ Email/phone validation (H04)

⏳ Rate limiting validation (H04)

Known Limitations:
HTML sanitization no implementado (usar en app layer)

No XSS protection built-in (FastAPI layer H08)

Contribuir a este CHANGELOG
Al hacer cambios en schemas:

✅ Añadir entrada en [Unreleased]

✅ Usar categoría correcta (Added, Changed, Validation, etc)

✅ Documentar breaking changes explícitamente

✅ Escribir tests para cambios

✅ Al release, mover [Unreleased] a nueva versión

✅ Actualizar migration guide si breaking

Mantenido por: Álvaro Fernández Mota
Última actualización: 11 Nov 2025