"""
Availability Engine - Manage available time slots
Conversational calendar logic without commands
100% FLEXIBLE - User decides ALL scheduling
"""

import logging
from typing import List, Dict, Optional
from datetime import datetime, timedelta, time

from theaia.services.booking_service import BookingService

logger = logging.getLogger(__name__)


class AvailabilityEngine:
    """Engine for calculating available time slots - 24/7 flexible scheduling"""
    
    def __init__(self):
        """Initialize availability engine"""
        self.booking_service = BookingService()
        
        # NO business hours restrictions - User decides everything
        self.business_hours = None  # No restrictions
        self.allow_24_7 = True  # Allow scheduling anytime
        
        # Default slot duration (minutes)
        self.slot_duration = 60
        
        # Minimum advance booking time (hours)
        self.min_advance_hours = 2
    
    def get_available_slots(
        self,
        date: datetime,
        duration_minutes: int = 60
    ) -> List[datetime]:
        """
        Get all available time slots for a specific date
        NO RESTRICTIONS - User can schedule 24/7
        Called when user says: "¿Qué horarios tienes disponibles mañana?"
        
        Args:
            date: Date to check
            duration_minutes: Appointment duration
        
        Returns:
            List of available datetime slots
        """
        try:
            # Check if date is in the past
            if date.date() < datetime.now().date():
                logger.warning(f"⚠️ Date is in the past: {date}")
                return []
            
            # Generate slots for entire day (00:00 - 23:59)
            # User can schedule ANYTIME - no day/hour restrictions
            all_slots = self._generate_slots_for_day(
                date,
                time(0, 0),   # Start at midnight
                time(23, 59),  # End before next midnight
                duration_minutes
            )
            
            # Filter out past slots (if today)
            now = datetime.now()
            min_booking_time = now + timedelta(hours=self.min_advance_hours)
            
            if date.date() == now.date():
                all_slots = [
                    slot for slot in all_slots
                    if slot >= min_booking_time
                ]
            
            # Filter out booked slots (ONLY restriction is conflicts)
            available_slots = []
            for slot in all_slots:
                end_time = slot + timedelta(minutes=duration_minutes)
                
                if not self.booking_service.check_conflict(slot, end_time):
                    available_slots.append(slot)
            
            logger.info(f"✅ Found {len(available_slots)} available slots for {date.date()} (24/7 scheduling)")
            return available_slots
            
        except Exception as e:
            logger.error(f"❌ Error getting available slots: {e}")
            return []
    
    def _generate_slots_for_day(
        self,
        date: datetime,
        start_time: time,
        end_time: time,
        duration_minutes: int
    ) -> List[datetime]:
        """
        Generate all possible time slots for a day
        
        Args:
            date: Date
            start_time: Start time (default 00:00)
            end_time: End time (default 23:59)
            duration_minutes: Slot duration
        
        Returns:
            List of datetime slots
        """
        slots = []
        
        # Combine date with start time
        current_slot = datetime.combine(date.date(), start_time)
        # End of day boundary (00:00 next day)
        end_of_day = datetime.combine(date.date() + timedelta(days=1), time(0, 0))
        
        # Generate slots for entire time range
        # Include slots that end at or before end_of_day
        while current_slot + timedelta(minutes=duration_minutes) <= end_of_day:
            slots.append(current_slot)
            current_slot += timedelta(minutes=self.slot_duration)
        
        return slots
    
    def is_business_hours(self, dt: datetime) -> bool:
        """
        Check if datetime is valid for scheduling
        Since we allow 24/7, always return True
        
        Args:
            dt: Datetime to check
        
        Returns:
            Always True (no restrictions)
        """
        # User can schedule anytime - no restrictions
        return True
    
    def get_next_available_slot(
        self,
        duration_minutes: int = 60,
        days_ahead: int = 7
    ) -> Optional[datetime]:
        """
        Get the next available slot
        Called when user says: "Dame el próximo horario disponible"
        
        Args:
            duration_minutes: Appointment duration
            days_ahead: How many days to look ahead
        
        Returns:
            Next available datetime or None
        """
        try:
            start_date = datetime.now().date()
            
            for i in range(days_ahead):
                check_date = datetime.combine(
                    start_date + timedelta(days=i),
                    time(0, 0)
                )
                
                slots = self.get_available_slots(check_date, duration_minutes)
                
                if slots:
                    logger.info(f"✅ Next available slot: {slots[0]}")
                    return slots[0]
            
            logger.warning(f"⚠️ No available slots in next {days_ahead} days")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting next available slot: {e}")
            return None
    
    def get_available_slots_for_week(
        self,
        start_date: Optional[datetime] = None,
        duration_minutes: int = 60
    ) -> Dict[str, List[datetime]]:
        """
        Get available slots for the entire week (including weekends)
        Called when user says: "Muéstrame disponibilidad de esta semana"
        
        Args:
            start_date: Start of week (default: today)
            duration_minutes: Appointment duration
        
        Returns:
            Dict with dates as keys and slots as values
        """
        try:
            if not start_date:
                start_date = datetime.now()
            
            week_availability = {}
            
            for i in range(7):
                check_date = datetime.combine(
                    start_date.date() + timedelta(days=i),
                    time(0, 0)
                )
                
                slots = self.get_available_slots(check_date, duration_minutes)
                
                if slots:
                    date_key = check_date.strftime('%Y-%m-%d')
                    week_availability[date_key] = slots
            
            logger.info(f"✅ Week availability: {len(week_availability)} days with slots")
            return week_availability
            
        except Exception as e:
            logger.error(f"❌ Error getting week availability: {e}")
            return {}
    
    def format_slots_for_display(
        self,
        slots: List[datetime],
        max_slots: int = 6
    ) -> List[str]:
        """
        Format slots for user-friendly display
        
        Args:
            slots: List of datetime slots
            max_slots: Maximum slots to display
        
        Returns:
            List of formatted time strings
        """
        if not slots:
            return []
        
        # Limit to max_slots
        display_slots = slots[:max_slots]
        
        # Format as "HH:MM"
        formatted = [slot.strftime('%H:%M') for slot in display_slots]
        
        return formatted
    
    def parse_natural_time(self, time_str: str) -> Optional[time]:
        """
        Parse natural language time
        Examples: "3 de la tarde", "15:00", "tres y media", "3 de la mañana"
        
        Args:
            time_str: Natural language time string
        
        Returns:
            time object or None
        """
        # Simplified version - in production use NLP
        
        time_str = time_str.lower().strip()
        
        # Try direct time format (HH:MM)
        try:
            if ':' in time_str:
                hour, minute = map(int, time_str.split(':'))
                return time(hour, minute)
        except:
            pass
        
        # Common Spanish phrases (24 hours support)
        time_mappings = {
            'medianoche': time(0, 0),
            '1 de la mañana': time(1, 0),
            '2 de la mañana': time(2, 0),
            '3 de la mañana': time(3, 0),
            'mediodía': time(12, 0),
            '12': time(12, 0),
            '1': time(13, 0),
            '2': time(14, 0),
            '3': time(15, 0),
            '3 de la tarde': time(15, 0),
            '4': time(16, 0),
            '5': time(17, 0),
            '6': time(18, 0),
            '7': time(19, 0),
            '8': time(20, 0),
            '9': time(21, 0),
            '10': time(22, 0),
            '11': time(23, 0),
        }
        
        for phrase, time_obj in time_mappings.items():
            if phrase in time_str:
                return time_obj
        
        logger.warning(f"⚠️ Could not parse time: {time_str}")
        return None
    
    def parse_natural_date(self, date_str: str) -> Optional[datetime]:
        """
        Parse natural language date
        Examples: "mañana", "el jueves", "sábado", "domingo", "15 de diciembre"
        
        Args:
            date_str: Natural language date string
        
        Returns:
            datetime object or None
        """
        # Simplified version - in production use NLP
        
        date_str = date_str.lower().strip()
        now = datetime.now()
        
        # Common Spanish phrases
        if 'hoy' in date_str:
            return now
        
        if 'mañana' in date_str:
            return now + timedelta(days=1)
        
        if 'pasado mañana' in date_str:
            return now + timedelta(days=2)
        
        # Weekdays (including weekends)
        weekdays = {
            'lunes': 0,
            'martes': 1,
            'miércoles': 2,
            'miercoles': 2,
            'jueves': 3,
            'viernes': 4,
            'sábado': 5,
            'sabado': 5,
            'domingo': 6
        }
        
        for day_name, day_num in weekdays.items():
            if day_name in date_str:
                days_ahead = (day_num - now.weekday()) % 7
                if days_ahead == 0:
                    days_ahead = 7  # Next week
                return now + timedelta(days=days_ahead)
        
        logger.warning(f"⚠️ Could not parse date: {date_str}")
        return None
    
    def configure_business_hours(
        self,
        day_of_week: int,
        start_time: Optional[time],
        end_time: Optional[time]
    ):
        """
        Optional: Configure user preferences for specific days
        NOT restrictions - just suggestions
        User can still override conversationally
        
        Args:
            day_of_week: 0=Monday, 6=Sunday
            start_time: Preferred start time
            end_time: Preferred end time
        """
        # This is now optional and doesn't restrict scheduling
        logger.info(f"ℹ️ User preference noted for day {day_of_week}, but not enforced")
        logger.info(f"ℹ️ User can still schedule outside these hours conversationally")
    
    def close(self):
        """Close resources"""
        if self.booking_service:
            self.booking_service.close()
