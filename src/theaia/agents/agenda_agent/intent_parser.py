"""
Intent Parser for AgendaAgent

Detects user intent and extracts entities from natural language messages.
Supports Spanish and English.
"""

import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime


class AgendaIntentParser:
    """
    Parses user messages to detect intent and extract entities.
    
    Supported intents:
    - create_event: User wants to create a new event
    - update_event: User wants to modify an existing event
    - delete_event: User wants to delete an event
    - query_events: User wants to see their events
    - mark_complete: User wants to mark an event as completed
    """
    
    def __init__(self):
        # Intent detection patterns (Spanish and English)
        self.intent_patterns = {
            "create_event": [
                # Spanish
                r'\b(crear|agendar|añadir|programar|planificar|poner)\b.*\b(evento|reunión|cita|meeting|appointment)\b',
                r'\b(tengo|hay)\b.*\b(reunión|cita|meeting)\b',
                r'\b(recuérdame|recordar)\b',
                # English
                r'\b(create|schedule|add|plan|set up)\b.*\b(event|meeting|appointment)\b',
                r'\b(i have|there is)\b.*\b(meeting|appointment)\b',
                r'\b(remind me)\b',
            ],
            "update_event": [
                # Spanish
                r'\b(modificar|cambiar|actualizar|editar|mover|reprogramar)\b.*\b(evento|reunión|cita)\b',
                r'\b(cambia|mueve|modifica)\b.*\b(reunión|cita|evento)\b',
                # English
                r'\b(modify|change|update|edit|move|reschedule)\b.*\b(event|meeting|appointment)\b',
                r'\b(change|move|update)\b.*\b(meeting|appointment|event)\b',
            ],
            "delete_event": [
                # Spanish
                r'\b(eliminar|borrar|cancelar|quitar|remover)\b.*\b(evento|reunión|cita)\b',
                r'\b(cancela|borra|elimina)\b.*\b(reunión|cita|evento)\b',
                # English
                r'\b(delete|remove|cancel|erase)\b.*\b(event|meeting|appointment)\b',
                r'\b(cancel|delete|remove)\b.*\b(meeting|appointment|event)\b',
            ],
            "query_events": [
                # Spanish
                r'\b(qué|que|cuáles|cuales|cuándo|cuando)\b.*\b(tengo|hay|eventos|reuniones|citas)\b',
                r'\b(mostrar|ver|listar|dame)\b.*\b(eventos|reuniones|citas|agenda)\b',
                r'\b(mi agenda|mis eventos|mis reuniones)\b',
                # English
                r'\b(what|which|when)\b.*\b(do i have|are there|events|meetings|appointments)\b',
                r'\b(show|display|list|get)\b.*\b(events|meetings|appointments|schedule)\b',
                r'\b(my schedule|my events|my meetings)\b',
            ],
            "mark_complete": [
                # Spanish
                r'\b(marcar|completar|finalizar|terminar)\b.*\b(evento|reunión|cita)\b.*\b(completado|finalizado|hecho)\b',
                r'\b(evento|reunión|cita)\b.*\b(completado|listo|hecho|terminado)\b',
                # English
                r'\b(mark|complete|finish|done)\b.*\b(event|meeting|appointment)\b.*\b(complete|done|finished)\b',
                r'\b(event|meeting|appointment)\b.*\b(complete|done|finished)\b',
            ],
        }
        
        # Entity extraction patterns
        self.entity_patterns = {
            # Event ID: #123, evento 123, reunión 456
            "event_id": r'(?:#|evento\s+|reunión\s+|cita\s+|event\s+|meeting\s+)(\d+)',
            
            # Participants: con Juan, con María y Pedro, with John
            "participants": r'\b(?:con|with)\s+((?:[A-ZÁ-Ú][a-zá-ú]+(?:\s+y\s+|\s+and\s+|,\s*)?)+)',
            
            # Location: en oficina, en zoom, at office
            "location": r'\b(?:en|at|in)\s+([A-Za-zá-úÁ-Ú\s]+?)(?:\s+(?:a las|at|el|on|con|with)|\s*$)',
            
            # Title extraction (simplified - gets first quoted text or noun phrase)
            "title": r'"([^"]+)"',
        }
    
    async def detect_intent(self, message: str) -> str:
        """
        Detects the primary intent from a user message.
        
        Args:
            message: User's natural language message
            
        Returns:
            Intent string: create_event, update_event, delete_event, 
                          query_events, mark_complete, or "unknown"
        """
        message_lower = message.lower()
        
        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    return intent
        
        return "unknown"
    
    async def extract_entities(self, message: str, intent: str) -> Dict[str, any]:
        """
        Extracts entities from message based on intent.
        
        Args:
            message: User's natural language message
            intent: Detected intent
            
        Returns:
            Dictionary with extracted entities:
            - title: Event title
            - datetime_str: Raw datetime string (to be parsed by datetime_parser)
            - location: Event location
            - participants: List of participant names
            - event_id: Event ID (for update/delete)
        """
        entities = {
            "title": None,
            "datetime_str": None,
            "location": None,
            "participants": [],
            "event_id": None,
        }
        
        # Extract event ID (for update/delete/mark_complete)
        if intent in ["update_event", "delete_event", "mark_complete"]:
            entities["event_id"] = self._extract_event_id(message)
        
        # Extract title
        entities["title"] = self._extract_title(message, intent)
        
        # Extract datetime string (raw, will be parsed later)
        entities["datetime_str"] = self._extract_datetime_str(message)
        
        # Extract location
        entities["location"] = self._extract_location(message)
        
        # Extract participants
        entities["participants"] = self._extract_participants(message)
        
        return entities
    
    def _extract_event_id(self, message: str) -> Optional[int]:
        """Extract event ID from message."""
        match = re.search(self.entity_patterns["event_id"], message, re.IGNORECASE)
        if match:
            return int(match.group(1))
        return None
    
    def _extract_title(self, message: str, intent: str) -> Optional[str]:
        """
        Extract event title from message.
        Priority: quoted text > noun phrases after verbs
        """
        # Try quoted text first
        match = re.search(self.entity_patterns["title"], message)
        if match:
            return match.group(1)
        
        # For create_event, try to extract noun phrase after action verb
        if intent == "create_event":
            # Spanish patterns
            patterns = [
                r'(?:crear|agendar|añadir|programar)\s+(?:evento|reunión|cita)?\s*[""]?([^""\n]+?)[""]?\s+(?:para|el|mañana|hoy)',
                r'(?:tengo|hay)\s+(?:reunión|cita|meeting)?\s+(?:de\s+)?[""]?([^""\n]+?)[""]?\s+(?:el|mañana|hoy|a las)',
            ]
            # English patterns
            patterns.extend([
                r'(?:create|schedule|add)\s+(?:event|meeting)?\s*[""]?([^""\n]+?)[""]?\s+(?:for|on|tomorrow|today)',
                r'(?:i have|there is)\s+(?:meeting|appointment)?\s+(?:about\s+)?[""]?([^""\n]+?)[""]?\s+(?:on|tomorrow|today|at)',
            ])
            
            for pattern in patterns:
                match = re.search(pattern, message, re.IGNORECASE)
                if match:
                    title = match.group(1).strip()
                    # Clean up common prepositions
                    title = re.sub(r'\s+(con|en|para|at|in|with)\s+.*$', '', title, flags=re.IGNORECASE)
                    return title
        
        return None
    
    def _extract_datetime_str(self, message: str) -> Optional[str]:
        """
        Extract datetime string for parsing.
        Returns raw string like "mañana a las 3pm", "el viernes", "en 2 horas"
        """
        # Common datetime patterns (Spanish and English)
        patterns = [
            # Absolute: "mañana a las 3pm", "el viernes a las 10"
            r'(mañana|hoy|pasado mañana)\s+a\s+las\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            r'(tomorrow|today)\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            r'el\s+(lunes|martes|miércoles|jueves|viernes|sábado|domingo)\s+a\s+las\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            r'(?:on\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            
            # Just time: "a las 3pm", "at 3pm"
            r'a\s+las\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            r'at\s+\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?',
            
            # Relative: "en 2 horas", "in 2 hours"
            r'en\s+\d+\s+(?:hora|horas|minuto|minutos|día|días)',
            r'in\s+\d+\s+(?:hour|hours|minute|minutes|day|days)',
            
            # Just day: "mañana", "el viernes"
            r'\b(mañana|hoy|pasado mañana)\b',
            r'\b(tomorrow|today)\b',
            r'el\s+(lunes|martes|miércoles|jueves|viernes|sábado|domingo)',
            r'(?:on\s+)?(monday|tuesday|wednesday|thursday|friday|saturday|sunday)',
            
            # Specific date: "04/12/2025", "2025-12-04"
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{4}-\d{1,2}-\d{1,2}',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_location(self, message: str) -> Optional[str]:
        """Extract location from message."""
        match = re.search(self.entity_patterns["location"], message, re.IGNORECASE)
        if match:
            location = match.group(1).strip()
            # Clean up trailing words
            location = re.sub(r'\s+(con|y|and|with).*$', '', location, flags=re.IGNORECASE)
            return location
        return None
    
    def _extract_participants(self, message: str) -> List[str]:
        """Extract participant names from message."""
        match = re.search(self.entity_patterns["participants"], message, re.IGNORECASE)
        if match:
            participants_str = match.group(1)
            # Split by "y", "and", or comma
            participants = re.split(r'\s+y\s+|\s+and\s+|,\s*', participants_str, flags=re.IGNORECASE)
            # Clean and return
            return [p.strip() for p in participants if p.strip()]
        return []
    
    def validate_entities(self, entities: Dict[str, any], intent: str) -> Tuple[bool, List[str]]:
        """
        Validates if required entities are present for the intent.
        
        Args:
            entities: Extracted entities
            intent: Detected intent
            
        Returns:
            Tuple of (is_valid, missing_fields)
        """
        required_fields = {
            "create_event": ["title", "datetime_str"],
            "update_event": ["event_id"],
            "delete_event": ["event_id"],
            "query_events": [],  # No required fields
            "mark_complete": ["event_id"],
        }
        
        if intent not in required_fields:
            return False, ["Unknown intent"]
        
        missing = []
        for field in required_fields[intent]:
            if not entities.get(field):
                missing.append(field)
        
        return len(missing) == 0, missing
