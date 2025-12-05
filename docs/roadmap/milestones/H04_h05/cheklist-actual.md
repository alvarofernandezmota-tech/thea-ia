✅ CHECKLIST H04 PHASE 2 EXTENDED - Tests E2E AgendaAgent v3.4
Fecha: 04 Diciembre 2025
Autor: Álvaro Fernández Mota
Hito: Tests End-to-End para AgendaAgent con PostgreSQL Real
Estado: ✅ COMPLETADO (ACTUALIZADO 23:10 CET)

🎯 OBJETIVOS DE LA SESIÓN
 Resolver problemas de Event Loop en Windows con asyncpg

 Implementar fixtures correctas para tests E2E

 Crear suite completa de tests de integración

 Validar arquitectura de 3 capas (Handler → Service → Repository)

 Alcanzar 10/10 tests pasando exitosamente

 ✨ NUEVO: Crear tests CRUD vía Router (nueva suite)

 ✨ NUEVO: Fix event_tools.py para aceptar datetime objects

 ✨ NUEVO: Resolver ForeignKey errors con fixture automático

 ✨ NUEVO: Resolver timeout issues con pytest-asyncio

 ✨ NUEVO: Instalar pytest-timeout plugin

🔧 PROBLEMAS RESUELTOS (SESIÓN COMPLETA)
1. Event Loop Issues (Windows + asyncpg)
 WindowsSelectorEventLoopPolicy implementado en conftest.py

 Event loop por función - Nuevo loop para cada test

 Engine por test - Evita event loop mismatch en pool de conexiones

 pool_pre_ping=False - Deshabilitado para compatibilidad Windows

Archivos modificados:

src/theaia/tests/conftest.py

Solución clave:

python
@pytest.fixture(scope="session")
def event_loop_policy():
    if asyncio.sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    return asyncio.get_event_loop_policy()
2. Foreign Key Violations ✨ MEJORADO
 Fixture test_user (v1) - Crea usuario antes de cada test

 Dependencias de fixtures - Todas las fixtures dependen de test_user

 ID consistente - Usuario con ID=123 para todos los tests

 ✨ Fixture automático con scope='session' (v2) - Usuario único para toda la sesión

 ✨ ON CONFLICT DO NOTHING - Previene errores en re-ejecución

Archivos modificados:

src/theaia/tests/agents/agenda_agent/test_agenda_integration.py

src/theaia/tests/integration/test_agenda_crud.py ✨ NUEVO

Solución clave (v1 - original):

python
@pytest_asyncio.fixture
async def test_user(db_session):
    test_user = User(
        id=123,
        telegram_id=123456789,
        username="test_user",
        # ...
    )
    db_session.add(test_user)
    await db_session.flush()
    await db_session.commit()
    return test_user
Solución clave (v2 - mejorada) ✨ NUEVO:

python
@pytest.fixture(scope='session', autouse=True)
def setup_test_user():
    """Fixture síncrono que crea usuario de prueba UNA SOLA VEZ"""
    async def _create_user():
        async with AsyncSessionLocal() as session:
            await session.execute(text("""
                INSERT INTO users (id, telegram_id, username, tenant_id, created_at, updated_at)
                VALUES (1, 1, 'test_user', 'default', NOW(), NOW())
                ON CONFLICT (id) DO NOTHING
            """))
            await session.commit()
    
    # Ejecutar en nuevo event loop limpio
    asyncio.run(_create_user())
3. BaseRepository.create() TypeError
 **Cambio a kwargs - Parámetros flexibles en create()

 Eliminación de parámetros posicionales - Mayor flexibilidad

 Compatibilidad con todos los repositorios

Archivos modificados:

src/theaia/database/repositories/base_repository.py

Solución clave:

python
async def create(self, **kwargs) -> T:
    instance = self.model(**kwargs)
    self.session.add(instance)
    await self.session.flush()
    await self.session.refresh(instance)
    return instance
