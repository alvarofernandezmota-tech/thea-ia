# Archivo: src/theaia/tests/e2e/test_agenda_agent_e2e.py

"""
End-to-end tests for AgendaAgent.
Tests complete workflows for calendar event management.
"""

import pytest
from datetime import datetime, timedelta
from src.theaia.agents.agenda_agent.handler import AgendaAgent
from src.theaia.agents.base_agent import AgentConfig


class TestAgendaAgentE2E:
    """End-to-end tests for AgendaAgent."""
    
    @pytest.fixture
    def agenda_agent(self):
        """Create AgendaAgent instance for testing."""
        config = AgentConfig(name="AgendaAgent_Test", log_level="ERROR")
        return AgendaAgent(config=config)
    
    def test_agent_initialization(self, agenda_agent):
        """Test AgendaAgent initialization."""
        assert agenda_agent.config.name == "AgendaAgent_Test"
        assert len(agenda_agent.conversation_managers) == 0
    
    def test_get_supported_intents(self, agenda_agent):
        """Test supported intents list."""
        intents = agenda_agent.get_supported_intents()
        
        assert "agenda" in intents
        assert "cita" in intents
        assert "reunión" in intents
        assert "evento" in intents
        assert "meeting" in intents
    
    def test_datetime_extraction_relative_date(self, agenda_agent):
        """Test date/time extraction with relative dates."""
        # Test "mañana"
        result = agenda_agent._extract_datetime("agendar reunión mañana a las 3 pm")
        
        assert result is not None
        assert "date" in result
        expected_date = (datetime.now() + timedelta(days=1)).date()
        assert result["date"] == expected_date
        assert result["time"] == "15:00"
    
    def test_datetime_extraction_today(self, agenda_agent):
        """Test date/time extraction with 'today'."""
        result = agenda_agent._extract_datetime("hoy a las 10:30")
        
        assert result is not None
        assert result["date"] == datetime.now().date()
        assert result["time"] == "10:30"
    
    def test_datetime_extraction_day_of_week(self, agenda_agent):
        """Test date/time extraction with day of week."""
        result = agenda_agent._extract_datetime("el lunes a las 9 am")
        
        assert result is not None
        assert "date" in result
        assert result["time"] == "09:00"
    
    def test_datetime_extraction_duration(self, agenda_agent):
        """Test duration extraction."""
        result = agenda_agent._extract_datetime("reunión de 2 horas")
        
        assert result is not None
        assert "duration_minutes" in result
        assert result["duration_minutes"] == 120
    
    def test_create_event_success(self, agenda_agent):
        """Test successful event creation."""
        event_data = {
            "title": "Reunión de equipo",
            "date": "2025-11-16",
            "time": "10:00",
            "duration_minutes": 60
        }
        
        response = agenda_agent.create_event("user_123", event_data)
        
        assert response["status"] == "ok"
        assert "creado" in response["message"].lower()
        assert response["context"]["event_created"] is True
    
    def test_create_event_missing_fields(self, agenda_agent):
        """Test event creation with missing fields."""
        event_data = {
            "title": "Reunión"
            # Missing date and time
        }
        
        response = agenda_agent.create_event("user_456", event_data)
        
        assert response["status"] == "error"
        assert "faltan campos" in response["message"].lower()
    
    def test_list_events_empty(self, agenda_agent):
        """Test listing events (empty)."""
        response = agenda_agent.list_events("user_789")
        
        assert response["status"] == "ok"
        assert response["context"]["events"] == []
    
    def test_handle_message_with_datetime(self, agenda_agent):
        """Test handling message with date/time extraction."""
        response = agenda_agent.handle(
            user_id="user_101",
            message="quiero agendar una reunión mañana a las 3 pm",
            context={}
        )
        
        assert response["status"] == "ok"
        assert "message" in response
        assert "context" in response
    
    def test_conversation_manager_per_user(self, agenda_agent):
        """Test that each user gets their own conversation manager."""
        # Create managers for 2 users
        manager1 = agenda_agent._get_conversation_manager("user_001")
        manager2 = agenda_agent._get_conversation_manager("user_002")
        
        assert manager1 is not manager2
        assert len(agenda_agent.conversation_managers) == 2
        
        # Getting same user again returns same manager
        manager1_again = agenda_agent._get_conversation_manager("user_001")
        assert manager1 is manager1_again
    
    def test_agent_cleanup(self, agenda_agent):
        """Test agent cleanup."""
        # Create some managers
        agenda_agent._get_conversation_manager("user_001")
        agenda_agent._get_conversation_manager("user_002")
        
        assert len(agenda_agent.conversation_managers) == 2
        
        # Cleanup
        agenda_agent.cleanup()
        
        assert len(agenda_agent.conversation_managers) == 0
        assert agenda_agent._is_initialized is False


class TestAgendaAgentDateTimeExtraction:
    """Focused tests for date/time extraction logic."""
    
    @pytest.fixture
    def agenda_agent(self):
        """Create AgendaAgent instance."""
        return AgendaAgent()
    
    def test_extract_time_24h_format(self, agenda_agent):
        """Test extracting time in 24h format."""
        result = agenda_agent._extract_datetime("reunión a las 15:30")
        
        assert result is not None
        assert result["time"] == "15:30"
    
    def test_extract_time_am_pm(self, agenda_agent):
        """Test extracting time with AM/PM."""
        result = agenda_agent._extract_datetime("cita a las 3 pm")
        
        assert result is not None
        assert result["time"] == "15:00"
    
    def test_extract_duration_hours(self, agenda_agent):
        """Test extracting duration in hours."""
        result = agenda_agent._extract_datetime("evento de 3 horas")
        
        assert result["duration_minutes"] == 180
    
    def test_extract_duration_minutes(self, agenda_agent):
        """Test extracting duration in minutes."""
        result = agenda_agent._extract_datetime("llamada de 30 minutos")
        
        assert result["duration_minutes"] == 30
    
    def test_no_extraction_when_no_datetime(self, agenda_agent):
        """Test that extraction returns None when no date/time found."""
        result = agenda_agent._extract_datetime("hola cómo estás")
        
        assert result is None
