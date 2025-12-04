"""
Test DEBUG - Ver qué datos llegan
"""

import pytest
from src.theaia.core.router import TheaRouter


@pytest.fixture
def router():
    return TheaRouter()


def test_debug_create_event(router):
    """Test para ver el flujo completo."""
    print("\n🔍 DEBUG: Crear Evento")
    print("=" * 50)
    
    result = router.handle(
        user_id="test_user_123",
        message="crear evento 'Reunión equipo' mañana a las 10:00"
    )
    
    print(f"\n📥 RESULTADO COMPLETO:")
    print(f"Status: {result.get('status')}")
    print(f"Intent: {result.get('intent')}")
    print(f"Agent: {result.get('agent')}")
    print(f"State: {result.get('state')}")
    print(f"Context: {result.get('context')}")
    print(f"\n💬 MENSAJE:")
    print(result.get('message'))
    
    # Mostrar todo el dict
    print(f"\n📦 DATOS COMPLETOS:")
    import json
    print(json.dumps(result, indent=2, default=str))


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
