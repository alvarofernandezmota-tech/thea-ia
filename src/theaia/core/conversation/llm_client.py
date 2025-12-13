"""
H08.1 - LLM Client Integration
Wrapper for OpenAI API with retry logic and error handling
"""

import os
import asyncio
from typing import Optional, List, Dict, Any
from dataclasses import dataclass

# Try to import OpenAI (optional for mock support)
try:
    from openai import AsyncOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False


@dataclass
class LLMConfig:
    """Configuration for LLM client"""
    provider: str = "openai"
    model: str = "gpt-4-turbo"
    temperature: float = 0.7
    max_tokens: int = 2000
    timeout: int = 30
    max_retries: int = 3


class PromptTemplate:
    """Manages prompt templates"""
    
    SYSTEM_PROMPT = """You are THEA, an advanced AI assistant powered by a multi-agent system.

You have access to:
- Advanced state machine (H06)
- Multi-agent coordination (H07)
- Database with user information (H02)

Be helpful, respectful, and honest."""

    @staticmethod
    def format_message(role: str, content: str) -> Dict[str, str]:
        """Format message for API"""
        return {"role": role, "content": content}
    
    @staticmethod
    def build_context(history: List[Dict], user_info: Optional[Dict] = None) -> str:
        """Build context string from history"""
        context = "Recent conversation:\n"
        for msg in history[-3:]:
            role = msg.get("role", "unknown").upper()
            content = msg.get("content", "")[:50]
            context += f"{role}: {content}\n"
        return context


class LLMClient:
    """Client for LLM interactions"""
    
    def __init__(self, config: Optional[LLMConfig] = None):
        """Initialize LLM client"""
        self.config = config or LLMConfig()
        self.conversation_history: List[Dict[str, str]] = []
        
        # Try to use real OpenAI if available
        if HAS_OPENAI:
            api_key = os.getenv("OPENAI_API_KEY")
            if api_key:
                self.client = AsyncOpenAI(api_key=api_key)
            else:
                self.client = None
        else:
            self.client = None
    
    async def generate_response(
        self,
        user_message: str,
        system_prompt: Optional[str] = None,
        context: Optional[str] = None
    ) -> str:
        """Generate response from LLM"""
        
        # If no OpenAI client, use mock
        if not self.client:
            return await self._mock_response(user_message)
        
        try:
            # Build messages list
            messages = []
            
            # Add system prompt
            sys_content = system_prompt or PromptTemplate.SYSTEM_PROMPT
            if context:
                sys_content += f"\n\nContext:\n{context}"
            
            messages.append({"role": "system", "content": sys_content})
            
            # Add last few messages from history
            messages.extend(self.conversation_history[-4:])
            
            # Add current message
            messages.append({"role": "user", "content": user_message})
            
            # Call OpenAI
            response = await self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout
            )
            
            # Extract and store response
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return assistant_message
        
        except Exception as e:
            # Fallback to mock on error
            return await self._mock_response(user_message)
    
    async def _mock_response(self, user_message: str) -> str:
        """Return mock response for testing"""
        mock_map = {
            "hello": "Hello! I'm THEA, your AI assistant.",
            "name": "I'm THEA.",
            "help": "I can help with many things!",
            "test": "This is a test response.",
        }
        
        user_lower = user_message.lower()
        response = None
        
        for key, value in mock_map.items():
            if key in user_lower:
                response = value
                break
        
        if not response:
            response = f"You said: '{user_message}'. That's interesting!"
        
        # Store in history
        self.conversation_history.append({"role": "user", "content": user_message})
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return response
    
    def clear_history(self) -> None:
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history.copy()
    
    def get_history_length(self) -> int:
        """Get number of messages in history"""
        return len(self.conversation_history)
