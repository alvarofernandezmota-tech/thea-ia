"""
DateTime Parser for AgendaAgent

Parses natural language date/time expressions into Python datetime objects.
Supports Spanish and English, relative and absolute dates.
"""

import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta
import pytz


class DateTimeParser:
    """
    Parses natural language date/time strings into datetime objects.
    
    Supports:
    - Absolute dates: "mañana a las 3pm", "el viernes", "04/12/2025"
    - Relative times: "en 2 horas", "en 30 minutos"
    - Day names: "lunes", "monday"
    - Times: "a las 3pm", "at 15:00"
    """
    
    def __init__(self, timezone: str = "UTC"):
        """
        Initialize parser with timezone.
        
        Args:
            timezone: Timezone string (e.g., "UTC", "Europe/Madrid", "America/New_York")
        """
        self.tz = pytz.timezone(timezone)
        
        # Spanish day names mapping
        self.spanish_days = {
            "lunes": 0,
            "martes": 1,
            "miércoles": 2,
            "miercoles": 2,  # Without accent
            "jueves": 3,
            "viernes": 4,
            "sábado": 5,
            "sabado": 5,  # Without accent
            "domingo": 6,
        }
        
        # English day names mapping
        self.english_days = {
            "monday": 0,
            "tuesday": 1,
            "wednesday": 2,
            "thursday": 3,
            "friday": 4,
            "saturday": 5,
            "sunday": 6,
        }
        
        # Relative time patterns
        self.relative_patterns = {
            # Spanish
            "en_hours": r'en\s+(\d+)\s+hora(?:s)?',
            "en_minutes": r'en\s+(\d+)\s+minuto(?:s)?',
            "en_days": r'en\s+(\d+)\s+día(?:s)?',
            # English
            "in_hours": r'in\s+(\d+)\s+hour(?:s)?',
            "in_minutes": r'in\s+(\d+)\s+minute(?:s)?',
            "in_days": r'in\s+(\d+)\s+day(?:s)?',
        }
    
    def parse(self, datetime_str: str, base_date: Optional[datetime] = None) -> Optional[datetime]:
        """
        Main parsing method. Tries multiple strategies to parse the datetime string.
        
        Args:
            datetime_str: Natural language datetime string
            base_date: Base datetime for relative calculations (defaults to now)
            
        Returns:
            Parsed datetime object or None if parsing fails
        """
        if not datetime_str:
            return None
        
        if base_date is None:
            base_date = datetime.now(self.tz)
        
        datetime_str = datetime_str.lower().strip()
        
        # Strategy 1: Relative times (en 2 horas, in 30 minutes)
        result = self._parse_relative(datetime_str, base_date)
        if result:
            return result
        
        # Strategy 2: Special keywords (hoy, mañana, today, tomorrow)
        result = self._parse_keywords(datetime_str, base_date)
        if result:
            return result
        
        # Strategy 3: Day names (el viernes, on monday)
        result = self._parse_day_names(datetime_str, base_date)
        if result:
            return result
        
        # Strategy 4: Explicit dates (04/12/2025, 2025-12-04)
        result = self._parse_explicit_date(datetime_str, base_date)
        if result:
            return result
        
        # Strategy 5: Use dateutil as fallback
        try:
            result = dateutil_parser.parse(datetime_str, default=base_date, fuzzy=True)
            # Ensure timezone awareness
            if result.tzinfo is None:
                result = self.tz.localize(result)
            return result
        except:
            pass
        
        return None
    
    def _parse_relative(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse relative time expressions."""
        
        # Hours
        for pattern_name in ["en_hours", "in_hours"]:
            match = re.search(self.relative_patterns[pattern_name], datetime_str, re.IGNORECASE)
            if match:
                hours = int(match.group(1))
                return base_date + timedelta(hours=hours)
        
        # Minutes
        for pattern_name in ["en_minutes", "in_minutes"]:
            match = re.search(self.relative_patterns[pattern_name], datetime_str, re.IGNORECASE)
            if match:
                minutes = int(match.group(1))
                return base_date + timedelta(minutes=minutes)
        
        # Days
        for pattern_name in ["en_days", "in_days"]:
            match = re.search(self.relative_patterns[pattern_name], datetime_str, re.IGNORECASE)
            if match:
                days = int(match.group(1))
                result = base_date + timedelta(days=days)
                # Try to extract time if specified
                time_str = self._extract_time(datetime_str)
                if time_str:
                    time_obj = self._parse_time(time_str)
                    if time_obj:
                        result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                return result
        
        return None
    
    def _parse_keywords(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse keyword-based expressions (hoy, mañana, today, tomorrow)."""
        
        result = None
        
        # Spanish keywords
        if re.search(r'\bhoy\b', datetime_str):
            result = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif re.search(r'\bmañana\b', datetime_str):
            result = (base_date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        elif re.search(r'\bpasado\s+mañana\b', datetime_str):
            result = (base_date + timedelta(days=2)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # English keywords
        elif re.search(r'\btoday\b', datetime_str):
            result = base_date.replace(hour=0, minute=0, second=0, microsecond=0)
        elif re.search(r'\btomorrow\b', datetime_str):
            result = (base_date + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        
        # If we found a day, try to extract time
        if result:
            time_str = self._extract_time(datetime_str)
            if time_str:
                time_obj = self._parse_time(time_str)
                if time_obj:
                    result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
            else:
                # Default to 9 AM if no time specified
                result = result.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return result
    
    def _parse_day_names(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse day names (el viernes, on monday)."""
        
        target_day = None
        
        # Check Spanish day names
        for day_name, day_num in self.spanish_days.items():
            if re.search(rf'\b{day_name}\b', datetime_str):
                target_day = day_num
                break
        
        # Check English day names
        if target_day is None:
            for day_name, day_num in self.english_days.items():
                if re.search(rf'\b{day_name}\b', datetime_str):
                    target_day = day_num
                    break
        
        if target_day is None:
            return None
        
        # Calculate next occurrence of target day
        current_day = base_date.weekday()
        days_ahead = target_day - current_day
        
        # If the day has already passed this week, go to next week
        if days_ahead <= 0:
            days_ahead += 7
        
        result = base_date + timedelta(days=days_ahead)
        result = result.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Try to extract time
        time_str = self._extract_time(datetime_str)
        if time_str:
            time_obj = self._parse_time(time_str)
            if time_obj:
                result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
        else:
            # Default to 9 AM
            result = result.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return result
    
    def _parse_explicit_date(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse explicit date formats (DD/MM/YYYY, YYYY-MM-DD)."""
        
        # DD/MM/YYYY or DD-MM-YYYY
        match = re.search(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})', datetime_str)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))
            
            try:
                result = datetime(year, month, day, tzinfo=self.tz)
                
                # Try to extract time
                time_str = self._extract_time(datetime_str)
                if time_str:
                    time_obj = self._parse_time(time_str)
                    if time_obj:
                        result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                else:
                    result = result.replace(hour=9, minute=0, second=0, microsecond=0)
                
                return result
            except ValueError:
                pass
        
        # YYYY-MM-DD
        match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', datetime_str)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            
            try:
                result = datetime(year, month, day, tzinfo=self.tz)
                
                # Try to extract time
                time_str = self._extract_time(datetime_str)
                if time_str:
                    time_obj = self._parse_time(time_str)
                    if time_obj:
                        result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                else:
                    result = result.replace(hour=9, minute=0, second=0, microsecond=0)
                
                return result
            except ValueError:
                pass
        
        return None
    
    def _extract_time(self, datetime_str: str) -> Optional[str]:
        """Extract time component from string."""
        patterns = [
            r'a\s+las\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?)',
            r'at\s+(\d{1,2}(?::\d{2})?\s*(?:am|pm|AM|PM)?)',
            r'(\d{1,2}:\d{2}\s*(?:am|pm|AM|PM)?)',
            r'(\d{1,2}\s*(?:am|pm|AM|PM))',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, datetime_str, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def _parse_time(self, time_str: str) -> Optional[datetime]:
        """Parse time string into datetime object (date part ignored)."""
        time_str = time_str.strip().lower()
        
        # Handle AM/PM
        is_pm = 'pm' in time_str
        is_am = 'am' in time_str
        time_str = re.sub(r'\s*(?:am|pm)', '', time_str, flags=re.IGNORECASE)
        
        # Parse HH:MM or HH
        if ':' in time_str:
            parts = time_str.split(':')
            try:
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
            except ValueError:
                return None
        else:
            try:
                hour = int(time_str)
                minute = 0
            except ValueError:
                return None
        
        # Apply AM/PM
        if is_pm and hour < 12:
            hour += 12
        elif is_am and hour == 12:
            hour = 0
        
        # Validate
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            return None
        
        return datetime.now().replace(hour=hour, minute=minute, second=0, microsecond=0)
    
    def parse_duration(self, duration_str: str) -> Optional[timedelta]:
        """
        Parse duration strings like "2 horas", "30 minutos", "1 día"
        
        Returns:
            timedelta object or None
        """
        duration_str = duration_str.lower().strip()
        
        # Hours
        match = re.search(r'(\d+)\s+hora(?:s)?', duration_str)
        if match:
            return timedelta(hours=int(match.group(1)))
        
        match = re.search(r'(\d+)\s+hour(?:s)?', duration_str)
        if match:
            return timedelta(hours=int(match.group(1)))
        
        # Minutes
        match = re.search(r'(\d+)\s+minuto(?:s)?', duration_str)
        if match:
            return timedelta(minutes=int(match.group(1)))
        
        match = re.search(r'(\d+)\s+minute(?:s)?', duration_str)
        if match:
            return timedelta(minutes=int(match.group(1)))
        
        # Days
        match = re.search(r'(\d+)\s+día(?:s)?', duration_str)
        if match:
            return timedelta(days=int(match.group(1)))
        
        match = re.search(r'(\d+)\s+day(?:s)?', duration_str)
        if match:
            return timedelta(days=int(match.group(1)))
        
        return None
    
    def format_datetime(self, dt: datetime, format_type: str = "full") -> str:
        """
        Format datetime into human-readable string.
        
        Args:
            dt: datetime object
            format_type: "full", "date_only", "time_only", "short"
            
        Returns:
            Formatted string
        """
        if format_type == "full":
            return dt.strftime("%d/%m/%Y %H:%M")
        elif format_type == "date_only":
            return dt.strftime("%d/%m/%Y")
        elif format_type == "time_only":
            return dt.strftime("%H:%M")
        elif format_type == "short":
            return dt.strftime("%d/%m %H:%M")
        else:
            return str(dt)

