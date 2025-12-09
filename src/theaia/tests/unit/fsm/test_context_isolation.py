"""
Tests for Context Isolation System

Author: Álvaro Fernández Mota
Date: 09 December 2025
Version: 1.0.0
"""

import pytest
from src.theaia.core.fsm.context_isolation import (
    ContextIsolation,
    ContextScope,
    ContextSnapshot,
    ContextNotFoundError,
    ContextScopeError
)


class TestContextScope:
    """Test ContextScope enum"""
    
    def test_scope_values(self):
        """Test scope enum values"""
        assert ContextScope.LOCAL.value == "local"
        assert ContextScope.SHARED.value == "shared"
        assert ContextScope.GLOBAL.value == "global"
    
    def test_scope_comparison(self):
        """Test scope comparison"""
        assert ContextScope.LOCAL != ContextScope.SHARED
        assert ContextScope.SHARED != ContextScope.GLOBAL
        assert ContextScope.LOCAL == ContextScope.LOCAL


class TestContextSnapshot:
    """Test ContextSnapshot dataclass"""
    
    def test_create_simple_snapshot(self):
        """Test creating a simple snapshot"""
        snapshot = ContextSnapshot(
            context_id="ctx_123",
            data={"key": "value"},
            scope=ContextScope.LOCAL
        )
        
        assert snapshot.context_id == "ctx_123"
        assert snapshot.data == {"key": "value"}
        assert snapshot.scope == ContextScope.LOCAL
        assert snapshot.parent_id is None
        assert snapshot.metadata == {}
    
    def test_create_snapshot_with_parent(self):
        """Test creating snapshot with parent"""
        snapshot = ContextSnapshot(
            context_id="ctx_child",
            data={"key": "value"},
            scope=ContextScope.SHARED,
            parent_id="ctx_parent"
        )
        
        assert snapshot.parent_id == "ctx_parent"
    
    def test_create_snapshot_with_metadata(self):
        """Test creating snapshot with metadata"""
        snapshot = ContextSnapshot(
            context_id="ctx_123",
            data={},
            scope=ContextScope.LOCAL,
            metadata={"created_by": "user_123"}
        )
        
        assert snapshot.metadata == {"created_by": "user_123"}


