src/utils/ - Utilities Module
Módulo de funciones helper y utilidades comunes

📋 Overview
El módulo utils/ contiene funciones helper reutilizables por toda la aplicación:

📅 datetime_utils: Parseo y formateo fechas

📝 text_utils: Normalización y limpieza texto

✅ validators: Validaciones custom

🔧 formatters: Formateo mensajes usuario

🛠️ helpers: Funciones misceláneas

🎯 Propósito
Centralizar lógica común para:

✅ Reutilización: Misma función en múltiples agentes

✅ Mantenibilidad: Cambiar en un lugar

✅ Testabilidad: Tests unitarios aislados

✅ Consistencia: Mismo comportamiento everywhere

📁 Estructura (H02)
text
src/utils/
├── __init__.py
├── datetime_utils.py      # Parseo y formateo fechas
├── text_utils.py          # Normalización texto
├── validators.py          # Validaciones custom
├── formatters.py          # Formateo respuestas
├── helpers.py             # Funciones misceláneas
└── README.md
🚀 Quick Start
datetime_utils:
python
from src.utils.datetime_utils import parse_datetime, format_datetime

# Parsear texto flexible
dt = parse_datetime("mañana 15:00")
# → datetime(2025, 11, 12, 15, 0)

dt = parse_datetime("en 2 horas")
# → datetime(2025, 11, 11, 18, 43)

# Formatear para usuario
formatted = format_datetime(dt)
# → "Miércoles 12 Nov, 15:00"
text_utils:
python
from src.utils.text_utils import normalize_text, extract_hashtags

# Normalizar
clean = normalize_text("  TEXTO  con    espacios  ")
# → "texto con espacios"

# Extraer hashtags
tags = extract_hashtags("Nota #importante #work")
# → ['importante', 'work']
validators:
python
from src.utils.validators import is_valid_email, is_valid_timezone

# Validar email
is_valid_email("user@example.com")  # → True
is_valid_email("invalid")  # → False

# Validar timezone
is_valid_timezone("Europe/Madrid")  # → True
formatters:
python
from src.utils.formatters import format_reminder_message, format_list

# Formatear reminder
message = format_reminder_message(reminder)
# → "📅 Reunión\nFecha: Miércoles 12 Nov, 15:00\n..."

# Formatear lista
items = ["Item 1", "Item 2", "Item 3"]
formatted = format_list(items, max_items=2)
# → "1. Item 1\n2. Item 2\n(y 1 más)"
📦 Dependencias
text
python-dateutil==2.8.2      # Parseo fechas flexible
pytz==2023.3                # Timezone support
email-validator==2.1.0      # Email validation
💡 Funciones Principales
datetime_utils.py:
Función	Descripción	Ejemplo
parse_datetime(text, tz)	Parsea texto a datetime	"mañana 15:00" → datetime
parse_relative_datetime(text)	Parsea expresiones relativas	"en 2 horas" → datetime
format_datetime(dt, tz)	Formatea datetime	dt → "Miércoles 12 Nov, 15:00"
get_next_weekday(dt, weekday)	Próximo día semana	dt, 0 → próximo lunes
convert_timezone(dt, from, to)	Convierte timezone	dt → dt en otro timezone
is_business_hours(dt)	Verifica horario laboral	dt → True/False
text_utils.py:
Función	Descripción	Ejemplo
normalize_text(text)	Normaliza texto	" TEXTO " → "texto"
remove_emojis(text)	Remueve emojis	"Hola 👋" → "Hola"
extract_hashtags(text)	Extrae #hashtags	"Nota #work" → ['work']
truncate(text, max_len)	Trunca texto	"Long text..." → "Long..."
sanitize_html(text)	Remueve HTML	"<b>Text</b>" → "Text"
extract_urls(text)	Extrae URLs	"Link: http://..." → [...]
validators.py:
Función	Descripción	Ejemplo
is_valid_email(email)	Valida email	"user@test.com" → True
is_valid_timezone(tz)	Valida timezone	"Europe/Madrid" → True
is_valid_url(url)	Valida URL	"http://..." → True
validate_datetime_range(start, end)	Valida rango	start < end → True
formatters.py:
Función	Descripción	Retorna
format_reminder_message(reminder)	Formatea reminder	Texto formateado
format_note_message(note)	Formatea nota	Texto formateado
format_event_message(event)	Formatea evento	Texto formateado
format_task_message(task)	Formatea tarea	Texto formateado
format_list(items, max)	Formatea lista	Lista numerada
format_error(error)	Formatea error	Error user-friendly
🧪 Testing
bash
# Ejecutar tests utils
pytest src/tests/unit/test_utils/ -v

# Con coverage
pytest --cov=src/utils --cov-report=html

# Solo datetime_utils
pytest src/tests/unit/test_utils/test_datetime_utils.py -v
📊 Coverage Objetivo
H02: >90% (funciones críticas bien testeadas)

Cada función con al menos 3 test cases

Edge cases cubiertos (None, empty, invalid)

🎯 Uso en Agentes
ReminderAgent:
python
from src.utils.datetime_utils import parse_datetime
from src.utils.formatters import format_reminder_message

async def create_reminder(self, text: str):
    # Parsear datetime
    reminder_dt = parse_datetime("mañana 15:00", user_timezone=self.user.timezone)
    
    # Crear reminder
    reminder = await self.repo.create(
        user_id=self.user_id,
        title="reunión",
        reminder_datetime=reminder_dt
    )
    
    # Formatear respuesta
    return format_reminder_message(reminder)
NoteAgent:
python
from src.utils.text_utils import extract_hashtags, normalize_text

async def create_note(self, content: str):
    # Extraer tags
    tags = extract_hashtags(content)  # ['shopping', 'urgent']
    
    # Limpiar content
    clean_content = normalize_text(content)
    
    # Guardar
    note = await self.repo.create(
        user_id=self.user_id,
        content=clean_content,
        tags=tags
    )
🔮 Próximos Pasos
H04: Advanced Utils
Business hours calculation

Language detection

Security utils (password hashing)

Performance decorators (cache, rate_limit)

H06: NLP Utils
Integration con spaCy

Entity extraction helpers

Intent classification utilities

📚 Recursos
python-dateutil

pytz

email-validator

Versión: 0.1.0
Estado: Planificación (H01)
Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota