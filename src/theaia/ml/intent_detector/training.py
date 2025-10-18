"""
Script de entrenamiento del IntentDetector — Thea IA 2.0
Guarda el modelo como tupla (modelo, vectorizador) en formato pickle.
"""

import os
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC


def train_intent_model():
    print("🚀 Entrenando modelo de intenciones (IntentDetector)...")

    # Dataset de entrenamiento
    data = [
        ("quiero agendar una cita", "agendar_cita"),
        ("agendar una reunión", "agendar_cita"),
        ("necesito ayuda", "help"),
        ("qué es inteligencia artificial", "query"),
        ("crear una nota", "nota"),
        ("nota importante para mañana", "nota"),
        ("recordarme una reunión", "recordatorio"),
        ("ayuda", "help"),
    ]

    X_texts, y_labels = zip(*data)

    # Vectorización
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(X_texts)

    # Entrenamiento
    model = LinearSVC()
    model.fit(X, y_labels)

    # Guardar como TUPLA
    model_dir = "src/theaia/ml/models"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, "model_intent.pkl")

    with open(model_path, "wb") as f:
        pickle.dump((model, vectorizer), f)  # ← TUPLA EXPLÍCITA

    print(f"✅ Modelo entrenado y guardado correctamente en: {model_path}")


if __name__ == "__main__":
    train_intent_model()
