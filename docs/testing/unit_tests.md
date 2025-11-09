📝 Unit Tests Guide — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: QA Team
Estado: ✅ Activo

📋 Propósito
Guía completa para escribir, ejecutar y mantener tests unitarios en THEA IA. Los tests unitarios validan que cada componente funciona correctamente en aislamiento.

Audiencia:

Desarrolladores escribiendo tests para sus módulos

QA validando cobertura unitaria

Revisores en PR verificando calidad

🎯 Qué es un test unitario
Un test unitario:

Prueba una función/clase/método específico

Usa mocks para aislar dependencias externas

Es rápido (milisegundos)

Es determinista (siempre mismo resultado)

Tiene una única razón de fallar

📂 Estructura y ubicación
Localización
text
src/theaia/tests/unit/
├── test_core_fsm.py           # Tests del FSM engine
├── test_core_managers.py       # Tests de managers (Context, Event, etc.)
├── test_agents_agenda.py       # Tests agente Agenda
├── test_agents_note.py         # Tests agente Notes
├── test_agents_event.py        # Tests agente Events
├── test_agents_query.py        # Tests agente Query
├── test_adapters_telegram.py   # Tests adapter Telegram
├── test_adapters_rest.py       # Tests adapter REST API
└── ...
Naming conventions
Archivos:

text
test_[modulo]_[submodulo].py
Ejemplos:

test_core_fsm.py (módulo: core, submódulo: fsm)

test_agents_agenda.py (módulo: agents, submódulo: agenda)

Funciones de test:

text
def test_[component]_[scenario]_[expected_result]():
Ejemplos:

python
def test_fsm_transition_valid_state_succeeds():
    ...

def test_fsm_transition_invalid_state_raises_error():
    ...

def test_agenda_agent_create_event_with_valid_data():
    ...

def test_agenda_agent_create_event_missing_title_raises_error():
    ...
🛠️ Herramientas y frameworks
Pytest
Runner: Ejecuta todos los tests automáticamente

Fixtures: Datos compartidos entre tests

Parametrize: Ejecutar el mismo test con diferentes inputs

Marks: Categorizar tests (@pytest.mark.unit, .smoke, .slow)

unittest.mock
Mock: Objeto fake que simula comportamiento

patch: Reemplazar función/clase durante el test

MagicMock: Mock con comportamiento inteligente

Faker
Generar datos sintéticos aleatorios

Emails, nombres, números, fechas, etc.

📝 Estructura básica de un test
python
import pytest
from unittest.mock import Mock, patch, MagicMock
from src.theaia.core.fsm import FSMEngine
from src.theaia.agents.agenda import AgendaAgent

# 1. SETUP (Prepare - Arranque)
@pytest.fixture
def fsm_engine():
    """Fixture que proporciona un FSM listo para test"""
    engine = FSMEngine()
    engine.initialize_states(['idle', 'processing', 'complete'])
    return engine

# 2. TEST (Act - Ejecutar, Assert - Verificar)
def test_fsm_transition_valid_state_succeeds(fsm_engine):
    """Test: Transición a estado válido debe tener éxito"""
    
    # Arrange (ya hecho por fixture)
    fsm_engine.current_state = 'idle'
    
    # Act
    fsm_engine.transition('processing')
    
    # Assert
    assert fsm_engine.current_state == 'processing'
    assert fsm_engine.history[-1] == 'processing'
🔍 Patrones comunes
Patrón 1: Aislar con Mocks
python
def test_agenda_agent_calls_calendar_api():
    """Agenda debe llamar a calendar API"""
    
    # Mock de dependencia externa
    with patch('src.theaia.agents.agenda.calendar_api') as mock_api:
        mock_api.create_event.return_value = {'event_id': '123'}
        
        # Test del agente
        agent = AgendaAgent()
        result = agent.create_event('Reunión', '2025-11-08 10:00')
        
        # Verificar que se llamó correctamente
        mock_api.create_event.assert_called_once()
        assert result['event_id'] == '123'
Patrón 2: Parametrizar múltiples casos
python
@pytest.mark.parametrize("input,expected", [
    ("2025-11-08", True),      # Fecha válida
    ("2025-13-32", False),     # Mes inválido
    ("invalid", False),        # Formato inválido
    ("", False),               # Vacío
])
def test_date_validation(input, expected):
    """Validar fechas con múltiples casos"""
    assert validate_date(input) == expected
Patrón 3: Excepciones esperadas
python
def test_fsm_transition_invalid_state_raises_error():
    """Transición a estado inválido debe lanzar error"""
    
    engine = FSMEngine()
    engine.current_state = 'idle'
    
    with pytest.raises(ValueError, match="Invalid state"):
        engine.transition('nonexistent_state')
Patrón 4: Test asíncronos
python
@pytest.mark.asyncio
async def test_agenda_async_create_event():
    """Test de función async"""
    
    agent = AgendaAgent()
    result = await agent.create_event_async('Reunión', '2025-11-08 10:00')
    
    assert result.status == 'created'
    assert result.event_id is not None
🚀 Comandos de ejecución
Tests unitarios solamente
bash
pytest src/theaia/tests/unit/ -v
Tests de un archivo específico
bash
pytest src/theaia/tests/unit/test_core_fsm.py -v
Tests de una función específica
bash
pytest src/theaia/tests/unit/test_core_fsm.py::test_fsm_transition_valid_state_succeeds -v
Tests con palabra clave
bash
pytest src/theaia/tests/unit/ -k "fsm" -v  # Solo tests que contengan "fsm"
Tests con salida detallada
bash
pytest src/theaia/tests/unit/ -vv --tb=long
Tests con stoppage al primer error
bash
pytest src/theaia/tests/unit/ -x
📊 Cobertura de unit tests
Medir cobertura
bash
pytest src/theaia/tests/unit/ --cov=src/theaia.core --cov-report=html
Target de cobertura unitaria
Módulo	Target	Actual
core/fsm	95%	🟡 92%
core/managers	90%	🟡 88%
agents/	85%	🟡 80%
adapters/	80%	🟡 75%
Total unit	90%	🟡 85%
✅ Checklist para escribir buenos tests unitarios
 El test tiene un nombre descriptivo (qué, cuándo, qué espera)

 El test prueba UNA cosa (una razón de fallar)

 El test usa fixtures para setup reutilizable

 Las dependencias externas están mockeadas/patched

 El test es determinista (siempre mismo resultado)

 El test es rápido (< 100ms)

 Hay al menos un caso de éxito y uno de error

 La cobertura >= 85% en el módulo

 El test documenta el comportamiento esperado

 La PR actualiza este documento si agrega nuevos patterns

🔗 Referencias y enlaces
Testing Overview — Estrategia general de testing

Integration Tests — Tests de integración

E2E Tests — Tests end-to-end

Coverage Report — Análisis de cobertura

CI/CD Pipeline — Ejecución automática

Audit Checklist — Auditoría de calidad

📌 Meta-información
Campo	Valor
Archivo	docs/testing/unit_tests.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	QA Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.2 (docs/testing/)

Sigue estándar THEA IA: Modular, auditable, escalable

Cambios deben reflejarse en CHANGELOG

Validado en sesión 35

Nota: Cualquier cambio significativo en patrones o herramientas debe documentarse aquí y reflejarse en el roadmap.

actuizado 8/11/25 a las 16.55
