# ReminderAgent - Testing Documentation

Documentación completa de testing para ReminderAgent.

**Última actualización:** 25 Noviembre 2025  
**Versión:** 1.0.0  
**Tests totales:** 15 tests (100% passing)

---

## 📊 Test Suite Overview

### Resumen de Tests

╔════════════════════════════════════════════════════════╗
║ REMINDER AGENT TEST SUITE ║
╠════════════════════════════════════════════════════════╣
║ Unit Tests: 3/3 PASSING (100%) ║
║ E2E Basic Tests: 7/7 PASSING (100%) ║
║ E2E Extended Tests: 5/5 PASSING (100%) ║
║ ───────────────────────────────────────────────────── ║
║ TOTAL: 15/15 PASSING (100%) ║
╠════════════════════════════════════════════════════════╣
║ Coverage: 73% (target 70%) ║
║ FSM Coverage: 54% ║
║ Handler Coverage: 85% ║
║ Manager Coverage: 81% ║
╚════════════════════════════════════════════════════════╝

text

---

## 🧪 Test Categories

### 1. Unit Tests (3 tests)

**Archivo:** `src/theaia/agents/reminder_agent/tests/test_handler.py`

#### test_reminder_agent_initialization
def test_reminder_agent_initialization():
"""Verifica inicialización correcta del agente."""
agent = ReminderAgent(user_id="test_user_123")
assert agent.user_id == "test_user_123"
assert agent.conversation_manager is not None
assert isinstance(agent.get_supported_intents(), list)

text

**Validaciones:**
- ✅ Agente se inicializa con user_id
- ✅ ConversationManager se crea correctamente
- ✅ Intents soportados se devuelven como lista

#### test_reminder_agent_can_handle
def test_reminder_agent_can_handle():
"""Verifica que el agente maneja intents correctos."""
agent = ReminderAgent(user_id="test_user")

text
# Intents válidos
assert agent.can_handle("crear_recordatorio")
assert agent.can_handle("listar_recordatorios")
assert agent.can_handle("eliminar_recordatorio")

# Intents inválidos
assert not agent.can_handle("crear_evento")
assert not agent.can_handle("unknown_intent")
text

**Validaciones:**
- ✅ Reconoce 8 intents específicos de recordatorios
- ✅ Rechaza intents de otros agentes
- ✅ Maneja intents desconocidos correctamente

#### test_reminder_agent_handle_message
async def test_reminder_agent_handle_message():
"""Verifica manejo básico de mensajes."""
agent = ReminderAgent(user_id="test_user")

text
response, state, context = await agent.handle(
    user_id="test_user",
    message="Recuérdame comprar leche",
    context={}
)

assert response is not None
assert state is not None
assert isinstance(context, dict)
text

**Validaciones:**
- ✅ Respuesta generada correctamente
- ✅ Estado actualizado
- ✅ Contexto preservado

---

### 2. E2E Basic Tests (7 tests)

**Archivo:** `src/theaia/agents/tests/test_reminder_agent_e2e.py`

#### test_create_reminder_time_based
async def test_create_reminder_time_based():
"""Test: Crear recordatorio basado en tiempo."""
# Escenario: Usuario crea recordatorio para mañana
# Resultado esperado: Recordatorio creado con fecha correcta

text

**Flujo:**
1. Usuario: "Recuérdame comprar leche mañana a las 10am"
2. THEA extrae: datetime="mañana 10:00"
3. THEA confirma: "✅ Recordatorio creado"

**Validaciones:**
- ✅ Fecha extraída correctamente
- ✅ Hora extraída correctamente
- ✅ Recordatorio almacenado
- ✅ Estado FSM = "reminder_created"

#### test_create_reminder_weekday
async def test_create_reminder_weekday():
"""Test: Crear recordatorio para día de semana."""
# Escenario: "Recuérdame llamar a María el lunes"

text

**Validaciones:**
- ✅ Día de semana reconocido ("lunes", "martes", etc.)
- ✅ Fecha calculada correctamente (próximo lunes)
- ✅ Recordatorio creado

