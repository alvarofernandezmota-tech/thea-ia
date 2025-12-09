"""
Tests for State Recovery System
Tests snapshot creation, restore, and recovery operations.

Author: Álvaro Fernández Mota
Date: 09 December 2025
"""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from src.theaia.core.fsm.state_recovery import (
    StateRecovery,
    StateSnapshot,
    SnapshotFormat,
    RecoveryStrategy
)


class MockFSM:
    """Mock FSM for testing"""
    def __init__(self, state="initial", context=None):
        self.current_state = state
        self.context = context or {}


class TestStateSnapshot:
    """Test StateSnapshot class"""
    
    def test_create_simple_snapshot(self):
        """Test creating a simple snapshot"""
        snapshot = StateSnapshot(
            snapshot_id="snap_1",
            timestamp=datetime.now(),
            state_name="processing",
            context={"key": "value"}
        )
        
        assert snapshot.snapshot_id == "snap_1"
        assert snapshot.state_name == "processing"
        assert snapshot.context["key"] == "value"
    
    def test_snapshot_auto_checksum(self):
        """Test checksum is auto-generated"""
        snapshot = StateSnapshot(
            snapshot_id="snap_1",
            timestamp=datetime.now(),
            state_name="test",
            context={}
        )
        
        assert snapshot.checksum is not None
        assert len(snapshot.checksum) == 64  # SHA256 hex
    
    def test_snapshot_verify_integrity_success(self):
        """Test integrity verification success"""
        snapshot = StateSnapshot(
            snapshot_id="snap_1",
            timestamp=datetime.now(),
            state_name="test",
            context={"data": 123}
        )
        
        assert snapshot.verify_integrity() is True
    
    def test_snapshot_verify_integrity_failure(self):
        """Test integrity verification failure"""
        snapshot = StateSnapshot(
            snapshot_id="snap_1",
            timestamp=datetime.now(),
            state_name="test",
            context={"data": 123}
        )
        
        # Tamper with data
        snapshot.context["data"] = 456
        
        assert snapshot.verify_integrity() is False
    
    def test_snapshot_to_dict(self):
        """Test converting snapshot to dict"""
        timestamp = datetime.now()
        snapshot = StateSnapshot(
            snapshot_id="snap_1",
            timestamp=timestamp,
            state_name="test",
            context={"key": "value"}
        )
        
        data = snapshot.to_dict()
        
        assert data["snapshot_id"] == "snap_1"
        assert data["state_name"] == "test"
        assert data["context"]["key"] == "value"
        assert "timestamp" in data
    
    def test_snapshot_from_dict(self):
        """Test creating snapshot from dict"""
        data = {
            "snapshot_id": "snap_1",
            "timestamp": datetime.now().isoformat(),
            "state_name": "test",
            "context": {"key": "value"},
            "metadata": {},
            "version": 1,
            "checksum": "abc123"
        }
        
        snapshot = StateSnapshot.from_dict(data)
        
        assert snapshot.snapshot_id == "snap_1"
        assert snapshot.state_name == "test"
        assert snapshot.context["key"] == "value"


