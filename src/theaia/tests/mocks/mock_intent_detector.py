# Archivo: src/theaia/tests/mocks/mock_intent_detector.py

class MockIntentDetector:
    """
    Un falso detector de intenciones que simula el comportamiento del real
    para ser usado exclusivamente en tests. No carga ningún modelo.
    Devuelve las intenciones exactas que los agentes esperan.
    """
    def __init__(self):
        # Mapeo de palabras clave a las intenciones que los agentes realmente entienden
        self.intent_map = {
            "cita": ["agendar"],
            "nota": ["nota"],
            "recordar": ["recordatorio"],
            "evento": ["evento"],
            "ayuda": ["ayuda"],
            "qué es": ["consulta"],
            "programar": ["programar"],
        }
        print("MockIntentDetector inicializado para testing.")

    def detect(self, text: str) -> list[str]:
        """
        Simula la detección de intenciones buscando palabras clave.
        """
        text_lower = text.lower()
        if text_lower.startswith("qué es"):
            return self.intent_map["qué es"]
            
        for keyword, intents in self.intent_map.items():
            if keyword in text_lower:
                return intents
        return []
