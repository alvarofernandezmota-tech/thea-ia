"""
DateTimeParser - Extractor avanzado de entidades temporales y de participantes

Extrae del mensaje del usuario:
- Fechas (mañana, próximo lunes, el 15 de enero, en 3 días, 04/12/2025)
- Horas (3pm, las 3 de la tarde, 15:00)
- Participantes (nombres, emails)
- Ubicación (sala, online, etc)
- Duración (2 horas, 30 minutos)

Soporta español e inglés con timezone awareness.

Autor: Álvaro Fernández Mota
Fecha: 09 Dic 2025
"""

import re
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple, Any
import logging
import pytz
from dateutil import parser as dateutil_parser
from dateutil.relativedelta import relativedelta

logger = logging.getLogger(__name__)


class DateTimeParser:
    """
    Extrae entidades temporales de mensajes en español e inglés.
    
    Características:
    - Fechas relativas (mañana, próximo lunes, en 3 días)
    - Fechas absolutas (el 15 de enero, 04/12/2025)
    - Horas (3pm, las 3 de la tarde, 15:00)
    - Participantes (nombres, emails)
    - Ubicación (sala, online)
    - Duración (2 horas, 30 minutos)
    """
    
    # Patrones regex compilados
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    TIME_PATTERN_24H = re.compile(r'\b([01]?[0-9]|2[0-3])[:.]?([0-5][0-9])\b')
    TIME_PATTERN_12H = re.compile(
        r'\b(1[0-2]|0?[1-9])\s*(:[0-5][0-9])?\s*(am|pm|a\.m\.|p\.m\.|AM|PM|A\.M\.|P\.M\.)\b'
    )
    DATE_PATTERN_DMY = re.compile(r'(\d{1,2})[/-](\d{1,2})[/-](\d{4})')
    DATE_PATTERN_YMD = re.compile(r'(\d{4})-(\d{1,2})-(\d{1,2})')
    
    # Mapeos de palabras clave
    SPANISH_MONTHS = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
        "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
        "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    SPANISH_WEEKDAYS = {
        "lunes": 0, "martes": 1, "miércoles": 2, "miercoles": 2,
        "jueves": 3, "viernes": 4, "sábado": 5, "sabado": 5, "domingo": 6
    }
    
    ENGLISH_WEEKDAYS = {
        "monday": 0, "tuesday": 1, "wednesday": 2, "thursday": 3,
        "friday": 4, "saturday": 5, "sunday": 6
    }
    
    def __init__(self, timezone: str = "UTC"):
        """
        Inicializa el parser con timezone.
        
        Args:
            timezone: Timezone string (e.g., "UTC", "Europe/Madrid", "America/New_York")
        """
        try:
            self.tz = pytz.timezone(timezone)
        except pytz.exceptions.UnknownTimeZoneError:
            logger.warning(f"Unknown timezone {timezone}, using UTC")
            self.tz = pytz.UTC
    
    
    @staticmethod
    def parse_date(message: str, base_date: Optional[datetime] = None) -> Optional[datetime]:
        """
        Extrae fecha del mensaje (versión estática).
        
        Soporta:
        - "mañana" → tomorrow
        - "pasado mañana" → day after tomorrow
        - "hoy" → today
        - "próximo lunes" → next Monday
        - "el 15 de enero" → Jan 15
        - "en 3 días" → today + 3 days
        - "04/12/2025" → Dec 4, 2025
        
        Args:
            message: Mensaje del usuario
            base_date: Fecha base (default: now)
            
        Returns:
            datetime object o None
        """
        parser = DateTimeParser()
        return parser.parse_datetime(message, base_date=base_date, extract_type="date")
    
    
    @staticmethod
    def parse_time(message: str) -> Optional[str]:
        """
        Extrae hora del mensaje (versión estática).
        
        Soporta:
        - "a las 3pm" → "15:00"
        - "las 3 de la tarde" → "15:00"
        - "15:00" → "15:00"
        - "3:30pm" → "15:30"
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Hora en formato "HH:MM" o None
        """
        parser = DateTimeParser()
        return parser.extract_time(message)
    
    
    @staticmethod
    def parse_participants(message: str) -> List[str]:
        """
        Extrae nombres de participantes (versión estática).
        
        Soporta:
        - "con Juan y María" → ["Juan", "María"]
        - "con juan@email.com" → ["juan@email.com"]
        - "invitar a juan" → ["juan"]
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Lista de nombres/emails
        """
        parser = DateTimeParser()
        return parser.extract_participants(message)
    
    
    @staticmethod
    def parse_location(message: str) -> Optional[str]:
        """
        Extrae ubicación del evento (versión estática).
        
        Soporta:
        - "en sala 5" → "sala 5"
        - "reunión online" → "online"
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Ubicación o None
        """
        parser = DateTimeParser()
        return parser.extract_location(message)
    
    
    @staticmethod
    def parse_all(message: str) -> Dict[str, Any]:
        """
        Extrae TODAS las entidades del mensaje (versión estática).
        
        Args:
            message: Mensaje del usuario
            
        Returns:
            Dict con todas las entidades extraídas
        """
        parser = DateTimeParser()
        return parser.extract_all(message)
    
    
    # ==================== MÉTODOS DE INSTANCIA ====================
    
    def parse_datetime(
        self,
        datetime_str: str,
        base_date: Optional[datetime] = None,
        extract_type: str = "full"
    ) -> Optional[datetime]:
        """
        Método principal de parsing. Intenta múltiples estrategias.
        
        Args:
            datetime_str: Natural language datetime string
            base_date: Base datetime para cálculos relativos
            extract_type: "full", "date", "time"
            
        Returns:
            datetime object o None
        """
        if not datetime_str:
            return None
        
        if base_date is None:
            base_date = datetime.now(self.tz)
        elif base_date.tzinfo is None:
            base_date = self.tz.localize(base_date)
        
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
            if result.tzinfo is None:
                result = self.tz.localize(result)
            return result
        except Exception as e:
            logger.debug(f"dateutil parsing failed: {e}")
        
        return None
    
    
    def _parse_relative(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse relative time expressions (en 2 horas, in 30 minutes)."""
        
        # Spanish: en N horas/minutos/días
        match = re.search(r'en\s+(\d+)\s+hora(?:s)?', datetime_str)
        if match:
            hours = int(match.group(1))
            return base_date + timedelta(hours=hours)
        
        match = re.search(r'en\s+(\d+)\s+minuto(?:s)?', datetime_str)
        if match:
            minutes = int(match.group(1))
            return base_date + timedelta(minutes=minutes)
        
        match = re.search(r'en\s+(\d+)\s+día(?:s)?', datetime_str)
        if match:
            days = int(match.group(1))
            result = base_date + timedelta(days=days)
            time_str = self.extract_time(datetime_str)
            if time_str:
                time_obj = self._parse_time_string(time_str)
                if time_obj:
                    result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
            return result
        
        # English: in N hours/minutes/days
        match = re.search(r'in\s+(\d+)\s+hour(?:s)?', datetime_str)
        if match:
            hours = int(match.group(1))
            return base_date + timedelta(hours=hours)
        
        match = re.search(r'in\s+(\d+)\s+minute(?:s)?', datetime_str)
        if match:
            minutes = int(match.group(1))
            return base_date + timedelta(minutes=minutes)
        
        match = re.search(r'in\s+(\d+)\s+day(?:s)?', datetime_str)
        if match:
            days = int(match.group(1))
            result = base_date + timedelta(days=days)
            time_str = self.extract_time(datetime_str)
            if time_str:
                time_obj = self._parse_time_string(time_str)
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
            time_str = self.extract_time(datetime_str)
            if time_str:
                time_obj = self._parse_time_string(time_str)
                if time_obj:
                    result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
            else:
                result = result.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return result
    
    
    def _parse_day_names(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse day names (el viernes, on monday)."""
        
        target_day = None
        
        # Check Spanish day names
        for day_name, day_num in self.SPANISH_WEEKDAYS.items():
            if re.search(rf'\b{day_name}\b', datetime_str):
                target_day = day_num
                break
        
        # Check English day names
        if target_day is None:
            for day_name, day_num in self.ENGLISH_WEEKDAYS.items():
                if re.search(rf'\b{day_name}\b', datetime_str):
                    target_day = day_num
                    break
        
        if target_day is None:
            return None
        
        # Calculate next occurrence of target day
        current_day = base_date.weekday()
        days_ahead = target_day - current_day
        
        if days_ahead <= 0:
            days_ahead += 7
        
        result = base_date + timedelta(days=days_ahead)
        result = result.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Try to extract time
        time_str = self.extract_time(datetime_str)
        if time_str:
            time_obj = self._parse_time_string(time_str)
            if time_obj:
                result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
        else:
            result = result.replace(hour=9, minute=0, second=0, microsecond=0)
        
        return result
    
    
    def _parse_explicit_date(self, datetime_str: str, base_date: datetime) -> Optional[datetime]:
        """Parse explicit date formats (DD/MM/YYYY, YYYY-MM-DD)."""
        
        # DD/MM/YYYY or DD-MM-YYYY
        match = self.DATE_PATTERN_DMY.search(datetime_str)
        if match:
            day = int(match.group(1))
            month = int(match.group(2))
            year = int(match.group(3))
            
            try:
                result = datetime(year, month, day, tzinfo=self.tz)
                
                time_str = self.extract_time(datetime_str)
                if time_str:
                    time_obj = self._parse_time_string(time_str)
                    if time_obj:
                        result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                else:
                    result = result.replace(hour=9, minute=0, second=0, microsecond=0)
                
                return result
            except ValueError:
                pass
        
        # YYYY-MM-DD
        match = self.DATE_PATTERN_YMD.search(datetime_str)
        if match:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            
            try:
                result = datetime(year, month, day, tzinfo=self.tz)
                
                time_str = self.extract_time(datetime_str)
                if time_str:
                    time_obj = self._parse_time_string(time_str)
                    if time_obj:
                        result = result.replace(hour=time_obj.hour, minute=time_obj.minute, second=0, microsecond=0)
                else:
                    result = result.replace(hour=9, minute=0, second=0, microsecond=0)
                
                return result
            except ValueError:
                pass
        
        return None
    
    
    def extract_time(self, message: str) -> Optional[str]:
        """
        Extrae hora del mensaje.
        
        Retorna: Hora en formato "HH:MM" o None
        """
        message_lower = message.lower()
        
        # CASO 1: Formato 24H (HH:MM o HH.MM)
        match = self.TIME_PATTERN_24H.search(message_lower)
        if match:
            hour = match.group(1).zfill(2)
            minute = match.group(2) if match.group(2) else "00"
            return f"{hour}:{minute}"
        
        # CASO 2: Formato 12H con am/pm
        match = self.TIME_PATTERN_12H.search(message_lower)
        if match:
            hour = int(match.group(1))
            minute = match.group(2)[1:] if match.group(2) else "00"
            period = match.group(3).lower()
            
            is_pm = "p" in period
            if is_pm and hour != 12:
                hour += 12
            elif not is_pm and hour == 12:
                hour = 0
            
            return f"{hour:02d}:{minute}"
        
        # CASO 3: "las 3 de la tarde" o "las 3 de la mañana"
        pattern = r'las\s+(\d{1,2})\s+de\s+la\s+(tarde|mañana|noche)'
        match = re.search(pattern, message_lower)
        if match:
            hour = int(match.group(1))
            period = match.group(2)
            
            if period == "tarde":
                hour = hour if hour == 12 else hour + 12
            elif period == "noche":
                hour = hour if hour >= 9 else hour + 12
            
            return f"{hour:02d}:00"
        
        # CASO 4: "a las 3"
        pattern = r'a\s+las\s+(\d{1,2})'
        match = re.search(pattern, message_lower)
        if match and "tarde" not in message_lower and "pm" not in message_lower:
            hour = int(match.group(1))
            return f"{hour:02d}:00"
        
        return None
    
    
    def extract_participants(self, message: str) -> List[str]:
        """
        Extrae nombres de participantes.
        
        Retorna: Lista de nombres/emails
        """
        participants = []
        
        # CASO 1: Emails
        emails = self.EMAIL_PATTERN.findall(message)
        participants.extend(emails)
        
        # CASO 2: Patrones "con [nombre] y [nombre]"
        pattern = r'con\s+([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)?)(?:\s+y\s+([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)?))*'
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            name1 = match.group(1).strip()
            if name1 and name1 not in participants:
                participants.append(name1)
            name2 = match.group(2)
            if name2 and name2.strip() not in participants:
                participants.append(name2.strip())
        
        # CASO 3: Patrones "a [nombre]" después de "invitar"
        pattern = r'invitar\s+a\s+([a-záéíóúñ]+(?:\s+[a-záéíóúñ]+)?)'
        match = re.search(pattern, message, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if name not in participants:
                participants.append(name)
        
        return list(set(participants))
    
    
    def extract_location(self, message: str) -> Optional[str]:
        """
        Extrae ubicación del evento.
        
        Retorna: Ubicación o None
        """
        message_lower = message.lower()
        
        # CASO 1: "en [lugar]"
        pattern = r'en\s+([a-záéíóúñ0-9\s]+?)(?:\s+(?:a|con|para|de)\s|$)'
        match = re.search(pattern, message_lower)
        if match:
            location = match.group(1).strip()
            if location and location not in ["evento", "reunión", "cita", "meeting"]:
                return location
        
        # CASO 2: Palabras clave de ubicación
        online_keywords = ["online", "virtual", "zoom", "meet", "teams", "remoto"]
        for keyword in online_keywords:
            if keyword in message_lower:
                return keyword
        
        return None
    
    
    def extract_title(self, message: str) -> Optional[str]:
        """
        Extrae título/nombre del evento.
        
        Retorna: Título o None
        """
        # CASO 1: Texto entre comillas
        pattern = r'[\'"]([a-záéíóúñA-ZÁÉÍÓÚÑ\s]+)[\'"]'
        match = re.search(pattern, message)
        if match:
            return match.group(1).strip()
        
        # CASO 2: Después de palabras clave
        keywords = ["llamado", "titulado", "sobre", "de"]
        for keyword in keywords:
            pattern = f'{keyword}\\s+([a-záéíóúñA-ZÁÉÍÓÚÑ\\s]+?)(?:\\s+(?:con|en|a)\\s|$)'
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                if len(title) > 2:
                    return title
        
        return None
    
    
    def extract_all(self, message: str) -> Dict[str, Any]:
        """
        Extrae TODAS las entidades del mensaje.
        
        Retorna: Dict con todas las entidades extraídas
        """
        return {
            "title": self.extract_title(message),
            "date": self.parse_datetime(message, extract_type="date"),
            "time": self.extract_time(message),
            "participants": self.extract_participants(message),
            "location": self.extract_location(message),
            "raw_message": message
        }
    
    
    def _parse_time_string(self, time_str: str) -> Optional[datetime]:
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
        
        Returns: timedelta object or None
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
        if not dt:
            return ""
        
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