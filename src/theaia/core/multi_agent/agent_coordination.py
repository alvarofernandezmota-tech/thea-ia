"""Agent Coordination System - H07.5

Provides distributed coordination mechanisms for multi-agent systems:
- Consensus-based decision making
- Leader election (Bully algorithm)
- Distributed locks (mutex pattern)
- Heartbeat monitoring for agent health
- Deadlock detection and prevention
"""

import asyncio
import time
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Set, Callable
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class ConsensusVote(Enum):
    """Consensus voting options."""
    AGREE = "agree"
    DISAGREE = "disagree"
    ABSTAIN = "abstain"


class LockStatus(Enum):
    """Distributed lock status."""
    FREE = "free"
    LOCKED = "locked"
    WAITING = "waiting"
    RELEASED = "released"


class AgentState(Enum):
    """Agent election state."""
    FOLLOWER = "follower"
    CANDIDATE = "candidate"
    LEADER = "leader"
    DEAD = "dead"


@dataclass
class ConsensusProposal:
    """Proposal for consensus voting."""
    proposal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    proposer_id: str = ""
    description: str = ""
    required_votes: int = 1
    timeout_seconds: float = 30.0
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    votes: Dict[str, ConsensusVote] = field(default_factory=dict)
    expired: bool = False
    result: Optional[bool] = None
    
    def is_expired(self) -> bool:
        """Check if proposal has expired."""
        elapsed = (datetime.utcnow() - self.created_at).total_seconds()
        return elapsed > self.timeout_seconds
    
    def get_agree_count(self) -> int:
        """Count AGREE votes."""
        return sum(1 for v in self.votes.values() if v == ConsensusVote.AGREE)
    
    def get_disagree_count(self) -> int:
        """Count DISAGREE votes."""
        return sum(1 for v in self.votes.values() if v == ConsensusVote.DISAGREE)
    
    def is_resolved(self) -> bool:
        """Check if consensus is reached."""
        return self.get_agree_count() >= self.required_votes


@dataclass
class DistributedLock:
    """Distributed lock with timeout and ownership."""
    lock_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    resource_id: str = ""
    owner_agent_id: Optional[str] = None
    status: LockStatus = LockStatus.FREE
    acquired_at: Optional[datetime] = None
    timeout_seconds: float = 60.0
    
    waiting_queue: List[str] = field(default_factory=list)
    
    def is_expired(self) -> bool:
        """Check if lock has expired."""
        if self.acquired_at is None:
            return False
        elapsed = (datetime.utcnow() - self.acquired_at).total_seconds()
        return elapsed > self.timeout_seconds and self.owner_agent_id is not None
    
    def acquire(self, agent_id: str) -> bool:
        """Try to acquire lock."""
        if self.status == LockStatus.FREE or self.is_expired():
            self.owner_agent_id = agent_id
            self.status = LockStatus.LOCKED
            self.acquired_at = datetime.utcnow()
            return True
        elif agent_id not in self.waiting_queue:
            self.waiting_queue.append(agent_id)
            self.status = LockStatus.WAITING
        return False
    
    def release(self, agent_id: str) -> bool:
        """Release lock if owner."""
        if self.owner_agent_id == agent_id:
            self.owner_agent_id = None
            self.status = LockStatus.RELEASED
            self.acquired_at = None
            return True
        return False
    
    def get_next_waiter(self) -> Optional[str]:
        """Get next waiting agent."""
        return self.waiting_queue.pop(0) if self.waiting_queue else None


@dataclass
class LeaderElectionState:
    """Tracks leader election state for an agent."""
    agent_id: str
    state: AgentState = AgentState.FOLLOWER
    current_leader: Optional[str] = None
    current_term: int = 0
    voted_for: Optional[str] = None
    last_heartbeat: datetime = field(default_factory=datetime.utcnow)
    heartbeat_timeout_ms: int = 150
    
    def is_heartbeat_expired(self) -> bool:
        """Check if heartbeat timeout expired."""
        elapsed_ms = (datetime.utcnow() - self.last_heartbeat).total_seconds() * 1000
        return elapsed_ms > self.heartbeat_timeout_ms


