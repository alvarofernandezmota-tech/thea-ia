🔗 Integration Tests Guide — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: QA Team
Estado: ✅ Activo

📋 Propósito
Guía completa para escribir, ejecutar y mantener tests de integración en THEA IA. Los tests de integración validan que múltiples módulos funcionan correctamente juntos.

Audiencia:

Desarrolladores testando interacción entre módulos

QA validando flujos cruzados

Revisores en PR verificando integración

🎯 Qué es un test de integración
Un test de integración:

Prueba interacción entre 2+ componentes/módulos

Usa mocks selectivos (mocka solo partes externas críticas)

Es medianamente rápido (cientos de milisegundos)

Valida contrato entre módulos

Tiene una sola razón clara de fallar

Diferencia unitarios vs integración
Aspecto	Unit	Integration
Scope	1 función/clase	2+ módulos
Mocks	Todos externos	Solo críticos
Velocidad	ms	100-500ms
Enfoque	Lógica individual	Comunicación
📂 Estructura y ubicación
Localización
text
src/theaia/tests/integration/
├── test_fsm_agents_flow.py          # FSM + Agents integración
├── test_adapters_integration.py     # Adapters + Core
├── test_agents_coordination.py      # Multi-agentes
├── test_context_managers_flow.py    # Context + Event managers
├── test_telegram_event_flow.py      # Telegram adapter + FSM + Agents
├── test_rest_api_integration.py     # REST API + Core + Adapters
└── ...
Naming conventions
Archivos:

text
test_[componente1]_[componente2]_[flujo].py
Ejemplos:

test_fsm_agents_flow.py (FSM + Agents)

test_telegram_event_flow.py (Telegram + FSM + Event)

Funciones de test:

text
def test_[comp1]_[comp2]_[flujo]_[resultado]():
Ejemplos:

python
def test_fsm_agents_state_transition_triggers_agent_workflow():
    ...

def test_telegram_adapter_receives_message_triggers_fsm():
    ...

def test_multi_agents_coordinate_for_complex_event():
    ...
🛠️ Herramientas específicas para integración
httpx + respx (para APIs HTTP)
python
import respx
import httpx

# Mock de llamadas HTTP
@respx.mock
def test_rest_api_call():
    respx.get("https://api.example.com/users").mock(
        return_value=httpx.Response(200, json={"users": []})
    )
    # Test aquí
AsyncMock (para código async)
python
from unittest.mock import AsyncMock

mock_async = AsyncMock(return_value="resultado")
result = await mock_async()
Testcontainers (opcional - para BD real en tests)
python
from testcontainers.postgres import PostgresContainer

with PostgresContainer() as postgres:
    # Tests con DB real durante test
    db = connect(postgres.get_connection_url())
📝 Estructura básica de un test de integración
python
import pytest
from unittest.mock import patch, AsyncMock
from src.theaia.core.fsm import FSMEngine
from src.theaia.agents.agenda import AgendaAgent
from src.theaia.adapters.telegram import TelegramAdapter

@pytest.fixture
def fsm_with_agent():
    """FSM + Agent integrado"""
    fsm = FSMEngine()
    agent = AgendaAgent()
    fsm.register_agent('agenda', agent)
    return fsm, agent

@pytest.fixture
def telegram_adapter():
    """Adapter Telegram"""
    return TelegramAdapter(token="test_token")

# TEST: Flujo completo
def test_telegram_message_triggers_fsm_and_agent(fsm_with_agent, telegram_adapter):
    """
    Flujo: Telegram recibe mensaje → FSM procesa → Agent actúa
    """
    fsm, agent = fsm_with_agent
    
    # Arrange
    fsm.current_state = 'idle'
    message = "Crear evento: Reunión mañana 10:00"
    
    # Act
    fsm.transition('processing')
    events = fsm.process_input(message)
    
    # Assert
    assert fsm.current_state == 'processing'
    assert len(events) > 0
    assert events.agent == 'agenda'
    assert 'Reunión' in events.data
🔍 Patrones comunes en integración
Patrón 1: Mock solo de dependencias externas
python
def test_fsm_agents_flow_with_external_api():
    """Mock solo API externa, resto real"""
    
    with patch('src.theaia.adapters.calendar_api.requests.get') as mock_api:
        mock_api.return_value.json.return_value = {'status': 'ok'}
        
        # FSM + Agent interactúan realmente
        fsm = FSMEngine()
        agent = AgendaAgent()
        fsm.register_agent('agenda', agent)
        
        # Test
        result = fsm.process('create_event', {'title': 'Test'})
        
        assert result.success
        mock_api.assert_called_once()