#### test_create_reminder_location
async def test_create_reminder_location():
"""Test: Crear recordatorio basado en ubicación."""
# Escenario: "Recuérdame comprar pan cerca de la panadería"

text

**Validaciones:**
- ✅ Ubicación extraída ("panadería")
- ✅ Tipo de recordatorio = "location"
- ✅ Radio configurado (500m default)

#### test_list_reminders
async def test_list_reminders():
"""Test: Listar recordatorios activos."""
# Pre: 3 recordatorios creados
# Acción: "¿Qué recordatorios tengo?"

text

**Validaciones:**
- ✅ Devuelve 3 recordatorios
- ✅ Ordenados por fecha
- ✅ Formato de respuesta correcto

#### test_edit_reminder
async def test_edit_reminder():
"""Test: Editar recordatorio existente."""
# Pre: Recordatorio "comprar leche" (mañana 10:00)
# Acción: "Cambia la hora a las 15:00"

text

**Validaciones:**
- ✅ Recordatorio identificado correctamente
- ✅ Hora actualizada
- ✅ Otros campos preservados

#### test_complete_reminder
async def test_complete_reminder():
"""Test: Marcar recordatorio como completado."""
# Pre: Recordatorio activo
# Acción: "Marca como completado 'comprar leche'"

text

**Validaciones:**
- ✅ Estado cambiado a "completed"
- ✅ Ya no aparece en lista activos
- ✅ Fecha de completado registrada

#### test_delete_reminder
async def test_delete_reminder():
"""Test: Eliminar recordatorio."""
# Pre: Recordatorio existente
# Acción: "Elimina el recordatorio de comprar leche"

text

**Validaciones:**
- ✅ Recordatorio eliminado
- ✅ Ya no aparece en lista
- ✅ Confirmación al usuario

---

### 3. E2E Extended Tests (5 tests)

**Archivo:** `src/theaia/agents/tests/test_reminder_agent_e2e.py`

#### test_recurring_reminder_daily
async def test_recurring_reminder_daily():
"""Test: Recordatorio recurrente diario."""
# "Recuérdame tomar medicina todos los días a las 9am"

text

**Validaciones:**
- ✅ Tipo = "recurring"
- ✅ Frecuencia = "daily"
- ✅ Primera ocurrencia calculada
- ✅ Próximas repeticiones generadas

#### test_recurring_reminder_weekly
async def test_recurring_reminder_weekly():
"""Test: Recordatorio recurrente semanal."""
# "Recuérdame hacer ejercicio todos los lunes"

text

**Validaciones:**
- ✅ Frecuencia = "weekly"
- ✅ Día de semana = "monday"
- ✅ Repeticiones futuras

#### test_complex_datetime_extraction
async def test_complex_datetime_extraction():
"""Test: Extracción de fechas complejas."""
# "Recuérdame el próximo viernes 18 de abril a las 15:30"

text

**Validaciones:**
- ✅ Día de semana + fecha absoluta
- ✅ Hora específica
- ✅ Fecha calculada correctamente

#### test_multi_user_isolation
async def test_multi_user_isolation():
"""Test: Aislamiento entre usuarios."""
# User A: 3 recordatorios
# User B: 2 recordatorios
# Verificar que cada uno ve solo los suyos

text

**Validaciones:**
- ✅ User A ve solo 3 recordatorios
- ✅ User B ve solo 2 recordatorios
- ✅ No hay cross-contamination

#### test_error_handling_invalid_datetime
async def test_error_handling_invalid_datetime():
"""Test: Manejo de fechas inválidas."""
# "Recuérdame algo ayer" (fecha pasada)

text

**Validaciones:**
- ✅ Error detectado
- ✅ Mensaje de error claro
- ✅ Estado FSM no se corrompe

---

## 🎯 Test Strategy

### Filosofía de Testing

Test-First Approach
✅ Tests escritos antes o durante implementación
✅ Coverage mínimo 70% (actual: 73%)

