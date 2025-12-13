"""
H08.5 - CLI Interface
Complete integration of LLM, Agent, Memory, and Tools
"""

import asyncio
from typing import Optional
from theaia.core.conversation.llm_client import LLMClient, LLMConfig
from theaia.core.conversation.conversational_agent import ConversationalAgent, AgentConfig
from theaia.core.conversation.memory import ConversationMemory, ContextBuilder
from theaia.core.conversation.tools import ToolRegistry, ToolExecutor, ToolChain


class ConversationCLI:
    """Interactive CLI for THEA agent"""
    
    def __init__(
        self,
        agent_name: str = "THEA",
        model: str = "gpt-4-turbo"
    ):
        """Initialize CLI with all components"""
        # LLM Configuration
        llm_config = LLMConfig(model=model)
        self.llm_client = LLMClient(llm_config)
        
        # Agent Configuration
        agent_config = AgentConfig(name=agent_name, model=model)
        self.agent = ConversationalAgent(config=agent_config, llm_config=llm_config)
        
        # Memory System
        self.memory = ConversationMemory(max_messages=100)
        
        # Tool System
        self.tool_registry = ToolRegistry()
        self.tool_executor = ToolExecutor(self.tool_registry)
        
        # State
        self.running = False
        self.user_name: Optional[str] = None
    
    async def start(self) -> None:
        """Start interactive session"""
        print("\n" + "="*60)
        print(f"🤖 {self.agent.config.name} - Conversational AI Agent")
        print("="*60)
        print("Type 'help' for commands | 'quit' to exit\n")
        
        self.running = True
        
        try:
            # Get user name
            self.user_name = input("👤 What's your name? ").strip() or "User"
            print(f"✅ Nice to meet you, {self.user_name}!\n")
            
            # Main loop
            while self.running:
                try:
                    user_input = input(f"{self.user_name}: ").strip()
                    
                    if not user_input:
                        continue
                    
                    if user_input.lower() == "quit":
                        await self.shutdown()
                        break
                    
                    if user_input.lower() == "help":
                        self.show_help()
                        continue
                    
                    if user_input.lower() == "memory":
                        self.show_memory()
                        continue
                    
                    if user_input.lower() == "clear":
                        self.memory.clear()
                        print("✅ Memory cleared\n")
                        continue
                    
                    # Process normal message
                    await self.process_message(user_input)
                
                except KeyboardInterrupt:
                    await self.shutdown()
                    break
                except Exception as e:
                    print(f"❌ Error: {e}\n")
        
        finally:
            await self.agent.llm_client.close()
    
    async def process_message(self, user_message: str) -> None:
        """Process user message and generate response"""
        print(f"\n🤖 {self.agent.config.name}: ", end="", flush=True)
        
        # Add to memory
        self.memory.add_message("user", user_message, {"user": self.user_name})
        
        # Prepare context
        context = ContextBuilder.build_with_summary(self.memory)
        
        # Get agent response
        response = await self.agent.chat(
            user_message,
            user_context={"name": self.user_name}
        )
        
        # Add response to memory
        self.memory.add_message("assistant", response)
        
        # Display response
        print(response + "\n")
    
    def show_help(self) -> None:
        """Show available commands"""
        print("""
📚 Available Commands:
  help    - Show this help message
  memory  - Show conversation memory summary
  clear   - Clear conversation history
  quit    - Exit the application

💡 Just type naturally to chat with THEA!
""")
    
    def show_memory(self) -> None:
        """Show memory summary"""
        summary = self.memory.get_summary()
        print(f"""
📝 Memory Summary:
  Total Messages: {summary['total_messages']}
  User Messages: {summary['user_messages']}
  Assistant Messages: {summary['assistant_messages']}
  Session: {summary['session_id']}
  Usage: {summary['usage_percent']:.1f}%

📋 Recent Conversation:
""")
        
        history = self.memory.get_history(last_n=3)
        for msg in history:
            role = "👤" if msg["role"] == "user" else "🤖"
            print(f"  {role} {msg['content'][:80]}...")
        print()
    
    async def shutdown(self) -> None:
        """Shutdown gracefully"""
        print(f"\n\n👋 Thanks for chatting, {self.user_name}!")
        print(f"📊 Final Stats:")
        summary = self.memory.get_summary()
        print(f"   - Messages: {summary['total_messages']}")
        print(f"   - Session: {summary['session_id']}")
        self.running = False


async def main():
    """Main entry point"""
    cli = ConversationCLI(agent_name="THEA", model="gpt-4-turbo")
    await cli.start()


if __name__ == "__main__":
    asyncio.run(main())
