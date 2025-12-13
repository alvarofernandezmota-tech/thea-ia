"""
Conversational Agent - Main conversation handler
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
from theaia.core.conversation.llm_client import LLMClient, LLMConfig


@dataclass
class AgentConfig:
    """Agent configuration"""
    name: str = "THEA"
    personality: str = "helpful and friendly"
    response_style: str = "conversational"
    model: str = "mixtral-8x7b-32768"


class ConversationalAgent:
    """Main conversational agent"""
    
    def __init__(self, config: AgentConfig, llm_config: LLMConfig):
        self.config = config
        self.llm_config = llm_config
        self.llm_client = LLMClient(llm_config)
    
    async def chat(
        self,
        message: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> str:
        """Chat with the agent"""
        
        # Build system prompt
        system_prompt = f"""You are {self.config.name}, a helpful AI assistant.
Personality: {self.config.personality}
Response style: {self.config.response_style}"""
        
        # Get response from LLM
        response = await self.llm_client.chat(
            message,
            system_prompt=system_prompt
        )
        
        return response
