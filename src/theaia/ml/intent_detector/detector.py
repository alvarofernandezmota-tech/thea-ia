# src/theaia/ml/intent_detector/detector.py

class IntentDetector:
    """
    Una clase simple para detectar intenciones. En el futuro,
    cargará un modelo real de Machine Learning.
    """
    def __init__(self, model_path: str = None):
        # Aquí cargarías tu modelo (ej: joblib.load(model_path))
        # Por ahora, no hace nada.
        self.model = "dummy_model"
        print("IntentDetector inicializado.")

    def predict(self, text: str) -> list[str]:
        """
        Simula la predicción de intenciones.
        """
        # Esta lógica será reemplazada por `self.model.predict()`
        text = text.lower()
        if "agendar" in text or "cita" in text:
            return ["agenda"]
        if "nota" in text or "apunte" in text:
            return ["notas"]
        return []
