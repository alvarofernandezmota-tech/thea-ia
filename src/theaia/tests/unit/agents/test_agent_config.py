"""
Unit tests for AgentConfig.

Tests configuration management, validation, and utility functions.
"""

import pytest
from src.theaia.agents.agent_config import (
    AgentConfig,
    AgentPriority,
    DEFAULT_AGENT_CONFIGS,
    get_agent_config,
    get_config_for_intent,
    list_all_intents,
    list_enabled_agents,
    get_agents_by_priority,
    AGENDA_CONFIG,
    NOTE_CONFIG,
    FALLBACK_CONFIG
)


class TestAgentConfig:
    """Test AgentConfig dataclass."""
    
    def test_config_creation(self):
        """Test basic config creation."""
        config = AgentConfig(
            name="test",
            display_name="Test Agent",
            description="Test description",
            intents=["test_intent"]
        )
        
        assert config.name == "test"
        assert config.display_name == "Test Agent"
        assert config.description == "Test description"
        assert config.intents == ["test_intent"]
        assert config.priority == AgentPriority.MEDIUM
        assert config.enabled is True
        assert config.requires_database is True
    
    def test_config_validation_empty_name(self):
        """Test validation fails with empty name."""
        with pytest.raises(ValueError, match="name cannot be empty"):
            AgentConfig(
                name="",
                display_name="Test",
                description="Test",
                intents=["test"]
            )
    
    def test_config_validation_no_intents(self):
        """Test validation fails with no intents."""
        with pytest.raises(ValueError, match="must handle at least one intent"):
            AgentConfig(
                name="test",
                display_name="Test",
                description="Test",
                intents=[]
            )
    
    def test_handles_intent(self):
        """Test intent matching (case-insensitive)."""
        config = AgentConfig(
            name="test",
            display_name="Test",
            description="Test",
            intents=["create_note", "edit_note"]
        )
        
        assert config.handles_intent("create_note") is True
        assert config.handles_intent("CREATE_NOTE") is True
        assert config.handles_intent("edit_note") is True
        assert config.handles_intent("delete_note") is False
    
    def test_add_remove_intent(self):
        """Test adding and removing intents."""
        config = AgentConfig(
            name="test",
            display_name="Test",
            description="Test",
            intents=["intent1"]
        )
        
        # Add intent
        config.add_intent("intent2")
        assert "intent2" in config.intents
        
        # Add duplicate (should not duplicate)
        config.add_intent("intent1")
        assert config.intents.count("intent1") == 1
        
        # Remove intent
        config.remove_intent("intent1")
        assert "intent1" not in config.intents
    
    def test_to_dict(self):
        """Test serialization to dict."""
        config = AgentConfig(
            name="test",
            display_name="Test Agent",
            description="Test description",
            intents=["test"],
            priority=AgentPriority.HIGH
        )
        
        data = config.to_dict()
        
        assert data["name"] == "test"
        assert data["display_name"] == "Test Agent"
        assert data["priority"] == "HIGH"
        assert data["intents"] == ["test"]
        assert data["enabled"] is True
    
    def test_from_dict(self):
        """Test deserialization from dict."""
        data = {
            "name": "test",
            "display_name": "Test Agent",
            "description": "Test description",
            "intents": ["test"],
            "priority": "HIGH",
            "enabled": True,
            "requires_database": False,
            "max_context_length": 5,
            "timeout_seconds": 20,
            "metadata": {"key": "value"}
        }
        
        config = AgentConfig.from_dict(data)
        
        assert config.name == "test"
        assert config.display_name == "Test Agent"
        assert config.priority == AgentPriority.HIGH
        assert config.enabled is True
        assert config.requires_database is False
        assert config.metadata == {"key": "value"}
    
    def test_display_name_auto_generation(self):
        """Test display_name auto-generated from name."""
        config = AgentConfig(
            name="agenda",
            display_name="",  # Empty will trigger auto-gen
            description="Test",
            intents=["test"]
        )
        
        assert config.display_name == "Agenda"


class TestPredefinedConfigs:
    """Test predefined agent configurations."""
    
    def test_default_configs_exist(self):
        """Test all default configs are defined."""
        expected_agents = ["agenda", "note", "reminder", "query", "help", "fallback", "schedule"]
        
        for agent_name in expected_agents:
            assert agent_name in DEFAULT_AGENT_CONFIGS
            config = DEFAULT_AGENT_CONFIGS[agent_name]
            assert isinstance(config, AgentConfig)
            assert config.enabled is True
    
    def test_agenda_config(self):
        """Test agenda agent config."""
        assert AGENDA_CONFIG.name == "agenda"
        assert AGENDA_CONFIG.priority == AgentPriority.HIGH
        assert AGENDA_CONFIG.requires_database is True
        assert "create_event" in AGENDA_CONFIG.intents
        assert AGENDA_CONFIG.metadata.get("supports_recurring") is True
    
    def test_note_config(self):
        """Test note agent config."""
        assert NOTE_CONFIG.name == "note"
        assert NOTE_CONFIG.priority == AgentPriority.MEDIUM
        assert "create_note" in NOTE_CONFIG.intents
        assert NOTE_CONFIG.metadata.get("supports_tags") is True
    
    def test_fallback_config(self):
        """Test fallback agent config."""
        assert FALLBACK_CONFIG.name == "fallback"
        assert FALLBACK_CONFIG.priority == AgentPriority.CRITICAL
        assert FALLBACK_CONFIG.requires_database is False
        assert "unknown" in FALLBACK_CONFIG.intents


class TestUtilityFunctions:
    """Test utility functions."""
    
    def test_get_agent_config(self):
        """Test get_agent_config function."""
        config = get_agent_config("agenda")
        assert config is not None
        assert config.name == "agenda"
        
        # Case insensitive
        config = get_agent_config("AGENDA")
        assert config is not None
        
        # Non-existent
        config = get_agent_config("nonexistent")
        assert config is None
    
    def test_get_config_for_intent(self):
        """Test intent-to-config mapping."""
        # Test agenda intent
        config = get_config_for_intent("create_event")
        assert config is not None
        assert config.name == "agenda"
        
        # Test note intent
        config = get_config_for_intent("create_note")
        assert config is not None
        assert config.name == "note"
        
        # Test priority selection (multiple matches)
        # "recordar" could match reminder (HIGH) or other
        config = get_config_for_intent("recordar")
        assert config is not None
        
        # Unknown intent
        config = get_config_for_intent("totally_unknown_intent")
        assert config is None
    
    def test_list_all_intents(self):
        """Test listing all intents."""
        intents = list_all_intents()
        
        assert isinstance(intents, list)
        assert len(intents) > 0
        assert "create_event" in intents
        assert "create_note" in intents
        assert "help" in intents
        # Should be sorted
        assert intents == sorted(intents)
    
    def test_list_enabled_agents(self):
        """Test listing enabled agents."""
        enabled = list_enabled_agents()
        
        assert isinstance(enabled, list)
        assert "agenda" in enabled
        assert "note" in enabled
        assert "fallback" in enabled
    
    def test_get_agents_by_priority(self):
        """Test filtering by priority."""
        high_priority = get_agents_by_priority(AgentPriority.HIGH)
        
        assert isinstance(high_priority, list)
        assert len(high_priority) > 0
        
        for config in high_priority:
            assert config.priority == AgentPriority.HIGH
        
        # Check agenda and reminder are HIGH
        names = [c.name for c in high_priority]
        assert "agenda" in names
        assert "reminder" in names


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
