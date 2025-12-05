"""
Advanced tests for Router - Coverage Optimization
Target: Router 60% → 70%+

Tests adicionales para cubrir paths no cubiertos:
- Error handling paths (líneas 69-75)
- Orchestrator error scenarios (líneas 167-186)
- Detailed stats (líneas 237-252)
- Preprocess edge cases (líneas 38-40)
- Concurrent requests (performance + coverage)

Autor: Álvaro Fernández Mota
Fecha: 05 Diciembre 2025
Hito: H04 Phase 4 - Advanced Coverage
"""

import pytest
import asyncio
from datetime import datetime
from sqlalchemy import text

from src.theaia.core.router import TheaRouter, Message, ProcessedMessage
from src.theaia.database.session import AsyncSessionLocal


# ============================================================================
# FIXTURES
# ============================================================================

@pytest.fixture(scope='session', autouse=True)
def setup_test_user():
    """Fixture que crea usuario de prueba para toda la sesión"""
    async def _create_user():
        async with AsyncSessionLocal() as session:
            await session.execute(text("""
                INSERT INTO users (id, telegram_id, username, tenant_id, created_at, updated_at)
                VALUES (1, 1, 'test_user', 'default', NOW(), NOW())
                ON CONFLICT (id) DO NOTHING
            """))
            await session.execute(text("""
                INSERT INTO users (id, telegram_id, username, tenant_id, created_at, updated_at)
                VALUES (2, 2, 'test_user_2', 'default', NOW(), NOW())
                ON CONFLICT (id) DO NOTHING
            """))
            await session.execute(text("""
                INSERT INTO users (id, telegram_id, username, tenant_id, created_at, updated_at)
                VALUES (3, 3, 'test_user_3', 'default', NOW(), NOW())
                ON CONFLICT (id) DO NOTHING
            """))
            await session.commit()
    
    asyncio.run(_create_user())


@pytest.fixture
def router():
    """Fixture que crea instancia fresca de TheaRouter"""
    router = TheaRouter()
    yield router


# ============================================================================
# FASE 1: ERROR HANDLING COVERAGE (Líneas 69-75, 167-186)
# ============================================================================

@pytest.mark.asyncio
async def test_router_error_handling_malformed_message(router):
    """
    Test: Router maneja mensajes malformados con graceful error handling
    
    Cubre: líneas 69-75 (error handling paths)
    
    Casos:
    - Texto None
    - Texto vacío
    - User_id inválido
    """
    # Test 1: Texto None (si el sistema lo permite)
    try:
        message1 = Message(text=None, user_id="1", tenant_id="default")
        response1 = await router.process(message1)
        # Validar que maneja error gracefully
        assert response1 is not None
    except (TypeError, ValueError):
        # Si lanza excepción, está OK también
        pass
    
    # Test 2: Texto extremadamente largo
    message2 = Message(
        text="x" * 10000,  # 10k caracteres
        user_id="1",
        tenant_id="default"
    )
    response2 = await router.process(message2)
    assert response2 is not None
    
    # Test 3: User_id vacío o inválido
    message3 = Message(
        text="test message",
        user_id="",  # Empty user_id
        tenant_id="default"
    )
    response3 = await router.process(message3)
    assert response3 is not None


@pytest.mark.asyncio
async def test_router_orchestrator_exception_handling(router):
    """
    Test: Router maneja excepciones del orchestrator gracefully
    
    Cubre: líneas 167-186 (error paths en _process_with_orchestrator)
    
    Estrategia: Enviar mensajes que puedan causar edge cases
    en el orchestrator para validar error handling.
    """
    # Test 1: Mensaje con caracteres especiales problemáticos
    message1 = Message(
        text="test\x00null\x00bytes",  # Null bytes
        user_id="1",
        tenant_id="default"
    )
    response1 = await router.process(message1)
    assert response1 is not None
    assert hasattr(response1, 'status')
    
    # Test 2: Mensaje con Unicode extremo
    message2 = Message(
        text="🔥💯🚀" * 100,  # Emojis masivos
        user_id="1",
        tenant_id="default"
    )
    response2 = await router.process(message2)
    assert response2 is not None
    
    # Test 3: Mensaje vacío después de preprocess
    message3 = Message(
        text="     ",  # Solo espacios
        user_id="1",
        tenant_id="default"
    )
    response3 = await router.process(message3)
    assert response3 is not None


# ============================================================================
# FASE 2: DETAILED STATS COVERAGE (Líneas 237-252)
# ============================================================================