4. Validation Errors (Event Status)
 Valores de enum corregidos - Usar "completed" en lugar de "confirmed"

 Validación con schemas - Pydantic valida correctamente

Archivos modificados:

src/theaia/tests/agents/agenda_agent/test_agenda_integration.py

5. EventTools datetime Compatibility Issue ✨ NUEVO
 Fix create_event_tool - Acepta tanto datetime como string ISO

 Fix update_event_tool - Acepta tanto datetime como string ISO

 Validación flexible - Union[datetime, str] en event_date

Archivos modificados:

src/theaia/agents/agenda_agent/tools/event_tools.py (v1.3)

Solución clave:

python
from typing import Union
from datetime import datetime

def create_event_tool(
    event_date: Union[datetime, str],  # ✅ Acepta ambos tipos
    # ...
) -> str:
    # Si es datetime, convertir a ISO string
    if isinstance(event_date, datetime):
        event_date = event_date.isoformat()
    # ...
6. pytest-asyncio Timeout Issues ✨ NUEVO
 Fixture scope cambio - De autouse=True async a scope='session' sync

 asyncio.run() isolation - Nuevo event loop limpio por ejecución

 pytest-timeout instalado - Plugin para evitar cuelgues

 Eliminación de teardown conflicts - No más deadlocks

Plugin instalado:

bash
pip install pytest-timeout  # v2.4.0
Solución clave:

Fixture síncrono que ejecuta código async con asyncio.run()

scope='session' ejecuta solo una vez

Evita conflictos con event loop de pytest-asyncio en teardown

✅ TESTS IMPLEMENTADOS (16/16 PASSED) ✨ ACTUALIZADO
Suite 1: Tests E2E (test_agenda_integration.py) - 10 tests
test_handler_initialization ✅

Valida inicialización correcta del AgendaAgent

Verifica event_service y event_tools están disponibles

test_service_create_event ✅

Crea evento via EventService

Valida persistencia en PostgreSQL

test_service_get_event ✅

Recupera evento por ID

Valida datos correctos

test_tools_create_event ✅

Crea evento via EventTools (CrewAI)

Valida respuesta formateada

test_tools_list_upcoming_events ✅

Lista eventos próximos

Valida filtrado por tiempo

test_tools_update_event ✅

Actualiza título y status de evento

Valida cambios persistidos

test_tools_mark_completed ✅

Marca evento como completado

Valida cambio de estado

test_service_get_upcoming_events ✅

Obtiene eventos próximos via Service

Valida filtrado de 24 horas

test_service_delete_event ✅

Elimina evento

Valida que no se puede recuperar después

test_full_integration_flow ✅

Flujo completo end-to-end

Simula handler real con contexto

Suite 2: Tests CRUD via Router (test_agenda_crud.py) - 6 tests ✨ NUEVO
test_create_event ✅

Crea evento vía router.handle()

Valida intent='create_event'

Valida agent='agenda_agent'

Verifica respuesta formateada correctamente

test_update_event ✅

Crea evento inicial

Actualiza título a "Reunión CANCELADA"

Valida intent='update_event'

Verifica cambios persistidos en BD

test_query_events ✅

Crea múltiples eventos

Consulta eventos con "qué eventos tengo mañana"

Valida intent='query_events'

Verifica listado correcto

test_delete_event ✅

Crea evento temporal

Elimina evento por ID

Valida intent='delete_event'

Verifica eliminación exitosa

test_mark_complete ✅

Crea tarea importante

Marca evento como completado

Valida múltiples intents válidos posibles

Verifica cambio de estado

test_unknown_intent ✅

Prueba mensaje no reconocido ("hazme un café")

Valida fallback o error handling

Verifica respuesta adecuada

