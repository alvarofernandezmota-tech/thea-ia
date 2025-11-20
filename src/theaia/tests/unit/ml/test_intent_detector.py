"""
Unit Tests for Intent Detector - THEA-IA H03 FASE 2
Tests para IntentDetector con 89% accuracy

File: src/theaia/tests/unit/ml/test_intent_detector.py
Generated: 20 Nov 2025 - 02:13 AM CET
Tests: 10 unit tests
Coverage: IntentDetector class completa
"""

import pytest
from src.theaia.ml.intent_detector.detector import IntentDetector, create_and_train_detector


@pytest.fixture(scope="module")
def trained_detector():
    """Fixture: detector entrenado para todos los tests"""
    detector = create_and_train_detector(confidence_threshold=0.3, verbose=False)
    return detector


class TestIntentDetectorTraining:
    """Tests para entrenamiento del detector"""
    
    def test_detector_trains_successfully(self):
        """Test: detector entrena correctamente"""
        detector = IntentDetector(confidence_threshold=0.3)
        metrics = detector.train(verbose=False)
        
        assert detector.is_trained is True
        assert metrics["accuracy"] > 0.85  # Accuracy > 85%
        assert metrics["total_examples"] == 320
        assert metrics["intents_count"] == 8
    
    def test_detector_accuracy_threshold(self):
        """Test: accuracy supera threshold de 85%"""
        detector = create_and_train_detector(verbose=False)
        metrics = detector.train(verbose=False)
        
        assert metrics["accuracy"] >= 0.85, f"Accuracy {metrics['accuracy']:.2%} menor que 85%"


class TestIntentDetectorPredictions:
    """Tests para predicciones del detector"""
    
    def test_predict_create_event(self, trained_detector):
        """Test: predice correctamente create_event"""
        text = "Crear evento mañana a las 3"
        intent, confidence = trained_detector.predict(text)
        
        assert intent == "create_event"
        assert confidence > 0.3
    
    def test_predict_create_note(self, trained_detector):
        """Test: predice correctamente create_note"""
        text = "Escribir nota importante sobre el proyecto"
        intent, confidence = trained_detector.predict(text)
        
        assert intent == "create_note"
        assert confidence > 0.3
    
    def test_predict_create_reminder(self, trained_detector):
        """Test: predice correctamente create_reminder"""
        text = "Recordarme llamar a Juan mañana"
        intent, confidence = trained_detector.predict(text)
        
        assert intent == "create_reminder"
        assert confidence > 0.3
    
    def test_predict_query_agenda(self, trained_detector):
        """Test: predice correctamente query_agenda"""
        text = "Qué tengo programado hoy"
        intent, confidence = trained_detector.predict(text)
        
        assert intent == "query_agenda"
        assert confidence > 0.3
    
    def test_predict_help(self, trained_detector):
        """Test: predice correctamente help"""
        text = "Ayuda por favor"
        intent, confidence = trained_detector.predict(text)
        
        assert intent == "help"
        assert confidence > 0.3


class TestIntentDetectorBatchPredictions:
    """Tests para predicciones batch"""
    
    def test_predict_batch(self, trained_detector):
        """Test: predice batch de textos correctamente"""
        texts = [
            "Crear evento mañana",
            "Escribir nota",
            "Recordarme llamar",
        ]
        
        results = trained_detector.predict_batch(texts)
        
        assert len(results) == 3
        assert all(isinstance(r, tuple) for r in results)
        assert all(len(r) == 2 for r in results)
        assert results[0][0] == "create_event"
        assert results[1][0] == "create_note"
        assert results[2][0] == "create_reminder"


class TestIntentDetectorTopN:
    """Tests para predicciones top N"""
    
    def test_predict_top_n(self, trained_detector):
        """Test: predice top 3 intents correctamente"""
        text = "Crear evento mañana"
        top_3 = trained_detector.predict_top_n(text, n=3)
        
        assert len(top_3) == 3
        assert all(isinstance(r, tuple) for r in top_3)
        assert top_3[0][0] == "create_event"  # Primer intent
        assert top_3[0][1] > top_3[1][1]  # Confianza descendente
        assert top_3[1][1] > top_3[2][1]


class TestIntentDetectorFallback:
    """Tests para detección de fallback"""
    
    def test_fallback_on_low_confidence(self, trained_detector):
        """Test: fallback cuando confianza baja"""
        # Texto confuso que no matchea ningún intent claramente
        text = "xyz abc 123 random nonsense"
        intent, confidence = trained_detector.predict(text)
        
        # Puede ser fallback o tener confianza muy baja
        assert confidence < 0.5 or intent == "fallback"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