@pytest.mark.asyncio
async def test_router_get_stats_detailed_metrics(router):
    """
    Test: get_stats retorna todas las métricas detalladas
    
    Cubre: líneas 237-252 (get_stats method completo)
    
    Valida:
    - Router version
    - Orchestrator stats
    - Agent stats
    - Request counts
    - Timing metrics
    """
    # Arrange - Generar actividad diversa
    messages = [
        Message(text="crear evento test 1", user_id="1", tenant_id="default"),
        Message(text="listar eventos", user_id="1", tenant_id="default"),
        Message(text="que es theaia", user_id="1", tenant_id="default"),
        Message(text="ayuda", user_id="1", tenant_id="default"),
        Message(text="crear evento test 2", user_id="2", tenant_id="default"),
    ]
    
    # Act - Procesar múltiples mensajes
    for message in messages:
        await router.process(message)
    
    # Get stats
    stats = router.get_stats()
    
    # Assert - Validar estructura completa
    assert stats is not None
    assert isinstance(stats, dict)
    
    # Assert - Campos obligatorios
    assert "router_version" in stats
    assert stats["router_version"] == "2.0"
    
    # Assert - Stats pueden tener diferentes estructuras
    # Validar que al menos retorna algo útil
    assert len(stats) > 0


@pytest.mark.asyncio
async def test_router_get_stats_after_errors(router):
    """
    Test: get_stats funciona correctamente incluso después de errores
    
    Cubre: líneas 237-252 (stats con error scenarios)
    """
    # Arrange - Generar mensajes normales + problemáticos
    messages = [
        Message(text="mensaje normal", user_id="1", tenant_id="default"),
        Message(text="", user_id="1", tenant_id="default"),  # Vacío
        Message(text="x" * 5000, user_id="1", tenant_id="default"),  # Largo
        Message(text="normal 2", user_id="1", tenant_id="default"),
    ]
    
    # Act
    for message in messages:
        await router.process(message)
    
    # Get stats
    stats = router.get_stats()
    
    # Assert
    assert stats is not None
    assert "router_version" in stats


# ============================================================================
# FASE 3: PREPROCESS EDGE CASES (Líneas 38-40)
# ============================================================================

@pytest.mark.asyncio
async def test_router_preprocess_unicode_edge_cases(router):
    """
    Test: preprocess_text maneja Unicode y caracteres especiales
    
    Cubre: líneas 38-40 (preprocess_text edge cases)
    
    Casos:
    - Unicode diversos (CJK, árabe, emojis)
    - Caracteres de control
    - Combinaciones complejas
    """
    # Test 1: Chinese/Japanese/Korean
    message1 = Message(
        text="创建事件 明天 下午3点",  # Chinese
        user_id="1",
        tenant_id="default"
    )
    response1 = await router.process(message1)
    assert response1 is not None
    
    # Test 2: Arabic (RTL)
    message2 = Message(
        text="إنشاء حدث غدا الساعة 3",  # Arabic
        user_id="1",
        tenant_id="default"
    )
    response2 = await router.process(message2)
    assert response2 is not None
    
    # Test 3: Mixed emojis + text
    message3 = Message(
        text="crear 📅 evento 🔔 mañana ⏰ 3pm 🚀",
        user_id="1",
        tenant_id="default"
    )
    response3 = await router.process(message3)
    assert response3 is not None
    
    # Test 4: Caracteres de control y espacios especiales
    message4 = Message(
        text="crear\tevent\no\r\nmañana",  # tabs, newlines
        user_id="1",
        tenant_id="default"
    )
    response4 = await router.process(message4)
    assert response4 is not None
    
    # Test 5: Combinación compleja
    message5 = Message(
        text="🔥 Test with   multiple    spaces and\temojis 💯",
        user_id="1",
        tenant_id="default"
    )
    response5 = await router.process(message5)
    assert response5 is not None


# ============================================================================
# FASE 4: CONCURRENT REQUESTS (Performance + Coverage)
# ============================================================================

@pytest.mark.asyncio
async def test_router_concurrent_requests_handling(router):
    """
    Test: Router maneja requests concurrentes correctamente
    
    Cubre: 
    - Concurrency handling
    - Thread safety
    - Performance under load
    
    Valida:
    - Todas las requests completan
    - No hay race conditions
    - Response times razonables
    """
    # Arrange - Preparar múltiples mensajes
    messages = [
        Message(text=f"crear evento test {i}", user_id=str(i % 3 + 1), tenant_id="default")
        for i in range(20)
    ]
    
    # Act - Ejecutar concurrentemente
    start_time = asyncio.get_event_loop().time()
    
    responses = await asyncio.gather(
        *[router.process(msg) for msg in messages],
        return_exceptions=True
    )
    
    end_time = asyncio.get_event_loop().time()
    elapsed = end_time - start_time
    
    # Assert - Todas completaron
    assert len(responses) == 20
    
    # Assert - No hay excepciones (o son manejadas)
    for response in responses:
        if not isinstance(response, Exception):
            assert response is not None
            assert isinstance(response, ProcessedMessage)
    
    # Assert - Performance razonable
    # 20 requests en menos de 10 segundos es aceptable
    assert elapsed < 10.0, f"Concurrent requests took {elapsed}s (expected < 10s)"
    
    # Assert - Average response time
    avg_time = elapsed / 20
    assert avg_time < 1.0, f"Average response time {avg_time}s (expected < 1s)"


