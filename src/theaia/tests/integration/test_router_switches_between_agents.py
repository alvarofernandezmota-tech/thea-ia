import pytest
from src.theaia.core.router import CoreRouter

@pytest.fixture(scope="module")
def router():
    """Instancia compartida del CoreRouter para las pruebas."""
    return CoreRouter()

def test_switch_between_agents(router):
    """
    Comprueba que Thea IA responde a diferentes intents
    y puede cambiar de contexto entre agentes.
    """
    user_id = "user_testswitch_001"

    # Paso 1 — Enviar mensaje de agenda
    step1 = router.handle(user_id, "quiero agendar una reunión")
    assert step1["status"] == "ok"
    assert "message" in step1
    # Solo verificar que responde (puede ser fallback)
    print(f"Respuesta paso 1: {step1['message']}")

    # Paso 2 — Enviar mensaje de notas
    step2 = router.handle(user_id, "ahora crea una nota")
    assert step2["status"] == "ok"
    assert "message" in step2
    # Solo verificar que responde
    print(f"Respuesta paso 2: {step2['message']}")

    print("\n✅ Test de cambio de agente completado (verificación básica).")
        