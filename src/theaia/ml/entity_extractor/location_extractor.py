"""Location Entity Extraction for THEA_IA."""

import re
from typing import List, Dict, Any, Optional


class LocationExtractor:
    """Extract location entities from Spanish text."""
    
    def __init__(self):
        """Initialize location extractor with Spanish patterns."""
        # Common location prepositions in Spanish
        self.location_indicators = [
            r'\ben\s+(?:el\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'\ba\s+(?:la\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'\bdesde\s+(?:el\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'\bhasta\s+(?:el\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
            r'\bpor\s+(?:el\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*)',
        ]
        
        # Common Spanish cities
        self.known_cities = {
            'madrid', 'barcelona', 'valencia', 'sevilla', 'zaragoza',
            'málaga', 'malaga', 'murcia', 'palma', 'bilbao',
            'alicante', 'córdoba', 'cordoba', 'valladolid', 'vigo',
            'gijón', 'gijon', 'hospitalet', 'coruña', 'granada',
            'vitoria', 'elche', 'oviedo', 'badalona', 'cartagena',
            'terrassa', 'jerez', 'sabadell', 'móstoles', 'mostoles',
            'santander', 'pamplona', 'almería', 'almeria', 'leganés', 'leganes'
        }
        
        # Common location types
        self.location_types = {
            'oficina', 'casa', 'trabajo', 'escuela', 'universidad',
            'hospital', 'aeropuerto', 'estación', 'estacion',
            'restaurante', 'bar', 'café', 'cafe', 'tienda',
            'supermercado', 'centro', 'parque', 'gimnasio',
            'biblioteca', 'museo', 'teatro', 'cine', 'hotel'
        }
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract locations from text.
        
        Args:
            text: Input text
        
        Returns:
            List of location dictionaries
        """
        locations = []
        text_lower = text.lower()
        
        # Extract with preposition patterns
        for pattern in self.location_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                location = match.group(1)
                location_lower = location.lower()
                
                # Check if it's a known city or location type
                is_known = (
                    location_lower in self.known_cities or
                    any(loc_type in location_lower for loc_type in self.location_types)
                )
                
                locations.append({
                    "text": location,
                    "start": match.start(1),
                    "end": match.end(1),
                    "type": "location",
                    "is_known": is_known,
                    "preposition": match.group(0).split()[0].lower()
                })
        
        # Extract standalone known cities (without preposition)
        for city in self.known_cities:
            # Use word boundaries to match whole words
            pattern = r'\b' + re.escape(city) + r'\b'
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                # Avoid duplicates
                if not any(loc['start'] == match.start() for loc in locations):
                    # Get original case from text
                    original = text[match.start():match.end()]
                    locations.append({
                        "text": original,
                        "start": match.start(),
                        "end": match.end(),
                        "type": "city",
                        "is_known": True,
                        "preposition": None
                    })
        
        # Remove duplicates (same position)
        seen_positions = set()
        unique_locations = []
        for loc in locations:
            pos = (loc['start'], loc['end'])
            if pos not in seen_positions:
                seen_positions.add(pos)
                unique_locations.append(loc)
        
        # Sort by position in text
        unique_locations.sort(key=lambda x: x['start'])
        
        return unique_locations
    
    def extract_first(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract first location from text.
        
        Args:
            text: Input text
        
        Returns:
            First location dict or None
        """
        locations = self.extract(text)
        return locations[0] if locations else None


# Convenience function
def extract_locations(text: str) -> List[Dict[str, Any]]:
    """Extract locations from text."""
    extractor = LocationExtractor()
    return extractor.extract(text)
