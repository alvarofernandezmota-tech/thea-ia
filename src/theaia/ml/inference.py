"""
Módulo de inferencia del IntentDetector — Thea IA 2.0

Realiza la carga del modelo entrenado para clasificación de intenciones.
Compatible con modelos guardados en formato de tupla (modelo, vectorizador).
Incluye manejo de errores, logs estructurados y fallback automático.
"""

import os
import pickle
import traceback


class IntentDetector:
    """
    Detector de intenciones modular de Thea IA 2.0.
    Usa un modelo de ML (por defecto, SVM) y un vectorizador de texto.
    """

    def __init__(self, model_path: str = None):
        """
        Inicializa el modelo y el vectorizador.

        Si no se indica ruta, busca automáticamente en:
        src/theaia/ml/models/model_intent.pkl
        """
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            default_path = os.path.join(base_dir, "models", "model_intent.pkl")
            self.model_path = model_path or default_path

            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"No se encontró el modelo en {self.model_path}")

            with open(self.model_path, "rb") as f:
                model_data = pickle.load(f)

            # Detectar si el modelo incluye vectorizador
            if isinstance(model_data, tuple) and len(model_data) == 2:
                self.model, self.vectorizer = model_data
            else:
                self.model = model_data
                self.vectorizer = None

            print(f"✅ Modelo de intenciones cargado correctamente desde: {self.model_path}")

        except Exception as e:
            print(f"[ERROR] No se pudo inicializar el IntentDetector: {e}")
            traceback.print_exc()
            self.model, self.vectorizer = None, None

    # --------------------------------------------------------------
    # MÉTODO PRINCIPAL DE PREDICCIÓN
    # --------------------------------------------------------------
    def predict(self, text: str):
        """
        Retorna una lista con la intención detectada para el texto dado.
        Si ocurre algún error, devuelve ['fallback'] para garantizar continuidad.
        """
        try:
            if not self.model:
                raise RuntimeError("El modelo no se cargó correctamente.")

            # Verificar vectorizador
            if self.vectorizer:
                X = self.vectorizer.transform([text])
            elif hasattr(self.model, "transform"):
                X = self.model.transform([text])
            else:
                raise ValueError("No hay vectorizador disponible para transformar el texto.")

            prediction = self.model.predict(X)

            # SVM y Scikit-learn retornan arrays o listas
            if isinstance(prediction, (list, tuple)):
                prediction = prediction[0]

            return [prediction]

        except Exception as e:
            print(f"[WARN] Error durante la predicción: {e}")
            return ["fallback"]

    # --------------------------------------------------------------
    # VALIDACIÓN DEL ESTADO INTERNO
    # --------------------------------------------------------------
    def is_ready(self) -> bool:
        """Devuelve True si el modelo está correctamente inicializado."""
        return self.model is not None and self.vectorizer is not None


# --------------------------------------------------------------
# MODO INTERACTIVO (si se ejecuta directamente)
# --------------------------------------------------------------
if __name__ == "__main__":
    detector = IntentDetector()

    if detector.is_ready():
        print("\n🔎 Pruebas del IntentDetector:")
        ejemplos = [
            "quiero agendar una cita",
            "crear nota de prueba",
            "recordarme una reunión mañana",
            "necesito ayuda",
            "texto aleatorio sin sentido"
        ]
        for frase in ejemplos:
            print(f"Entrada: {frase} → Intención: {detector.predict(frase)}")
    else:
        print("❌ El modelo no está listo para inferencia.")