class TestStateRecovery:
    """Test StateRecovery class"""
    
    def test_create_recovery_system(self):
        """Test creating recovery system"""
        recovery = StateRecovery()
        
        assert recovery.max_snapshots == 50
        assert recovery.auto_recovery is False
        assert len(recovery.snapshots) == 0
    
    def test_create_recovery_with_fsm(self):
        """Test recovery with FSM"""
        fsm = MockFSM(state="active", context={"user": "alice"})
        recovery = StateRecovery(fsm=fsm)
        
        assert recovery.fsm is fsm
    
    def test_create_snapshot_no_fsm(self):
        """Test creating snapshot without FSM"""
        recovery = StateRecovery()
        
        snapshot_id = recovery.create_snapshot(
            state_name="manual_state",
            context={"data": 123}
        )
        
        assert snapshot_id is not None
        assert len(recovery.snapshots) == 1
    
    def test_create_snapshot_from_fsm(self):
        """Test creating snapshot from FSM state"""
        fsm = MockFSM(state="processing", context={"count": 5})
        recovery = StateRecovery(fsm=fsm)
        
        snapshot_id = recovery.create_snapshot()
        
        snapshot = recovery.get_snapshot(snapshot_id)
        assert snapshot.state_name == "processing"
        assert snapshot.context["count"] == 5
    
    def test_create_snapshot_with_label(self):
        """Test creating labeled snapshot"""
        recovery = StateRecovery()
        
        snapshot_id = recovery.create_snapshot(
            label="before_update",
            state_name="ready",
            context={}
        )
        
        assert "before_update" in snapshot_id
    
    def test_create_snapshot_with_metadata(self):
        """Test creating snapshot with metadata"""
        recovery = StateRecovery()
        
        snapshot_id = recovery.create_snapshot(
            state_name="test",
            context={},
            author="alice",
            reason="backup"
        )
        
        snapshot = recovery.get_snapshot(snapshot_id)
        assert snapshot.metadata["author"] == "alice"
        assert snapshot.metadata["reason"] == "backup"
    
    def test_restore_snapshot(self):
        """Test restoring from snapshot"""
        fsm = MockFSM(state="initial", context={"value": 0})
        recovery = StateRecovery(fsm=fsm)
        
        # Create snapshot
        snapshot_id = recovery.create_snapshot()
        
        # Change FSM state
        fsm.current_state = "changed"
        fsm.context["value"] = 100
        
        # Restore
        result = recovery.restore_snapshot(snapshot_id)
        
        assert result is True
        assert fsm.current_state == "initial"
        assert fsm.context["value"] == 0
    
    def test_restore_snapshot_not_found(self):
        """Test restoring non-existent snapshot"""
        recovery = StateRecovery()
        
        with pytest.raises(ValueError, match="Snapshot not found"):
            recovery.restore_snapshot("nonexistent")
    
    def test_restore_snapshot_integrity_fail(self):
        """Test restore with failed integrity check"""
        fsm = MockFSM()
        recovery = StateRecovery(
            fsm=fsm,
            recovery_strategy=RecoveryStrategy.FAIL
        )
        
        # Create and tamper with snapshot
        snapshot_id = recovery.create_snapshot(state_name="test", context={})
        snapshot = recovery.snapshots[snapshot_id]
        snapshot.checksum = "invalid"
        
        with pytest.raises(RuntimeError, match="integrity check failed"):
            recovery.restore_snapshot(snapshot_id)
    
    def test_restore_snapshot_integrity_skip(self):
        """Test restore with skip strategy"""
        fsm = MockFSM()
        recovery = StateRecovery(
            fsm=fsm,
            recovery_strategy=RecoveryStrategy.SKIP
        )
        
        # Create and tamper
        snapshot_id = recovery.create_snapshot(state_name="test", context={})
        snapshot = recovery.snapshots[snapshot_id]
        snapshot.checksum = "invalid"
        
        result = recovery.restore_snapshot(snapshot_id)
        
        assert result is False
    
    def test_restore_snapshot_emergency_strategy(self):
        """Test restore with emergency strategy"""
        fsm = MockFSM(state="normal")
        recovery = StateRecovery(
            fsm=fsm,
            recovery_strategy=RecoveryStrategy.EMERGENCY
        )
        
        # Create and tamper
        snapshot_id = recovery.create_snapshot(state_name="test", context={})
        snapshot = recovery.snapshots[snapshot_id]
        snapshot.checksum = "invalid"
        
        result = recovery.restore_snapshot(snapshot_id)
        
        assert result is True
        assert fsm.current_state == "emergency"
    
    def test_get_snapshot(self):
        """Test getting snapshot by ID"""
        recovery = StateRecovery()
        
        snapshot_id = recovery.create_snapshot(state_name="test", context={})
        snapshot = recovery.get_snapshot(snapshot_id)
        
        assert snapshot is not None
        assert snapshot.snapshot_id == snapshot_id
    
    def test_get_snapshot_not_found(self):
        """Test getting non-existent snapshot"""
        recovery = StateRecovery()
        
        snapshot = recovery.get_snapshot("nonexistent")
        
        assert snapshot is None
    
    def test_list_snapshots_empty(self):
        """Test listing snapshots when empty"""
        recovery = StateRecovery()
        
        snapshots = recovery.list_snapshots()
        
        assert len(snapshots) == 0
    
    def test_list_snapshots_multiple(self):
        """Test listing multiple snapshots"""
        recovery = StateRecovery()
        
        # Create multiple snapshots
        for i in range(5):
            recovery.create_snapshot(
                state_name=f"state_{i}",
                context={"index": i}
            )
        
        snapshots = recovery.list_snapshots()
        
        assert len(snapshots) == 5
        # Should be in reverse order (most recent first)
        assert snapshots[0].context["index"] == 4
    
    def test_list_snapshots_with_limit(self):
        """Test listing snapshots with limit"""
        recovery = StateRecovery()
        
        for i in range(10):
            recovery.create_snapshot(state_name="test", context={})
        
        snapshots = recovery.list_snapshots(limit=3)
        
        assert len(snapshots) == 3
    
    def test_list_snapshots_filter_by_state(self):
        """Test filtering snapshots by state name"""
        recovery = StateRecovery()
        
        recovery.create_snapshot(state_name="state_a", context={})
        recovery.create_snapshot(state_name="state_b", context={})
        recovery.create_snapshot(state_name="state_a", context={})
        
        snapshots = recovery.list_snapshots(state_name="state_a")
        
        assert len(snapshots) == 2
    
    def test_delete_snapshot(self):
        """Test deleting a snapshot"""
        recovery = StateRecovery()
        
        snapshot_id = recovery.create_snapshot(state_name="test", context={})
        
        result = recovery.delete_snapshot(snapshot_id)
        
        assert result is True
        assert len(recovery.snapshots) == 0
    
    def test_delete_snapshot_not_found(self):
        """Test deleting non-existent snapshot"""
        recovery = StateRecovery()
        
        result = recovery.delete_snapshot("nonexistent")
        
        assert result is False
    
    def test_clear_all_snapshots(self):
        """Test clearing all snapshots"""
        recovery = StateRecovery()
        
        for i in range(5):
            recovery.create_snapshot(state_name="test", context={})
        
        count = recovery.clear_all_snapshots()
        
        assert count == 5
        assert len(recovery.snapshots) == 0
    
    def test_get_latest_snapshot(self):
        """Test getting latest snapshot"""
        recovery = StateRecovery()
        
        recovery.create_snapshot(state_name="old", context={})
        latest_id = recovery.create_snapshot(state_name="new", context={})
        
        latest = recovery.get_latest_snapshot()
        
        assert latest.snapshot_id == latest_id
        assert latest.state_name == "new"
    
    def test_get_latest_snapshot_empty(self):
        """Test getting latest when empty"""
        recovery = StateRecovery()
        
        latest = recovery.get_latest_snapshot()
        
        assert latest is None
    
    def test_rollback_to_latest(self):
        """Test rollback to latest snapshot"""
        fsm = MockFSM(state="initial", context={"value": 0})
        recovery = StateRecovery(fsm=fsm)
        
        # Create snapshot
        recovery.create_snapshot()
        
        # Change state
        fsm.current_state = "changed"
        fsm.context["value"] = 100
        
        # Rollback
        result = recovery.rollback_to_latest()
        
        assert result is True
        assert fsm.current_state == "initial"
    
    def test_rollback_to_latest_no_snapshots(self):
        """Test rollback with no snapshots"""
        recovery = StateRecovery()
        
        result = recovery.rollback_to_latest()
        
        assert result is False
    
    def test_get_snapshot_stats_empty(self):
        """Test stats with no snapshots"""
        recovery = StateRecovery()
        
        stats = recovery.get_snapshot_stats()
        
        assert stats["total_snapshots"] == 0
        assert stats["oldest_snapshot"] is None
    
    def test_get_snapshot_stats_with_snapshots(self):
        """Test stats with snapshots"""
        recovery = StateRecovery()
        
        recovery.create_snapshot(state_name="state_a", context={})
        recovery.create_snapshot(state_name="state_b", context={})
        recovery.create_snapshot(state_name="state_a", context={})
        
        stats = recovery.get_snapshot_stats()
        
        assert stats["total_snapshots"] == 3
        assert stats["states_covered"] == 2
        assert "state_a" in stats["state_names"]
        assert "state_b" in stats["state_names"]
    
    def test_max_snapshots_cleanup(self):
        """Test automatic cleanup of old snapshots"""
        recovery = StateRecovery(max_snapshots=5)
        
        # Create more than max
        for i in range(10):
            recovery.create_snapshot(state_name=f"state_{i}", context={})
        
        assert len(recovery.snapshots) == 5
        # Should keep most recent
        snapshots = recovery.list_snapshots()
        assert snapshots[-1].state_name == "state_5"  # Oldest kept
    
    def test_snapshot_persistence(self):
        """Test saving and loading from disk"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create recovery with storage
            recovery1 = StateRecovery(storage_path=tmpdir)
            
            snapshot_id = recovery1.create_snapshot(
                state_name="persisted",
                context={"data": 123}
            )
            
            # Create new recovery instance (loads from disk)
            recovery2 = StateRecovery(storage_path=tmpdir)
            
            snapshot = recovery2.get_snapshot(snapshot_id)
            assert snapshot is not None
            assert snapshot.state_name == "persisted"
            assert snapshot.context["data"] == 123
    
    def test_snapshot_disk_cleanup(self):
        """Test disk cleanup when deleting snapshots"""
        with tempfile.TemporaryDirectory() as tmpdir:
            recovery = StateRecovery(storage_path=tmpdir)
            
            snapshot_id = recovery.create_snapshot(
                state_name="test",
                context={}
            )
            
            # Verify file exists
            file_path = Path(tmpdir) / f"{snapshot_id}.json"
            assert file_path.exists()
            
            # Delete snapshot
            recovery.delete_snapshot(snapshot_id)
            
            # Verify file removed
            assert not file_path.exists()
    
    def test_restore_without_fsm(self):
        """Test restore works without FSM attached"""
        recovery = StateRecovery()
        
        snapshot_id = recovery.create_snapshot(
            state_name="test",
            context={}
        )
        
        result = recovery.restore_snapshot(snapshot_id)
        
        assert result is True
