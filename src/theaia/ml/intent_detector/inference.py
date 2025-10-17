# Archivo: src/theaia/ml/intent_detector/inference.py

import joblib
import os
from typing import List

class IntentDetector:
    """
    Clase para cargar el modelo de detección de intenciones y predecir
    la intención de un mensaje de texto.
    """
    def __init__(self, model_path: str = None):
        """
        Inicializa el detector de intenciones.
        
        Args:
            model_path (str, optional): Ruta al archivo del modelo.
                                        Si no se proporciona, busca en la ruta por defecto.
        """
        if model_path is None:
            # Construye la ruta al modelo por defecto basado en la estructura del proyecto
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            model_path = os.path.join(base_dir, 'models', 'model_intent.pkl')

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"El modelo no se encontró en la ruta: {model_path}")
            
        try:
            self.model = joblib.load(model_path)
            print(f"Modelo de detección de intenciones cargado desde {model_path}")
        except Exception as e:
            print(f"Error al cargar el modelo: {e}")
            self.model = None

    def detect(self, text: str) -> List[str]:
        """
        Detecta las intenciones en un texto dado.
        
        Args:
            text (str): El mensaje del usuario.
        
        Returns:
            List[str]: Una lista de intenciones predichas. Puede estar vacía si hay un error.
        """
        if self.model is None:
            print("Error: El modelo de detección de intenciones no está cargado.")
            return []
            
        try:
            # El modelo espera una lista de textos para predecir
            predictions = self.model.predict([text])
            # La salida puede ser una lista de listas si hay múltiples etiquetas,
            # así que la aplanamos si es necesario.
            intents = predictions[0] if predictions else []
            if isinstance(intents, str):
                return [intents] # Si solo devuelve una cadena, la convertimos en lista
            return list(intents)
        except Exception as e:
            print(f"Error durante la predicción de la intención: {e}")
            return []

# Ejemplo de uso (opcional, para testing directo del módulo)
if __name__ == '__main__':
    # Creamos una instancia del detector, que cargará el modelo por defecto
    detector = IntentDetector()
    
    # Probamos con algunos mensajes
    test_messages = [
        "quiero agendar una cita para mañana",
        "crea una nota sobre la reunión",
        "qué tiempo hace hoy?",
        "necesito ayuda con la app"
    ]
    
    for msg in test_messages:
        detected_intents = detector.detect(msg)
        print(f"Mensaje: '{msg}' -> Intenciones detectadas: {detected_intents}")

