"""Unit Tests for Router Integration - H03 FASE 3 BLOQUE 3.2"""

import pytest
from src.theaia.ml.intent_detector.router_integration import NLPPipeline

@pytest.fixture(scope="module")
def pipeline():
    return NLPPipeline()

class TestNLPPipeline:
    def test_process_returns_dict(self, pipeline):
        result = pipeline.process("Crear evento mañana")
        assert isinstance(result, dict)
        assert all(k in result for k in ['intent','confidence','entities','text'])
    
    def test_intent_detection(self, pipeline):
        result = pipeline.process("Crear evento mañana a las 3")
        assert result['intent'] == 'create_event'
        assert result['confidence'] > 0.3
    
    def test_entity_extraction(self, pipeline):
        result = pipeline.process("Reunión mañana a las 15:00")
        assert len(result['entities']['DATE']) > 0
        assert len(result['entities']['TIME']) > 0
    
    def test_combined_intent_entities(self, pipeline):
        result = pipeline.process("Crear evento con María mañana")
        assert result['intent'] == 'create_event'
        assert len(result['entities']['DATE']) > 0
    
    def test_process_batch(self, pipeline):
        texts = ["Crear evento mañana", "Escribir nota"]
        results = pipeline.process_batch(texts)
        assert len(results) == 2
        assert all('intent' in r for r in results)

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
