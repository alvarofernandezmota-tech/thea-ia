unit/ - Unit Tests
Tests unitarios (70% de la suite)

📋 Overview
Tests aislados de componentes individuales:

⚡ Rápidos (<1ms por test)

🔒 Aislados (sin DB, sin network)

🎯 Específicos (una función/método)

📊 Muchos (70% total tests)

📁 Estructura
text
unit/
├── test_config/           # Settings, logging
├── test_database/         # Models, repositories
├── test_models/           # Pydantic schemas
├── test_adapters/         # Adapters (mock externos)
├── test_agents/           # Agents (mock repos)
├── test_core/             # CoreManager
├── test_utils/            # Helpers, utils
├── test_ml/               # (H06) NLP
└── test_services/         # (H04-H05) Services
🚀 Quick Start
bash
# Ejecutar todos los unit tests
pytest src/tests/unit/ -v

# Solo un módulo
pytest src/tests/unit/test_utils/ -v

# Con coverage
pytest src/tests/unit/ --cov=src --cov-report=html
✅ Características Unit Test
✅ Debe ser:
Rápido (<1ms idealmente)

Aislado (sin side effects)

Determinista (siempre mismo resultado)

Fácil de entender

❌ NO debe:
Tocar database real

Hacer network requests

Depender de otros tests

Usar sleep() o timers reales

💡 Ejemplo
python
# test_utils/test_datetime_utils.py
import pytest
from datetime import datetime, timedelta
from src.utils.datetime_utils import parse_datetime

def test_parse_datetime_tomorrow():
    """Parsea 'mañana 15:00' correctamente"""
    # Arrange
    text = "mañana 15:00"
    
    # Act
    result = parse_datetime(text)
    
    # Assert
    tomorrow = datetime.now() + timedelta(days=1)
    assert result.day == tomorrow.day
    assert result.hour == 15
    assert result.minute == 0

def test_parse_datetime_invalid_raises_error():
    """Input inválido debe lanzar ValueError"""
    with pytest.raises(ValueError):
        parse_datetime("texto inválido")

@pytest.mark.parametrize("text,expected_days", [
    ("hoy", 0),
    ("mañana", 1),
    ("pasado mañana", 2),
])
def test_parse_relative_dates(text, expected_days):
    """Parsea fechas relativas correctamente"""
    result = parse_datetime(text)
    expected = datetime.now() + timedelta(days=expected_days)
    assert result.day == expected.day
🎯 Coverage Target
>90% en unit tests

Prioridad:

config/ >95%

models/ >95%

utils/ >95%

database/ >90%

agents/ >85%

adapters/ >85%

core/ >80%

📚 Por Implementar
Ver subcarpetas para detalles:

test_config/ - H02 Día 1

test_database/ - H02 Día 1-3

test_models/ - H02 Día 2-3

test_utils/ - H02 Día 2

test_adapters/ - H02 Día 3

test_agents/ - H02 Día 3

test_core/ - H02 Día 3

Implementar en: H02 (12-16 Nov)
Última actualización: 11 Nov 2025