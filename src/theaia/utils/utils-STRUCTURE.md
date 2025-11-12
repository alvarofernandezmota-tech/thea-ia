Estructura Planificada - src/utils/
Módulo: Utils (Utilidades y Helpers)
Propósito: Funciones helper reutilizables
Patrón: Pure Functions (stateless)

📋 Estado Actual (11 Nov 2025 - H01)
text
src/utils/
├── __init__.py (placeholder)
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅
Estado: Sin implementación, solo planificación

🎯 H02 (12-16 Nov): Utils Base
Estructura Objetivo:
text
src/utils/
│
├── __init__.py
│   # Exports funciones principales
│   from .datetime_utils import parse_datetime, format_datetime
│   from .text_utils import normalize_text, extract_hashtags
│   from .validators import is_valid_email, is_valid_timezone
│   from .formatters import format_reminder_message, format_list
│
├── datetime_utils.py ← 🆕 DÍA 1 (CRÍTICO)
│   # Parseo y formateo fechas/horas
│   #
│   # def parse_datetime(text: str, user_timezone: str = "Europe/Madrid") -> datetime:
│   #     """Parsea texto flexible a datetime"""
│   #     # Entiende: "mañana 15:00", "en 2 horas", "viernes 18:00"
│   #     pass
│   #
│   # def parse_relative_datetime(text: str) -> datetime:
│   #     """Parsea expresiones relativas"""
│   #     # "en 1 hora", "mañana", "la próxima semana"
│   #     pass
│   #
│   # def format_datetime(dt: datetime, user_timezone: str = "Europe/Madrid") -> str:
│   #     """Formatea datetime para usuario"""
│   #     # Output: "Lunes 15 Nov 2025, 15:00"
│   #     pass
│   #
│   # def get_next_weekday(dt: datetime, weekday: int) -> datetime:
│   #     """Obtiene próximo día semana (0=Lunes)"""
│   #     pass
│   #
│   # def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
│   #     """Convierte entre timezones"""
│   #     pass
│   #
│   # def is_business_hours(dt: datetime) -> bool:
│   #     """Verifica si es horario laboral (9-18 L-V)"""
│   #     pass
│
├── text_utils.py ← 🆕 DÍA 2
│   # Normalización y limpieza texto
│   #
│   # def normalize_text(text: str) -> str:
│   #     """Normaliza: lowercase, strip, spaces únicos"""
│   #     return text.lower().strip()
│   #
│   # def remove_emojis(text: str) -> str:
│   #     """Remueve emojis"""
│   #     pass
│   #
│   # def extract_hashtags(text: str) -> list[str]:
│   #     """Extrae #hashtags"""
│   #     return re.findall(r'#(\w+)', text)
│   #
│   # def truncate(text: str, max_length: int, suffix: str = "...") -> str:
│   #     """Trunca texto con sufijo"""
│   #     if len(text) <= max_length:
│   #         return text
│   #     return text[:max_length - len(suffix)] + suffix
│   #
│   # def sanitize_html(text: str) -> str:
│   #     """Remueve HTML tags"""
│   #     return html.escape(text)
│   #
│   # def extract_urls(text: str) -> list[str]:
│   #     """Extrae URLs"""
│   #     return re.findall(r'https?://\S+', text)
│
├── validators.py ← 🆕 DÍA 2
│   # Validaciones custom
│   #
│   # def is_valid_email(email: str) -> bool:
│   #     """Valida formato email"""
│   #     try:
│   #         validate_email(email)
│   #         return True
│   #     except:
│   #         return False
│   #
│   # def is_valid_timezone(tz: str) -> bool:
│   #     """Valida timezone pytz"""
│   #     try:
│   #         pytz.timezone(tz)
│   #         return True
│   #     except:
│   #         return False
│   #
│   # def is_valid_url(url: str) -> bool:
│   #     """Valida formato URL"""
│   #     pattern = r'^https?://\S+$'
│   #     return bool(re.match(pattern, url))
│   #
│   # def validate_datetime_range(start: datetime, end: datetime) -> bool:
│   #     """Valida end después de start"""
│   #     return end > start
│
├── formatters.py ← 🆕 DÍA 3
│   # Formateo respuestas usuario
│   #
│   # def format_reminder_message(reminder) -> str:
│   #     """Formatea reminder para mostrar"""
│   #     return f"""📅 {reminder.title}
│   # Fecha: {format_datetime(reminder.reminder_datetime)}
│   # {f'Descripción: {reminder.description}' if reminder.description else ''}"""
│   #
│   # def format_note_message(note) -> str:
│   #     """Formatea nota"""
│   #     tags_str = " ".join(f"#{tag}" for tag in note.tags) if note.tags else ""
│   #     return f"""📝 {note.title or 'Nota'}
│   # {note.content}
│   # {tags_str}"""
│   #
│   # def format_event_message(event) -> str:
│   #     """Formatea evento"""
│   #     pass
│   #
│   # def format_task_message(task) -> str:
│   #     """Formatea tarea"""
│   #     pass
│   #
│   # def format_list(items: list, max_items: int = 10) -> str:
│   #     """Formatea lista con límite"""
│   #     lines = [f"{i}. {item}" for i, item in enumerate(items[:max_items], 1)]
│   #     if len(items) > max_items:
│   #         lines.append(f"\n(y {len(items) - max_items} más)")
│   #     return "\n".join(lines)
│   #
│   # def format_error(error: Exception) -> str:
│   #     """Formatea error user-friendly"""
│   #     return f"❌ Error: {str(error)}"
│
├── helpers.py ← 🆕 DÍA 3 (opcional)
│   # Funciones misceláneas
│   #
│   # def generate_unique_id() -> str:
│   #     """Genera UUID único"""
│   #     return str(uuid.uuid4())
│   #
│   # def chunks(lst: list, n: int) -> Iterator:
│   #     """Split lista en chunks de tamaño n"""
│   #     for i in range(0, len(lst), n):
│   #         yield lst[i:i + n]
│   #
│   # async def retry_async(
│   #     func: Callable,
│   #     max_retries: int = 3,
│   #     delay: float = 1.0
│   # ):
│   #     """Retry async function con exponential backoff"""
│   #     pass
│
├── README.md
├── ROADMAP.md
├── CHANGELOG.md
├── STRUCTURE.md (este archivo)
└── DEPENDENCIES.md
🔗 Dependencias Internas
text
src/utils/ depende de:
├── src.config.constants (DEFAULT_TIMEZONE, etc)
└── [Sin otras dependencias internas]
text
src/utils/ es usado por:
├── src/agents/ (TODOS - parseo datetime, formateo mensajes)
├── src/adapters/ (text cleaning, validation)
├── src/models/ (validators en Pydantic)
└── src/core/ (formateo respuestas)
📐 Diseño Funciones
Pure Functions:
python
# ✅ BUENO: Pure function (sin side effects)
def normalize_text(text: str) -> str:
    return text.lower().strip()

