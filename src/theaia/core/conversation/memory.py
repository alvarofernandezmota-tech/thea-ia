"""
H08.3 - Conversation Memory System
Manages conversation history with persistence and search capabilities
"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field


@dataclass
class Message:
    """Represents a single message in conversation"""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ConversationMemory:
    """Manages conversation history and memory"""
    
    def __init__(
        self,
        max_messages: int = 100,
        ttl_seconds: Optional[int] = None,
        session_id: Optional[str] = None
    ):
        """
        Initialize memory
        
        Args:
            max_messages: Maximum messages to store
            ttl_seconds: Time to live for messages (None = infinite)
            session_id: Session identifier
        """
        self.messages: List[Message] = []
        self.max_messages = max_messages
        self.ttl_seconds = ttl_seconds
        self.session_id = session_id or f"session_{datetime.now().timestamp()}"
        self.created_at = datetime.now()
    
    def add_message(
        self,
        role: str,
        content: str,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add message to memory"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        
        # Enforce max size
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
        
        # Clean expired messages if TTL set
        if self.ttl_seconds:
            self._cleanup_expired()
    
    def get_history(self, last_n: int = 10) -> List[Dict[str, str]]:
        """Get last N messages as dicts"""
        messages = self.messages[-last_n:]
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in messages
        ]
    
    def get_full_history(self) -> List[Dict[str, str]]:
        """Get all messages"""
        return self.get_history(last_n=len(self.messages))
    
    def search(self, keyword: str) -> List[Dict[str, Any]]:
        """Search messages by keyword"""
        results = []
        keyword_lower = keyword.lower()
        
        for i, msg in enumerate(self.messages):
            if keyword_lower in msg.content.lower():
                results.append({
                    "index": i,
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                })
        
        return results
    
    def get_user_messages(self) -> List[str]:
        """Get all user messages"""
        return [msg.content for msg in self.messages if msg.role == "user"]
    
    def get_assistant_messages(self) -> List[str]:
        """Get all assistant messages"""
        return [msg.content for msg in self.messages if msg.role == "assistant"]
    
    def clear(self) -> None:
        """Clear all messages"""
        self.messages = []
    
    def get_message_count(self) -> int:
        """Get total messages"""
        return len(self.messages)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get memory summary"""
        user_count = len([m for m in self.messages if m.role == "user"])
        assistant_count = len([m for m in self.messages if m.role == "assistant"])
        
        return {
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "total_messages": len(self.messages),
            "user_messages": user_count,
            "assistant_messages": assistant_count,
            "max_capacity": self.max_messages,
            "usage_percent": (len(self.messages) / self.max_messages) * 100
        }
    
    def _cleanup_expired(self) -> None:
        """Remove expired messages based on TTL"""
        if not self.ttl_seconds:
            return
        
        now = datetime.now()
        cutoff = now - timedelta(seconds=self.ttl_seconds)
        
        self.messages = [
            msg for msg in self.messages
            if msg.timestamp > cutoff
        ]


class ContextBuilder:
    """Builds context strings from memory and metadata"""
    
    @staticmethod
    def build_from_memory(memory: ConversationMemory, max_history: int = 5) -> str:
        """Build context from conversation memory"""
        context = "Conversation context:\n"
        
        history = memory.get_history(last_n=max_history)
        for msg in history:
            role = msg["role"].upper()
            content = msg["content"][:100]  # Truncate long messages
            context += f"{role}: {content}\n"
        
        return context
    
    @staticmethod
    def build_with_summary(memory: ConversationMemory) -> str:
        """Build context with memory summary"""
        summary = memory.get_summary()
        context = f"""Memory Summary:
- Total messages: {summary['total_messages']}
- User messages: {summary['user_messages']}
- Assistant messages: {summary['assistant_messages']}
- Session started: {summary['created_at']}

Recent conversation:
"""
        
        history = memory.get_history(last_n=3)
        for msg in history:
            role = msg["role"].upper()
            content = msg["content"][:80]
            context += f"{role}: {content}\n"
        
        return context