class TestContextIsolation:
    """Test ContextIsolation class"""
    
    def test_create_isolation_system(self):
        """Test creating isolation system"""
        isolation = ContextIsolation()
        
        assert isolation.contexts == {}
        assert isolation.context_hierarchy == {}
        assert isolation.context_scopes == {}
        assert isolation.snapshots == {}
    
    def test_create_context(self):
        """Test creating a context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("user_123")
        
        assert ctx_id == "user_123"
        assert "user_123" in isolation.contexts
        assert isolation.contexts["user_123"] == {}
    
    def test_create_context_with_scope(self):
        """Test creating context with specific scope"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", scope=ContextScope.SHARED)
        
        assert isolation.context_scopes[ctx_id] == ContextScope.SHARED
    
    def test_create_context_with_parent(self):
        """Test creating child context"""
        isolation = ContextIsolation()
        parent_id = isolation.create_context("parent")
        child_id = isolation.create_context("child", parent_id=parent_id)
        
        assert isolation.context_hierarchy[child_id] == parent_id
    
    def test_create_context_with_initial_data(self):
        """Test creating context with initial data"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", initial_data={"key": "value"})
        
        assert isolation.contexts[ctx_id] == {"key": "value"}
    
    def test_context_exists(self):
        """Test checking if context exists"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        assert isolation.context_exists(ctx_id) is True
        assert isolation.context_exists("nonexistent") is False
    
    def test_get_context(self):
        """Test getting context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", initial_data={"key": "value"})
        
        context = isolation.get_context(ctx_id)
        assert context == {"key": "value"}
    
    def test_get_context_not_found(self):
        """Test getting non-existent context raises error"""
        isolation = ContextIsolation()
        
        with pytest.raises(ContextNotFoundError):
            isolation.get_context("nonexistent")
    
    def test_set_value(self):
        """Test setting value in context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        isolation.set_value(ctx_id, "key", "value")
        assert isolation.contexts[ctx_id]["key"] == "value"
    
    def test_get_value(self):
        """Test getting value from context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        isolation.set_value(ctx_id, "key", "value")
        
        value = isolation.get_value(ctx_id, "key")
        assert value == "value"
    
    def test_get_value_default(self):
        """Test getting value with default"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        value = isolation.get_value(ctx_id, "nonexistent", default="default")
        assert value == "default"
    
    def test_delete_value(self):
        """Test deleting value from context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        isolation.set_value(ctx_id, "key", "value")
        
        result = isolation.delete_value(ctx_id, "key")
        assert result is True
        assert "key" not in isolation.contexts[ctx_id]
    
    def test_delete_value_nonexistent(self):
        """Test deleting non-existent value returns False"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        result = isolation.delete_value(ctx_id, "nonexistent")
        assert result is False
    
    def test_clear_context(self):
        """Test clearing context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", initial_data={"key": "value"})
        
        isolation.clear_context(ctx_id)
        assert isolation.contexts[ctx_id] == {}
    
    def test_delete_context(self):
        """Test deleting context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        result = isolation.delete_context(ctx_id)
        assert result is True
        assert ctx_id not in isolation.contexts
    
    def test_delete_context_with_children(self):
        """Test deleting context with children"""
        isolation = ContextIsolation()
        parent_id = isolation.create_context("parent")
        child_id = isolation.create_context("child", parent_id=parent_id)
        
        # Should delete parent and child
        result = isolation.delete_context(parent_id, cascade=True)
        assert result is True
        assert parent_id not in isolation.contexts
        assert child_id not in isolation.contexts
    
    def test_get_parent_context(self):
        """Test getting parent context"""
        isolation = ContextIsolation()
        parent_id = isolation.create_context("parent", initial_data={"key": "parent_value"})
        child_id = isolation.create_context("child", parent_id=parent_id)
        
        parent = isolation.get_parent_context(child_id)
        assert parent == {"key": "parent_value"}
    
    def test_get_parent_context_no_parent(self):
        """Test getting parent context when no parent"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        parent = isolation.get_parent_context(ctx_id)
        assert parent is None
    
    def test_get_children_contexts(self):
        """Test getting children contexts"""
        isolation = ContextIsolation()
        parent_id = isolation.create_context("parent")
        child1_id = isolation.create_context("child1", parent_id=parent_id)
        child2_id = isolation.create_context("child2", parent_id=parent_id)
        
        children = isolation.get_children_contexts(parent_id)
        assert len(children) == 2
        assert child1_id in children
        assert child2_id in children
    
    def test_merge_contexts(self):
        """Test merging contexts"""
        isolation = ContextIsolation()
        ctx1_id = isolation.create_context("ctx1", initial_data={"key1": "value1"})
        ctx2_id = isolation.create_context("ctx2", initial_data={"key2": "value2"})
        
        merged = isolation.merge_contexts(ctx1_id, ctx2_id)
        assert merged == {"key1": "value1", "key2": "value2"}
    
    def test_merge_contexts_override(self):
        """Test merging contexts with override"""
        isolation = ContextIsolation()
        ctx1_id = isolation.create_context("ctx1", initial_data={"key": "value1"})
        ctx2_id = isolation.create_context("ctx2", initial_data={"key": "value2"})
        
        merged = isolation.merge_contexts(ctx1_id, ctx2_id)
        assert merged["key"] == "value2"  # ctx2 overrides ctx1
    
    def test_merge_contexts_scope_error(self):
        """Test merging contexts with incompatible scopes raises error"""
        isolation = ContextIsolation()
        ctx1_id = isolation.create_context("ctx1", scope=ContextScope.LOCAL)
        ctx2_id = isolation.create_context("ctx2", scope=ContextScope.GLOBAL)
        
        with pytest.raises(ContextScopeError):
            isolation.merge_contexts(ctx1_id, ctx2_id, allow_scope_mixing=False)
    
    def test_isolate_context_local(self):
        """Test isolating LOCAL scope context"""
        isolation = ContextIsolation()
        parent_id = isolation.create_context("parent", initial_data={"parent_key": "value"})
        child_id = isolation.create_context("child", parent_id=parent_id, scope=ContextScope.LOCAL)
        isolation.set_value(child_id, "child_key", "child_value")
        
        isolated = isolation.isolate_context(child_id)
        assert "child_key" in isolated
        assert "parent_key" not in isolated  # LOCAL scope: no parent data
    
    def test_isolate_context_shared(self):
        """Test isolating SHARED scope context"""
        isolation = ContextIsolation()
        parent_id = isolation.create_context("parent", initial_data={"parent_key": "value"})
        child_id = isolation.create_context("child", parent_id=parent_id, scope=ContextScope.SHARED)
        isolation.set_value(child_id, "child_key", "child_value")
        
        isolated = isolation.isolate_context(child_id)
        assert "child_key" in isolated
        assert "parent_key" in isolated  # SHARED scope: includes parent data
    
    def test_isolate_context_global(self):
        """Test isolating GLOBAL scope context"""
        isolation = ContextIsolation()
        ctx1_id = isolation.create_context("ctx1", initial_data={"key1": "value1"}, scope=ContextScope.GLOBAL)
        ctx2_id = isolation.create_context("ctx2", initial_data={"key2": "value2"}, scope=ContextScope.GLOBAL)
        
        isolated = isolation.isolate_context(ctx1_id)
        # GLOBAL scope: should include all global contexts
        assert "key1" in isolated
        assert "key2" in isolated
    
    def test_create_snapshot(self):
        """Test creating context snapshot"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", initial_data={"key": "value"})
        
        snapshot = isolation.create_snapshot(ctx_id)
        assert snapshot.context_id == ctx_id
        assert snapshot.data == {"key": "value"}
    
    def test_create_snapshot_with_metadata(self):
        """Test creating snapshot with metadata"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", initial_data={"key": "value"})
        
        snapshot = isolation.create_snapshot(ctx_id, metadata={"reason": "backup"})
        assert snapshot.metadata == {"reason": "backup"}
    
    def test_restore_snapshot(self):
        """Test restoring context from snapshot"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1", initial_data={"key": "original"})
        snapshot = isolation.create_snapshot(ctx_id)
        
        # Modify context
        isolation.set_value(ctx_id, "key", "modified")
        
        # Restore
        isolation.restore_snapshot(ctx_id, snapshot)
        assert isolation.get_value(ctx_id, "key") == "original"
    
    def test_list_snapshots(self):
        """Test listing snapshots for context"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        isolation.create_snapshot(ctx_id)
        isolation.create_snapshot(ctx_id)
        
        snapshots = isolation.list_snapshots(ctx_id)
        assert len(snapshots) == 2
    
    def test_list_snapshots_empty(self):
        """Test listing snapshots for context with no snapshots"""
        isolation = ContextIsolation()
        ctx_id = isolation.create_context("ctx_1")
        
        snapshots = isolation.list_snapshots(ctx_id)
        assert snapshots == []
    
    def test_cleanup_empty_contexts(self):
        """Test cleaning up empty contexts"""
        isolation = ContextIsolation()
        ctx1_id = isolation.create_context("ctx1")
        ctx2_id = isolation.create_context("ctx2", initial_data={"key": "value"})
        
        removed = isolation.cleanup_empty_contexts()
        assert removed == 1
        assert ctx1_id not in isolation.contexts
        assert ctx2_id in isolation.contexts
    
    def test_get_context_stats(self):
        """Test getting context statistics"""
        isolation = ContextIsolation()
        isolation.create_context("ctx1", scope=ContextScope.LOCAL)
        isolation.create_context("ctx2", scope=ContextScope.SHARED)
        isolation.create_context("ctx3", scope=ContextScope.GLOBAL)
        
        stats = isolation.get_context_stats()
        assert stats["total_contexts"] == 3
        assert stats["local_contexts"] == 1
        assert stats["shared_contexts"] == 1
        assert stats["global_contexts"] == 1
        assert stats["total_snapshots"] == 0


class TestContextHierarchy:
    """Test context hierarchy functionality"""
    
    def test_nested_context_inheritance(self):
        """Test nested context inheritance"""
        isolation = ContextIsolation()
        
        # Create hierarchy: grandparent -> parent -> child
        grandparent_id = isolation.create_context("grandparent", 
                                                   initial_data={"level": "grandparent"},
                                                   scope=ContextScope.SHARED)
        parent_id = isolation.create_context("parent", 
                                             parent_id=grandparent_id,
                                             initial_data={"level": "parent"},
                                             scope=ContextScope.SHARED)
        child_id = isolation.create_context("child", 
                                           parent_id=parent_id,
                                           initial_data={"level": "child"},
                                           scope=ContextScope.SHARED)
        
        isolated = isolation.isolate_context(child_id)
        assert isolated["level"] == "child"  # Child overrides parent
    
    def test_get_context_chain(self):
        """Test getting full context chain"""
        isolation = ContextIsolation()
        
        grandparent_id = isolation.create_context("grandparent")
        parent_id = isolation.create_context("parent", parent_id=grandparent_id)
        child_id = isolation.create_context("child", parent_id=parent_id)
        
        chain = isolation.get_context_chain(child_id)
        assert len(chain) == 3
        assert grandparent_id in chain
        assert parent_id in chain
        assert child_id in chain
    
    def test_get_context_chain_root(self):
        """Test getting context chain for root context"""
        isolation = ContextIsolation()
        root_id = isolation.create_context("root")
        
        chain = isolation.get_context_chain(root_id)
        assert len(chain) == 1
        assert root_id in chain


class TestMultiTenant:
    """Test multi-tenant context isolation"""
    
    def test_tenant_isolation(self):
        """Test tenant contexts are isolated"""
        isolation = ContextIsolation()
        
        tenant1_id = isolation.create_context("tenant1", 
                                              initial_data={"secret": "tenant1_secret"},
                                              scope=ContextScope.LOCAL)
        tenant2_id = isolation.create_context("tenant2", 
                                              initial_data={"secret": "tenant2_secret"},
                                              scope=ContextScope.LOCAL)
        
        ctx1 = isolation.isolate_context(tenant1_id)
        ctx2 = isolation.isolate_context(tenant2_id)
        
        assert ctx1["secret"] == "tenant1_secret"
        assert ctx2["secret"] == "tenant2_secret"
    
    def test_global_shared_data(self):
        """Test global data accessible across contexts"""
        isolation = ContextIsolation()
        
        # Create global context
        global_id = isolation.create_context("global", 
                                            initial_data={"global_key": "global_value"},
                                            scope=ContextScope.GLOBAL)
        
        # Create another global context
        another_global_id = isolation.create_context("another_global",
                                                     initial_data={"another_key": "another_value"},
                                                     scope=ContextScope.GLOBAL)
        
        # Both should see each other's data
        isolated1 = isolation.isolate_context(global_id)
        isolated2 = isolation.isolate_context(another_global_id)
        
        assert "global_key" in isolated1
        assert "another_key" in isolated1
        assert "global_key" in isolated2
        assert "another_key" in isolated2
