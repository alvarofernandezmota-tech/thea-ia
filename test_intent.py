import re
from src.theaia.core.router import CoreRouter

# Patrón para agenda
pattern = re.compile(r"\b(quiero\s+)?agendar(s)?\s+(una\s+)?cita(s)?\b", re.IGNORECASE)
tests = [
    "quiero agendar cita",
    "quiero agendar citas",
    "agendar cita",
    "agendar citas",
    "quiero agendar una cita"
]

print("Regex matches:")
for t in tests:
    print(f"'{t}' -> {bool(pattern.search(t))}")

# Detección de intent en CoreRouter
router = CoreRouter()
print("\n_detect_intent results:")
for t in tests:
    intent = router._detect_intent(t)
    print(f"'{t}' -> intent: {intent}")
