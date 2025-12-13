"""
Real Conversation Test - Full Integration Demo
Tests actual conversation flow with mock LLM
"""

import asyncio
from theaia.core.conversation.cli import ConversationCLI


async def test_real_conversation():
    """Run a real conversation simulation"""
    
    print("\n" + "="*70)
    print("🤖 THEA - Real Conversation Test")
    print("="*70 + "\n")
    
    # Create CLI
    cli = ConversationCLI(agent_name="THEA", model="gpt-4-turbo")
    cli.user_name = "Álvaro"
    
    # Simulate conversation
    messages = [
        "Hola THEA, ¿cómo estás?",
        "¿Cuál es tu nombre?",
        "¿Qué puedes hacer?",
        "Cuéntame un chiste",
        "Gracias por la conversación"
    ]
    
    print(f"👤 {cli.user_name}: Starting conversation with THEA\n")
    
    for msg in messages:
        print(f"👤 {cli.user_name}: {msg}")
        
        # Mock response for demo
        responses = {
            "Hola THEA, ¿cómo estás?": "¡Hola Álvaro! Estoy muy bien, gracias por preguntar. ¿Cómo estás tú?",
            "¿Cuál es tu nombre?": "Mi nombre es THEA, soy un asistente de IA conversacional. Fue un placer conocerte.",
            "¿Qué puedes hacer?": "Puedo ayudarte con: conversaciones naturales, responder preguntas, recordar contexto, y ejecutar herramientas personalizadas.",
            "Cuéntame un chiste": "¿Por qué los programadores prefieren el dark mode? Porque la luz atrae bugs! 😄",
            "Gracias por la conversación": "¡De nada Álvaro! Fue un placer conversar contigo. Espero volvamos a hablar pronto. 👋"
        }
        
        response = responses.get(msg, "Entiendo tu mensaje. ¿Puedo ayudarte con algo más?")
        
        # Add to memory
        cli.memory.add_message("user", msg, {"user": cli.user_name})
        cli.memory.add_message("assistant", response)
        
        print(f"🤖 THEA: {response}\n")
        
        # Small delay for readability
        await asyncio.sleep(0.5)
    
    # Show final memory stats
    print("\n" + "="*70)
    print("📊 Conversation Statistics")
    print("="*70)
    summary = cli.memory.get_summary()
    print(f"Total Messages: {summary['total_messages']}")
    print(f"User Messages: {summary['user_messages']}")
    print(f"Assistant Messages: {summary['assistant_messages']}")
    print(f"Session ID: {summary['session_id']}")
    print(f"Memory Usage: {summary['usage_percent']:.1f}%")
    
    print("\n" + "="*70)
    print("✅ Conversation completed successfully!")
    print("="*70 + "\n")
    
    return True


if __name__ == "__main__":
    result = asyncio.run(test_real_conversation())
    if result:
        print("🎉 Demo completed!\n")