# ❌ MALO: Con state (usar clase si necesitas)
class TextNormalizer:
    def __init__(self):
        self.cache = {}
Beneficios Pure Functions:

Fácil testear

No side effects

Thread-safe

Predictable

Composable

Type Hints:
python
from typing import Optional, List
from datetime import datetime

def parse_datetime(
    text: str,
    user_timezone: str = "Europe/Madrid"
) -> datetime:
    pass

def extract_hashtags(text: str) -> List[str]:
    pass
Error Handling:
python
def parse_datetime(text: str, user_timezone: str) -> datetime:
    """Parse datetime con error claro"""
    try:
        # Parsear
        return parsed_dt
    except Exception as e:
        raise ValueError(
            f"No pude entender '{text}'. "
            f"Ejemplos: 'mañana 15:00', 'en 2 horas', '2025-11-15'"
        ) from e
📊 Métricas Estimadas
H02:
Archivos: 4-5 archivos Python

Funciones: ~30 funciones

LOC: ~600

Tests LOC: ~800

Coverage: >90%

🎯 Criterios Completitud
H02 Done cuando:
✅ datetime_utils implementado (parse + format)

✅ text_utils implementado (normalize + extract)

✅ validators implementados (email, timezone, url)

✅ formatters implementados (reminder, note, event, task)

✅ Tests >90% coverage

✅ Type hints completos

✅ Docstrings con examples

✅ Performance <10ms per call

✅ Integración agents funciona

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota