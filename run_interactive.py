"""
Interactive THEA CLI Demo
Run: python run_interactive.py
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from theaia.core.conversation.cli import ConversationCLI


async def interactive_demo():
    """Run interactive demo with mock responses"""
    
    print("\n" + "="*70)
    print("🤖 THEA - Interactive Demo (Mock Mode)")
    print("="*70)
    print("Type 'quit' to exit | 'help' for commands | 'memory' to see history\n")
    
    cli = ConversationCLI(agent_name="THEA", model="gpt-4-turbo")
    
    # Get user name
    name = input("👤 What's your name? ").strip() or "User"
    cli.user_name = name
    print(f"✅ Nice to meet you, {name}!\n")
    
    # Mock responses
    mock_responses = {
        "hola": "¡Hola! ¿Cómo estás? Me da gusto conocerte.",
        "cómo estás": "Estoy muy bien, gracias por preguntar. ¿En qué puedo ayudarte?",
        "nombre": "Mi nombre es THEA, soy un asistente inteligente.",
        "ayuda": "Puedo: conversar, recordar contexto, hacer preguntas, y resolver problemas.",
        "gracias": "¡De nada! Fue un placer ayudarte.",
        "adiós": "¡Hasta luego! Espero volvamos a hablar.",
    }
    
    while True:
        try:
            user_input = input(f"{name}: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() == "quit":
                print(f"\n👋 Goodbye, {name}! Final stats:")
                summary = cli.memory.get_summary()
                print(f"   Messages: {summary['total_messages']}")
                print(f"   Session: {summary['session_id']}\n")
                break
            
            if user_input.lower() == "help":
                cli.show_help()
                continue
            
            if user_input.lower() == "memory":
                cli.show_memory()
                continue
            
            # Find matching response
            response = "Entiendo tu mensaje. ¿Puedo ayudarte con algo más?"
            for keyword, resp in mock_responses.items():
                if keyword in user_input.lower():
                    response = resp
                    break
            
            # Add to memory
            cli.memory.add_message("user", user_input, {"user": name})
            cli.memory.add_message("assistant", response)
            
            print(f"THEA: {response}\n")
            
        except KeyboardInterrupt:
            print(f"\n\n👋 Goodbye, {name}!\n")
            break
        except Exception as e:
            print(f"❌ Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(interactive_demo())
