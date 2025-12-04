"""
Simple NLP Engine for AgendaAgent

Dictionary-based NLP that simulates LLM behavior without AI.
Uses synonym matching and score-based intent detection.
Can be replaced with real LLM later without changing interface.
"""

from typing import Dict, List, Tuple, Optional
import re
from dataclasses import dataclass


@dataclass
class IntentMatch:
    """Intent match result with confidence score."""
    intent: str
    confidence: float
    matched_keywords: List[str]


class SimpleNLPEngine:
    """
    Simple NLP engine using dictionary-based matching.
    
    Provides the same interface as an LLM would, but uses
    predefined dictionaries and patterns for matching.
    """
    
    def __init__(self):
        """Initialize NLP engine with knowledge base."""
        
        # Intent keywords with synonyms and variations
        self.intent_keywords = {
            "create_event": {
                "primary": ["crear", "agendar", "añadir", "programar", "planificar", "poner"],
                "secondary": ["nuevo", "evento", "reunión", "cita", "meeting", "appointment"],
                "phrases": [
                    "tengo reunión",
                    "tengo cita",
                    "hay reunión",
                    "quiero agendar",
                    "necesito programar",
                    "recuérdame",
                    "recordar",
                ]
            },
            "update_event": {
                "primary": ["modificar", "cambiar", "actualizar", "editar", "mover", "reprogramar"],
                "secondary": ["evento", "reunión", "cita"],
                "phrases": [
                    "cambia la reunión",
                    "mueve el evento",
                    "modifica la cita",
                ]
            },
            "delete_event": {
                "primary": ["eliminar", "borrar", "cancelar", "quitar", "remover"],
                "secondary": ["evento", "reunión", "cita"],
                "phrases": [
                    "cancela la reunión",
                    "borra el evento",
                    "elimina la cita",
                ]
            },
            "query_events": {
                "primary": ["qué", "que", "cuáles", "cuales", "cuándo", "cuando", "mostrar", "ver", "listar"],
                "secondary": ["tengo", "hay", "eventos", "reuniones", "citas", "agenda"],
                "phrases": [
                    "qué tengo",
                    "cuándo tengo",
                    "mis eventos",
                    "mi agenda",
                    "mostrar agenda",
                    "ver eventos",
                ]
            },
            "mark_complete": {
                "primary": ["marcar", "completar", "finalizar", "terminar"],
                "secondary": ["completado", "hecho", "finalizado", "terminado"],
                "phrases": [
                    "evento completado",
                    "reunión terminada",
                    "ya pasó",
                ]
            }
        }
        
        # Entity type keywords
        self.entity_keywords = {
            "datetime": {
                "relative": ["mañana", "hoy", "pasado mañana", "en", "dentro de"],
                "absolute": ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"],
                "time": ["a las", "at", "am", "pm"],
            },
            "location": {
                "prepositions": ["en", "at", "in"],
                "common": ["oficina", "casa", "zoom", "meet", "teams", "sala"],
            },
            "participants": {
                "prepositions": ["con", "with"],
            }
        }
        
        # Common variations and typos
        self.normalizations = {
            # Accents
            "reunion": "reunión",
            "programar": "programar",
            "despues": "después",
            "tambien": "también",
            # Typos
            "agerdar": "agendar",
            "cambair": "cambiar",
            # Abbreviations
            "mtg": "meeting",
            "apt": "appointment",
        }
    
    async def detect_intent(self, message: str) -> str:
        """
        Detect intent from message using keyword matching.
        
        Args:
            message: User message
            
        Returns:
            Intent name or "unknown"
        """
        message_normalized = self._normalize(message)
        
        # Try phrase matching first (highest confidence)
        for intent, keywords in self.intent_keywords.items():
            for phrase in keywords.get("phrases", []):
                if phrase in message_normalized:
                    return intent
        
        # Score-based matching
        scores = {}
        for intent, keywords in self.intent_keywords.items():
            score = self._calculate_intent_score(message_normalized, keywords)
            scores[intent] = score
        
        # Get highest score
        if scores:
            best_intent = max(scores, key=scores.get)
            best_score = scores[best_intent]
            
            # Require minimum confidence
            if best_score >= 0.3:
                return best_intent
        
        return "unknown"
    
    async def detect_intent_with_confidence(self, message: str) -> IntentMatch:
        """
        Detect intent with confidence score and matched keywords.
        
        Args:
            message: User message
            
        Returns:
            IntentMatch object
        """
        message_normalized = self._normalize(message)
        
        # Calculate scores for all intents
        matches = []
        for intent, keywords in self.intent_keywords.items():
            score, matched = self._calculate_intent_score_detailed(
                message_normalized, 
                keywords
            )
            matches.append(IntentMatch(
                intent=intent,
                confidence=score,
                matched_keywords=matched
            ))
        
        # Sort by confidence
        matches.sort(key=lambda x: x.confidence, reverse=True)
        
        # Return best match or unknown
        if matches and matches[0].confidence >= 0.3:
            return matches[0]
        
        return IntentMatch(
            intent="unknown",
            confidence=0.0,
            matched_keywords=[]
        )
    
    def _normalize(self, text: str) -> str:
        """Normalize text (lowercase, remove accents, fix typos)."""
        text = text.lower().strip()
        
        # Apply normalizations
        for typo, correct in self.normalizations.items():
            text = text.replace(typo, correct)
        
        return text
    
    def _calculate_intent_score(
        self, 
        message: str, 
        keywords: Dict[str, List[str]]
    ) -> float:
        """
        Calculate intent match score.
        
        Args:
            message: Normalized message
            keywords: Intent keywords dictionary
            
        Returns:
            Score between 0 and 1
        """
        score = 0.0
        
        # Primary keywords (weight: 0.6)
        primary_matches = sum(
            1 for kw in keywords.get("primary", [])
            if kw in message
        )
        if primary_matches > 0:
            score += 0.6
        
        # Secondary keywords (weight: 0.3)
        secondary_matches = sum(
            1 for kw in keywords.get("secondary", [])
            if kw in message
        )
        if secondary_matches > 0:
            score += 0.3
        
        # Phrase matches (weight: 1.0 - guaranteed)
        for phrase in keywords.get("phrases", []):
            if phrase in message:
                return 1.0
        
        return min(score, 1.0)
    
    def _calculate_intent_score_detailed(
        self,
        message: str,
        keywords: Dict[str, List[str]]
    ) -> Tuple[float, List[str]]:
        """
        Calculate score with list of matched keywords.
        
        Returns:
            Tuple of (score, matched_keywords)
        """
        score = 0.0
        matched = []
        
        # Primary keywords
        for kw in keywords.get("primary", []):
            if kw in message:
                score += 0.6
                matched.append(kw)
                break
        
        # Secondary keywords
        for kw in keywords.get("secondary", []):
            if kw in message:
                score += 0.3
                matched.append(kw)
        
        # Phrase matches
        for phrase in keywords.get("phrases", []):
            if phrase in message:
                score = 1.0
                matched.append(f"phrase: {phrase}")
                break
        
        return min(score, 1.0), matched
    
    def extract_entities(self, message: str, intent: str) -> Dict[str, any]:
        """
        Extract entities from message based on intent.
        
        Args:
            message: User message
            intent: Detected intent
            
        Returns:
            Dictionary with extracted entities
        """
        entities = {}
        message_normalized = self._normalize(message)
        
        if intent == "create_event":
            # Extract title (text between quotes or after 'evento/reunión')
            title_match = re.search(r'["\']([^"\']+)["\']', message)
            if title_match:
                entities["title"] = title_match.group(1)
            else:
                # Try to extract after 'evento' or 'reunión'
                for keyword in ["evento", "reunión", "cita", "meeting"]:
                    pattern = rf'{keyword}\s+([^,\.;]+)'
                    match = re.search(pattern, message_normalized)
                    if match:
                        entities["title"] = match.group(1).strip()
                        break
            
            # Extract datetime string for datetime_parser
            # Look for temporal expressions
            datetime_patterns = [
                r'(mañana\s+a\s+las\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)',
                r'(hoy\s+a\s+las\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)',
                r'(pasado\s+mañana\s+a\s+las\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)',
                r'(el\s+\w+\s+a\s+las\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)',
                r'(\d{1,2}/\d{1,2}/\d{4}\s+a\s+las\s+\d{1,2}(?::\d{2})?(?:\s*(?:am|pm))?)',
            ]
            
            datetime_str = None
            for pattern in datetime_patterns:
                match = re.search(pattern, message_normalized)
                if match:
                    datetime_str = match.group(1)
                    break
            
            # If still no match, try to find any datetime-related text
            if not datetime_str:
                # Look for 'mañana', 'hoy', etc. + time
                temporal_words = ['mañana', 'hoy', 'pasado mañana', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']
                for word in temporal_words:
                    if word in message_normalized:
                        # Extract from that word to end (or to next punctuation)
                        idx = message_normalized.index(word)
                        rest = message_normalized[idx:]
                        # Take until punctuation or end
                        end_match = re.search(r'[,\.;]', rest)
                        if end_match:
                            datetime_str = rest[:end_match.start()].strip()
                        else:
                            datetime_str = rest.strip()
                        break
            
            if datetime_str:
                entities["datetime_str"] = datetime_str
            
            # Extract location
            location_match = re.search(r'en\s+([^,\.;]+)', message_normalized)
            if location_match:
                entities["location"] = location_match.group(1).strip()
            
            # Extract participants
            participants_match = re.search(r'con\s+([^,\.;]+)', message_normalized)
            if participants_match:
                participants_str = participants_match.group(1).strip()
                # Split by 'y', 'and', ','
                participants = re.split(r'\s+y\s+|\s+and\s+|,\s*', participants_str)
                entities["participants"] = [p.strip() for p in participants if p.strip()]
        
        elif intent == "query_events":
            # Extract time range for queries
            if "hoy" in message_normalized:
                entities["time_range"] = "today"
            elif "mañana" in message_normalized:
                entities["time_range"] = "tomorrow"
            elif "semana" in message_normalized:
                entities["time_range"] = "week"
            elif "mes" in message_normalized:
                entities["time_range"] = "month"
        
        return entities
    
    def extract_entities_hints(self, message: str) -> Dict[str, List[str]]:
        """
        Extract hints about entities in message.
        
        Returns hints that can help other parsers (datetime_parser, etc.)
        
        Args:
            message: User message
            
        Returns:
            Dictionary with entity hints
        """
        message_normalized = self._normalize(message)
        hints = {}
        
        # Datetime hints
        datetime_hints = []
        for keyword in self.entity_keywords["datetime"]["relative"]:
            if keyword in message_normalized:
                datetime_hints.append(f"relative: {keyword}")
        for keyword in self.entity_keywords["datetime"]["absolute"]:
            if keyword in message_normalized:
                datetime_hints.append(f"day: {keyword}")
        
        if datetime_hints:
            hints["datetime"] = datetime_hints
        
        # Location hints
        location_hints = []
        for prep in self.entity_keywords["location"]["prepositions"]:
            if f" {prep} " in message_normalized:
                location_hints.append(f"preposition: {prep}")
        
        if location_hints:
            hints["location"] = location_hints
        
        # Participants hints
        for prep in self.entity_keywords["participants"]["prepositions"]:
            if f" {prep} " in message_normalized:
                hints["participants"] = [f"preposition: {prep}"]
        
        return hints
    
    def suggest_missing_info(
        self,
        intent: str,
        current_entities: Dict[str, any]
    ) -> Optional[str]:
        """
        Suggest what information is missing based on intent.
        
        Args:
            intent: Detected intent
            current_entities: Already extracted entities
            
        Returns:
            Suggestion string or None
        """
        required_fields = {
            "create_event": ["title", "datetime"],
            "update_event": ["event_id"],
            "delete_event": ["event_id"],
            "mark_complete": ["event_id"],
        }
        
        required = required_fields.get(intent, [])
        missing = [field for field in required if not current_entities.get(field)]
        
        if not missing:
            return None
        
        suggestions = {
            "title": "el título o descripción del evento",
            "datetime": "la fecha y hora (ej: mañana a las 3pm)",
            "event_id": "el número del evento (ej: #123)",
        }
        
        missing_names = [suggestions.get(field, field) for field in missing]
        
        if len(missing_names) == 1:
            return f"Me falta {missing_names[0]}"
        else:
            return f"Me faltan: {', '.join(missing_names)}"
