Changelog - src/utils/
Todos los cambios notables en el módulo utils/ serán documentados aquí.

El formato está basado en Keep a Changelog,
y este proyecto adhiere a Semantic Versioning.

[Unreleased]
Planificado para H04 (20-23 Nov 2025)
Advanced datetime helpers (business hours, recurrence)

Language detection (langdetect)

Security utils (password hashing, token generation)

Performance decorators (cache, rate_limit)

Planificado para H06 (24-27 Nov 2025)
NLP utils (entity extraction, intent detection)

Integration spaCy/transformers

[0.2.0] - 2025-11-16 (H02 Target)
Added
datetime_utils.py:

parse_datetime(text, timezone) - Parseo flexible fechas

parse_relative_datetime(text) - "en 2 horas", "mañana"

format_datetime(dt, timezone) - Formato user-friendly

get_next_weekday(dt, weekday) - Próximo lunes, martes, etc

convert_timezone(dt, from_tz, to_tz) - Conversión timezones

is_business_hours(dt) - Verificar horario laboral

text_utils.py:

normalize_text(text) - Lowercase, strip, spaces

remove_emojis(text) - Limpiar emojis

extract_hashtags(text) - Extraer #tags

truncate(text, max_length) - Truncar con "..."

sanitize_html(text) - Remover HTML tags

extract_urls(text) - Extraer URLs

validators.py:

is_valid_email(email) - Validar email format

is_valid_timezone(tz) - Validar pytz timezone

is_valid_url(url) - Validar URL format

validate_datetime_range(start, end) - End después start

formatters.py:

format_reminder_message(reminder) - Formatear reminder user

format_note_message(note) - Formatear nota

format_event_message(event) - Formatear evento

format_task_message(task) - Formatear tarea

format_list(items, max_items) - Lista con límite

format_error(error) - Error user-friendly

helpers.py (opcional):

generate_unique_id() - UUID generación

chunks(lst, n) - Split lista en chunks

retry_async(func, retries) - Retry async function

Tests:

test_datetime_utils.py (>90% coverage)

test_text_utils.py

test_validators.py

test_formatters.py

test_helpers.py

Features
Type hints completos

Docstrings con examples

Error messages claros

Performance <10ms per call

No dependencies circulares

Dependencies
python-dateutil==2.8.2

pytz==2023.3

email-validator==2.1.0

[0.1.0] - 2025-11-03 (H01)
Added
Estructura inicial del módulo

Documentación completa:

README.md - Overview, ejemplos

ROADMAP.md - Evolución planificada

CHANGELOG.md - Este archivo

STRUCTURE.md - Estructura detallada

DEPENDENCIES.md - Dependencias

Arquitectura funciones helper definida

Categorización (datetime, text, validators, formatters)

Planning
H02: Utils base funcionales (~30 funciones)

H04: Advanced utils (security, performance)

H06: NLP utils

Tipos de Cambios
Added - Para nuevas funcionalidades

Changed - Para cambios en funcionalidades existentes

Deprecated - Para funcionalidades que serán eliminadas

Removed - Para funcionalidades eliminadas

Fixed - Para corrección de bugs

Performance - Para mejoras performance

Versioning
MAJOR (X.0.0): Breaking changes (signature función cambia, comportamiento diferente)

MINOR (0.X.0): Nuevas funciones (compatible)

PATCH (0.0.X): Bug fixes (compatible)

Ejemplos:
0.2.0 → 1.0.0 (MAJOR):

python
# Breaking: Cambio signature
# Antes
parse_datetime(text)
# Ahora
parse_datetime(text, timezone)  # timezone required
0.2.0 → 0.3.0 (MINOR):

python
# Nueva función (no breaking)
def format_currency(amount, currency="EUR"):
    pass
0.2.0 → 0.2.1 (PATCH):

python
# Fix bug parseo
# Antes: "en 2 hora" fallaba
# Ahora: "en 2 hora" funciona (typo tolerance)
Migration Guides
Migración a v0.2.0 (desde v0.1.0)
No migration needed - v0.1.0 solo documentación.

Primera implementación real es v0.2.0 (H02).

Usage Examples:
python
# Datetime parsing
from src.utils.datetime_utils import parse_datetime, format_datetime

dt = parse_datetime("mañana 15:00")
formatted = format_datetime(dt)  # "Miércoles 12 Nov, 15:00"

# Text cleaning
from src.utils.text_utils import normalize_text, extract_hashtags

clean = normalize_text("  TEXTO con    espacios  ")  # "texto con espacios"
tags = extract_hashtags("Nota #importante #work")  # ['importante', 'work']

# Validation
from src.utils.validators import is_valid_email

if is_valid_email("user@example.com"):
    # Valid
    pass
Performance Tracking
Benchmarks (Target H02):
Función	Target	Actual (TBD)
parse_datetime	<10ms	-
normalize_text	<1ms	-
is_valid_email	<1ms	-
format_reminder	<5ms	-
Breaking Changes History
v0.2.0:
Ninguno (primera implementación)

v1.0.0 (futuro - TBD):
TBD cuando llegue

Deprecation Policy
Cuando deprecar función:

Version N: Mark deprecated, añadir warning

python
import warnings

def old_function():
    warnings.warn(
        "old_function is deprecated, use new_function instead",
        DeprecationWarning,
        stacklevel=2
    )
    return new_function()
Version N+1 (minor): Mantener con warning

Version N+2 (major): Eliminar

Timeline: Mínimo 2 minor versions (3-6 meses) antes eliminar.

Contribuir a este CHANGELOG
Al hacer cambios en utils:

✅ Añadir entrada en [Unreleased]

✅ Usar categoría correcta (Added, Fixed, Performance, etc)

✅ Documentar breaking changes

✅ Escribir tests

✅ Benchmark performance si relevante

✅ Al release, mover a versión nueva

Mantenido por: Álvaro Fernández Mota
Última actualización: 11 Nov 2025