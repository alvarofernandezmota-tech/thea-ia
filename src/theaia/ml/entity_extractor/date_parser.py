"""Date and Time Entity Extraction for THEA_IA."""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import re
from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta


class DateTimeExtractor:
    """Extract and parse date/time entities from text."""
    
    def __init__(self):
        """Initialize date/time extractor."""
        self.relative_patterns = {
            r'\bmañana\b': ('days', 1),
            r'\bpasado mañana\b': ('days', 2),
            r'\bhoy\b': ('days', 0),
            r'\bahora\b': ('hours', 0),
            r'\ben (\d+) horas?\b': ('hours', 'match'),
            r'\ben (\d+) días?\b': ('days', 'match'),
            r'\ben (\d+) semanas?\b': ('weeks', 'match'),
            r'\ben (\d+) meses?\b': ('months', 'match'),
            r'\bla próxima semana\b': ('weeks', 1),
            r'\bel próximo mes\b': ('months', 1),
        }
        
        self.weekdays = {
            'lunes': 0, 'martes': 1, 'miércoles': 2, 'miercoles': 2,
            'jueves': 3, 'viernes': 4, 'sábado': 5, 'sabado': 5,
            'domingo': 6
        }
    
    def extract(self, text: str, reference_date: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Extract date/time from text.
        
        Args:
            text: Input text
            reference_date: Reference date (default: now)
        
        Returns:
            Dict with extracted datetime info
        """
        if reference_date is None:
            reference_date = datetime.now()
        
        text_lower = text.lower()
        
        # Try relative patterns
        result = self._extract_relative(text_lower, reference_date)
        if result:
            return result
        
        # Try weekday patterns
        result = self._extract_weekday(text_lower, reference_date)
        if result:
            return result
        
        # Try absolute date parsing
        result = self._extract_absolute(text)
        if result:
            return result
        
        return {"found": False}
    
    def _extract_relative(self, text: str, ref_date: datetime) -> Optional[Dict[str, Any]]:
        """Extract relative dates (mañana, en 2 días, etc)."""
        for pattern, (unit, value) in self.relative_patterns.items():
            match = re.search(pattern, text)
            if match:
                if value == 'match':
                    value = int(match.group(1))
                
                if unit == 'days':
                    target_date = ref_date + timedelta(days=value)
                elif unit == 'hours':
                    target_date = ref_date + timedelta(hours=value)
                elif unit == 'weeks':
                    target_date = ref_date + timedelta(weeks=value)
                elif unit == 'months':
                    target_date = ref_date + relativedelta(months=value)
                else:
                    continue
                
                return {
                    "found": True,
                    "datetime": target_date,
                    "type": "relative",
                    "pattern": pattern,
                    "text": match.group(0)
                }
        
        return None
    
    def _extract_weekday(self, text: str, ref_date: datetime) -> Optional[Dict[str, Any]]:
        """Extract weekday references (el lunes, próximo martes, etc)."""
        for day_name, day_num in self.weekdays.items():
            if day_name in text:
                # Calculate next occurrence of this weekday
                current_weekday = ref_date.weekday()
                days_ahead = day_num - current_weekday
                
                if days_ahead <= 0:  # Target day already passed this week
                    days_ahead += 7
                
                target_date = ref_date + timedelta(days=days_ahead)
                
                return {
                    "found": True,
                    "datetime": target_date,
                    "type": "weekday",
                    "weekday": day_name,
                    "text": day_name
                }
        
        return None
    
    def _extract_absolute(self, text: str) -> Optional[Dict[str, Any]]:
        """Extract absolute dates (15/11/2025, 15 de noviembre, etc)."""
        try:
            # Try parsing with dateutil
            parsed_date = date_parser.parse(text, fuzzy=True)
            
            return {
                "found": True,
                "datetime": parsed_date,
                "type": "absolute",
                "text": text
            }
        except (ValueError, OverflowError):
            return None
    
    def extract_time(self, text: str) -> Optional[Dict[str, Any]]:
        """
        Extract time from text (10:30, 15h, a las tres, etc).
        
        Args:
            text: Input text
        
        Returns:
            Dict with extracted time info
        """
        text_lower = text.lower()
        
        # Pattern: HH:MM (10:30, 15:45)
        time_pattern = r'\b(\d{1,2}):(\d{2})\b'
        match = re.search(time_pattern, text)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2))
            
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return {
                    "found": True,
                    "hour": hour,
                    "minute": minute,
                    "text": match.group(0)
                }
        
        # Pattern: HH (15h, 15 horas)
        hour_pattern = r'\b(\d{1,2})h\b|\b(\d{1,2}) horas?\b'
        match = re.search(hour_pattern, text_lower)
        if match:
            hour = int(match.group(1) or match.group(2))
            
            if 0 <= hour <= 23:
                return {
                    "found": True,
                    "hour": hour,
                    "minute": 0,
                    "text": match.group(0)
                }
        
        return {"found": False}


# Convenience function
def extract_datetime(text: str, reference_date: Optional[datetime] = None) -> Dict[str, Any]:
    """Extract datetime from text."""
    extractor = DateTimeExtractor()
    return extractor.extract(text, reference_date)
