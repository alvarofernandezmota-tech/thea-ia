"""
Módulo de inferencia del IntentDetector — Thea IA 2.0 (VERSIÓN FINAL)
Compatible con modelos guardados como (modelo, vectorizador) en tupla pickle.
Interfaz pública: detect() / Implementación interna: predict()
"""

import os
import pickle


class IntentDetector:
    """
    Detector de intenciones con soporte completo para modelo + vectorizador.
    Interfaz pública estable para CoreRouter y otros componentes.
    """

    def __init__(self, model_path: str = None):
        """Carga el modelo y vectorizador desde archivo pickle."""
        if model_path is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, "models", "model_intent.pkl")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"El modelo no se encontró en la ruta: {model_path}")

        with open(model_path, "rb") as f:
            data = pickle.load(f)

        if isinstance(data, tuple) and len(data) == 2:
            self.model, self.vectorizer = data
        else:
            raise ValueError("El formato del modelo no es compatible. Debe ser una tupla (modelo, vectorizador).")

        print(f"Modelo de detección de intenciones cargado desde {model_path}")

    def predict(self, text: str):
        """
        Método interno: Predice la intención del texto dado.
        Retorna una lista con la intención detectada como STRING puro.
        """
        try:
            if not self.model or not self.vectorizer:
                raise ValueError("Modelo o vectorizador no cargado correctamente.")

            X = self.vectorizer.transform([text])
            prediction = self.model.predict(X)
            
            # Conversión segura: numpy array → string
            if hasattr(prediction, '__iter__') and len(prediction) > 0:
                prediction = str(prediction[0])
            else:
                prediction = str(prediction)
            
            return [prediction]

        except Exception as e:
            print(f"Error durante la predicción de la intención: {e}")
            return []

    def detect(self, text: str):
        """
        Interfaz pública: Detecta la intención del texto.
        Este método es llamado por CoreRouter y otros componentes.
        
        Args:
            text (str): Mensaje del usuario
            
        Returns:
            list: Lista con la intención detectada (string)
        """
        return self.predict(text)


# Modo interactivo para pruebas
if __name__ == "__main__":
    detector = IntentDetector()
    
    ejemplos = [
        'quiero agendar una cita para mañana',
        'crea una nota sobre la reunión',
        'qué tiempo hace hoy?',
        'necesito ayuda con la app'
    ]
    
    for mensaje in ejemplos:
        intenciones = detector.detect(mensaje)
        print(f"Mensaje: '{mensaje}' -> Intenciones detectadas: {intenciones}")
