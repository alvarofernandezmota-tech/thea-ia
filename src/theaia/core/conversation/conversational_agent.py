"""
H08.2 - Conversational Agent
Main agent class that uses LLM and integrates with H07 multi-agent system
"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
from datetime import datetime
import asyncio

from theaia.core.conversation.llm_client import LLMClient, LLMConfig, PromptTemplate


@dataclass
class AgentConfig:
    """Configuration for conversational agent"""
    name: str = "THEA"
    personality: str = "helpful, friendly, professional"
    tone: str = "conversational"
    max_history: int = 20
    model: str = "gpt-4-turbo"


class ConversationalAgent:
    """Main conversational agent class"""
    
    def __init__(
        self,
        agent_id: str = "conversational_agent",
        config: Optional[AgentConfig] = None,
        llm_config: Optional[LLMConfig] = None
    ):
        """Initialize conversational agent"""
        self.agent_id = agent_id
        self.config = config or AgentConfig()
        
        # Initialize LLM client
        llm_config = llm_config or LLMConfig(model=self.config.model)
        self.llm_client = LLMClient(llm_config)
        
        # Agent state
        self.conversation_history: List[Dict[str, str]] = []
        self.user_context: Dict[str, Any] = {}
        self.session_id: str = f"session_{datetime.now().timestamp()}"
        self.created_at = datetime.now()
    
    async def chat(
        self,
        user_message: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: Message from user
            user_context: Optional user context (name, preferences, etc)
        
        Returns:
            Agent response
        """
        # Update context if provided
        if user_context:
            self.user_context.update(user_context)
        
        # Build system prompt
        system_prompt = self._build_system_prompt()
        
        # Build context string
        context = self._build_context()
        
        # Get LLM response
        response = await self.llm_client.generate_response(
            user_message=user_message,
            system_prompt=system_prompt,
            context=context
        )
        
        # Store in history
        self.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": datetime.now().isoformat()
        })
        self.conversation_history.append({
            "role": "assistant",
            "content": response,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep history size limited
        if len(self.conversation_history) > self.config.max_history:
            self.conversation_history = self.conversation_history[-self.config.max_history:]
        
        return response
    
    def _build_system_prompt(self) -> str:
        """Build system prompt with personality"""
        base_prompt = PromptTemplate.SYSTEM_PROMPT
        
        personality_prompt = f"""
Your personality: {self.config.personality}
Tone: {self.config.tone}
Agent ID: {self.agent_id}
Session ID: {self.session_id}
"""
        
        return base_prompt + personality_prompt
    
    def _build_context(self) -> str:
        """Build context from history and user info"""
        context = ""
        
        # Add user context if available
        if self.user_context:
            context += "User Information:\n"
            for key, value in self.user_context.items():
                context += f"- {key}: {value}\n"
            context += "\n"
        
        # Add recent conversation history
        if self.conversation_history:
            context += PromptTemplate.build_context(
                self.conversation_history[-6:],
                self.user_context
            )
        
        return context
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def get_history_length(self) -> int:
        """Get number of messages in history"""
        return len(self.conversation_history)
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_session_info(self) -> Dict[str, Any]:
        """Get session information"""
        return {
            "agent_id": self.agent_id,
            "session_id": self.session_id,
            "created_at": self.created_at.isoformat(),
            "message_count": len(self.conversation_history),
            "user_context": self.user_context
        }
    
    async def close(self) -> None:
        """Close agent and clean up"""
        await self.llm_client.close()