class ConsensusEngine:
    """Manages consensus voting for group decisions."""
    
    def __init__(self):
        self.proposals: Dict[str, ConsensusProposal] = {}
        self.lock = asyncio.Lock()
    
    async def propose(self, proposer_id: str, description: str, 
                     required_votes: int = 1, timeout_seconds: float = 30.0) -> str:
        """Create new proposal."""
        async with self.lock:
            proposal = ConsensusProposal(
                proposer_id=proposer_id,
                description=description,
                required_votes=required_votes,
                timeout_seconds=timeout_seconds
            )
            self.proposals[proposal.proposal_id] = proposal
            logger.info(f"Proposal created: {proposal.proposal_id} by {proposer_id}")
            return proposal.proposal_id
    
    async def vote(self, proposal_id: str, agent_id: str, 
                  vote: ConsensusVote) -> bool:
        """Cast vote on proposal."""
        async with self.lock:
            if proposal_id not in self.proposals:
                logger.warning(f"Proposal {proposal_id} not found")
                return False
            
            proposal = self.proposals[proposal_id]
            if proposal.is_expired():
                proposal.expired = True
                return False
            
            proposal.votes[agent_id] = vote
            
            # Check if consensus reached
            if proposal.is_resolved():
                proposal.result = True
                logger.info(f"Consensus reached on {proposal_id}: AGREED")
            
            return True
    
    async def get_result(self, proposal_id: str) -> Optional[bool]:
        """Get proposal result."""
        async with self.lock:
            if proposal_id not in self.proposals:
                return None
            
            proposal = self.proposals[proposal_id]
            if proposal.is_expired():
                proposal.expired = True
                return False
            
            return proposal.result
    
    async def cleanup_expired(self):
        """Remove expired proposals."""
        async with self.lock:
            expired_ids = [
                pid for pid, p in self.proposals.items() 
                if p.is_expired()
            ]
            for pid in expired_ids:
                del self.proposals[pid]
            return len(expired_ids)


class DistributedLockManager:
    """Manages distributed locks across agents."""
    
    def __init__(self):
        self.locks: Dict[str, DistributedLock] = {}
        self.lock = asyncio.Lock()
        self.lock_callbacks: Dict[str, List[Callable]] = {}  # resource_id -> callbacks
    
    async def acquire_lock(self, resource_id: str, agent_id: str, 
                          timeout_seconds: float = 60.0) -> Optional[str]:
        """Try to acquire lock on resource."""
        async with self.lock:
            if resource_id not in self.locks:
                self.locks[resource_id] = DistributedLock(
                    resource_id=resource_id,
                    timeout_seconds=timeout_seconds
                )
            
            lock = self.locks[resource_id]
            if lock.acquire(agent_id):
                logger.info(f"Lock acquired: {resource_id} by {agent_id}")
                await self._trigger_callbacks(resource_id, "acquired")
                return lock.lock_id
            
            logger.debug(f"Lock not available: {resource_id} for {agent_id}")
            return None
    
    async def release_lock(self, lock_id: str, agent_id: str, 
                          resource_id: str) -> bool:
        """Release lock."""
        async with self.lock:
            if resource_id not in self.locks:
                return False
            
            lock = self.locks[resource_id]
            if lock.release(agent_id):
                logger.info(f"Lock released: {resource_id} by {agent_id}")
                
                # Grant lock to next waiting agent
                next_agent = lock.get_next_waiter()
                if next_agent:
                    lock.acquire(next_agent)
                    logger.info(f"Lock granted to next waiter: {next_agent}")
                
                await self._trigger_callbacks(resource_id, "released")
                return True
            
            return False
    
    async def is_locked(self, resource_id: str) -> bool:
        """Check if resource is locked."""
        async with self.lock:
            if resource_id not in self.locks:
                return False
            lock = self.locks[resource_id]
            return lock.status == LockStatus.LOCKED
    
    async def cleanup_expired(self):
        """Release expired locks."""
        async with self.lock:
            released = 0
            for lock in self.locks.values():
                if lock.is_expired():
                    lock.owner_agent_id = None
                    lock.status = LockStatus.FREE
                    released += 1
            return released
    
    async def register_callback(self, resource_id: str, callback: Callable):
        """Register callback for lock events."""
        if resource_id not in self.lock_callbacks:
            self.lock_callbacks[resource_id] = []
        self.lock_callbacks[resource_id].append(callback)
    
    async def _trigger_callbacks(self, resource_id: str, event: str):
        """Trigger callbacks for resource."""
        if resource_id in self.lock_callbacks:
            for callback in self.lock_callbacks[resource_id]:
                try:
                    if asyncio.iscoroutinefunction(callback):
                        await callback(resource_id, event)
                    else:
                        callback(resource_id, event)
                except Exception as e:
                    logger.error(f"Error in lock callback: {e}")


