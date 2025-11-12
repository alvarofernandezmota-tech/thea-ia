Dependencias - src/utils/
Módulo: Utils (Utilidades y Helpers)
Versión actual: 0.1.0 (H01 - Planificación)
Última actualización: 11 Nov 2025

📦 Dependencias Python
H02 (12-16 Nov): Utils Base
Producción:
text
# Date/Time
python-dateutil==2.8.2          # Parseo flexible fechas
pytz==2023.3                    # Timezone support

# Validation
email-validator==2.1.0          # Email validation
Desarrollo:
text
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1

# Code Quality
black==23.12.0
pylint==3.0.3
mypy==1.7.1
H04 (20-23 Nov): Utils Advanced
Adicionales Producción:
text
# Language Detection
langdetect==1.0.9               # Language detection

# Security
passlib[bcrypt]==1.7.4          # Password hashing

# Performance
cachetools==5.3.2               # Caching utilities
H06 (24-27 Nov): NLP Utils
Adicionales Producción:
text
# NLP (si implementado)
spacy==3.7.2                    # NLP framework
🔗 Dependencias Internas (THEA IA)
Módulos que usa utils/:
python
# Mínimas dependencias
from src.config.constants import (
    DEFAULT_TIMEZONE,
    DEFAULT_LANGUAGE,
    REGEX_DATETIME
)
Módulos que usan utils/:
python
# src/agents/ (TODOS)
from src.utils.datetime_utils import parse_datetime, format_datetime
from src.utils.text_utils import normalize_text, extract_hashtags
from src.utils.formatters import format_reminder_message, format_list

# src/adapters/
from src.utils.text_utils import sanitize_html, normalize_text
from src.utils.validators import is_valid_url

# src/models/
from src.utils.validators import is_valid_email, is_valid_timezone
# Usado en Pydantic validators

# src/database/repositories/
from src.utils.datetime_utils import parse_datetime
# Conversión user input

# src/core/
from src.utils.formatters import format_error
🔐 Variables de Entorno
Ninguna - Este módulo no usa variables entorno directamente.

Obtiene defaults de src/config/constants.py.

📊 Tabla Resumen Dependencias
Hito	Deps Producción	Deps Desarrollo	Dependencias Internas
H02	3	3	1 (config.constants)
H04	+3	0	0
H06	+1 (spacy)	0	0
Total	7	3	1
🚀 Instalación Dependencias
H02 (Setup inicial):
bash
# Instalar producción
pip install python-dateutil==2.8.2 pytz==2023.3 email-validator==2.1.0

# Instalar desarrollo
pip install pytest==7.4.3 black==23.12.0 mypy==1.7.1

# Verificar instalación
python -c "from dateutil import parser; print('OK')"
python -c "import pytz; print('OK')"
python -c "from email_validator import validate_email; print('OK')"
🧪 Testing Utils
Test datetime_utils:
python
# tests/unit/test_utils/test_datetime_utils.py
import pytest
from datetime import datetime, timedelta
from src.utils.datetime_utils import parse_datetime, format_datetime

def test_parse_datetime_tomorrow():
    """Parsea 'mañana 15:00'"""
    dt = parse_datetime("mañana 15:00")
    tomorrow = datetime.now() + timedelta(days=1)
    
    assert dt.day == tomorrow.day
    assert dt.hour == 15
    assert dt.minute == 0

def test_parse_datetime_relative():
    """Parsea 'en 2 horas'"""
    dt = parse_datetime("en 2 horas")
    expected = datetime.now() + timedelta(hours=2)
    
    # Margin 1 minute
    assert abs((dt - expected).seconds) < 60

def test_format_datetime():
    """Formatea datetime user-friendly"""
    dt = datetime(2025, 11, 15, 15, 0)
    formatted = format_datetime(dt)
    
    assert "15" in formatted  # Día
    assert "Nov" in formatted or "11" in formatted  # Mes
    assert "15:00" in formatted  # Hora
Test text_utils:
python
def test_normalize_text():
    """Normaliza texto"""
    result = normalize_text("  TEXTO  con    espacios  ")
    assert result == "texto con espacios"

def test_extract_hashtags():
    """Extrae hashtags"""
    text = "Nota #importante #work #urgent"
    tags = extract_hashtags(text)
    assert tags == ["importante", "work", "urgent"]

def test_remove_emojis():
    """Remueve emojis"""
    text = "Hola 👋 mundo 🌍"
    clean = remove_emojis(text)
    assert "👋" not in clean
    assert "🌍" not in clean
Test validators:
python
def test_is_valid_email():
    """Valida emails"""
    assert is_valid_email("user@example.com") == True
    assert is_valid_email("invalid") == False
    assert is_valid_email("@example.com") == False

