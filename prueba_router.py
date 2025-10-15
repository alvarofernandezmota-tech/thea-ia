from src.theaia.core.router import CoreRouter

router = CoreRouter()
resp1, state1, ctx1 = router.handle("test1", "Quiero agendar reunión", "initial", {})
print("Resp1:", resp1)
print("State1:", state1)

resp2, state2, ctx2 = router.handle("test1", "cita", state1, ctx1)
print("Resp2:", resp2)
print("State2:", state2)
