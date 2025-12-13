"""
LLM Client - Groq OpenAI-compatible Integration
"""

import os
from typing import Optional, List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class LLMConfig:
    """LLM Configuration"""
    
    def __init__(
        self,
        model: str = "llama-3.1-8b-instant",
        temperature: float = 0.7,
        max_tokens: int = 2048
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens


class LLMClient:
    """LLM Client using Groq OpenAI-compatible API"""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                raise ValueError("GROQ_API_KEY not found in .env")
            
            # Use OpenAI client with Groq endpoint
            self.client = OpenAI(
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1"
            )
        except Exception as e:
            raise Exception(f"Groq initialization error: {e}")
        
        self.conversation_history: List[Dict[str, str]] = []
    
    async def chat(
        self,
        message: str,
        system_prompt: Optional[str] = None
    ) -> str:
        """Send message to Groq and get response"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": message
        })
        
        # Build messages for API
        messages: List[Dict[str, str]] = []
        
        # Add system prompt if provided
        if system_prompt:
            messages.append({
                "role": "system",
                "content": system_prompt
            })
        
        # Add conversation history (keep last 10 for context)
        messages.extend(self.conversation_history[-10:])
        
        try:
            # Call Groq API (OpenAI compatible)
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=messages,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            
            # Extract answer
            answer = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer
            })
            
            return answer
        
        except Exception as e:
            error_msg = f"❌ Groq Error: {str(e)}"
            print(error_msg)
            return error_msg
    
    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict]:
        """Get conversation history"""
        if last_n:
            return self.conversation_history[-last_n:]
        return self.conversation_history
    
    def get_history_length(self) -> int:
        """Get total conversation history length"""
        return len(self.conversation_history)
    
    async def close(self):
        """Cleanup resources"""
        pass