class LeaderElectionManager:
    """Manages leader election using Bully algorithm."""
    
    def __init__(self):
        self.agents: Dict[str, LeaderElectionState] = {}
        self.lock = asyncio.Lock()
    
    async def register_agent(self, agent_id: str):
        """Register agent in election system."""
        async with self.lock:
            if agent_id not in self.agents:
                self.agents[agent_id] = LeaderElectionState(agent_id=agent_id)
                logger.info(f"Agent registered: {agent_id}")
    
    async def start_election(self, agent_id: str) -> Optional[str]:
        """Start leader election (Bully algorithm)."""
        async with self.lock:
            if agent_id not in self.agents:
                await self.register_agent(agent_id)
            
            agent = self.agents[agent_id]
            agent.state = AgentState.CANDIDATE
            agent.current_term += 1
            agent.voted_for = agent_id
            
            # Bully algorithm: agent with highest ID becomes leader
            higher_agents = [
                a for a in self.agents.values() 
                if a.agent_id > agent_id and a.state != AgentState.DEAD
            ]
            
            if not higher_agents:
                # No higher agents, this agent is leader
                agent.state = AgentState.LEADER
                agent.current_leader = agent_id
                
                # Update all other agents
                for other in self.agents.values():
                    if other.agent_id != agent_id:
                        other.current_leader = agent_id
                        other.state = AgentState.FOLLOWER
                
                logger.info(f"Leader elected: {agent_id}")
                return agent_id
            
            # Send election messages to higher agents (mocked)
            logger.debug(f"Election started by {agent_id}, higher agents exist")
            return None
    
    async def heartbeat(self, leader_id: str):
        """Process heartbeat from leader."""
        async with self.lock:
            for agent in self.agents.values():
                if agent.agent_id != leader_id:
                    agent.last_heartbeat = datetime.utcnow()
                    agent.current_leader = leader_id
                    agent.state = AgentState.FOLLOWER
    
    async def detect_leader_failure(self) -> Optional[str]:
        """Detect leader failure and trigger new election."""
        async with self.lock:
            # Find current leader
            leaders = [a for a in self.agents.values() if a.state == AgentState.LEADER]
            
            if not leaders:
                return None
            
            leader = leaders[0]
            
            # Check if heartbeat expired
            if leader.is_heartbeat_expired():
                logger.warning(f"Leader {leader.agent_id} failed")
                leader.state = AgentState.DEAD
                return leader.agent_id
            
            return None
    
    async def get_leader(self) -> Optional[str]:
        """Get current leader."""
        async with self.lock:
            leaders = [a for a in self.agents.values() if a.state == AgentState.LEADER]
            return leaders[0].agent_id if leaders else None
    
    async def get_agent_state(self, agent_id: str) -> Optional[AgentState]:
        """Get agent state."""
        async with self.lock:
            if agent_id in self.agents:
                return self.agents[agent_id].state
            return None


