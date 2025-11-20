"""Person Name Entity Extraction for THEA_IA."""

import re
from typing import List, Dict, Any, Optional


class PersonNameExtractor:
    """Extract person names from Spanish text."""
    
    def __init__(self):
        """Initialize person name extractor with Spanish patterns."""
        # Common Spanish name patterns
        self.name_indicators = [
            r'\bcon\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
            r'\bde\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
            r'\ba\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
            r'\bpara\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)',
        ]
        
        # Common Spanish first names
        self.common_names = {
            'juan', 'maría', 'maria', 'josé', 'jose', 'antonio',
            'francisco', 'manuel', 'david', 'daniel', 'carlos',
            'pedro', 'miguel', 'javier', 'alejandro', 'fernando',
            'sergio', 'pablo', 'jorge', 'rafael', 'luis',
            'ana', 'carmen', 'isabel', 'laura', 'marta',
            'sara', 'elena', 'patricia', 'raquel', 'cristina',
            'silvia', 'monica', 'mónica', 'beatriz', 'rosa'
        }
        
        # Titles/honorifics
        self.titles = {
            'sr.', 'sr', 'señor', 'sra.', 'sra', 'señora',
            'dr.', 'dr', 'doctor', 'dra.', 'dra', 'doctora',
            'prof.', 'prof', 'profesor', 'profa.', 'profa', 'profesora',
            'ing.', 'ing', 'ingeniero', 'lic.', 'lic', 'licenciado'
        }
    
    def extract(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract person names from text.
        
        Args:
            text: Input text
        
        Returns:
            List of name dictionaries
        """
        names = []
        text_lower = text.lower()
        
        # Extract with preposition patterns
        for pattern in self.name_indicators:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.group(1)
                name_lower = name.lower().split()[0]  # First word
                
                # Check if first word is a known name
                is_known = name_lower in self.common_names
                
                # Skip if it looks like a location indicator
                if name_lower in ['el', 'la', 'los', 'las']:
                    continue
                
                names.append({
                    "text": name,
                    "start": match.start(1),
                    "end": match.end(1),
                    "type": "person",
                    "is_known": is_known,
                    "preposition": match.group(0).split()[0].lower()
                })
        
        # Extract names with titles
        for title in self.titles:
            # Pattern: title + name
            pattern = r'\b' + re.escape(title) + r'\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)?)'
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                name = match.group(1)
                # Avoid duplicates
                if not any(n['start'] == match.start(1) for n in names):
                    names.append({
                        "text": name,
                        "start": match.start(1),
                        "end": match.end(1),
                        "type": "person",
                        "is_known": name.lower().split()[0] in self.common_names,
                        "title": title,
                        "preposition": None
                    })
        
        # Extract standalone common names (capitalized)
        for name in self.common_names:
            # Pattern: capitalized version of known name
            capitalized = name.capitalize()
            pattern = r'\b' + re.escape(capitalized) + r'\b'
            matches = re.finditer(pattern, text)
            for match in matches:
                # Avoid duplicates
                if not any(n['start'] == match.start() for n in names):
                    names.append({
                        "text": match.group(0),
                        "start": match.start(),
                        "end": match.end(),
                        "type": "person",
                        "is_known": True,
                        "preposition": None
                    })
        
        # Remove duplicates (same position)
        seen_positions = set()
        unique_names = []
        for name in names:
            pos = (name['start'], name['end'])
            if pos not in seen_positions:
                seen_positions.add(pos)
                unique_names.append(name)
        
        # Sort by position in text
        unique_names.sort(key=lambda x: x['start'])
        
        return unique_names
    
    def extract_first(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract first person name from text.
        
        Args:
            text: Input text
        
        Returns:
            First name dict or None
        """
        names = self.extract(text)
        return names[0] if names else None


# Convenience function
def extract_person_names(text: str) -> List[Dict[str, Any]]:
    """Extract person names from text."""
    extractor = PersonNameExtractor()
    return extractor.extract(text)
