"""
Entity Extraction Pipeline - THEA-IA H03 FASE 3
Extract DATE, TIME, PERSON, LOCATION from user messages

File: src/theaia/ml/entity_extractor/pipeline.py
Updated: 20 Nov 2025 - 02:25 AM CET
NER: spaCy + Custom patterns + Intent-aware
"""

import re
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import spacy


class EntityExtractor:
    """Extract entities: DATE, TIME, PERSON, LOCATION"""
    
    def __init__(self):
        """Initialize spaCy and patterns"""
        try:
            self.nlp = spacy.load('es_core_news_sm')
        except OSError:
            print("[WARNING] spaCy model not found. Run: python -m spacy download es_core_news_sm")
            self.nlp = None
        
        self.date_patterns = [
            r'mañana', r'hoy', r'ayer',
            r'(?:el |)(\d{1,2})\s+de\s+(\w+)',
            r'próximo\s+(\w+)', r'siguiente\s+(\w+)',
            r'(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})'
        ]
        self.time_patterns = [
            r'(\d{1,2}):(\d{2})', r'las\s+(\d{1,2})',
            r'(mañana|tarde|noche)',
        ]
    
    def extract(self, text: str) -> Dict:
        """Extract all entities from text"""
        entities = {
            'DATE': [],
            'TIME': [],
            'PERSON': [],
            'LOCATION': [],
            'raw_ents': []
        }
        
        if not self.nlp:
            return entities
        
        doc = self.nlp(text)
        
        # spaCy NER
        for ent in doc.ents:
            if ent.label_ == 'PER':
                entities['PERSON'].append({'text': ent.text, 'confidence': 0.95})
            elif ent.label_ == 'LOC':
                entities['LOCATION'].append({'text': ent.text, 'confidence': 0.90})
            elif ent.label_ == 'DATE':
                entities['DATE'].append({'text': ent.text, 'confidence': 0.92})
            
            entities['raw_ents'].append({
                'text': ent.text,
                'label': ent.label_,
                'start': ent.start_char,
                'end': ent.end_char
            })
        
        # Custom date patterns
        for pattern in self.date_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.group() not in [e['text'] for e in entities['DATE']]:
                    entities['DATE'].append({
                        'text': match.group(),
                        'confidence': 0.85,
                        'source': 'pattern'
                    })
        
        # Custom time patterns
        for pattern in self.time_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if match.group() not in [e['text'] for e in entities['TIME']]:
                    entities['TIME'].append({
                        'text': match.group(),
                        'confidence': 0.88,
                        'source': 'pattern'
                    })
        
        return entities
    
    def extract_batch(self, texts: List[str]) -> List[Dict]:
        """Extract entities from multiple texts"""
        return [self.extract(text) for text in texts]
    
    def extract_intent_aware(self, text: str, intent: str) -> Dict:
        """Extract entities based on detected intent"""
        entities = self.extract(text)
        
        # Filter by intent
        if intent in ["create_event", "evento"]:
            return {k: v for k, v in entities.items() if k in ['DATE', 'TIME', 'LOCATION']}
        elif intent in ["create_note", "nota"]:
            return {k: v for k, v in entities.items() if k in ['PERSON', 'LOCATION']}
        elif intent in ["query_agenda", "consulta"]:
            return {k: v for k, v in entities.items() if k in ['DATE', 'TIME']}
        elif intent in ["create_reminder", "recordatorio"]:
            return {k: v for k, v in entities.items() if k in ['DATE', 'TIME', 'PERSON']}
        
        return entities


if __name__ == "__main__":
    extractor = EntityExtractor()
    
    test_cases = [
        "Crear evento mañana a las 15:00 con María",
        "Recordarme el 25 de noviembre en la sala 3",
        "Escribir nota para Juan esta tarde",
    ]
    
    for text in test_cases:
        entities = extractor.extract(text)
        print(f"Text: {text}")
        print(f"Entities: {entities}\n")
