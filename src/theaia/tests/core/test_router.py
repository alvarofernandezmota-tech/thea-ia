from src.theaia.core.router import TheaRouter

def test_pipeline_routing_and_fallback():
    router = TheaRouter()
    uid = "user_orquestacion"

    # Test de intent NOTA
    resp = router.handle(uid, "Escribe una nota: llamar a Juan")
    assert resp["status"] == "ok"
    assert resp["state"] != "error"
    assert "nota" in resp["context"].get("last_intent", "")

    # Test de intent AYUDA
    resp = router.handle(uid, "Necesito ayuda con el sistema")
    assert resp["context"]["last_intent"] == "ayuda"

    # Test de fallback real (mensaje sin sentido)
    resp = router.handle(uid, "asldkjqwopzmxnv")
    assert resp["context"]["last_intent"] == "fallback"
    assert "No he entendido" in resp["message"] or resp["status"] == "ok"

    # Test de error interno en agente
    def fake_handle(*a, **kwa): raise Exception("Forzado!")
    router.agent_registry["nota"] = type("FakeBadAgent", (), {"__init__": lambda self, uid: None, "handle": fake_handle})
    resp = router.handle(uid, "Escribe una nota de error")
    assert resp["status"] == "error"

    print("TEST INTEGRACIÓN ORQUESTADA > todo correctísimo")
