# test_groq_manual.py (VERSION CORREGIDA - USER FIX)
import asyncio
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

async def test_groq_real():
    """Test rápido de BookingAgent con Groq REAL (sin mocks)"""
    
    print("🔧 Inicializando servicios...")
    
    # Imports
    from src.theaia.services.user_service import UserService
    from src.theaia.services.booking_service import BookingService
    from src.theaia.services.availability_engine import AvailabilityEngine
    from src.theaia.services.groq_tools import GroqTools
    from src.theaia.agents.booking_agent import BookingAgent
    
    # Setup servicios
    user_service = UserService()
    booking_service = BookingService()
    availability_engine = AvailabilityEngine()
    
    # Usuario test - USAR ID EXISTENTE (FIX)
    test_user_id = 1  # ID por defecto en BD
    print(f"✅ Usando usuario test ID: {test_user_id}")
    
    # Crear GroqTools
    groq_tools = GroqTools(
        booking_service=booking_service,
        availability_engine=availability_engine,
        user_id=test_user_id,
        user_service=user_service
    )
    
    # Crear BookingAgent
    agent = BookingAgent(
        user_service=user_service,
        booking_service=booking_service,
        availability_engine=availability_engine,
        groq_tools=groq_tools
    )
    
    print("✅ BookingAgent inicializado\n")
    
    # ========== TEST 1: Saludo ==========
    print("🤖 TEST 1: Saludo")
    print("Usuario: 'Hola'\n")
    
    try:
        response1 = await agent.chat(
            user_message="Hola",
            user_id=test_user_id,
            conversation_history=[]
        )
        print(f"✅ Bot: {response1}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return
    
    # ========== TEST 2: Check availability ==========
    print("🤖 TEST 2: Verificar disponibilidad")
    print("Usuario: '¿Qué horarios tienes disponibles mañana?'\n")
    
    try:
        response2 = await agent.chat(
            user_message="¿Qué horarios tienes disponibles mañana?",
            user_id=test_user_id,
            conversation_history=[
                {"role": "user", "content": "Hola"},
                {"role": "assistant", "content": response1}
            ]
        )
        print(f"✅ Bot: {response2}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return
    
    # ========== TEST 3: Agendar cita ==========
    print("🤖 TEST 3: Agendar cita")
    print("Usuario: 'Quiero agendar una cita mañana a las 3pm'\n")
    
    try:
        response3 = await agent.chat(
            user_message="Quiero agendar una cita mañana a las 3pm",
            user_id=test_user_id,
            conversation_history=[
                {"role": "user", "content": "Hola"},
                {"role": "assistant", "content": response1},
                {"role": "user", "content": "¿Qué horarios tienes disponibles mañana?"},
                {"role": "assistant", "content": response2}
            ]
        )
        print(f"✅ Bot: {response3}\n")
    except Exception as e:
        print(f"❌ Error: {e}\n")
        return
    
    print("=" * 60)
    print("✅ ¡TODOS LOS TESTS PASARON CON GROQ REAL!")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_groq_real())
