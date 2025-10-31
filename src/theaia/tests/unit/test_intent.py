"""
Test de detección de intents en Thea IA — agenda y derivados.

Este test valida que las frases típicas de agenda sean correctamente reconocidas por el sistema de intents.
Utiliza la infraestructura actual: CoreRouter → IntentDetector.
Perfecto para comprobar la robustez del pipeline de NLP/intent en Thea IA.

- Autor: Equipo QA Thea IA
- Última revisión: 2025-10-31
"""

import re
from src.theaia.core.router import CoreRouter

# -----------------------------------------------
# PATRÓN REGEX PARA FRASES DE AGENDA — DOCS QA
# -----------------------------------------------
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

# -----------------------------------------------
# TEST INTENT DETECTION DEL ECOSISTEMA
# -----------------------------------------------
router = CoreRouter()

print("\nIntentDetector results:")
for t in tests:
    # Usamos el intent_detector real; esta es la forma estándar dentro de Thea IA v0.14
    intent = router.intent_detector.detect(t)
    print(f"'{t}' -> intent: {intent}")
    # Si quieres asertar el resultado, añade un assert según tus intents soportados, por ejemplo:
    # assert "agenda" in intent or "horario" in intent  # <-- Ajusta según la configuración real de intentos

# -----------------------------------------------
# NOTA PARA DESARROLLADORES:
# - Este test NO usa _detect_intent (deprecated).
# - Siempre compara con la arquitectura que estás usando y actualiza el patrón/intents según evolución de Core.
# - Si actualizas detection, documenta el nuevo pipeline aquí.
# -----------------------------------------------

