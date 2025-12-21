"""
Interactive THEA CLI - Groq Real IA
Run: python run_real.py
"""

import sys
import asyncio
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.insert(0, str(Path(__file__).parent / "src"))

from theaia.core.conversation.cli import ConversationCLI


async def main():
    """Run interactive with real Groq IA"""
    
    # Verificar API key
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("\n❌ ERROR: GROQ_API_KEY no encontrada en .env")
        return
    
    print("\n" + "="*70)
    print("🤖 THEA - Interactive (Groq Real IA - FREE)")
    print("="*70)
    print("Commands: 'quit' | 'help' | 'memory'\n")
    
    cli = ConversationCLI(agent_name="THEA", model="llama-3.1-8b-instant")
    
    # Get user name
    name = input("👤 Your name? ").strip() or "User"
    cli.user_name = name
    print(f"✅ Hello {name}! Chat with THEA (Real IA, powered by Groq)\n")
    
    while True:
        try:
            user_input = input(f"{name}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print(f"\n👋 Goodbye, {name}!")
                summary = cli.memory.get_summary()
                print(f"📊 Total Messages: {summary['total_messages']}")
                print(f"📊 Session: {summary['session_id']}\n")
                break
            
            if user_input.lower() == "help":
                cli.show_help()
                continue
            
            if user_input.lower() == "memory":
                cli.show_memory()
                continue
            
            # Get REAL response from Groq IA
            print(f"\n🤖 THEA: ", end="", flush=True)
            
            try:
                response = await cli.agent.chat(user_input)
                print(response + "\n")
                
                # Add to memory
                cli.memory.add_message("user", user_input, {"user": name})
                cli.memory.add_message("assistant", response)
            
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye!\n")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