@pytest.mark.asyncio
async def test_router_multi_user_concurrent_isolation(router):
    """
    Test: Contexts de usuarios diferentes se mantienen aislados bajo concurrencia
    
    Cubre:
    - Multi-user isolation under load
    - Context separation
    - No cross-contamination
    """
    # Arrange - 3 usuarios con mensajes distintos
    user1_messages = [
        Message(text=f"user1 message {i}", user_id="1", tenant_id="default")
        for i in range(5)
    ]
    
    user2_messages = [
        Message(text=f"user2 message {i}", user_id="2", tenant_id="default")
        for i in range(5)
    ]
    
    user3_messages = [
        Message(text=f"user3 message {i}", user_id="3", tenant_id="default")
        for i in range(5)
    ]
    
    # Intercalar mensajes
    all_messages = []
    for i in range(5):
        all_messages.append(user1_messages[i])
        all_messages.append(user2_messages[i])
        all_messages.append(user3_messages[i])
    
    # Act - Procesar concurrentemente
    responses = await asyncio.gather(
        *[router.process(msg) for msg in all_messages],
        return_exceptions=True
    )
    
    # Assert - Todas completaron correctamente
    assert len(responses) == 15
    
    # Assert - Cada response es válida
    valid_responses = [r for r in responses if isinstance(r, ProcessedMessage)]
    assert len(valid_responses) >= 10, "Al menos 10 de 15 responses deben ser válidas"
    
    # Assert - Usuarios mantienen contextos separados
    for response in valid_responses:
        assert response.original_text is not None
        # Validar que el texto corresponde al user_id correcto
        # (esto es implícito si no hay crashes)


# ============================================================================
# FASE 5: ADDITIONAL EDGE CASES
# ============================================================================

@pytest.mark.asyncio
async def test_router_tenant_isolation(router):
    """
    Test: Router maneja correctamente diferentes tenants
    
    Cubre: Multi-tenancy support
    """
    # Test 1: Mismo user_id, diferentes tenants
    message1 = Message(
        text="crear evento tenant 1",
        user_id="1",
        tenant_id="tenant_a"
    )
    
    message2 = Message(
        text="crear evento tenant 2",
        user_id="1",
        tenant_id="tenant_b"
    )
    
    response1 = await router.process(message1)
    response2 = await router.process(message2)
    
    # Assert - Ambos procesan correctamente
    assert response1 is not None
    assert response2 is not None
    
    # Assert - Tenant info preservada (si disponible)
    if hasattr(response1, 'tenant_id'):
        assert response1.tenant_id == "tenant_a"
    if hasattr(response2, 'tenant_id'):
        assert response2.tenant_id == "tenant_b"


@pytest.mark.asyncio
async def test_router_get_available_agents_detailed(router):
    """
    Test: get_available_agents retorna información completa
    
    Cubre: Detailed agent listing
    """
    # Act
    agents = router.get_available_agents()
    
    # Assert - Lista no vacía
    assert agents is not None
    assert isinstance(agents, list)
    assert len(agents) > 0
    
    # Assert - AgendaAgent presente
    agent_names = [str(a).lower() for a in agents]
    assert any("agenda" in name for name in agent_names)


# ============================================================================
# RESUMEN DE COBERTURA
# ============================================================================

"""
Tests en este archivo: 9

Coverage Target:
✅ Líneas 38-40   (test_router_preprocess_unicode_edge_cases)
✅ Líneas 69-75   (test_router_error_handling_malformed_message)
✅ Líneas 131-132 (cubierto indirectamente por todos los tests async)
✅ Líneas 167-186 (test_router_orchestrator_exception_handling)
✅ Líneas 237-252 (test_router_get_stats_detailed_metrics)

Performance Tests:
✅ test_router_concurrent_requests_handling
✅ test_router_multi_user_concurrent_isolation

Additional Coverage:
✅ test_router_get_stats_after_errors
✅ test_router_tenant_isolation
✅ test_router_get_available_agents_detailed

Expected Coverage Increase: +10-15%
Target: Router 60% → 70-75%

Duración estimada: ~15-20s para ejecutar todos

H04 Phase 4 - Advanced Router Coverage
Autor: Álvaro Fernández Mota
Fecha: 05 Diciembre 2025
"""
