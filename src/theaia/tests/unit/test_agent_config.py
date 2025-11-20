"""Tests for AgentConfig."""

import pytest
from src.theaia.agents.agent_config import (
    AgentConfig,
    AGENDA_CONFIG,
    NOTE_CONFIG,
    REMINDER_CONFIG,
    get_agent_config,
    AGENT_CONFIGS
)


class TestAgentConfig:
    """Test AgentConfig functionality."""
    
    def test_create_config(self):
        """Test creating agent config."""
        config = AgentConfig(
            name="TestAgent",
            supported_intents=["test"],
            requires_database=True
        )
        
        assert config.name == "TestAgent"
        assert "test" in config.supported_intents
        assert config.requires_database is True
    
    def test_add_intent(self):
        """Test adding intent."""
        config = AgentConfig(name="Test")
        config.add_intent("new_intent")
        
        assert "new_intent" in config.supported_intents
    
    def test_add_intent_duplicate(self):
        """Test adding duplicate intent (should not duplicate)."""
        config = AgentConfig(name="Test", supported_intents=["intent1"])
        config.add_intent("intent1")
        
        assert config.supported_intents.count("intent1") == 1
    
    def test_remove_intent(self):
        """Test removing intent."""
        config = AgentConfig(name="Test", supported_intents=["intent1", "intent2"])
        config.remove_intent("intent1")
        
        assert "intent1" not in config.supported_intents
        assert "intent2" in config.supported_intents
    
    def test_supports_intent(self):
        """Test checking if intent supported."""
        config = AgentConfig(name="Test", supported_intents=["intent1"])
        
        assert config.supports_intent("intent1") is True
        assert config.supports_intent("unknown") is False
    
    def test_to_dict(self):
        """Test converting config to dict."""
        config = AgentConfig(
            name="Test",
            supported_intents=["intent1"],
            requires_database=True,
            max_context_length=5
        )
        
        result = config.to_dict()
        
        assert result["name"] == "Test"
        assert result["supported_intents"] == ["intent1"]
        assert result["requires_database"] is True
        assert result["max_context_length"] == 5
    
    def test_from_dict(self):
        """Test creating config from dict."""
        data = {
            "name": "Test",
            "supported_intents": ["intent1", "intent2"],
            "requires_database": False,
            "max_context_length": 8,
            "timeout_seconds": 25
        }
        
        config = AgentConfig.from_dict(data)
        
        assert config.name == "Test"
        assert config.supported_intents == ["intent1", "intent2"]
        assert config.requires_database is False
        assert config.max_context_length == 8
        assert config.timeout_seconds == 25
    
    def test_from_dict_defaults(self):
        """Test from_dict with missing fields uses defaults."""
        data = {"name": "Test"}
        config = AgentConfig.from_dict(data)
        
        assert config.name == "Test"
        assert config.supported_intents == []
        assert config.requires_database is False
        assert config.max_context_length == 10


class TestPredefinedConfigs:
    """Test predefined agent configurations."""
    
    def test_agenda_config(self):
        """Test agenda agent config."""
        assert AGENDA_CONFIG.name == "AgendaAgent"
        assert "create_event" in AGENDA_CONFIG.supported_intents
        assert AGENDA_CONFIG.requires_database is True
    
    def test_note_config(self):
        """Test note agent config."""
        assert NOTE_CONFIG.name == "NoteAgent"
        assert "create_note" in NOTE_CONFIG.supported_intents
        assert NOTE_CONFIG.requires_database is True
    
    def test_reminder_config(self):
        """Test reminder agent config."""
        assert REMINDER_CONFIG.name == "ReminderAgent"
        assert "create_reminder" in REMINDER_CONFIG.supported_intents
        assert REMINDER_CONFIG.requires_database is True
    
    def test_get_agent_config(self):
        """Test getting config by name."""
        config = get_agent_config("agenda")
        
        assert config is not None
        assert config.name == "AgendaAgent"
    
    def test_get_agent_config_case_insensitive(self):
        """Test case insensitive config lookup."""
        config = get_agent_config("AGENDA")
        
        assert config is not None
        assert config.name == "AgendaAgent"
    
    def test_get_agent_config_not_found(self):
        """Test getting non-existent config."""
        config = get_agent_config("unknown")
        
        assert config is None
    
    def test_all_configs_registered(self):
        """Test all predefined configs are registered."""
        assert "agenda" in AGENT_CONFIGS
        assert "note" in AGENT_CONFIGS
        assert "reminder" in AGENT_CONFIGS
        assert "query" in AGENT_CONFIGS
        assert "help" in AGENT_CONFIGS
        assert "fallback" in AGENT_CONFIGS
