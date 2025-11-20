"""E2E Tests for NoteAgent - THEA_IA.

NoteAgent maneja notas rápidas del usuario:
- Capturar ideas y apuntes sin fecha
- Listas de tareas simples
- Recordatorios informales
- Búsqueda y gestión de notas
"""

import pytest
from unittest.mock import MagicMock
from src.theaia.agents.note_agent.handler import NoteAgent


@pytest.fixture
def note_agent():
    """Create NoteAgent instance for testing.
    
    NoteAgent uses ConversationManager for state management.
    No direct DB dependency - simpler architecture.
    """
    agent = NoteAgent(user_id="test_user_123")
    # Mock conversation manager for predictable testing
    agent.conversation_manager = MagicMock()
    agent.conversation_manager.handle_message = MagicMock(
        return_value=(
            "Nota guardada correctamente",
            "completed",
            {"user_id": "test_user_123", "note_created": True}
        )
    )
    return agent


class TestNoteAgentE2E:
    """Test NoteAgent end-to-end functionality."""

    def test_agent_initialization(self, note_agent):
        """Test agent initialization with user_id."""
        assert note_agent.user_id == "test_user_123"
        assert note_agent.conversation_manager is not None
        assert hasattr(note_agent, 'get_supported_intents')
        assert hasattr(note_agent, 'handle')

    def test_get_supported_intents(self, note_agent):
        """Test getting supported intents for notes."""
        intents = note_agent.get_supported_intents()
        
        assert isinstance(intents, list)
        assert len(intents) > 0
        assert "nota" in intents
        assert "notas" in intents
        # Puede incluir: apunte, memoria, etc.

    def test_handle_create_note_simple(self, note_agent):
        """Test creating a simple note.
        
        Use case: "Apuntar comprar leche"
        """
        response, state, context = note_agent.handle(
            user_id="test_user_123",
            message="Apuntar comprar leche",
            context={"intent": "nota"}
        )
        
        assert response is not None
        assert isinstance(response, str)
        assert len(response) > 0
        assert state is not None
        assert isinstance(context, dict)
        assert context["user_id"] == "test_user_123"

    def test_handle_delegates_to_conversation_manager(self, note_agent):
        """Test that handle delegates to conversation manager.
        
        NoteAgent is a thin wrapper around ConversationManager.
        """
        message = "Crear nota sobre Python"
        context = {"intent": "nota", "user_id": "test_user_123"}
        
        response, state, new_context = note_agent.handle(
            "test_user_123",
            message,
            context
        )
        
        # Verify delegation
        note_agent.conversation_manager.handle_message.assert_called_once_with(
            "test_user_123",
            message,
            context
        )
        
        assert response == "Nota guardada correctamente"
        assert state == "completed"
        assert new_context["note_created"] is True

    def test_handle_returns_valid_tuple_structure(self, note_agent):
        """Test handle returns (response, state, context) tuple."""
        response, state, context = note_agent.handle(
            "test_user_123",
            "Nota de prueba",
            {"intent": "nota"}
        )
        
        # Validate structure
        assert isinstance(response, str), "Response must be string"
        assert isinstance(state, str), "State must be string"
        assert isinstance(context, dict), "Context must be dict"
        assert "user_id" in context, "Context must have user_id"

    def test_user_id_consistency(self, note_agent):
        """Test user_id remains consistent across calls."""
        original_user_id = note_agent.user_id
        
        # Make multiple calls
        for i in range(5):
            note_agent.handle(
                "test_user_123",
                f"Nota número {i}",
                {"intent": "nota"}
            )
        
        # user_id should not change
        assert note_agent.user_id == original_user_id
        assert note_agent.user_id == "test_user_123"

    def test_supports_multiple_intent_variations(self, note_agent):
        """Test agent supports various note intent keywords.
        
        THEA_IA supports natural language variations.
        """
        intents = note_agent.get_supported_intents()
        
        # Must support at least these common variations
        expected_intents = ["nota", "notas"]
        for intent in expected_intents:
            assert intent in intents, f"Intent '{intent}' should be supported"

    def test_conversation_manager_exists(self, note_agent):
        """Test conversation manager is properly initialized."""
        assert hasattr(note_agent, 'conversation_manager')
        assert note_agent.conversation_manager is not None
        assert hasattr(note_agent.conversation_manager, 'handle_message')


