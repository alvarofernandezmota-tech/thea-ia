🎬 E2E Tests Guide — THEA IA
Versión: 1.0
Última actualización: 2025-11-08 (Sesión 35)
Responsable: QA Team
Estado: ✅ Activo

📋 Propósito
Guía completa para escribir, ejecutar y mantener tests end-to-end (E2E) en THEA IA. Los tests E2E validan flujos completos del usuario desde entrada hasta salida, sin mocks excepto APIs externas críticas.

Audiencia:

QA/Testers validando flujos de usuario

Desarrolladores verificando casos de uso

Auditores validando experiencia global

🎯 Qué es un test E2E
Un test E2E:

Prueba flujo completo de usuario de inicio a fin

Usa 0 mocks internos (todo real excepto APIs externas)

Es lento (segundos a minutos)

Valida experiencia del usuario real

Tiene múltiples razones potenciales de fallar

Pirámide de tests THEA IA
text
        🎬 E2E (5-10%)
         Lentos, raros
       ┌──────────────┐
       │  End-to-End  │
       │  (5-10%)     │
       └──────────────┘
           ↑ ↑ ↑
       🔗 Integration (20-30%)
         Medianos, más frecuentes
       ┌──────────────┐
       │ Integration  │
       │ (20-30%)     │
       └──────────────┘
           ↑ ↑ ↑
       📝 Unit (60-75%)
         Rápidos, frecuentes
       ┌──────────────┐
       │    Unit      │
       │  (60-75%)    │
       └──────────────┘
📂 Estructura y ubicación
Localización
text
src/theaia/tests/e2e/
├── test_telegram_user_flow.py          # Usuario Telegram completo
├── test_agenda_create_modify_flow.py    # Crear/modificar evento
├── test_note_search_flow.py             # Buscar y crear notas
├── test_multi_agent_complex_task.py     # Tarea compleja multi-agente
├── test_rest_api_user_flow.py           # REST API flujo completo
├── test_error_recovery_flow.py          # Manejo de errores/recuperación
└── conftest.py                          # Fixtures E2E compartidos
Naming conventions
Archivos:

text
test_[feature]_[user_action]_flow.py
Ejemplos:

test_telegram_user_flow.py (Usuario Telegram)

test_agenda_create_modify_flow.py (Crear y modificar evento)

Funciones de test:

text
def test_[feature]_[scenario]_[expected_outcome]():
Ejemplos:

python
def test_agenda_user_creates_event_via_telegram_successfully():
    ...

def test_user_creates_event_then_modifies_title():
    ...

def test_user_complex_task_with_multiple_agents():
    ...
🛠️ Herramientas E2E
pytest-asyncio
Tests de flujos async completos

Manejo de eventos asincronos

pytest-timeout
bash
pip install pytest-timeout
Evitar tests que se cuelguen

@pytest.mark.timeout(60) para timeout de 60s

pytest-xdist (opcional - paralelización)
bash
pip install pytest-xdist
pytest -n auto  # Usa todos los cores
Selenum/Playwright (opcional - UI testing)
Si tienes interfaz web/UI

pip install playwright

📝 Estructura básica de un test E2E
python
import pytest
import asyncio
from src.theaia.adapters.telegram import TelegramAdapter
from src.theaia.core.fsm import FSMEngine
from src.theaia.agents.agenda import AgendaAgent

@pytest.fixture
async def full_system():
    """Sistema completo THEA IA listo"""
    fsm = FSMEngine()
    telegram = TelegramAdapter(token="test_token")
    
    agents = {
        'agenda': AgendaAgent(),
        'note': NoteAgent(),
        'query': QueryAgent(),
    }
    
    for name, agent in agents.items():
        fsm.register_agent(name, agent)
    
    await fsm.initialize()
    
    yield fsm, telegram, agents
    
    await fsm.shutdown()

@pytest.mark.asyncio
@pytest.mark.timeout(30)
async def test_telegram_user_creates_event_flow(full_system):
    """
    E2E: Usuario crea evento vía Telegram
    
    Flujo:
    1. Usuario envía mensaje a Telegram
    2. Adapter procesa mensaje
    3. FSM procesa con agentes
    4. Evento se crea
    5. Usuario recibe confirmación
    """
    fsm, telegram, agents = full_system
    
    # Arrange: Preparar mensaje de usuario
    user_message = "Crear evento: Reunión mañana 10:00"
    
    # Act: Usuario envía mensaje
    result = await telegram.process_message_async(
        chat_id="123456",
        message_text=user_message
    )
    
    # Assert: Validar flujo completo
    assert result.success
    assert result.event_id is not None
    
    # Verificar que evento fue creado realmente
    event = agents['agenda'].get_event(result.event_id)
    assert event.title == "Reunión"
    assert event.datetime == "2025-11-09 10:00"
    
    # Verificar respuesta al usuario
    response = result.user_message
    assert "Evento creado" in response
    assert "Reunión" in response
🔍 Patrones comunes E2E
Patrón 1: Flujo lineal simple
python
@pytest.mark.asyncio
async def test_create_note_via_telegram():
    """Paso 1 → Paso 2 → Paso 3 → Validar resultado"""
    
    adapter = TelegramAdapter()
    
    # 1. Usuario envía comando
    msg1 = await adapter.send_message("nueva nota")
    assert "¿Título?" in msg1
    
    # 2. Usuario responde
    msg2 = await adapter.send_message("Mi nota importante")
    assert "¿Contenido?" in msg2
    
    # 3. Usuario confirma
    msg3 = await adapter.send_message("Contenido de la nota")
    assert "Nota creada" in msg3
    
    # Validar que nota existe en sistema
    notes = adapter.get_user_notes("123456")
    assert len(notes) == 1
    assert notes.title == "Mi nota importante"
