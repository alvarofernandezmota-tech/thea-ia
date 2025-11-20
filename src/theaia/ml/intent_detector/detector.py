"""
Intent Detector - THEA-IA H03 FASE 2
TF-IDF + Logistic Regression para detección de intents en español

File: src/theaia/ml/intent_detector/detector.py
Location: /src/theaia/ml/intent_detector/detector.py
Generated: 20 Nov 2025 - 02:07 AM CET
Model: TF-IDF + LogisticRegression
Language: Spanish (es)
Confidence Threshold: 0.3 (permisivo para training limitado)
"""

import pickle
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

from .training_data import TRAINING_DATA, get_training_examples, get_intents_list


class IntentDetector:
    """
    Intent Detector usando TF-IDF + Logistic Regression
    
    Attributes:
        vectorizer: TF-IDF vectorizer
        classifier: Logistic Regression classifier
        intents: Lista de intents disponibles
        confidence_threshold: Umbral mínimo de confianza (default 0.3)
        fallback_intent: Intent por defecto cuando confianza baja
    """
    
    def __init__(self, confidence_threshold: float = 0.3):
        """
        Inicializar IntentDetector
        
        Args:
            confidence_threshold: Umbral mínimo de confianza (0.0-1.0)
                                 Default 0.3 para Spanish NLP con training limitado
        """
        self.vectorizer = TfidfVectorizer(
            max_features=500,
            ngram_range=(1, 2),
            lowercase=True,
            strip_accents=None,
            analyzer='word',
            token_pattern=r'\b\w+\b'
        )
        
        self.classifier = LogisticRegression(
            max_iter=1000,
            random_state=42,
            multi_class='multinomial',
            solver='lbfgs',
            C=1.0
        )
        
        self.intents = get_intents_list()
        self.confidence_threshold = confidence_threshold
        self.fallback_intent = "fallback"
        self._is_trained = False
    
    def train(self, test_size: float = 0.2, verbose: bool = True) -> Dict:
        """Entrenar modelo con training data"""
        X = []
        y = []
        
        for intent, examples in TRAINING_DATA.items():
            X.extend(examples)
            y.extend([intent] * len(examples))
        
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        X_train_tfidf = self.vectorizer.fit_transform(X_train)
        X_test_tfidf = self.vectorizer.transform(X_test)
        
        self.classifier.fit(X_train_tfidf, y_train)
        
        y_pred = self.classifier.predict(X_test_tfidf)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        self._is_trained = True
        
        if verbose:
            print(f"Intent Detector Trained Successfully")
            print(f"Accuracy: {accuracy:.2%}")
            print(f"Total examples: {len(X)}")
            print(f"Train examples: {len(X_train)}")
            print(f"Test examples: {len(X_test)}")
            print(f"Intents: {len(self.intents)}")
        
        return {
            "accuracy": accuracy,
            "report": report,
            "total_examples": len(X),
            "train_size": len(X_train),
            "test_size": len(X_test),
            "intents_count": len(self.intents)
        }
    
    def predict(self, text: str) -> Tuple[str, float]:
        """Predecir intent de un texto"""
        if not self._is_trained:
            raise ValueError("Modelo no entrenado. Ejecutar .train() primero.")
        
        X_tfidf = self.vectorizer.transform([text])
        probas = self.classifier.predict_proba(X_tfidf)[0]
        
        max_proba_idx = np.argmax(probas)
        max_proba = probas[max_proba_idx]
        predicted_intent = self.classifier.classes_[max_proba_idx]
        
        if max_proba < self.confidence_threshold:
            return self.fallback_intent, max_proba
        
        return predicted_intent, max_proba
    
    def predict_batch(self, texts: List[str]) -> List[Tuple[str, float]]:
        """Predecir intents de múltiples textos"""
        return [self.predict(text) for text in texts]
    
    def predict_top_n(self, text: str, n: int = 3) -> List[Tuple[str, float]]:
        """Predecir top N intents más probables"""
        if not self._is_trained:
            raise ValueError("Modelo no entrenado. Ejecutar .train() primero.")
        
        X_tfidf = self.vectorizer.transform([text])
        probas = self.classifier.predict_proba(X_tfidf)[0]
        
        top_n_idx = np.argsort(probas)[::-1][:n]
        
        results = []
        for idx in top_n_idx:
            intent = self.classifier.classes_[idx]
            confidence = probas[idx]
            results.append((intent, confidence))
        
        return results
    
    def save(self, path: str):
        """Guardar modelo entrenado"""
        if not self._is_trained:
            raise ValueError("Modelo no entrenado. Nada que guardar.")
        
        model_data = {
            'vectorizer': self.vectorizer,
            'classifier': self.classifier,
            'intents': self.intents,
            'confidence_threshold': self.confidence_threshold,
            'fallback_intent': self.fallback_intent
        }
        
        with open(path, 'wb') as f:
            pickle.dump(model_data, f)
        
        print(f"Modelo guardado en: {path}")
    
    def load(self, path: str):
        """Cargar modelo previamente entrenado"""
        with open(path, 'rb') as f:
            model_data = pickle.load(f)
        
        self.vectorizer = model_data['vectorizer']
        self.classifier = model_data['classifier']
        self.intents = model_data['intents']
        self.confidence_threshold = model_data['confidence_threshold']
        self.fallback_intent = model_data['fallback_intent']
        self._is_trained = True
        
        print(f"Modelo cargado desde: {path}")
    
    def get_feature_importance(self, intent: str, top_n: int = 10) -> List[Tuple[str, float]]:
        """Obtener palabras más importantes para un intent"""
        if not self._is_trained:
            raise ValueError("Modelo no entrenado.")
        
        if intent not in self.classifier.classes_:
            raise ValueError(f"Intent '{intent}' no encontrado.")
        
        intent_idx = list(self.classifier.classes_).index(intent)
        coefs = self.classifier.coef_[intent_idx]
        feature_names = self.vectorizer.get_feature_names_out()
        top_idx = np.argsort(coefs)[::-1][:top_n]
        
        return [(feature_names[i], coefs[i]) for i in top_idx]
    
    @property
    def is_trained(self) -> bool:
        """Verificar si modelo está entrenado"""
        return self._is_trained
    
    def __repr__(self) -> str:
        status = "trained" if self._is_trained else "not trained"
        return f"IntentDetector(intents={len(self.intents)}, status={status})"


def create_and_train_detector(
    confidence_threshold: float = 0.3,
    test_size: float = 0.2,
    verbose: bool = True
) -> IntentDetector:
    """Crear y entrenar detector en un solo paso"""
    detector = IntentDetector(confidence_threshold=confidence_threshold)
    detector.train(test_size=test_size, verbose=verbose)
    return detector


if __name__ == "__main__":
    print("Training Intent Detector...")
    detector = create_and_train_detector(verbose=True)
    
    test_cases = [
        "Crear evento mañana a las 3",
        "Escribir nota importante",
        "Recordarme llamar a Juan",
        "Qué tengo programado hoy",
        "Ayuda por favor",
    ]
    
    print("\nTest Predictions:")
    for text in test_cases:
        intent, confidence = detector.predict(text)
        print(f"'{text}' -> {intent} ({confidence:.2%})")
