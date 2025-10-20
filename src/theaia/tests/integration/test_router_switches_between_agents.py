import pytest
from src.theaia.core.router import CoreRouter

@pytest.fixture(scope="module")
def router():
    """Instancia compartida del CoreRouter para las pruebas."""
    return CoreRouter()

def test_switch_between_agents(router):
    """
    Comprueba que Thea IA cambia correctamente entre Agenda y Notas
    y mantiene coherencia en el estado FSM.
    """
    user_id = "user_testswitch_001"
    context = {}

    # Paso 1 — Iniciar Agenda
    step1 = router.handle(user_id, "quiero agendar una reunión", context)
    assert step1["status"] == "ok"
    assert "día" in step1["message"].lower()
    context = step1["context"]

    # Paso 2 — Cambiar a Notas
    step2 = router.handle(user_id, "ahora crea una nota", context)
    assert step2["status"] == "ok"
    assert "guardar" in step2["message"].lower()
    assert step2["context"]["delegated_intent"] in ["nota", "notas", "crear_nota"]

    print("\n✅ Cambio de agente validado correctamente (Agenda → Notas).")
