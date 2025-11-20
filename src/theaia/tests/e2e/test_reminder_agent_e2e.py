"""E2E Tests for ReminderAgent - THEA_IA.

ReminderAgent maneja recordatorios con fecha/hora:
- Crear recordatorios con tiempo específico
- Alarmas y notificaciones
- Gestión de recordatorios activos
- Cancelación de recordatorios
"""

import pytest
from unittest.mock import MagicMock
from src.theaia.agents.reminder_agent.handler import ReminderAgent


@pytest.fixture
def reminder_agent():
    """Create ReminderAgent instance for testing.
    
    ReminderAgent uses ConversationManager for state management.
    Similar architecture to NoteAgent but handles time-based reminders.
    """
    agent = ReminderAgent(user_id="test_user_456")
    # Mock conversation manager for predictable testing
    agent.conversation_manager = MagicMock()
    agent.conversation_manager.handle_message = MagicMock(
        return_value=(
            "Recordatorio creado para mañana a las 10:00",
            "completed",
            {"user_id": "test_user_456", "reminder_created": True}
        )
    )
    return agent


class TestReminderAgentE2E:
    """Test ReminderAgent end-to-end functionality."""

    def test_agent_initialization(self, reminder_agent):
        """Test agent initialization with user_id."""
        assert reminder_agent.user_id == "test_user_456"
        assert reminder_agent.conversation_manager is not None
        assert hasattr(reminder_agent, 'get_supported_intents')
        assert hasattr(reminder_agent, 'handle')

    def test_get_supported_intents(self, reminder_agent):
        """Test getting supported intents for reminders."""
        intents = reminder_agent.get_supported_intents()
        
        assert isinstance(intents, list)
        assert len(intents) > 0
        assert "recordatorio" in intents
        # Puede incluir: alarma, recuérdame, reminder

    def test_handle_create_reminder_simple(self, reminder_agent):
        """Test creating a simple reminder.
        
        Use case: "Recuérdame llamar al dentista"
        """
        response, state, context = reminder_agent.handle(
            user_id="test_user_456",
            message="Recuérdame llamar al dentista",
            context={"intent": "recordatorio"}
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        assert state is not None
        assert isinstance(context, dict)
        assert context["user_id"] == "test_user_456"

    def test_handle_delegates_to_conversation_manager(self, reminder_agent):
        """Test that handle delegates to conversation manager.
        
        ReminderAgent is a thin wrapper around ConversationManager.
        """
        message = "Recordatorio para mañana a las 10"
        context = {"intent": "recordatorio", "user_id": "test_user_456"}
        
        response, state, new_context = reminder_agent.handle(
            "test_user_456",
            message,
            context
        )
        
        # Verify delegation
        reminder_agent.conversation_manager.handle_message.assert_called_once_with(
            "test_user_456",
            message,
            context
        )
        
        assert "Recordatorio creado" in response
        assert state == "completed"
        assert new_context["reminder_created"] is True

    def test_handle_returns_valid_tuple_structure(self, reminder_agent):
        """Test handle returns (response, state, context) tuple."""
        response, state, context = reminder_agent.handle(
            "test_user_456",
            "Alarma para las 8:00",
            {"intent": "recordatorio"}
        )
        
        # Validate structure
        assert isinstance(response, str), "Response must be string"
        assert isinstance(state, str), "State must be string"
        assert isinstance(context, dict), "Context must be dict"
        assert "user_id" in context, "Context must have user_id"

    def test_user_id_consistency(self, reminder_agent):
        """Test user_id remains consistent across calls."""
        original_user_id = reminder_agent.user_id
        
        # Make multiple calls
        for i in range(5):
            reminder_agent.handle(
                "test_user_456",
                f"Recordatorio número {i}",
                {"intent": "recordatorio"}
            )
        
        # user_id should not change
        assert reminder_agent.user_id == original_user_id
        assert reminder_agent.user_id == "test_user_456"

    def test_supports_multiple_intent_variations(self, reminder_agent):
        """Test agent supports various reminder intent keywords.
        
        THEA_IA supports natural language variations.
        """
        intents = reminder_agent.get_supported_intents()
        
        # Must support at least recordatorio
        assert "recordatorio" in intents, "Intent 'recordatorio' should be supported"
        
        # May support additional variations
        # alarma, recuérdame, reminder

    def test_conversation_manager_exists(self, reminder_agent):
        """Test conversation manager is properly initialized."""
        assert hasattr(reminder_agent, 'conversation_manager')
        assert reminder_agent.conversation_manager is not None
        assert hasattr(reminder_agent.conversation_manager, 'handle_message')


class TestReminderAgentConversationFlow:
    """Test multi-turn conversation flows for reminder creation."""

    def test_multi_turn_reminder_creation(self):
        """Test conversation flow for creating a reminder.
        
        Flow:
        1. User: "Crear recordatorio"
        2. Bot: "¿Para cuándo?"
        3. User: "Mañana a las 10"
        4. Bot: "¿Qué te recuerdo?"
        5. User: "Llamar al doctor"
        6. Bot: "Recordatorio creado"
        """
        agent = ReminderAgent(user_id="flow_user")
        agent.conversation_manager = MagicMock()
        
        # Turn 1: Initiate reminder creation
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "¿Para cuándo quieres el recordatorio?",
                "awaiting_reminder_time",
                {"user_id": "flow_user", "intent": "recordatorio"}
            )
        )
        
        response1, state1, context1 = agent.handle(
            "flow_user",
            "Crear recordatorio",
            {"intent": "recordatorio"}
        )
        
        assert "cuándo" in response1.lower()
        assert state1 == "awaiting_reminder_time"
        
        # Turn 2: Provide time
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "¿Qué te recuerdo?",
                "awaiting_reminder_content",
                {
                    "user_id": "flow_user",
                    "reminder_time": "mañana 10:00"
                }
            )
        )
        
        response2, state2, context2 = agent.handle(
            "flow_user",
            "Mañana a las 10",
            {"intent": "recordatorio", "state": "awaiting_reminder_time"}
        )
        
        assert "recuerdo" in response2.lower()
        assert state2 == "awaiting_reminder_content"
        
        # Turn 3: Provide content
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "Recordatorio 'Llamar al doctor' creado para mañana a las 10:00",
                "completed",
                {
                    "user_id": "flow_user",
                    "reminder": "Llamar al doctor",
                    "time": "mañana 10:00",
                    "reminder_id": 456
                }
            )
        )
        
        response3, state3, context3 = agent.handle(
            "flow_user",
            "Llamar al doctor",
            {"intent": "recordatorio", "state": "awaiting_reminder_content"}
        )
        
        assert "creado" in response3.lower()
        assert state3 == "completed"
        assert context3["reminder"] == "Llamar al doctor"

    def test_context_preservation_with_time_data(self):
        """Test context preserves time-related data."""
        agent = ReminderAgent(user_id="time_user")
        agent.conversation_manager = MagicMock()
        
        initial_context = {
            "user_id": "time_user",
            "timezone": "CET",
            "active_reminders": ["reminder1", "reminder2"]
        }
        
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "Recordatorio creado",
                "completed",
                {
                    **initial_context,
                    "active_reminders": ["reminder1", "reminder2", "reminder3"],
                    "last_reminder_time": "2025-11-16 10:00:00"
                }
            )
        )
        
        response, state, context = agent.handle(
            "time_user",
            "Recordatorio para mañana",
            initial_context
        )
        
        # Context should preserve timezone and update reminders
        assert context["timezone"] == "CET"
        assert len(context["active_reminders"]) == 3
        assert "last_reminder_time" in context

    def test_error_handling_in_conversation(self):
        """Test graceful error handling during conversation."""
        agent = ReminderAgent(user_id="error_user")
        agent.conversation_manager = MagicMock()
        
        # Simulate conversation manager error
        agent.conversation_manager.handle_message = MagicMock(
            side_effect=Exception("Reminder error")
        )
        
        # Should propagate exception for handling at higher level
        with pytest.raises(Exception) as exc_info:
            agent.handle(
                "error_user",
                "test message",
                {"intent": "recordatorio"}
            )
        
        assert "Reminder error" in str(exc_info.value)


