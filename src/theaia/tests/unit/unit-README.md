# unit/ - Unit Tests

Tests unitarios fundamentales para componentes aislados.

---

## 📋 Overview

Tests aislados de componentes individuales con características:

- ⚡ **Rápidos** (<1ms por test ideal)
- 🔒 **Aislados** (sin DB, sin network)
- 🎯 **Específicos** (una función/método)
- 📊 **Numerosos** (70% del total de tests)

---

## 📁 Estructura

unit/
├── test_agent_config.py # ✅ AgentConfig (15 tests, 100%)
├── test_base_agent.py # ✅ BaseAgent (15 tests, 93%)
├── test_context_persistence.py # ✅ Context (1 test)
├── test_date_parser.py # ✅ DateTimeExtractor (15 tests, 91%)
├── test_entity_extraction.py # ✅ Location+Person (18 tests, 99%)
├── test_fsm_specials.py # ✅ FSM special cases (3 tests)
├── test_router.py # ✅ Router (4 tests)
└── test_state_machine.py # ✅ StateMachine (6 tests)

text

**Total Unit Tests: 77 tests**

---

## 🚀 Quick Start

Ejecutar todos los unit tests
pytest src/theaia/tests/unit/ -v

Solo un archivo
pytest src/theaia/tests/unit/test_agent_config.py -v

Con coverage
pytest src/theaia/tests/unit/ --cov=src/theaia/agents --cov-report=html

text

---

## ✅ Tests Implementados

### **🔧 Agent Configuration (15 tests)**
- `test_agent_config.py`: Configuración de agents
  - Create/modify configs
  - Intent management
  - Serialization (to_dict/from_dict)
  - Predefined configs registry
  - **Coverage: 100%**

### **🤖 BaseAgent (15 tests)**
- `test_base_agent.py`: Funcionalidad base de agents
  - Lifecycle (initialize/cleanup)
  - Intent handling
  - Error handling
  - Status reporting
  - **Coverage: 93%**

### **📅 Entity Extraction (48 tests total)**

**DateTimeExtractor (15 tests, 91%)**
- `test_date_parser.py`:
  - Relative dates: "mañana", "hoy", "en 3 días"
  - Weekdays: "lunes", "martes"
  - Time formats: "10:30", "15h"
  - Edge cases & invalid inputs

**LocationExtractor (18 tests, 100%)**
- `test_entity_extraction.py`:
  - Spanish cities (35+ ciudades)
  - Location types: "oficina", "casa"
  - Prepositions: "en", "a", "desde"
  - Accent handling

**PersonNameExtractor (18 tests, 98%)**
- `test_entity_extraction.py`:
  - Common Spanish names (35+ nombres)
  - Titles: "Dr.", "Sr.", "Prof."
  - Preposition patterns
  - Complex sentences

### **🔄 FSM & Router (13 tests)**
- `test_fsm_specials.py`: Casos especiales FSM (3 tests)
- `test_router.py`: Agent routing (4 tests)
- `test_state_machine.py`: State transitions (6 tests)

### **📦 Context (1 test)**
- `test_context_persistence.py`: Context persistence

---

## 💡 Ejemplo de Unit Test

test_agent_config.py
import pytest
from src.theaia.agents.agent_config import AgentConfig

def test_create_config():
"""Test creating agent config."""
config = AgentConfig(
name="TestAgent",
supported_intents=["test"],
requires_database=True
)

text
assert config.name == "TestAgent"
assert "test" in config.supported_intents
assert config.requires_database is True
def test_add_intent():
"""Test adding intent to config."""
config = AgentConfig(name="Test")
config.add_intent("new_intent")

text
assert "new_intent" in config.supported_intents
assert config.supports_intent("new_intent") is True
text

---

## 🎯 Coverage Stats (15 Nov 2025)

| Component | Coverage | Tests | Status |
|-----------|----------|-------|--------|
| AgentConfig | 100% | 15 | ✅ |
| BaseAgent | 93% | 15 | ✅ |
| DateTimeExtractor | 91% | 15 | ✅ |
| LocationExtractor | 100% | 18 | ✅ |
| PersonExtractor | 98% | 18 | ✅ |
| FSM/Router | 85%+ | 13 | ✅ |
| **TOTAL UNIT** | **~92%** | **77** | ✅ |

---

## ✅ Características Unit Test

**✅ Debe ser:**
- Rápido (<1ms idealmente)
- Aislado (sin side effects)
- Determinista (siempre mismo resultado)
- Fácil de entender

**❌ NO debe:**
- Tocar database real
- Hacer network requests
- Depender de otros tests
- Usar sleep() o timers reales

---

## 📚 Convenciones

### Naming
def test_<component><behavior><expected>():
"""Test that <component> <behavior> results in <expected>."""

text

### Estructura AAA
def test_example():
# Arrange
config = AgentConfig(name="Test")

text
# Act
result = config.supports_intent("test")

# Assert
assert result is False
text

### Parametrization
@pytest.mark.parametrize("text,expected", [
("hoy", 0),
("mañana", 1),
("pasado mañana", 2),
])
def test_relative_dates(text, expected):
result = parse_date(text)
assert result.days == expected

text

---

## 🎯 Next Steps

**Priority Unit Tests (Phase 4):**
- [ ] API endpoints unit tests
- [ ] Service layer unit tests
- [ ] Additional FSM states coverage
- [ ] Advanced NER tests

---

**Implementado:** H02 (12-14 Nov), H03 (15-16 Nov)  
**Última actualización:** 15 Nov 2025, 23:55 CET