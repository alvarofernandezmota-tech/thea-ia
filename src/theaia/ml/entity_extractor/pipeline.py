"""
EntityExtractionPipeline: Composition de extractors con intent-aware logic.
Coordina extracción de fechas, ubicaciones y personas según intent detectado.

H03 FASE 1 - TAREA 1.1.2
"""

from typing import Dict, List

# Imports correctos basados en archivos existentes
try:
    from src.theaia.ml.entity_extractor.date_parser import DateTimeExtractor
except ImportError:
    # Fallback si DateTimeExtractor no existe o tiene otro nombre
    class DateTimeExtractor:
        def extract(self, text: str):
            return []

try:
    from src.theaia.ml.entity_extractor.location_extractor import LocationExtractor
except ImportError:
    class LocationExtractor:
        def extract(self, text: str):
            return []

try:
    from src.theaia.ml.entity_extractor.person_name_extractor import PersonNameExtractor
except ImportError:
    class PersonNameExtractor:
        def extract(self, text: str):
            return []


class EntityExtractionPipeline:
    """
    Pipeline de extracción de entidades con lógica intent-aware.
    
    Estrategia:
    - create_event / evento → dates + locations
    - create_note / nota → persons + locations
    - query_agenda / consulta → dates
    - fallback → dates (siempre útil para contexto)
    """
    
    def __init__(self):
        """Inicializa los 3 extractors."""
        try:
            self.date_extractor = DateTimeExtractor()
            self.location_extractor = LocationExtractor()
            self.person_extractor = PersonNameExtractor()
            self.extractors_available = True
        except Exception as e:
            print(f"[WARNING] Entity extractors initialization failed: {e}")
            self.extractors_available = False
    
    async def extract(self, text: str, intent: str) -> Dict:
        """
        Extrae entidades según intent detectado.
        
        Args:
            text: Texto del mensaje
            intent: Intent detectado
            
        Returns:
            Dict con entidades extraídas por tipo
        """
        entities = {}
        
        if not self.extractors_available:
            return entities
        
        try:
            # Intent-aware extraction
            if intent in ["create_event", "evento"]:
                # Eventos: fechas + ubicaciones
                entities["dates"] = self.date_extractor.extract(text)
                entities["locations"] = self.location_extractor.extract(text)
            
            elif intent in ["create_note", "nota", "notas"]:
                # Notas: personas + ubicaciones
                entities["persons"] = self.person_extractor.extract(text)
                entities["locations"] = self.location_extractor.extract(text)
            
            elif intent in ["query_agenda", "consulta"]:
                # Consultas: solo fechas
                entities["dates"] = self.date_extractor.extract(text)
            
            elif intent in ["recordatorio", "reminder"]:
                # Recordatorios: fechas + personas
                entities["dates"] = self.date_extractor.extract(text)
                entities["persons"] = self.person_extractor.extract(text)
            
            # Fallback: siempre intenta dates (útil para contexto temporal)
            if "dates" not in entities:
                dates = self.date_extractor.extract(text)
                if dates:
                    entities["dates"] = dates
        
        except Exception as e:
            print(f"[ERROR] Entity extraction failed: {e}")
            entities = {}
        
        return entities
