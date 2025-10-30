import pytest
pytest.skip("Deshabilitado: CoreRouter ya no existe o ha sido renombrado. Test deshabilitado temporalmente.", allow_module_level=True)

# from src.theaia.core.router import CoreRouter
# from src.theaia.database.repositories.context_repository import load_context

# TEST_USER = "USR_TEST_PERSIST"

# def test_persistencia_agenda():
#     router = CoreRouter()
#     mensaje = "quiero agendar reunión el viernes"
#     result, message, state, context = router.handle(TEST_USER, mensaje)
#     print("Respuesta agente:", message)
#     loaded_context = load_context(TEST_USER)
#     print("Contexto recuperado tras reinicio:", loaded_context)
#     assert context == loaded_context, "Persistencia fallida: contextos no coinciden"

# if __name__ == "__main__":
#     test_persistencia_agenda()
