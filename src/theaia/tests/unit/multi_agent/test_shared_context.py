"""Tests for SharedContext - Coverage target: >85%"""
import pytest
from datetime import datetime
from src.theaia.core.multi_agent.shared_context import ContextEntry, SharedContext

class TestContextEntryBasic:
    def test_entry_creation(self):
        entry = ContextEntry(key="test", value="data", owner_agent_id="agent1")
        assert entry.key == "test" and entry.value == "data" and entry.owner_agent_id == "agent1"
    
    def test_entry_timestamps(self):
        entry = ContextEntry(key="test", value="data", owner_agent_id="agent1")
        assert entry.created_at is not None and entry.updated_at is not None
    
    def test_entry_no_ttl(self):
        entry = ContextEntry(key="test", value="data", owner_agent_id="agent1")
        assert entry.is_expired() is False
    
    def test_entry_with_ttl_not_expired(self):
        entry = ContextEntry(key="test", value="data", owner_agent_id="agent1", ttl_seconds=300)
        assert entry.is_expired() is False
    
    def test_entry_with_ttl_expired(self):
        entry = ContextEntry(key="test", value="data", owner_agent_id="agent1", ttl_seconds=0)
        import time; time.sleep(0.1)
        assert entry.is_expired() is True
    
    def test_update_value(self):
        entry = ContextEntry(key="test", value="old", owner_agent_id="agent1")
        old_time = entry.updated_at
        import time; time.sleep(0.01)
        entry.update_value("new")
        assert entry.value == "new" and entry.updated_at > old_time

class TestSharedContextBasic:
    def test_context_initialization(self):
        ctx = SharedContext()
        assert len(ctx._context) == 0 and len(ctx._agent_keys) == 0
    
    def test_set_value(self):
        ctx = SharedContext()
        result = ctx.set("key1", "value1", "agent1")
        assert result is True and ctx.get("key1") == "value1"
    
    def test_set_multiple_values(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.set("key2", "value2", "agent1")
        assert ctx.get("key1") == "value1" and ctx.get("key2") == "value2"
    
    def test_get_nonexistent_key(self):
        ctx = SharedContext()
        assert ctx.get("fake") is None

class TestSharedContextOwnership:
    def test_owner_can_update(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        result = ctx.set("key1", "value2", "agent1")
        assert result is True and ctx.get("key1") == "value2"
    
    def test_non_owner_cannot_update(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        result = ctx.set("key1", "value2", "agent2")
        assert result is False and ctx.get("key1") == "value1"
    
    def test_owner_can_delete(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        result = ctx.delete("key1", "agent1")
        assert result is True and ctx.get("key1") is None
    
    def test_non_owner_cannot_delete(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        result = ctx.delete("key1", "agent2")
        assert result is False and ctx.get("key1") == "value1"

class TestSharedContextEntry:
    def test_get_entry(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        entry = ctx.get_entry("key1")
        assert entry is not None and entry.value == "value1" and entry.owner_agent_id == "agent1"
    
    def test_get_entry_nonexistent(self):
        ctx = SharedContext()
        entry = ctx.get_entry("fake")
        assert entry is None
    
    def test_get_entry_expired(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1", ttl_seconds=0)
        import time; time.sleep(0.1)
        entry = ctx.get_entry("key1")
        assert entry is None

class TestSharedContextTTL:
    def test_set_with_ttl(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1", ttl_seconds=300)
        assert ctx.get("key1") == "value1"
    
    def test_get_expired_returns_none(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1", ttl_seconds=0)
        import time; time.sleep(0.1)
        assert ctx.get("key1") is None
    
    def test_cleanup_expired(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1", ttl_seconds=0)
        ctx.set("key2", "value2", "agent1", ttl_seconds=300)
        import time; time.sleep(0.1)
        expired = ctx.cleanup_expired()
        assert len(expired) == 1 and "key1" in expired and ctx.get("key2") == "value2"

class TestSharedContextSubscriptions:
    def test_subscribe(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        result = ctx.subscribe("key1", "agent2")
        assert result is True
    
    def test_subscribe_nonexistent_key(self):
        ctx = SharedContext()
        result = ctx.subscribe("fake", "agent1")
        assert result is False
    
    def test_unsubscribe(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.subscribe("key1", "agent2")
        result = ctx.unsubscribe("key1", "agent2")
        assert result is True
    
    def test_get_subscribers(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.subscribe("key1", "agent2")
        ctx.subscribe("key1", "agent3")
        subs = ctx.get_subscribers("key1")
        assert len(subs) == 2 and "agent2" in subs and "agent3" in subs
    
    def test_get_subscribers_nonexistent(self):
        ctx = SharedContext()
        subs = ctx.get_subscribers("fake")
        assert len(subs) == 0

class TestSharedContextAgentKeys:
    def test_get_agent_keys(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.set("key2", "value2", "agent1")
        keys = ctx.get_agent_keys("agent1")
        assert len(keys) == 2 and "key1" in keys and "key2" in keys
    
    def test_get_agent_keys_empty(self):
        ctx = SharedContext()
        keys = ctx.get_agent_keys("agent1")
        assert len(keys) == 0
    
    def test_clear_agent_context(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.set("key2", "value2", "agent1")
        count = ctx.clear_agent_context("agent1")
        assert count == 2 and ctx.get("key1") is None and ctx.get("key2") is None

class TestSharedContextMetadata:
    def test_set_with_metadata(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1", metadata={"type": "config"})
        entry = ctx.get_entry("key1")
        assert entry.metadata["type"] == "config"
    
    def test_update_metadata(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1", metadata={"v": 1})
        ctx.set("key1", "value2", "agent1", metadata={"v": 2})
        entry = ctx.get_entry("key1")
        assert entry.metadata["v"] == 2

class TestSharedContextExportImport:
    def test_export_context(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.set("key2", "value2", "agent1")
        exported = ctx.export_context()
        assert len(exported) == 2 and "key1" in exported and "key2" in exported
    
    def test_export_specific_keys(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.set("key2", "value2", "agent1")
        exported = ctx.export_context(keys=["key1"])
        assert len(exported) == 1 and "key1" in exported
    
    def test_import_context(self):
        ctx = SharedContext()
        data = {"key1": {"value": "value1", "metadata": {}}, "key2": {"value": "value2", "metadata": {}}}
        count = ctx.import_context(data, "agent1")
        assert count == 2 and ctx.get("key1") == "value1" and ctx.get("key2") == "value2"

class TestSharedContextStatistics:
    def test_get_statistics(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        ctx.set("key2", "value2", "agent2")
        stats = ctx.get_statistics()
        assert stats["total_entries"] == 2 and stats["total_agents"] == 2

class TestSharedContextHistory:
    def test_history_tracked(self):
        ctx = SharedContext()
        ctx.set("key1", "value1", "agent1")
        history = ctx.get_history()
        assert len(history) > 0 and history[-1]["action"] == "set"
    
    def test_history_limit(self):
        ctx = SharedContext()
        for i in range(10):
            ctx.set(f"key{i}", f"value{i}", "agent1")
        history = ctx.get_history(limit=5)
        assert len(history) == 5

class TestSharedContextEdgeCases:
    def test_delete_nonexistent(self):
        ctx = SharedContext()
        result = ctx.delete("fake", "agent1")
        assert result is False
    
    def test_unsubscribe_nonexistent(self):
        ctx = SharedContext()
        result = ctx.unsubscribe("fake", "agent1")
        assert result is False
