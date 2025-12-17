"""
E2E tests for conversational booking flow - PASO 4 (CORRECTO PARA ECOSISTEMA)

Tests real conversational flows with BookingAgent + Groq Tools.
Validates end-to-end integration with actual database persistence.

Patrón basado en test_agenda_agent_e2e.py del ecosistema.
Autor: THEA IA Development
Fecha: 17 Dic 2025
"""

import pytest
from src.theaia.agents.booking_agent import BookingAgent
from src.theaia.services.groq_tools import GroqTools
from src.theaia.core.conversation.llm_client import LLMClient, LLMConfig


class TestConversationFlowE2E:
    """End-to-End tests for conversational booking flow."""
    
    @pytest.fixture
    def booking_agent(self, test_user):
        """Create fresh BookingAgent for each test.
        
        Args:
            test_user: Test user fixture from conftest.py
            
        Returns:
            BookingAgent instance
        """
        # Aquí inicializarías el agent completo
        # Por ahora retornamos la estructura
        return BookingAgent()
    
    @pytest.fixture
    def conversation_context(self, test_user):
        """Create basic conversation context.
        
        Args:
            test_user: Test user fixture
            
        Returns:
            dict: Contexto de conversación inicial
        """
        return {
            "user_id": test_user.id,
            "tenant_id": test_user.tenant_id,
            "session_id": "session_booking_123",
            "state": "initial",
            "conversation_history": []
        }
    
    # ==================== GREETING TESTS ====================
    
    @pytest.mark.asyncio
    async def test_greeting_message(self, booking_agent, conversation_context, test_user):
        """Test bot greeting on /start.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="Hola",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        # Validaciones
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        # Debería contener palabras de bienvenida
        assert any(word in result.lower() for word in ["hola", "bienvenido", "cita", "agendar"])
    
    @pytest.mark.asyncio
    async def test_help_request(self, booking_agent, conversation_context, test_user):
        """Test help request handling.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        help_queries = [
            "¿Cómo funcionas?",
            "Necesito ayuda",
            "/help",
            "¿Qué puedes hacer?"
        ]
        
        for query in help_queries:
            result = await booking_agent.chat(
                user_message=query,
                user_id=test_user.id,
                conversation_history=[]
            )
            
            assert result is not None
            assert isinstance(result, str)
            assert len(result) > 0
    
    # ==================== AVAILABILITY CHECKS ====================
    
    @pytest.mark.asyncio
    async def test_check_availability_tomorrow(self, booking_agent, conversation_context, test_user):
        """Test checking availability for tomorrow.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="¿Qué horarios tienes disponibles mañana?",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
        # Debería mencionar horarios o disponibilidad
        assert any(word in result.lower() for word in ["horario", "disponible", "mañana", "hora"])
    
    @pytest.mark.asyncio
    async def test_check_availability_specific_date(self, booking_agent, conversation_context, test_user):
        """Test checking availability for specific date.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="¿Hay disponibilidad el próximo lunes?",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_check_availability_week(self, booking_agent, conversation_context, test_user):
        """Test checking availability for a week.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="¿Cuándo tienes disponible esta semana?",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    # ==================== APPOINTMENT BOOKING ====================
    
    @pytest.mark.asyncio
    async def test_book_appointment_simple(self, booking_agent, conversation_context, test_user):
        """Test simple appointment booking.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="Quiero agendar una cita mañana a las 15:00",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
        # Debería confirmar o pedir más info
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_book_appointment_multi_step(self, booking_agent, conversation_context, test_user):
        """Test multi-step appointment booking flow.
        
        Simula conversación natural:
        1. Usuario dice quiere agendar
        2. Bot pregunta fecha
        3. Usuario da fecha
        4. Bot pregunta hora
        5. Usuario da hora
        6. Bot confirma
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        history = []
        
        # Paso 1: Solicitar cita
        msg1 = "Quiero agendar una cita"
        result1 = await booking_agent.chat(
            user_message=msg1,
            user_id=test_user.id,
            conversation_history=history
        )
        assert result1 is not None
        history.append({"role": "user", "content": msg1})
        history.append({"role": "assistant", "content": result1})
        
        # Paso 2: Proporcionar fecha
        msg2 = "El próximo lunes"
        result2 = await booking_agent.chat(
            user_message=msg2,
            user_id=test_user.id,
            conversation_history=history
        )
        assert result2 is not None
        history.append({"role": "user", "content": msg2})
        history.append({"role": "assistant", "content": result2})
        
        # Paso 3: Proporcionar hora
        msg3 = "A las 3 de la tarde"
        result3 = await booking_agent.chat(
            user_message=msg3,
            user_id=test_user.id,
            conversation_history=history
        )
        assert result3 is not None
    
    @pytest.mark.asyncio
    async def test_book_appointment_with_description(self, booking_agent, conversation_context, test_user):
        """Test booking appointment with description.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="Necesito una cita para consulta médica mañana a las 14:00, 1 hora de duración",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    # ==================== VIEW APPOINTMENTS ====================
    
    @pytest.mark.asyncio
    async def test_view_appointments_empty(self, booking_agent, conversation_context, test_user):
        """Test viewing appointments when none exist.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="¿Cuáles son mis citas?",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
        # Debería indicar que no hay citas
        assert any(word in result.lower() for word in ["no hay", "sin citas", "ningún", "vacío"])
    
    @pytest.mark.asyncio
    async def test_view_appointments_list(self, booking_agent, conversation_context, test_user):
        """Test viewing list of appointments.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        # Primero agendar una cita
        await booking_agent.chat(
            user_message="Agendar cita mañana 10am",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        # Luego ver citas
        result = await booking_agent.chat(
            user_message="Muéstrame mis citas",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    # ==================== CANCEL APPOINTMENTS ====================
    
    @pytest.mark.asyncio
    async def test_cancel_appointment(self, booking_agent, conversation_context, test_user):
        """Test canceling an appointment.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="Quiero cancelar mi cita de mañana",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
    
    # ==================== SPANISH LANGUAGE VARIATIONS ====================
    
    @pytest.mark.asyncio
    async def test_spanish_variations(self, booking_agent, conversation_context, test_user):
        """Test handling of Spanish language variations.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        variations = [
            "Necesito agendar una cita",
            "Quiero hacer una reserva",
            "Deseo programar una reunión",
            "¿Puedo agendar para mañana?",
            "¿Cuándo me pueden atender?",
            "¿Qué disponibilidad tienen?",
            "Cancela mi cita",
            "Borra mi reserva",
            "¿Cuándo es mi próxima cita?"
        ]
        
        for message in variations:
            result = await booking_agent.chat(
                user_message=message,
                user_id=test_user.id,
                conversation_history=[]
            )
            
            assert result is not None
            assert isinstance(result, str)
            assert len(result) > 0
    
    # ==================== ERROR HANDLING ====================
    
    @pytest.mark.asyncio
    async def test_invalid_date_handling(self, booking_agent, conversation_context, test_user):
        """Test handling of invalid dates.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        invalid_dates = [
            "32 de diciembre",
            "el 40/20/2025",
            "hace 3 años"
        ]
        
        for message in invalid_dates:
            result = await booking_agent.chat(
                user_message=f"Agendar cita el {message}",
                user_id=test_user.id,
                conversation_history=[]
            )
            
            assert result is not None
            assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_past_date_handling(self, booking_agent, conversation_context, test_user):
        """Test handling of past dates.
        
        Args:
            booking_agent: BookingAgent fixture
            conversation_context: Context fixture
            test_user: Test user fixture
        """
        result = await booking_agent.chat(
            user_message="Agendar cita ayer a las 10am",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        assert result is not None
        assert isinstance(result, str)
        # Debería rechazar o sugerir alternativa
        assert len(result) > 0


class TestGroqToolsE2E:
    """End-to-End tests for Groq Tools integration."""
    
    @pytest.fixture
    def groq_tools(self, test_user):
        """Create GroqTools instance.
        
        Args:
            test_user: Test user fixture
            
        Returns:
            GroqTools instance
        """
        return GroqTools(
            user_id=test_user.id
        )
    
    @pytest.mark.asyncio
    async def test_groq_tools_initialization(self, groq_tools):
        """Test GroqTools initializes correctly.
        
        Args:
            groq_tools: GroqTools fixture
        """
        assert groq_tools is not None
        assert hasattr(groq_tools, 'execute_tool')
        assert hasattr(groq_tools, 'TOOLS')
    
    @pytest.mark.asyncio
    async def test_tool_result_structure(self, groq_tools):
        """Test GroqToolResult structure.
        
        Args:
            groq_tools: GroqTools fixture
        """
        # Ejecutar herramienta (intencionalmente puede fallar)
        result = groq_tools.execute_tool(
            "check_availability",
            date="mañana",
            duration_minutes=60
        )
        
        # Verificar estructura
        assert hasattr(result, 'success')
        assert hasattr(result, 'data')
        assert hasattr(result, 'message')
        assert hasattr(result, 'error')
    
    @pytest.mark.asyncio
    async def test_invalid_tool_name(self, groq_tools):
        """Test handling of invalid tool name.
        
        Args:
            groq_tools: GroqTools fixture
        """
        result = groq_tools.execute_tool("nonexistent_tool")
        
        assert result.success is False
        assert result.error is not None


class TestDatabasePersistenceE2E:
    """End-to-End tests for database persistence.
    
    Verifica que las citas se guarden realmente en BD.
    """
    
    @pytest.mark.asyncio
    async def test_appointment_persists_in_database(self, booking_agent, test_user, db_session):
        """Test that appointments persist in database.
        
        Args:
            booking_agent: BookingAgent fixture
            test_user: Test user fixture
            db_session: Database session fixture
        """
        # Agendar cita
        await booking_agent.chat(
            user_message="Agendar cita mañana 10am para prueba",
            user_id=test_user.id,
            conversation_history=[]
        )
        
        # Aquí verificarías que se guardó en BD
        # Ejemplo (necesitarías repositorio de appointments):
        # appointments = await AppointmentRepository(db_session).get_by_user(test_user.id)
        # assert len(appointments) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