Patrón 2: Multi-módulos coordinados
python
def test_multi_agents_coordinate():
    """Múltiples agentes coordinándose"""
    
    fsm = FSMEngine()
    agenda = AgendaAgent()
    note = NoteAgent()
    query = QueryAgent()
    
    fsm.register_agent('agenda', agenda)
    fsm.register_agent('note', note)
    fsm.register_agent('query', query)
    
    # Complejo: Query → Agenda → Note
    fsm.transition('processing')
    result = fsm.process('complex_task', {
        'query': 'eventos de mañana',
        'action': 'crear nota'
    })
    
    assert result.involved_agents == ['query', 'agenda', 'note']
Patrón 3: Flujo async entre componentes
python
@pytest.mark.asyncio
async def test_async_adapter_fsm_flow():
    """Adapter async + FSM"""
    
    adapter = TelegramAdapter(token="test")
    fsm = FSMEngine()
    
    # Mock solo Telegram API
    with patch.object(adapter, 'send_message', new_callable=AsyncMock):
        result = await adapter.process_message_async("Crear evento")
        
        assert result.processed
        adapter.send_message.assert_called()
Patrón 4: Validar contrato entre módulos
python
def test_adapter_fsm_contract():
    """FSM y Adapter respetan contrato"""
    
    adapter = TelegramAdapter()
    fsm = FSMEngine()
    
    # Contrato: Adapter llama FSM.process con específico formato
    input_data = adapter.parse_message("texto")
    output = fsm.process(input_data)
    
    # Validaciones de contrato
    assert 'event_id' in output  # FSM siempre retorna event_id
    assert isinstance(output['data'], dict)
    assert 'timestamp' in output
🚀 Comandos de ejecución
Tests de integración solamente
bash
pytest src/theaia/tests/integration/ -v
Tests de un archivo específico
bash
pytest src/theaia/tests/integration/test_fsm_agents_flow.py -v
Tests de integración + coverage
bash
pytest src/theaia/tests/integration/ --cov=src/theaia --cov-report=html
Tests lentos (e2e integraciones complejas)
bash
pytest src/theaia/tests/integration/ -m "slow" -v
Parar en primer error
bash
pytest src/theaia/tests/integration/ -x -v
📊 Cobertura de integración
Target de cobertura de integración
Flujo	Target	Actual
FSM ↔ Agents	85%	🟡 80%
Adapters ↔ FSM	80%	🟡 75%
Multi-agents	75%	⏳ 70%
Total integration	80%	🟡 75%
✅ Checklist para tests de integración
 El test prueba 2+ módulos interactuando

 Solo APIs externas críticas están mockeadas

 El test es determinista (mismo resultado siempre)

 El test documenta el flujo/contrato esperado

 Hay casos de éxito y error/edge

 Usan fixtures compartidos de ambos módulos

 No son excesivamente lentos (< 500ms)

 El naming es descriptivo del flujo

 Verifican eventos/cambios de estado entre módulos

 La cobertura >= 75% en módulos involucrados

🚨 Errores comunes en tests de integración
❌ NO hacer:

Mockear todo (entonces no es integración)

Tests que dependen uno del otro (siempre aislados)

Tests lentos sin razón (optimizar queries, fixtures)

Casos de éxito solamente (incluir errores)

✅ SÍ hacer:

Mock solo de dependencias externas críticas

Tests independientes y aislados

Documentación del flujo siendo testeado

Mix de casos success/error/edge

🔗 Referencias y enlaces
Testing Overview — Estrategia general

Unit Tests — Tests unitarios

E2E Tests — Tests end-to-end

Coverage Report — Análisis de cobertura

CI/CD Pipeline — Ejecución automática

Audit Checklist — Auditoría de calidad

📌 Meta-información
Campo	Valor
Archivo	docs/testing/integration_tests.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	QA Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.2 (docs/testing/)

Sigue estándar THEA IA: Modular, auditable, escalable

Cambios deben reflejarse en CHANGELOG

Validado en sesión 35

Nota: Cualquier nuevo patrón de integración debe documentarse aquí y comunicarse al equipo.