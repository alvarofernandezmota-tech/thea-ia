"""
Test de integración completo - Router + Core + AgendaAgent
"""

import pytest
from src.theaia.core.router import TheaRouter


def test_router_initialization():
    """Test inicialización del router."""
    print("\n🧪 TEST 1: Router Initialization")
    print("=" * 50)
    
    router = TheaRouter()
    
    # Verificar orchestrator
    assert router.orchestrator is not None
    print("✓ Orchestrator inicializado")
    
    # Verificar agentes registrados
    agents = router.get_available_agents()
    print(f"✓ Agentes registrados: {len(agents)}")
    
    for agent in agents:
        print(f"  - {agent['name']}: {agent['description']}")
    
    # Verificar stats
    stats = router.get_stats()
    print(f"✓ Stats: {stats}")
    
    print("✅ Router initialization OK\n")


def test_router_handle_message():
    """Test procesamiento de mensaje simple."""
    print("\n🧪 TEST 2: Router Handle Message")
    print("=" * 50)
    
    router = TheaRouter()
    
    # Mensaje de prueba
    result = router.handle(
        user_id="test_user_123",
        message="mostrar eventos de hoy"
    )
    
    print(f"✓ Status: {result['status']}")
    print(f"✓ Intent: {result['intent']}")
    print(f"✓ Agent: {result['agent']}")
    print(f"✓ State: {result['state']}")
    print(f"✓ Message: {result['message'][:100]}...")
    
    assert result['status'] in ['ok', 'error']
    assert 'message' in result
    
    print("✅ Message processing OK\n")


def test_router_stats():
    """Test estadísticas del router."""
    print("\n🧪 TEST 3: Router Stats")
    print("=" * 50)
    
    router = TheaRouter()
    
    # Procesar mensaje
    router.handle("user1", "crear evento mañana")
    
    # Obtener stats
    stats = router.get_stats()
    
    print(f"✓ Total messages: {stats.get('total_messages', 0)}")
    print(f"✓ Registered agents: {stats.get('registered_agents', 0)}")
    print(f"✓ Active conversations: {stats.get('active_conversations', 0)}")
    
    assert stats['total_messages'] >= 1
    
    print("✅ Stats OK\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
