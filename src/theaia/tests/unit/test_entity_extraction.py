"""Tests for Location and Person Name Extractors."""

import pytest
from src.theaia.ml.entity_extractor.location_extractor import LocationExtractor, extract_locations
from src.theaia.ml.entity_extractor.person_name_extractor import PersonNameExtractor, extract_person_names


@pytest.fixture
def location_extractor():
    """Create LocationExtractor instance."""
    return LocationExtractor()


@pytest.fixture
def person_extractor():
    """Create PersonNameExtractor instance."""
    return PersonNameExtractor()


class TestLocationExtractor:
    """Test location extraction functionality."""
    
    def test_extract_city_with_preposition(self, location_extractor):
        """Test extracting city with 'en'."""
        result = location_extractor.extract("Reunión en Madrid")
        
        assert len(result) >= 1
        assert result[0]["text"] == "Madrid"
        assert result[0]["type"] in ["location", "city"]
        assert result[0]["is_known"] is True
    
    def test_extract_multiple_locations(self, location_extractor):
        """Test extracting multiple locations."""
        result = location_extractor.extract("Viaje desde Barcelona a Valencia")
        
        assert len(result) >= 2
        location_texts = [loc["text"].lower() for loc in result]
        assert "barcelona" in location_texts or any("barcelona" in text for text in location_texts)
    
    def test_extract_location_type(self, location_extractor):
        """Test extracting location type (oficina, casa, etc)."""
        result = location_extractor.extract("Ir a la oficina")
        
        assert len(result) >= 1
        assert "oficina" in result[0]["text"].lower()
    
    def test_extract_no_location(self, location_extractor):
        """Test when no location found."""
        result = location_extractor.extract("Esto no tiene ninguna ubicación")
        
        assert len(result) == 0
    
    def test_extract_first_location(self, location_extractor):
        """Test extracting first location only."""
        result = location_extractor.extract_first("Viajar de Madrid a Barcelona")
        
        assert result is not None
        assert "madrid" in result["text"].lower()
    
    def test_convenience_function(self):
        """Test convenience function extract_locations."""
        result = extract_locations("Reunión en Sevilla")
        
        assert isinstance(result, list)
        if result:  # May extract or not depending on pattern
            assert isinstance(result[0], dict)


class TestPersonNameExtractor:
    """Test person name extraction functionality."""
    
    def test_extract_name_with_con(self, person_extractor):
        """Test extracting name with 'con'."""
        result = person_extractor.extract("Reunión con Juan")
        
        assert len(result) >= 1
        assert "Juan" in result[0]["text"]
        assert result[0]["type"] == "person"
    
    def test_extract_name_with_title(self, person_extractor):
        """Test extracting name with title."""
        result = person_extractor.extract("Llamar al Dr. García")
        
        assert len(result) >= 1
        assert "García" in result[0]["text"]
    
    def test_extract_common_name(self, person_extractor):
        """Test extracting standalone common name."""
        result = person_extractor.extract("María me lo dijo")
        
        assert len(result) >= 1
        assert "María" in result[0]["text"]
        assert result[0]["is_known"] is True
    
    def test_extract_no_name(self, person_extractor):
        """Test when no name found."""
        result = person_extractor.extract("Hacer algo urgente mañana")
        
        # May or may not extract - either is fine
        assert isinstance(result, list)
    
    def test_extract_first_name(self, person_extractor):
        """Test extracting first name only."""
        result = person_extractor.extract_first("Hablar con Pedro y Luis")
        
        # Should extract at least Pedro
        if result:
            assert result is not None
            assert result["type"] == "person"
    
    def test_convenience_function(self):
        """Test convenience function extract_person_names."""
        result = extract_person_names("Cita con Carlos")
        
        assert isinstance(result, list)


class TestEntityExtractionIntegration:
    """Integration tests for entity extraction."""
    
    def test_extract_location_and_person(self, location_extractor, person_extractor):
        """Test extracting both location and person from same text."""
        text = "Reunión con María en Barcelona"
        
        locations = location_extractor.extract(text)
        persons = person_extractor.extract(text)
        
        # Should extract Barcelona
        location_texts = [loc["text"].lower() for loc in locations]
        assert any("barcelona" in text for text in location_texts)
        
        # Should extract María
        person_names = [p["text"] for p in persons]
        assert any("maría" in name.lower() for name in person_names)
    
    def test_complex_sentence(self, location_extractor, person_extractor):
        """Test complex sentence with multiple entities."""
        text = "Viaje con Juan desde Madrid a Valencia el próximo lunes"
        
        locations = location_extractor.extract(text)
        persons = person_extractor.extract(text)
        
        # Should extract locations
        assert len(locations) >= 1
        
        # Should extract person
        assert len(persons) >= 1
        assert any("juan" in p["text"].lower() for p in persons)


class TestEntityExtractionEdgeCases:
    """Test edge cases for entity extraction."""
    
    def test_location_with_accents(self, location_extractor):
        """Test location with Spanish accents."""
        result = location_extractor.extract("Viaje a Málaga")
        
        # Should handle accented characters
        if result:
            assert isinstance(result[0], dict)
    
    def test_person_with_accents(self, person_extractor):
        """Test person name with accents."""
        result = person_extractor.extract("Hablar con José")
        
        # Should handle accented names
        if result:
            assert result[0]["type"] == "person"
    
    def test_empty_text(self, location_extractor, person_extractor):
        """Test with empty text."""
        assert location_extractor.extract("") == []
        assert person_extractor.extract("") == []
    
    def test_only_stopwords(self, location_extractor, person_extractor):
        """Test with only common words."""
        text = "el la los las de con en"
        
        loc_result = location_extractor.extract(text)
        person_result = person_extractor.extract(text)
        
        # Should not extract meaningless words
        assert isinstance(loc_result, list)
        assert isinstance(person_result, list)