def test_is_valid_timezone():
    """Valida timezones"""
    assert is_valid_timezone("Europe/Madrid") == True
    assert is_valid_timezone("America/New_York") == True
    assert is_valid_timezone("Invalid/Timezone") == False
Ejecutar tests:
bash
# Todos los tests utils
pytest src/tests/unit/test_utils/ -v

# Con coverage
pytest --cov=src/utils --cov-report=html

# Solo datetime_utils
pytest src/tests/unit/test_utils/test_datetime_utils.py -v

# Performance benchmark
pytest --benchmark-only
⚠️ Troubleshooting
1. dateutil.parser falla con input usuario
python
# Problema: parser.parse() muy permisivo o muy estricto

# Solución: Wrapper con validación
def parse_datetime(text: str, user_timezone: str = "Europe/Madrid") -> datetime:
    # Pre-validate común patterns
    patterns = {
        r"mañana": lambda: datetime.now() + timedelta(days=1),
        r"en (\d+) horas?": lambda m: datetime.now() + timedelta(hours=int(m.group(1))),
    }
    
    for pattern, handler in patterns.items():
        if match := re.match(pattern, text, re.IGNORECASE):
            return handler(match)
    
    # Fallback to dateutil
    try:
        return parser.parse(text)
    except ParserError:
        raise ValueError(f"No entiendo '{text}'")
2. Timezone issues naive/aware
python
# Problema: Mezclar naive y aware datetimes

# Solución: Siempre timezone aware
import pytz

def parse_datetime(text: str, user_timezone: str = "Europe/Madrid") -> datetime:
    dt = parser.parse(text)
    
    # Make aware si naive
    if dt.tzinfo is None:
        tz = pytz.timezone(user_timezone)
        dt = tz.localize(dt)
    
    return dt
3. email-validator muy estricto
python
# Problema: Rechaza emails válidos (ej: no DNS check)

# Solución: Configurar validación
from email_validator import validate_email, EmailNotValidError

def is_valid_email(email: str) -> bool:
    try:
        # check_deliverability=False para no hacer DNS check
        validate_email(email, check_deliverability=False)
        return True
    except EmailNotValidError:
        return False
4. Performance lento con muchos parseos
python
# Problema: parse_datetime llamado muchas veces

# Solución: Cache results comunes
from functools import lru_cache

@lru_cache(maxsize=128)
def parse_datetime_cached(text: str, user_timezone: str) -> datetime:
    return parse_datetime(text, user_timezone)

# O cachetools para TTL
from cachetools import TTLCache
cache = TTLCache(maxsize=128, ttl=300)  # 5 min

def parse_datetime_with_cache(text: str, tz: str) -> datetime:
    key = (text, tz)
    if key in cache:
        return cache[key]
    result = parse_datetime(text, tz)
    cache[key] = result
    return result
📈 Performance
Benchmarks Target (H02):
Función	Target	Notas
parse_datetime	<10ms	Sin cache
normalize_text	<1ms	Simple string ops
is_valid_email	<1ms	Regex only
format_reminder	<5ms	String formatting
Optimization Tips:
python
# 1. Regex precompilado
import re
HASHTAG_PATTERN = re.compile(r'#(\w+)')

def extract_hashtags(text: str) -> list[str]:
    return HASHTAG_PATTERN.findall(text)

# 2. Early returns
def normalize_text(text: str) -> str:
    if not text:
        return ""
    return text.lower().strip()

# 3. Generator expressions para grandes listas
def chunks(lst: list, n: int):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
📚 Recursos
Documentación Oficial:
python-dateutil

pytz

email-validator

Tutoriales:
dateutil parser

Working with Timezones

🔄 Actualización Dependencias
Política:
python-dateutil: Actualizar cada 6 meses (bug fixes)

pytz: Actualizar cada 3 meses (timezone data changes)

email-validator: Actualizar cada 6 meses

Comando:
bash
# Ver outdated
pip list --outdated | grep -E "dateutil|pytz|email-validator"

# Actualizar
pip install --upgrade python-dateutil pytz email-validator

# Verificar no rompe
pytest src/tests/unit/test_utils/ -v
🎯 Checklist Producción
Antes de H02 release:

 Todas las deps instaladas

 Tests pasan (>90% coverage)

 parse_datetime entiende casos comunes

 format_datetime user-friendly

 Validators funcionan correctamente

 Performance <10ms

 Type hints completos

 Docstrings con examples

Última actualización: 11 Nov 2025
Versión: 1.0
Responsable: Álvaro Fernández Mota