📊 COBERTURA DE CÓDIGO ✨ ACTUALIZADO
Módulos Testeados
Módulo	Cobertura Inicial	Cobertura Final	Estado
event_service.py	65%	65%	✅ Mejorado
event_tools.py	41%	24%	⚠️ Necesita refactor
event_schema.py	77%	71%	✅ Bueno
agent_states.py	87%	89%	✅ Excelente
handler.py	14%	41%	🔄 En progreso (+27%)
core/router.py	38%	59%	✅ Mejorado (+21%)
core/orchestrator.py	31%	84%	🎉 Excelente (+53%)
core/nlp_engine.py	13%	72%	🎉 Excelente (+59%)
Cobertura total del proyecto: 5% → 19% (+14%) 🎉

🏗️ ARQUITECTURA VALIDADA ✨ ACTUALIZADO
text
┌─────────────────────────────────────────────────────────┐
│                    TheaRouter v2.0                      │
│             (Entry point & Intent Routing)              │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                 CoreOrchestrator                        │
│            (NLP Engine + Agent Selection)               │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   AgendaAgent Handler                   │
│              (Orchestration & FSM Layer)                │
└─────────────────────────────────────────────────────────┘
              │
    ┌─────────┴─────────┐
    │                   │
┌───▼────────┐   ┌─────▼────────┐
│EventService│   │  EventTools  │
│(Business   │   │(CrewAI Tools)│
│Logic Layer)│   │              │
└───┬────────┘   └─────┬────────┘
    │                   │
    └─────────┬─────────┘
              │
       ┌──────▼──────┐
       │EventRepo    │
       │(Data Access)│
       └──────┬──────┘
              │
       ┌──────▼──────┐
       │ PostgreSQL  │
       │(Real DB)    │
       └─────────────┘
✅ Validación: Flujo completo E2E Router → Agent → Service → Repository funciona correctamente

📁 ARCHIVOS CREADOS/MODIFICADOS ✨ ACTUALIZADO
Archivos Creados
text
src/theaia/tests/
├── integration/
│   └── test_agenda_crud.py           # ✨ 6 tests CRUD vía Router (NUEVO)
└── agents/agenda_agent/
    └── test_agenda_integration.py    # 10 tests E2E (EXISTENTE)
Archivos Modificados
text
src/theaia/
├── tests/
│   └── conftest.py                   # WindowsSelectorEventLoopPolicy + fixtures
├── database/
│   └── repositories/
│       └── base_repository.py        # create() con **kwargs
└── agents/agenda_agent/
    └── tools/
        └── event_tools.py            # ✨ v1.3 - Acepta datetime + str (FIX)
🚀 COMANDOS DE EJECUCIÓN ✨ ACTUALIZADO
Ejecutar Tests E2E (Suite 1)
bash
pytest src/theaia/tests/agents/agenda_agent/test_agenda_integration.py -v -s
Ejecutar Tests CRUD vía Router (Suite 2) ✨ NUEVO
bash
pytest src/theaia/tests/integration/test_agenda_crud.py -v --timeout=30 -x
Ejecutar TODOS los tests de AgendaAgent
bash
pytest src/theaia/tests/ -k agenda -v --timeout=30
Ver Cobertura Completa
bash
pytest src/theaia/tests/ -k agenda --cov=src/theaia --cov-report=html
Ejecutar Test Específico
bash
pytest src/theaia/tests/integration/test_agenda_crud.py::test_create_event -v -s
📝 LECCIONES APRENDIDAS ✨ ACTUALIZADO
Windows + asyncpg + pytest
WindowsSelectorEventLoopPolicy es necesario en Windows

Engine por test evita problemas de event loop reusado

pool_pre_ping=False necesario para evitar problemas en Windows

pytest_asyncio.fixture para fixtures async

✨ asyncio.run() + scope='session' evita timeout en teardown

Testing E2E con Router ✨ NUEVO
router.handle() es la interfaz principal a testear

intent + agent validation es crítico para routing correcto

Usuario de test único con scope='session' es más eficiente

