"""
BookingAgent - Specialized agent for conversational appointment booking.

Features:
- Natural language understanding (Groq LLM)
- Tool calling for real appointment management
- Conversation history and context awareness
- 24/7 flexible scheduling with Spanish support
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from theaia.core.conversation.llm_client import LLMClient, LLMConfig
from theaia.services.groq_tools import GroqTools
from theaia.services.user_service import UserService
from theaia.services.booking_service import BookingService
from theaia.services.availability_engine import AvailabilityEngine

logger = logging.getLogger(__name__)


class BookingAgent:
    """
    Specialized agent for handling appointment booking conversations.
    
    Uses Groq LLM with tool calling to:
    - Understand natural language booking requests
    - Call tools for scheduling, checking availability, cancelling
    - Maintain conversation context
    - Provide Spanish responses
    """
    
    SYSTEM_PROMPT = """
Eres THEA IA, un asistente personal amigable y profesional para agendar citas.
Tienes acceso a herramientas REALES para gestionar citas.

PERSONALIDAD:
- Amigable pero profesional
- Español natural de España
- Conciso y claro
- Usa emojis ocasionalmente (📅, ✅, ⏰, 👋, 🗓️, 📋, ❌)

CAPACIDADES (herramientas REALES disponibles):
✅ check_availability - Ver horarios disponibles para una fecha
✅ create_appointment - Agendar citas reales en la BD
✅ get_appointments - Consultar citas del usuario
✅ cancel_appointment - Cancelar citas existentes

ESTRATEGIA DE CONVERSACIÓN:
1. Entiende exactamente qué necesita el usuario
2. Usa herramientas apropiadas automáticamente (sin comandos)
3. Confirma ANTES de hacer cambios importantes
4. Sé conciso - máximo 2-3 líneas normalmente
5. Directo al punto - pregunta solo lo necesario
6. Si algo falla, sugiere alternativas

IMPORTANTE:
- TÚ TIENES HERRAMIENTAS REALES, úsalas cuando sea apropiado
- Los datos se guardan en BD (no son simulados)
- Soporta horarios 24/7 (sin restricciones horarias)
- Maneja español fluido para fechas y horas
- Siempre confirma acciones importantes
- Sé natural, como una conversación real
    """
    
    def __init__(
        self,
        user_service: UserService,
        booking_service: BookingService,
        availability_engine: AvailabilityEngine,
        groq_tools: GroqTools,
        llm_client: Optional[LLMClient] = None
    ):
        """Initialize BookingAgent."""
        self.user_service = user_service
        self.booking_service = booking_service
        self.availability_engine = availability_engine
        self.groq_tools = groq_tools
        
        # Initialize LLM Client if not provided
        if llm_client is None:
            config = LLMConfig(
                model="mixtral-8x7b-32768",
                temperature=0.7,
                max_tokens=2048
            )
            self.llm_client = LLMClient(config)
        else:
            self.llm_client = llm_client
        
        # Setup tools in LLMClient
        self.llm_client.setup_tools(self.groq_tools)
        
        logger.info("✅ BookingAgent initialized with Groq tools")
    
    async def chat(
        self,
        user_message: str,
        user_id: int,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> str:
        """Process user message and return response with tool calling."""
        try:
            logger.info(f"📨 User {user_id}: {user_message}")
            
            # Build messages for LLM
            messages: List[Dict[str, str]] = []
            
            # Add conversation history if provided
            if conversation_history:
                messages.extend(conversation_history[-5:])  # Keep last 5 for context
            
            # Add current user message
            messages.append({
                "role": "user",
                "content": user_message
            })
            
            # Call Groq with tool support
            response = await self.llm_client.call_with_tools(
                messages=messages,
                system_prompt=self.SYSTEM_PROMPT,
                max_iterations=5
            )
            
            logger.info(f"✅ Response: {response[:100]}...")
            return response
            
        except Exception as e:
            error_msg = f"❌ Error in chat: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return "Disculpa, tuve un problema procesando tu solicitud. ¿Puedes repetir?"
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.llm_client.clear_history()
        logger.debug("🧹 Conversation history cleared")
    
    def get_history(self, last_n: Optional[int] = None) -> List[Dict[str, str]]:
        """Get conversation history."""
        return self.llm_client.get_history(last_n)


__all__ = ["BookingAgent"]