class TestNoteAgentConversationFlow:
    """Test multi-turn conversation flows for note creation."""

    def test_multi_turn_note_creation(self):
        """Test conversation flow for creating a note.
        
        Flow:
        1. User: "Crear nota"
        2. Bot: "¿Qué quieres apuntar?"
        3. User: "Comprar pan y leche"
        4. Bot: "Nota guardada"
        """
        agent = NoteAgent(user_id="flow_user")
        agent.conversation_manager = MagicMock()
        
        # Turn 1: Initiate note creation
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "¿Qué quieres apuntar?",
                "awaiting_note_content",
                {"user_id": "flow_user", "intent": "nota"}
            )
        )
        
        response1, state1, context1 = agent.handle(
            "flow_user",
            "Crear nota",
            {"intent": "nota"}
        )
        
        assert "apuntar" in response1.lower()
        assert state1 == "awaiting_note_content"
        
        # Turn 2: Provide note content
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "Nota 'Comprar pan y leche' guardada correctamente",
                "completed",
                {
                    "user_id": "flow_user",
                    "note": "Comprar pan y leche",
                    "note_id": 123
                }
            )
        )
        
        response2, state2, context2 = agent.handle(
            "flow_user",
            "Comprar pan y leche",
            {"intent": "nota", "state": "awaiting_note_content"}
        )
        
        assert "guardada" in response2.lower()
        assert state2 == "completed"
        assert context2["note"] == "Comprar pan y leche"

    def test_context_preservation_across_turns(self):
        """Test context data is preserved during conversation."""
        agent = NoteAgent(user_id="context_user")
        agent.conversation_manager = MagicMock()
        
        initial_context = {
            "user_id": "context_user",
            "previous_notes": ["nota1", "nota2"],
            "note_count": 2
        }
        
        agent.conversation_manager.handle_message = MagicMock(
            return_value=(
                "Nota guardada",
                "completed",
                {
                    **initial_context,
                    "note_count": 3,
                    "previous_notes": ["nota1", "nota2", "nota3"]
                }
            )
        )
        
        response, state, context = agent.handle(
            "context_user",
            "Apuntar nota3",
            initial_context
        )
        
        # Context should be updated but preserve history
        assert context["note_count"] == 3
        assert len(context["previous_notes"]) == 3
        assert "nota1" in context["previous_notes"]

    def test_error_handling_in_conversation(self):
        """Test graceful error handling during conversation."""
        agent = NoteAgent(user_id="error_user")
        agent.conversation_manager = MagicMock()
        
        # Simulate conversation manager error
        agent.conversation_manager.handle_message = MagicMock(
            side_effect=Exception("Conversation error")
        )
        
        # Should propagate exception for handling at higher level
        with pytest.raises(Exception) as exc_info:
            agent.handle(
                "error_user",
                "test message",
                {"intent": "nota"}
            )
        
        assert "Conversation error" in str(exc_info.value)


class TestNoteAgentIntegration:
    """Test NoteAgent integration with THEA_IA system."""

    def test_agent_compatible_with_base_agent_interface(self, note_agent):
        """Test NoteAgent follows BaseAgent interface."""
        # Required methods from BaseAgent
        assert callable(getattr(note_agent, 'get_supported_intents', None))
        assert callable(getattr(note_agent, 'handle', None))
        
        # Required attributes
        assert hasattr(note_agent, 'user_id')

    def test_intent_routing_compatibility(self, note_agent):
        """Test intents are router-compatible."""
        intents = note_agent.get_supported_intents()
        
        # All intents should be strings
        assert all(isinstance(intent, str) for intent in intents)
        
        # All intents should be lowercase for consistency
        assert all(intent.islower() for intent in intents)

    def test_response_format_consistency(self, note_agent):
        """Test response format matches THEA_IA standards."""
        response, state, context = note_agent.handle(
            "test_user",
            "test message",
            {"intent": "nota"}
        )
        
        # Response should be user-friendly Spanish text
        assert isinstance(response, str)
        assert len(response) > 0
        
        # State should be valid FSM state
        assert isinstance(state, str)
        assert len(state) > 0
        
        # Context should preserve user_id
        assert "user_id" in context