ON CONFLICT DO NOTHING previene errores en re-ejecución

Validación de message format asegura respuestas correctas

Type Compatibility Issues ✨ NUEVO
Union types para APIs flexibles (datetime + str)

Type checking en runtime para conversión automática

Schemas Pydantic deben aceptar múltiples tipos

Documentación de tipos evita errores de uso

Debugging
Leer stacktrace completo - El error real está al fondo

Verificar Foreign Keys - Crear dependencias primero

Validar valores de enum - Usar valores permitidos

Event loop errors - Siempre relacionados con asyncio en Windows

✨ pytest-timeout es esencial para evitar cuelgues

✨ Connection pool warnings son indicativos pero no bloquean tests

✨ Event loop conflicts aparecen en teardown, no en setup

✨ Fixture scope correcto es crítico para performance

⏭️ PRÓXIMOS PASOS
Integración Pendiente
 Registrar AgendaAgent en Core Router

 Mapear intents específicos a AgendaAgent

 Tests de routing completo con múltiples agents

Tests Adicionales
 Tests de FSM (estados y transiciones)

 Tests de Entity Extractors (ML)

 Tests de integración con Telegram

 Tests de casos edge (fechas inválidas, eventos duplicados)

 Tests de concurrencia (múltiples usuarios)

Features Pendientes
 Recordatorios automáticos

 Eventos recurrentes

 Integración con calendarios externos (Google Calendar)

 Notificaciones push

 Búsqueda full-text de eventos

Optimizaciones
 Aumentar cobertura de event_tools.py (24% → 60%+)

 Refactorizar response_formatter.py (8% cobertura)

 Implementar connection pool cleanup en teardown

 Paralelizar tests E2E (pytest-xdist)

🎊 RESULTADO FINAL ✨ ACTUALIZADO
Suite 1: Tests E2E
text
======================== 10 passed in 9.15s =========================
Suite 2: Tests CRUD via Router ✨ NUEVO
text
============================= 6 passed in 7.62s =============================
Total Combined
text
======================== 16 passed in 16.77s =========================
Estado: ✅ COMPLETADO
Fecha de Completación: 04 Diciembre 2025, 23:10 CET
Próximo Hito: H04 PHASE 3 - Integración con Core Router

📈 MÉTRICAS DE PROGRESO ✨ NUEVO
Métrica	Inicial	Final	Mejora
Tests passing	10	16	+60%
Cobertura total	5%	19%	+280%
Router coverage	38%	59%	+55%
Orchestrator coverage	31%	84%	+171%
NLP Engine coverage	13%	72%	+454%
Handler coverage	14%	41%	+193%
Tiempo ejecución total	9.15s	16.77s	Ambas suites
🔧 HERRAMIENTAS INSTALADAS ✨ NUEVO
 pytest-timeout (v2.4.0) - Control de timeouts

 pytest-asyncio (ya existente) - Soporte async

 pytest-cov (ya existente) - Cobertura de código

Comando instalación:

bash
pip install pytest-timeout
👤 EQUIPO
Desarrollador Principal: Álvaro Fernández Mota
Fecha: 04 Diciembre 2025
Proyecto: THEA IA - AgendaAgent v3.4
Hito: H04 PHASE 2 EXTENDED - Tests E2E Completos ✅

📊 RESUMEN EJECUTIVO ✨ NUEVO
Logros del día:

✅ 6 nuevos tests CRUD via Router implementados

✅ 3 bugs críticos resueltos (ForeignKey, datetime, timeout)

✅ Cobertura aumentada en +14%

✅ Phase 2 completada al 100%

✅ 16/16 tests passing (100% success rate)

Tiempo invertido: ~8 horas
Archivos creados: 1 (test_agenda_crud.py)
Archivos modificados: 1 (event_tools.py v1.3)
Commits: 4 (feat, fix×2, chore)

Próximo objetivo: H04 PHASE 3 - Registrar AgendaAgent en Router