class DeadlockDetector:
    """Detects and prevents deadlocks in distributed system."""
    
    def __init__(self):
        self.wait_for_graph: Dict[str, Set[str]] = {}  # agent -> agents it waits for
        self.lock = asyncio.Lock()
        self.max_wait_time_seconds = 300  # 5 minutes
    
    async def add_wait_edge(self, waiting_agent: str, held_by_agent: str):
        """Add edge to wait-for graph."""
        async with self.lock:
            if waiting_agent not in self.wait_for_graph:
                self.wait_for_graph[waiting_agent] = set()
            self.wait_for_graph[waiting_agent].add(held_by_agent)
    
    async def remove_wait_edge(self, waiting_agent: str, held_by_agent: str):
        """Remove edge from wait-for graph."""
        async with self.lock:
            if waiting_agent in self.wait_for_graph:
                self.wait_for_graph[waiting_agent].discard(held_by_agent)
    
    async def detect_cycle(self) -> Optional[List[str]]:
        """Detect cycle in wait-for graph using DFS."""
        async with self.lock:
            visited = set()
            rec_stack = set()
            
            def dfs(node: str, path: List[str]) -> Optional[List[str]]:
                visited.add(node)
                rec_stack.add(node)
                path.append(node)
                
                for neighbor in self.wait_for_graph.get(node, set()):
                    if neighbor not in visited:
                        result = dfs(neighbor, path.copy())
                        if result:
                            return result
                    elif neighbor in rec_stack:
                        # Found cycle
                        cycle_start = path.index(neighbor)
                        return path[cycle_start:] + [neighbor]
                
                rec_stack.remove(node)
                return None
            
            for node in self.wait_for_graph:
                if node not in visited:
                    result = dfs(node, [])
                    if result:
                        logger.error(f"Deadlock detected: {' -> '.join(result)}")
                        return result
            
            return None
    
    async def get_statistics(self) -> Dict:
        """Get deadlock detector statistics."""
        async with self.lock:
            return {
                "total_agents": len(self.wait_for_graph),
                "total_edges": sum(len(v) for v in self.wait_for_graph.values()),
                "agents_waiting": len([a for a in self.wait_for_graph if self.wait_for_graph[a]])
            }


class CoordinationEngine:
    """Main coordination engine combining all coordination mechanisms."""
    
    def __init__(self):
        self.consensus = ConsensusEngine()
        self.locks = DistributedLockManager()
        self.leader_election = LeaderElectionManager()
        self.deadlock_detector = DeadlockDetector()
        
        self.cleanup_task: Optional[asyncio.Task] = None
    
    async def start(self, cleanup_interval: float = 10.0):
        """Start coordination engine background tasks."""
        self.cleanup_task = asyncio.create_task(
            self._cleanup_loop(cleanup_interval)
        )
        logger.info("Coordination engine started")
    
    async def stop(self):
        """Stop coordination engine."""
        if self.cleanup_task:
            self.cleanup_task.cancel()
            try:
                await self.cleanup_task
            except asyncio.CancelledError:
                pass
        logger.info("Coordination engine stopped")
    
    async def _cleanup_loop(self, interval: float):
        """Periodically cleanup expired resources."""
        try:
            while True:
                await asyncio.sleep(interval)
                
                expired_proposals = await self.consensus.cleanup_expired()
                expired_locks = await self.locks.cleanup_expired()
                
                if expired_proposals > 0 or expired_locks > 0:
                    logger.debug(
                        f"Cleanup: {expired_proposals} proposals, {expired_locks} locks"
                    )
        except asyncio.CancelledError:
            pass
    
    async def get_statistics(self) -> Dict:
        """Get coordination engine statistics."""
        return {
            "consensus_proposals": len(self.consensus.proposals),
            "active_locks": sum(1 for l in self.locks.locks.values() 
                               if l.status == LockStatus.LOCKED),
            "registered_agents": len(self.leader_election.agents),
            "deadlock_info": await self.deadlock_detector.get_statistics()
        }