class TestReminderAgentIntegration:
    """Test ReminderAgent integration with THEA_IA system."""

    def test_agent_compatible_with_base_agent_interface(self, reminder_agent):
        """Test ReminderAgent follows BaseAgent interface."""
        # Required methods from BaseAgent
        assert callable(getattr(reminder_agent, 'get_supported_intents', None))
        assert callable(getattr(reminder_agent, 'handle', None))
        
        # Required attributes
        assert hasattr(reminder_agent, 'user_id')

    def test_intent_routing_compatibility(self, reminder_agent):
        """Test intents are router-compatible."""
        intents = reminder_agent.get_supported_intents()
        
        # All intents should be strings
        assert all(isinstance(intent, str) for intent in intents)
        
        # All intents should be lowercase for consistency
        assert all(intent.islower() for intent in intents)

    def test_response_format_consistency(self, reminder_agent):
        """Test response format matches THEA_IA standards."""
        response, state, context = reminder_agent.handle(
            "test_user",
            "test message",
            {"intent": "recordatorio"}
        )
        
        # Response should be user-friendly Spanish text
        assert isinstance(response, str)
        assert len(response) > 0
        
        # State should be valid FSM state
        assert isinstance(state, str)
        assert len(state) > 0
        
        # Context should preserve user_id
        assert "user_id" in context

    def test_reminder_specific_functionality(self, reminder_agent):
        """Test reminder-specific features vs note features.
        
        ReminderAgent differs from NoteAgent by handling time-based alerts.
        """
        intents = reminder_agent.get_supported_intents()
        
        # Should have reminder-specific intents
        reminder_keywords = ["recordatorio", "alarma", "reminder"]
        has_reminder_intent = any(keyword in intents for keyword in reminder_keywords)
        assert has_reminder_intent, "Should have reminder-specific intent"
