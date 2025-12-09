"""
Context Isolation System
Provides context isolation for nested FSMs and multi-tenant scenarios.

Author: Álvaro Fernández Mota
Date: 09 December 2025
Version: 1.0.0
"""

from typing import Optional, Dict, Any, List, Set
from dataclasses import dataclass, field
from enum import Enum
from copy import deepcopy
import logging

logger = logging.getLogger(__name__)


class ContextNotFoundError(Exception):
    """Raised when context is not found"""
    pass


class ContextScopeError(Exception):
    """Raised when context scope operation is invalid"""
    pass


class ContextScope(Enum):
    """Context scope levels"""
    LOCAL = "local"      # Only current FSM
    SHARED = "shared"    # Parent and children
    GLOBAL = "global"    # All FSMs


@dataclass
class ContextSnapshot:
    """Snapshot of context state"""
    context_id: str
    data: Dict[str, Any]
    scope: ContextScope
    parent_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContextIsolation:
    """
    Manages isolated contexts for FSMs.
    
    Features:
        - Context isolation per FSM/user/tenant
        - Context inheritance in nested FSMs
        - Automatic cleanup
        - Context snapshots
    
    Example:
        >>> isolation = ContextIsolation()
        >>> ctx_id = isolation.create_context("user_123")
        >>> isolation.set_value(ctx_id, "key", "value")
    """
    
    def __init__(self):
        """Initialize context isolation system"""
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.context_hierarchy: Dict[str, Optional[str]] = {}
        self.context_scopes: Dict[str, ContextScope] = {}
        self.snapshots: Dict[str, List[ContextSnapshot]] = {}
        
        logger.info("ContextIsolation system initialized")
    
    def create_context(
        self,
        context_id: str,
        parent_id: Optional[str] = None,
        scope: ContextScope = ContextScope.LOCAL,
        initial_data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Create a new isolated context.
        
        Args:
            context_id: Unique context identifier
            parent_id: Parent context ID (for nested contexts)
            scope: Context scope level
            initial_data: Initial context data
            
        Returns:
            Created context ID
        """
        if initial_data is None:
            initial_data = {}
        
        # Create context with deep copy to avoid reference issues
        self.contexts[context_id] = deepcopy(initial_data)
        self.context_hierarchy[context_id] = parent_id
        self.context_scopes[context_id] = scope
        self.snapshots[context_id] = []
        
        logger.debug(f"Context created: {context_id} (scope={scope.value}, parent={parent_id})")
        return context_id
    
    def context_exists(self, context_id: str) -> bool:
        """
        Check if context exists.
        
        Args:
            context_id: Context identifier
            
        Returns:
            True if exists, False otherwise
        """
        return context_id in self.contexts
    
    def get_context(self, context_id: str) -> Dict[str, Any]:
        """
        Get context data.
        
        Args:
            context_id: Context identifier
            
        Returns:
            Context data dictionary
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        return self.contexts[context_id]
    
    def set_value(self, context_id: str, key: str, value: Any):
        """
        Set value in context.
        
        Args:
            context_id: Context identifier
            key: Key to set
            value: Value to set
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        self.contexts[context_id][key] = value
    
    def get_value(
        self,
        context_id: str,
        key: str,
        default: Any = None
    ) -> Any:
        """
        Get value from context.
        
        Args:
            context_id: Context identifier
            key: Key to get
            default: Default value if key not found
            
        Returns:
            Value or default
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        return self.contexts[context_id].get(key, default)
    
    def delete_value(self, context_id: str, key: str) -> bool:
        """
        Delete value from context.
        
        Args:
            context_id: Context identifier
            key: Key to delete
            
        Returns:
            True if deleted, False if key not found
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        if key in self.contexts[context_id]:
            del self.contexts[context_id][key]
            return True
        return False
    
    def clear_context(self, context_id: str):
        """
        Clear all data from context.
        
        Args:
            context_id: Context identifier
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        self.contexts[context_id].clear()
    
    def delete_context(self, context_id: str, cascade: bool = False) -> bool:
        """
        Delete context.
        
        Args:
            context_id: Context identifier
            cascade: If True, delete child contexts too
            
        Returns:
            True if deleted, False if not found
        """
        if context_id not in self.contexts:
            return False
        
        # Delete children if cascade
        if cascade:
            children = self.get_children_contexts(context_id)
            for child_id in children:
                self.delete_context(child_id, cascade=True)
        
        # Delete context
        del self.contexts[context_id]
        del self.context_hierarchy[context_id]
        del self.context_scopes[context_id]
        if context_id in self.snapshots:
            del self.snapshots[context_id]
        
        logger.debug(f"Context deleted: {context_id}")
        return True
    
    def get_parent_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """
        Get parent context data.
        
        Args:
            context_id: Context identifier
            
        Returns:
            Parent context data or None
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        parent_id = self.context_hierarchy.get(context_id)
        if parent_id and parent_id in self.contexts:
            return self.contexts[parent_id]
        return None
    
    def get_children_contexts(self, context_id: str) -> List[str]:
        """
        Get list of child context IDs.
        
        Args:
            context_id: Context identifier
            
        Returns:
            List of child context IDs
        """
        children = []
        for child_id, parent_id in self.context_hierarchy.items():
            if parent_id == context_id:
                children.append(child_id)
        return children
    
    def merge_contexts(
        self,
        context_id1: str,
        context_id2: str,
        allow_scope_mixing: bool = True
    ) -> Dict[str, Any]:
        """
        Merge two contexts (ctx2 overrides ctx1).
        
        Args:
            context_id1: First context ID
            context_id2: Second context ID
            allow_scope_mixing: Allow mixing different scopes
            
        Returns:
            Merged context data
            
        Raises:
            ContextNotFoundError: If contexts not found
            ContextScopeError: If scope mixing not allowed
        """
        if context_id1 not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id1}")
        if context_id2 not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id2}")
        
        # Check scope compatibility
        if not allow_scope_mixing:
            scope1 = self.context_scopes[context_id1]
            scope2 = self.context_scopes[context_id2]
            if scope1 != scope2:
                raise ContextScopeError(f"Cannot merge contexts with different scopes: {scope1} vs {scope2}")
        
        # Merge (ctx2 overrides ctx1)
        merged = deepcopy(self.contexts[context_id1])
        merged.update(self.contexts[context_id2])
        return merged
    
    def isolate_context(self, context_id: str) -> Dict[str, Any]:
        """
        Get isolated context based on scope.
        
        Args:
            context_id: Context identifier
            
        Returns:
            Isolated context data
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        scope = self.context_scopes[context_id]
        
        if scope == ContextScope.LOCAL:
            # LOCAL: Only own context
            return deepcopy(self.contexts[context_id])
        
        elif scope == ContextScope.SHARED:
            # SHARED: Include parent context
            result = {}
            parent_id = self.context_hierarchy.get(context_id)
            if parent_id and parent_id in self.contexts:
                result.update(self.contexts[parent_id])
            result.update(self.contexts[context_id])
            return result
        
        elif scope == ContextScope.GLOBAL:
            # GLOBAL: Include all global contexts
            result = {}
            for ctx_id, ctx_scope in self.context_scopes.items():
                if ctx_scope == ContextScope.GLOBAL:
                    result.update(self.contexts[ctx_id])
            return result
        
        return {}
    
    def create_snapshot(
        self,
        context_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> ContextSnapshot:
        """
        Create snapshot of context.
        
        Args:
            context_id: Context identifier
            metadata: Optional snapshot metadata
            
        Returns:
            ContextSnapshot object
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        snapshot = ContextSnapshot(
            context_id=context_id,
            data=deepcopy(self.contexts[context_id]),
            scope=self.context_scopes[context_id],
            parent_id=self.context_hierarchy.get(context_id),
            metadata=metadata or {}
        )
        
        self.snapshots[context_id].append(snapshot)
        logger.debug(f"Snapshot created for context: {context_id}")
        return snapshot
    
    def restore_snapshot(self, context_id: str, snapshot: ContextSnapshot):
        """
        Restore context from snapshot.
        
        Args:
            context_id: Context identifier
            snapshot: Snapshot to restore
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        self.contexts[context_id] = deepcopy(snapshot.data)
        logger.debug(f"Context restored from snapshot: {context_id}")
    
    def list_snapshots(self, context_id: str) -> List[ContextSnapshot]:
        """
        List all snapshots for context.
        
        Args:
            context_id: Context identifier
            
        Returns:
            List of snapshots
        """
        return self.snapshots.get(context_id, [])
    
    def cleanup_empty_contexts(self) -> int:
        """
        Remove all empty contexts.
        
        Returns:
            Number of contexts removed
        """
        empty_contexts = [
            ctx_id for ctx_id, ctx_data in self.contexts.items()
            if not ctx_data
        ]
        
        for ctx_id in empty_contexts:
            self.delete_context(ctx_id)
        
        logger.info(f"Cleaned up {len(empty_contexts)} empty contexts")
        return len(empty_contexts)
    
    def get_context_stats(self) -> Dict[str, Any]:
        """
        Get context statistics.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            "total_contexts": len(self.contexts),
            "local_contexts": sum(1 for s in self.context_scopes.values() if s == ContextScope.LOCAL),
            "shared_contexts": sum(1 for s in self.context_scopes.values() if s == ContextScope.SHARED),
            "global_contexts": sum(1 for s in self.context_scopes.values() if s == ContextScope.GLOBAL),
            "total_snapshots": sum(len(snaps) for snaps in self.snapshots.values())
        }
        return stats
    
    def get_context_chain(self, context_id: str) -> List[str]:
        """
        Get full context hierarchy chain.
        
        Args:
            context_id: Context identifier
            
        Returns:
            List of context IDs from root to current
            
        Raises:
            ContextNotFoundError: If context not found
        """
        if context_id not in self.contexts:
            raise ContextNotFoundError(f"Context not found: {context_id}")
        
        chain = [context_id]
        current_id = context_id
        
        # Traverse up to root
        while self.context_hierarchy.get(current_id):
            parent_id = self.context_hierarchy[current_id]
            chain.insert(0, parent_id)
            current_id = parent_id
        
        return chain
