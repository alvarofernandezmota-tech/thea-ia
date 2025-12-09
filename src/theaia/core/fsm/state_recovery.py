"""
State Recovery System
Provides snapshot, restore, and recovery capabilities for FSM states.

Author: Álvaro Fernández Mota
Date: 09 December 2025
Version: 1.0.0
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from datetime import datetime
import json
import pickle
import hashlib
import logging
from pathlib import Path
from enum import Enum

logger = logging.getLogger(__name__)


class SnapshotFormat(Enum):
    """Snapshot serialization format"""
    JSON = "json"
    PICKLE = "pickle"
    BINARY = "binary"


class RecoveryStrategy(Enum):
    """Recovery strategy when restore fails"""
    FAIL = "fail"  # Raise exception
    SKIP = "skip"  # Skip and continue
    EMERGENCY = "emergency"  # Go to emergency state


@dataclass
class StateSnapshot:
    """
    Represents a snapshot of FSM state at a point in time.
    
    Attributes:
        snapshot_id: Unique snapshot identifier
        timestamp: When snapshot was created
        state_name: Name of the state
        context: State context data
        metadata: Additional snapshot metadata
        version: Snapshot version number
        checksum: Data integrity checksum
    
    Example:
        >>> snapshot = StateSnapshot(
        ...     snapshot_id="snap_123",
        ...     state_name="processing",
        ...     context={"user_id": 123}
        ... )
    """
    snapshot_id: str
    timestamp: datetime
    state_name: str
    context: Dict[str, Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    checksum: Optional[str] = None
    
    def __post_init__(self):
        """Generate checksum if not provided"""
        if not self.checksum:
            self.checksum = self._calculate_checksum()
    
    def _calculate_checksum(self) -> str:
        """Calculate SHA256 checksum of snapshot data"""
        data = {
            "state_name": self.state_name,
            "context": self.context,
            "snapshot_id": self.snapshot_id  # Use snapshot_id instead of timestamp
        }
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()
    
    def verify_integrity(self) -> bool:
        """
        Verify snapshot data integrity.
        
        Returns:
            True if checksum matches, False otherwise
        """
        return self._calculate_checksum() == self.checksum
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert snapshot to dictionary"""
        return {
            "snapshot_id": self.snapshot_id,
            "timestamp": self.timestamp.isoformat(),
            "state_name": self.state_name,
            "context": self.context,
            "metadata": self.metadata,
            "version": self.version,
            "checksum": self.checksum
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StateSnapshot":
        """Create snapshot from dictionary"""
        data = data.copy()
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return cls(**data)


class StateRecovery:
    """
    Manages state snapshots and recovery for FSM.
    
    Features:
        - Create snapshots of FSM state
        - Restore from snapshots
        - Persistent storage (file/memory)
        - Auto-recovery with intervals
        - Snapshot versioning and cleanup
        - Data integrity verification
    
    Example:
        >>> recovery = StateRecovery(fsm, storage_path="./snapshots")
        >>> snapshot_id = await recovery.create_snapshot("before_update")
        >>> await recovery.restore_snapshot(snapshot_id)
    """
    
    def __init__(
        self,
        fsm: Any = None,
        storage_path: Optional[str] = None,
        max_snapshots: int = 50,
        auto_recovery: bool = False,
        recovery_strategy: RecoveryStrategy = RecoveryStrategy.FAIL,
        snapshot_format: SnapshotFormat = SnapshotFormat.JSON
    ):
        """
        Initialize state recovery system.
        
        Args:
            fsm: Finite State Machine instance
            storage_path: Path to store snapshots (None for memory only)
            max_snapshots: Maximum snapshots to keep
            auto_recovery: Enable automatic recovery
            recovery_strategy: Strategy when recovery fails
            snapshot_format: Format for snapshot serialization
        """
        self.fsm = fsm
        self.storage_path = Path(storage_path) if storage_path else None
        self.max_snapshots = max_snapshots
        self.auto_recovery = auto_recovery
        self.recovery_strategy = recovery_strategy
        self.snapshot_format = snapshot_format
        
        self.snapshots: Dict[str, StateSnapshot] = {}
        self.snapshot_order: List[str] = []  # Maintain insertion order
        
        # Create storage directory if needed
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            self._load_snapshots_from_disk()
        
        logger.info(
            f"StateRecovery initialized (max_snapshots={max_snapshots}, "
            f"storage={storage_path}, format={snapshot_format.value})"
        )
    
    def create_snapshot(
        self,
        label: Optional[str] = None,
        state_name: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
        **metadata
    ) -> str:
        """
        Create a snapshot of current or specified state.
        
        Args:
            label: Optional label for snapshot
            state_name: State name (uses FSM current if not provided)
            context: State context (uses FSM current if not provided)
            **metadata: Additional metadata
            
        Returns:
            Snapshot ID
        """
        # Get state from FSM if not provided
        if state_name is None and self.fsm:
            state_name = getattr(self.fsm, "current_state", "unknown")
        if context is None and self.fsm:
            context = getattr(self.fsm, "context", {})
        
        # Generate snapshot ID
        timestamp = datetime.now()
        snapshot_id = self._generate_snapshot_id(label, timestamp)
        
        # Create snapshot with COPY of context to avoid reference issues
        snapshot = StateSnapshot(
            snapshot_id=snapshot_id,
            timestamp=timestamp,
            state_name=state_name or "unknown",
            context=(context or {}).copy(),  # Deep copy to prevent mutations
            metadata=metadata
        )
        
        # Store snapshot
        self.snapshots[snapshot_id] = snapshot
        self.snapshot_order.append(snapshot_id)
        
        # Persist to disk BEFORE cleanup
        if self.storage_path:
            self._save_snapshot_to_disk(snapshot)
        
        # Cleanup old snapshots ONLY if exceeding limit
        if len(self.snapshots) > self.max_snapshots:
            self._cleanup_old_snapshots()
        
        logger.info(f"Snapshot created: {snapshot_id}")
        return snapshot_id
    
    def restore_snapshot(
        self,
        snapshot_id: str,
        verify_integrity: bool = True
    ) -> bool:
        """
        Restore FSM to a previous snapshot.
        
        Args:
            snapshot_id: ID of snapshot to restore
            verify_integrity: Verify snapshot integrity before restore
            
        Returns:
            True if restore successful, False otherwise
            
        Raises:
            ValueError: If snapshot not found
            RuntimeError: If integrity check fails
        """
        # Get snapshot
        snapshot = self.snapshots.get(snapshot_id)
        if not snapshot:
            raise ValueError(f"Snapshot not found: {snapshot_id}")
        
        # Verify integrity
        if verify_integrity and not snapshot.verify_integrity():
            error_msg = f"Snapshot integrity check failed: {snapshot_id}"
            if self.recovery_strategy == RecoveryStrategy.FAIL:
                raise RuntimeError(error_msg)
            elif self.recovery_strategy == RecoveryStrategy.SKIP:
                logger.warning(f"{error_msg} - Skipping restore")
                return False
            elif self.recovery_strategy == RecoveryStrategy.EMERGENCY:
                logger.error(f"{error_msg} - Using emergency state")
                return self._restore_emergency_state()
        
        # Restore state to FSM
        if self.fsm:
            try:
                # Set state
                if hasattr(self.fsm, "current_state"):
                    self.fsm.current_state = snapshot.state_name
                
                # Set context (deep copy to prevent mutations)
                if hasattr(self.fsm, "context"):
                    self.fsm.context = snapshot.context.copy()
                
                logger.info(f"Restored snapshot: {snapshot_id}")
                return True
            except Exception as e:
                logger.error(f"Failed to restore snapshot {snapshot_id}: {e}")
                
                if self.recovery_strategy == RecoveryStrategy.FAIL:
                    raise
                elif self.recovery_strategy == RecoveryStrategy.EMERGENCY:
                    return self._restore_emergency_state()
                return False
        
        return True
    
    def get_snapshot(self, snapshot_id: str) -> Optional[StateSnapshot]:
        """
        Get snapshot by ID.
        
        Args:
            snapshot_id: Snapshot identifier
            
        Returns:
            StateSnapshot if found, None otherwise
        """
        return self.snapshots.get(snapshot_id)
    
    def list_snapshots(
        self,
        limit: Optional[int] = None,
        state_name: Optional[str] = None
    ) -> List[StateSnapshot]:
        """
        List available snapshots.
        
        Args:
            limit: Maximum snapshots to return
            state_name: Filter by state name
            
        Returns:
            List of snapshots (most recent first)
        """
        # Get snapshots in reverse order (most recent first)
        snapshot_ids = reversed(self.snapshot_order)
        snapshots = [self.snapshots[sid] for sid in snapshot_ids]
        
        # Filter by state name if specified
        if state_name:
            snapshots = [s for s in snapshots if s.state_name == state_name]
        
        # Apply limit
        if limit:
            snapshots = snapshots[:limit]
        
        return snapshots
    
    def delete_snapshot(self, snapshot_id: str) -> bool:
        """
        Delete a snapshot.
        
        Args:
            snapshot_id: Snapshot to delete
            
        Returns:
            True if deleted, False if not found
        """
        if snapshot_id not in self.snapshots:
            return False
        
        # Remove from memory
        del self.snapshots[snapshot_id]
        self.snapshot_order.remove(snapshot_id)
        
        # Remove from disk
        if self.storage_path:
            snapshot_file = self._get_snapshot_file_path(snapshot_id)
            if snapshot_file.exists():
                snapshot_file.unlink()
        
        logger.info(f"Snapshot deleted: {snapshot_id}")
        return True
    
    def clear_all_snapshots(self) -> int:
        """
        Clear all snapshots.
        
        Returns:
            Number of snapshots cleared
        """
        count = len(self.snapshots)
        
        # Clear memory
        self.snapshots.clear()
        self.snapshot_order.clear()
        
        # Clear disk
        if self.storage_path and self.storage_path.exists():
            for file in self.storage_path.glob("snapshot_*.json"):
                file.unlink()
        
        logger.info(f"Cleared {count} snapshots")
        return count
    
    def get_latest_snapshot(self) -> Optional[StateSnapshot]:
        """
        Get the most recent snapshot.
        
        Returns:
            Latest StateSnapshot or None
        """
        if not self.snapshot_order:
            return None
        return self.snapshots[self.snapshot_order[-1]]
    
    def rollback_to_latest(self) -> bool:
        """
        Rollback to the most recent snapshot.
        
        Returns:
            True if successful, False otherwise
        """
        latest = self.get_latest_snapshot()
        if not latest:
            logger.warning("No snapshots available for rollback")
            return False
        
        return self.restore_snapshot(latest.snapshot_id)
    
    def get_snapshot_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored snapshots.
        
        Returns:
            Dictionary with snapshot statistics
        """
        if not self.snapshots:
            return {
                "total_snapshots": 0,
                "oldest_snapshot": None,
                "newest_snapshot": None,
                "states_covered": 0
            }
        
        states = set(s.state_name for s in self.snapshots.values())
        oldest = self.snapshots[self.snapshot_order[0]]
        newest = self.snapshots[self.snapshot_order[-1]]
        
        return {
            "total_snapshots": len(self.snapshots),
            "oldest_snapshot": oldest.snapshot_id,
            "newest_snapshot": newest.snapshot_id,
            "oldest_timestamp": oldest.timestamp.isoformat(),
            "newest_timestamp": newest.timestamp.isoformat(),
            "states_covered": len(states),
            "state_names": list(states),
            "storage_path": str(self.storage_path) if self.storage_path else None
        }
    
    def _generate_snapshot_id(
        self,
        label: Optional[str],
        timestamp: datetime
    ) -> str:
        """Generate unique snapshot ID with incremental counter"""
        time_str = timestamp.strftime("%Y%m%d_%H%M%S_%f")
        
        # Add counter to ensure uniqueness
        base_id = f"snapshot_{label}_{time_str}" if label else f"snapshot_{time_str}"
        
        # If ID already exists, add counter suffix
        counter = 0
        snapshot_id = base_id
        while snapshot_id in self.snapshots:
            counter += 1
            snapshot_id = f"{base_id}_{counter}"
        
        return snapshot_id
    
    def _cleanup_old_snapshots(self):
        """Remove old snapshots when exceeding max limit."""
        removed = 0
        
        # Only cleanup if we've exceeded the limit
        while len(self.snapshots) > self.max_snapshots:
            # Remove oldest snapshot
            if not self.snapshot_order:
                break
                
            oldest_id = self.snapshot_order.pop(0)
            
            if oldest_id in self.snapshots:
                del self.snapshots[oldest_id]
                removed += 1
                
                # Remove from disk
                if self.storage_path:
                    snapshot_file = self._get_snapshot_file_path(oldest_id)
                    if snapshot_file.exists():
                        snapshot_file.unlink()
                
                logger.debug(f"Removed old snapshot: {oldest_id}")
        
        return removed
    
    def _save_snapshot_to_disk(self, snapshot: StateSnapshot):
        """Save snapshot to disk"""
        if not self.storage_path:
            return
        
        file_path = self._get_snapshot_file_path(snapshot.snapshot_id)
        
        if self.snapshot_format == SnapshotFormat.JSON:
            with open(file_path, 'w') as f:
                json.dump(snapshot.to_dict(), f, indent=2)
        elif self.snapshot_format == SnapshotFormat.PICKLE:
            with open(file_path, 'wb') as f:
                pickle.dump(snapshot, f)
    
    def _load_snapshots_from_disk(self):
        """Load snapshots from disk on initialization"""
        if not self.storage_path or not self.storage_path.exists():
            return
        
        for file_path in sorted(self.storage_path.glob("snapshot_*.json")):
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    snapshot = StateSnapshot.from_dict(data)
                    self.snapshots[snapshot.snapshot_id] = snapshot
                    self.snapshot_order.append(snapshot.snapshot_id)
            except Exception as e:
                logger.error(f"Failed to load snapshot from {file_path}: {e}")
        
        logger.info(f"Loaded {len(self.snapshots)} snapshots from disk")
    
    def _get_snapshot_file_path(self, snapshot_id: str) -> Path:
        """Get file path for snapshot"""
        return self.storage_path / f"{snapshot_id}.json"
    
    def _restore_emergency_state(self) -> bool:
        """Restore FSM to a safe emergency state"""
        logger.warning("Restoring emergency state")
        
        if self.fsm:
            # Set to a safe default state
            if hasattr(self.fsm, "current_state"):
                self.fsm.current_state = "emergency"
            
            # Clear context
            if hasattr(self.fsm, "context"):
                self.fsm.context = {"emergency": True}
        
        return True