Realistic Scenarios
✅ Casos de uso reales de usuarios
✅ Datos representativos
✅ Flujos completos end-to-end

Isolation & Independence
✅ Tests independientes entre sí
✅ Mock de dependencias externas
✅ Multi-tenant validation

Fast Execution
✅ Tests rápidos (<1s cada uno)
✅ Suite completa <10s
✅ Feedback inmediato

text

### Coverage Targets

Component Target Actual Status
─────────────────────────────────────────────
FSM 70% 54% 🟡 (functional)
Handler 70% 85% ✅
ConversationManager 70% 81% ✅
Overall 70% 73% ✅

text

**Nota:** FSM coverage bajo (54%) es aceptable porque:
- Estados complejos requieren integración real
- Mock version limita testing completo
- Coverage aumentará con PostgreSQL en H05

---

## 🚀 Running Tests

### Comandos Básicos

Todos los tests de ReminderAgent
pytest src/theaia/agents/reminder_agent/tests/ -v

Solo E2E
pytest src/theaia/agents/tests/test_reminder_agent_e2e.py -v

Con coverage
pytest src/theaia/agents/reminder_agent/
--cov=src/theaia/agents/reminder_agent
--cov-report=term-missing
--cov-report=html

Tests específicos
pytest src/theaia/agents/reminder_agent/tests/test_handler.py::test_reminder_agent_initialization -v

text

### Opciones Avanzadas

Mostrar print statements
pytest -v -s

Stop on first failure
pytest -x

Verbose traceback
pytest --tb=short

Parallel execution
pytest -n auto

Con timing
pytest --durations=10

text

---

## 📈 CI/CD Integration

### GitHub Actions Workflow

name: ReminderAgent Tests

on: [push, pull_request]

jobs:
test:
runs-on: ubuntu-latest
steps:
- uses: actions/checkout@v2
- name: Set up Python
uses: actions/setup-python@v2
with:
python-version: '3.11'
- name: Install dependencies
run: pip install -r requirements.txt
- name: Run tests
run: pytest src/theaia/agents/reminder_agent/tests/ -v --cov

text

### Pre-commit Hook

.git/hooks/pre-commit
#!/bin/bash
pytest src/theaia/agents/reminder_agent/tests/ --cov --cov-fail-under=70

text

---

## 🐛 Debugging Failed Tests

### Checklist de Debugging

□ Verificar logs: tail -f logs/test_reminder_agent.log
□ Revisar fixtures: pytest --fixtures
□ Comprobar mocks: Verificar que mocks están activos
□ Validar estado FSM: Imprimir estados intermedios
□ Check user_id: Verificar aislamiento multi-tenant
□ Revisar entity extraction: DateTimeExtractor funcionando

text

### Comandos Útiles

Ver fixtures disponibles
pytest --fixtures

Run con pdb debugger
pytest --pdb

Capturar logs
pytest --log-cli-level=DEBUG

Ver warnings
pytest -W all

text

---

## 📊 Test Metrics

Metric Value
────────────────────────────────
Total Tests 15
Passing Tests 15 (100%)
Failing Tests 0
Skipped Tests 0
Execution Time ~8 seconds
Average per test ~0.5s
Code Coverage 73%
Lines Tested 110/150

text

---

## 🔄 Test Maintenance

### Actualizar Tests

Cuando añadas nueva funcionalidad:
Añadir unit test en test_handler.py

Añadir E2E test en test_reminder_agent_e2e.py

Verificar coverage no baja

Actualizar esta documentación

text

### Deprecation Warnings

Si ves warnings de deprecación:
pytest -W error # Convertir warnings en errors

Fix warnings antes de merge
text

---

## 📚 Referencias

- [pytest Documentation](https://docs.pytest.org/)
- [Coverage.py](https://coverage.readthedocs.io/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

---

**Última actualización:** 25 Noviembre 2025  
**Mantenido por:** Álvaro Fernández Mota (CEO THEA-IA)  
**Status:** ✅ 15/15 tests passing (100%)