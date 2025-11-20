"""Unit Tests for Entity Extractor - THEA-IA H03 FASE 3"""
import pytest
from src.theaia.ml.entity_extractor.pipeline import EntityExtractor

@pytest.fixture(scope="module")
def extractor():
    return EntityExtractor()

class TestEntityExtractorDates:
    def test_extract_date_manana(self, extractor):
        entities = extractor.extract("Crear evento mañana a las 3")
        assert len(entities['DATE']) > 0
    
    def test_extract_date_pattern(self, extractor):
        entities = extractor.extract("Recordarme el 25 de noviembre")
        assert len(entities['DATE']) > 0

class TestEntityExtractorTimes:
    def test_extract_time_hhmm(self, extractor):
        entities = extractor.extract("Reunión a las 15:00")
        assert len(entities['TIME']) > 0
    
    def test_extract_time_tarde(self, extractor):
        entities = extractor.extract("Llamar esta tarde")
        assert len(entities['TIME']) > 0

class TestEntityExtractorPersons:
    def test_extract_person(self, extractor):
        entities = extractor.extract("Hablar con Juan mañana")
        assert 'PERSON' in entities

class TestEntityExtractorBatch:
    def test_extract_batch(self, extractor):
        results = extractor.extract_batch(["evento mañana", "15:00"])
        assert len(results) == 2

class TestEntityExtractorStructure:
    def test_extract_returns_dict(self, extractor):
        entities = extractor.extract("Prueba")
        assert all(k in entities for k in ['DATE','TIME','PERSON','LOCATION','raw_ents'])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