Patrón 2: Rama condicional (success/error)
python
@pytest.mark.asyncio
@pytest.mark.parametrize("user_input,expected_result", [
    ("crear evento mañana 10am", "success"),
    ("crear evento en fecha inválida", "error"),
    ("crear evento sin hora", "ask_clarification"),
])
async def test_event_creation_branches(user_input, expected_result):
    """Validar diferentes ramas del flujo"""
    
    adapter = TelegramAdapter()
    result = await adapter.process_message_async(user_input)
    
    assert result.status == expected_result
Patrón 3: Flujo multi-paso con estado
python
@pytest.mark.asyncio
async def test_complex_task_with_multiple_agents():
    """Usuario ejecuta tarea compleja que involucra múltiples agentes"""
    
    fsm = FSMEngine()
    adapter = TelegramAdapter()
    
    # Tarea: "Crea evento mañana y guarda nota sobre asuntos a tratar"
    user_input = (
        "Reunión con equipo mañana 10am. "
        "Asuntos: presupuesto, roadmap Q2, validación testing"
    )
    
    # Procesar
    result = await adapter.process_message_async(user_input)
    
    # Validar que múltiples acciones sucedieron
    assert result.event_created
    assert result.note_created
    
    # Validar estado final
    event = result.event
    note = result.note
    
    assert "reunión" in event.title.lower()
    assert "presupuesto" in note.content
    assert event.datetime == "2025-11-09 10:00"
Patrón 4: Recuperación de errores
python
@pytest.mark.asyncio
async def test_system_recovers_from_api_error():
    """Sistema se recupera cuando API externa falla"""
    
    adapter = TelegramAdapter()
    
    # 1. API falla
    with patch.object(adapter, 'calendar_api', side_effect=ConnectionError):
        result = await adapter.send_message("crear evento")
        assert result.status == "error"
        assert "intente nuevamente" in result.message
    
    # 2. API se recupera
    with patch.object(adapter, 'calendar_api', return_value={'status': 'ok'}):
        result = await adapter.send_message("crear evento")
        assert result.status == "success"
🚀 Comandos de ejecución
Tests E2E solamente
bash
pytest src/theaia/tests/e2e/ -v --tb=short
Tests E2E con timeout
bash
pytest src/theaia/tests/e2e/ -v --timeout=60
Tests E2E específicos
bash
pytest src/theaia/tests/e2e/test_telegram_user_flow.py -v
Tests E2E en paralelo (si usa pytest-xdist)
bash
pytest src/theaia/tests/e2e/ -n auto
Tests E2E con cobertura
bash
pytest src/theaia/tests/e2e/ --cov=src/theaia --cov-report=html
📊 Cobertura E2E
Target de cobertura E2E
Flujo	Target	Actual
Telegram user flow	70%	🟡 65%
Agenda complex task	65%	⏳ 60%
Multi-agent task	60%	⏳ 50%
Total E2E	70%	🟡 60%
Nota sobre cobertura E2E
Los E2E tienen menor % de cobertura porque son flujos, no exhaustivos

Enfoque: Flujos críticos de usuario, no código

El resto está cubierto por unit + integration

✅ Checklist para tests E2E
 El test simula un flujo de usuario real

 Sin mocks internos (solo APIs externas críticas)

 El test tiene un nombre que describe la acción de usuario

 Hay validaciones en múltiples pasos del flujo

 El test es repetible (puede correr múltiples veces)

 Tiene timeout configurado (evitar cuelgues)

 Documenta el flujo esperado en docstring

 Incluye casos de error cuando aplica

 No depende de estado de test anterior

 Usa fixtures compartidos para setup común

🚨 Errores comunes en E2E
❌ NO hacer:

Mockear todo (entonces no es E2E)

Tests que dependen orden de ejecución

Tests demasiado largos o complejos

Sin timeout (tests que se cuelgan)

Sin validar estado intermedio

Tests "felices" solamente

✅ SÍ hacer:

Flujos reales del usuario

Tests aislados e independientes

Claros, enfocados en un escenario

Timeout + logs detallados

Validaciones en pasos clave

Mix success/error/edge cases

🔗 Referencias y enlaces
Testing Overview — Estrategia general

Unit Tests — Tests unitarios

Integration Tests — Tests de integración

Coverage Report — Análisis de cobertura

CI/CD Pipeline — Ejecución automática

Audit Checklist — Auditoría de calidad

📌 Meta-información
Campo	Valor
Archivo	docs/testing/e2e_tests.md
Versión	1.0
Última revisión	2025-11-08 (Sesión 35)
Responsable	QA Team
Estado	✅ Activo
🛡️ Auditoría y cumplimiento
Parte del Hito 35.1.2 (docs/testing/)

Sigue estándar THEA IA: Modular, auditable, escalable

Cambios deben reflejarse en CHANGELOG

Validado en sesión 35

Nota: Cualquier nuevo flujo E2E crítico debe documentarse como escenario aquí.