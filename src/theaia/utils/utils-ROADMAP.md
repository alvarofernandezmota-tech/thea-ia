ROADMAP-utils.md
Roadmap - src/utils/
Módulo: Utils (Utilidades y Helpers)
Versión actual: 0.1.0 (H01 - Planificación)
Próxima versión: 0.2.0 (H02 - Implementación Base)

📊 Estado Actual (11 Nov 2025 - H01)
Completado ✅
Arquitectura módulo definida

Funciones helper identificadas

Categorización (datetime, text, validators, formatters)

Documentación completa

Dependencias identificadas

Pendiente ⏳
Implementación funciones Python

Tests unitarios

Integración con agents

🎯 H02 (12-16 Nov 2025): Utils Base
Objetivo: Helpers funcionales para MVP

Día 1 (12 Nov) - CRÍTICO:
datetime_utils.py (prioritario para reminders/events):

parse_datetime(text, timezone) → datetime

parse_relative_datetime(text) → datetime

format_datetime(dt, timezone) → str

get_next_weekday(dt, weekday) → datetime

Criterio Done Día 1:
✅ parse_datetime entiende: "mañana 15:00", "en 2 horas", "viernes 18:00"
✅ format_datetime devuelve formato user-friendly
✅ Tests >90% coverage

Día 2 (13 Nov):
text_utils.py:

normalize_text(text) → str

remove_emojis(text) → str

extract_hashtags(text) → list[str]

truncate(text, max_length) → str

sanitize_html(text) → str

validators.py:

is_valid_email(email) → bool

is_valid_timezone(tz) → bool

is_valid_url(url) → bool

validate_datetime_range(start, end) → bool

Criterio Done Día 2:
✅ text_utils normalizan y limpian correctamente
✅ validators detectan inputs inválidos
✅ Tests casos edge

Día 3 (14 Nov):
formatters.py:

format_reminder_message(reminder) → str

format_note_message(note) → str

format_event_message(event) → str

format_task_message(task) → str

format_list(items, max_items) → str

format_error(error) → str

helpers.py (opcional):

generate_unique_id() → str

chunks(lst, n) → Iterator

retry_async(func, max_retries)

Criterio Done Día 3:
✅ formatters devuelven mensajes user-friendly
✅ format_list maneja límites correctamente
✅ Integración con agents funciona

Criterios Done H02:
✅ 4-5 archivos implementados

✅ ~25-30 funciones helper

✅ datetime parsing flexible funciona

✅ Tests >90% coverage

✅ Sin dependencias circulares

✅ Documentación inline (docstrings)

✅ Type hints completos

✅ Integración agents OK

🏢 H04 (20-23 Nov 2025): Utils Enterprise
Objetivo: Helpers avanzados

Nuevas Features:
1. Advanced Datetime:

Business hours calculation

Timezone conversion multi-region

Recurrence patterns (daily, weekly, monthly)

Holiday calendar integration

2. Advanced Text:

Language detection (langdetect)

Sentiment analysis básico

Keyword extraction

Spell checking (pyspellchecker)

3. Security Utils:

hash_password(password) → str

verify_password(password, hash) → bool

generate_token(length) → str

sanitize_sql(text) → str

4. Performance Utils:

cache_result(ttl) decorator

rate_limit(calls, period) decorator

measure_time() context manager

Criterios Done H04:
✅ Advanced datetime helpers

✅ Language detection

✅ Security utils completos

✅ Performance decorators

✅ Tests >90%

🔮 H06 (24-27 Nov 2025): ML Utils
NLP Helpers:

nlp_utils.py:

extract_entities(text) → dict

detect_intent(text) → str

summarize_text(text, max_length) → str

Integration con spaCy/transformers

📈 Métricas de Éxito
Hito	Archivos	Funciones	Tests Coverage	Performance
H02	4-5	~30	>90%	<10ms/call
H04	+2-3	~50	>90%	<10ms
H06	+1	~60	>85%	<50ms (NLP)
🚧 Riesgos y Mitigaciones
Riesgo 1: parse_datetime no entiende input usuario
Impacto: ALTO
Mitigación:

Parseo flexible con dateutil

Fallbacks razonables

Mensajes error claros

Ejemplos en error messages

Riesgo 2: Performance datetime parsing lento
Impacto: MEDIO
Mitigación:

Caché resultados comunes

Regex pre-check antes parsing complejo

Benchmark performance (target <10ms)

Riesgo 3: Timezone issues causan bugs
Impacto: ALTO
Mitigación:

Siempre timezone aware

Tests con múltiples timezones

Default a Europe/Madrid

User timezone en profile

📝 Decisiones Técnicas
¿Por qué python-dateutil vs arrow?
Razón:

Más flexible parsing

Mejor soporte timezones

Más mantenido

Integración estándar biblioteca

¿Por qué funciones vs clases?
Razón:

Utils son stateless

Más simple importar funciones

Mejor para type hints

Más pythonic para helpers

¿Por qué separar formatters?
Razón:

Responsabilidad única

Fácil customizar por user

Tests aislados

Reutilización clara

🔄 Proceso de Cambio
Añadir Nueva Función:
Identificar categoría (datetime, text, validator, formatter)

Implementar en archivo correspondiente

Añadir docstring completo (args, returns, examples)

Escribir tests (happy path + edge cases)

Actualizar __init__.py exports

Documentar en README.md

Actualizar CHANGELOG.md

Modificar Función Existente:
Evaluar si breaking change

Si breaking: deprecation warning primero

Tests actualizados

Documentación actualizada

CHANGELOG.md updated

💡 Best Practices
Docstrings:
python
def parse_datetime(text: str, user_timezone: str = "Europe/Madrid") -> datetime:
    """
    Parsea texto flexible a datetime.
    
    Args:
        text: Texto con fecha/hora (ej: "mañana 15:00", "en 2 horas")
        user_timezone: Timezone del usuario (default: Europe/Madrid)
    
    Returns:
        datetime: Objeto datetime timezone-aware
    
    Raises:
        ValueError: Si texto no puede ser parseado
    
    Examples:
        >>> parse_datetime("mañana 15:00")
        datetime(2025, 11, 12, 15, 0, tzinfo=...)
        
        >>> parse_datetime("en 2 horas")
        datetime(2025, 11, 11, 18, 20, tzinfo=...)
    """
    pass
Type Hints:
python
from typing import Optional, List
from datetime import datetime, date

def parse_datetime(
    text: str,
    user_timezone: str = "Europe/Madrid"
) -> datetime:
    pass

def extract_hashtags(text: str) -> List[str]:
    pass

def format_list(
    items: List[str],
    max_items: int = 10
) -> str:
    pass
Error Handling:
python
def parse_datetime(text: str, user_timezone: str = "Europe/Madrid") -> datetime:
    try:
        # Intentar parsear
        dt = parser.parse(text)
        return dt
    except (ValueError, ParserError) as e:
        # Error claro al usuario
        raise ValueError(
            f"No pude entender la fecha '{text}'. "
            f"Intenta: 'mañana 15:00', 'en 2 horas', '2025-11-15 15:00'"
        ) from e
📞 Feedback y Contribuciones
Issues Reportadas:
Ninguna aún (módulo en planificación)

Feature Requests:
Ninguna aún

Cómo Contribuir:
Suggest nuevas funciones útiles

Report bugs en parsing

Improve error messages

Submit PRs con tests

Última actualización: 11 Nov 2025
Próxima revisión: H02 complete (16 Nov 2025)
Responsable: Álvaro Fernández Mota