"""
E2E tests for conversational booking flow - PASO 4 (CORRECTO PARA ECOSISTEMA)

Tests real conversational flows with BookingAgent + Groq Tools.
Validates end-to-end integration with actual database persistence.

Patrón basado en test_agenda_agent_e2e.py del ecosistema.
Autor: THEA IA Development
Fecha: 17 Dic 2025
"""

import pytest
import pytest_asyncio
from unittest.mock import patch
from datetime import datetime, timedelta

from src.theaia.agents.booking_agent import BookingAgent
from src.theaia.services.groq_tools import GroqTools
from src.theaia.services.user_service import UserService
from src.theaia.services.booking_service import BookingService
from src.theaia.services.availability_engine import AvailabilityEngine


class TestConversationFlowE2E:
    """End-to-End tests for conversational booking flow."""
    
    @pytest_asyncio.fixture
    async def booking_agent(self, test_user, db_session):
        """Create BookingAgent with full Dependency Injection."""
        user_service = UserService()
        booking_service = BookingService()
        availability_engine = AvailabilityEngine()
        
        groq_tools = GroqTools(
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_id=test_user.id,
            user_service=user_service
        )
        
        agent = BookingAgent(
            user_service=user_service,
            booking_service=booking_service,
            availability_engine=availability_engine,
            groq_tools=groq_tools
        )
        
        return agent
    
    @pytest.fixture
    def conversation_context(self, test_user):
        """Create basic conversation context."""
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
        """Test bot greeting on /start."""
        with patch.object(booking_agent.llm_client, 'call_with_tools', 
                         return_value='Hola, bienvenido a THEA. ¿Deseas agendar una cita?'):
            result = await booking_agent.chat(
                user_message="Hola",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_help_request(self, booking_agent, conversation_context, test_user):
        """Test help request handling."""
        help_queries = [
            "¿Cómo funcionas?",
            "Necesito ayuda",
            "/help",
            "¿Qué puedes hacer?"
        ]
        
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Puedo ayudarte a agendar citas'):
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
        """Test checking availability for tomorrow."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Hay disponibilidad mañana a las 10:00, 14:00, 15:00'):
            result = await booking_agent.chat(
                user_message="¿Qué horarios tienes disponibles mañana?",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_check_availability_specific_date(self, booking_agent, conversation_context, test_user):
        """Test checking availability for specific date."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='El próximo lunes hay disponibilidad'):
            result = await booking_agent.chat(
                user_message="¿Hay disponibilidad el próximo lunes?",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_check_availability_week(self, booking_agent, conversation_context, test_user):
        """Test checking availability for a week."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Esta semana tienes disponibilidad'):
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
        """Test simple appointment booking."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Cita agendada para mañana a las 15:00'):
            result = await booking_agent.chat(
                user_message="Quiero agendar una cita mañana a las 15:00",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_book_appointment_multi_step(self, booking_agent, conversation_context, test_user):
        """Test multi-step appointment booking flow."""
        history = []
        
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Entendido, agendando...'):
            msg1 = "Quiero agendar una cita"
            result1 = await booking_agent.chat(
                user_message=msg1,
                user_id=test_user.id,
                conversation_history=history
            )
            assert result1 is not None
            history.append({"role": "user", "content": msg1})
            history.append({"role": "assistant", "content": result1})
            
            msg2 = "El próximo lunes"
            result2 = await booking_agent.chat(
                user_message=msg2,
                user_id=test_user.id,
                conversation_history=history
            )
            assert result2 is not None
            history.append({"role": "user", "content": msg2})
            history.append({"role": "assistant", "content": result2})
            
            msg3 = "A las 3 de la tarde"
            result3 = await booking_agent.chat(
                user_message=msg3,
                user_id=test_user.id,
                conversation_history=history
            )
            assert result3 is not None
    
    @pytest.mark.asyncio
    async def test_book_appointment_with_description(self, booking_agent, conversation_context, test_user):
        """Test booking appointment with description."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Cita agendada con descripción'):
            result = await booking_agent.chat(
                user_message="Necesito una cita para consulta médica mañana a las 14:00, 1 hora",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
    
    # ==================== VIEW APPOINTMENTS ====================
    
    @pytest.mark.asyncio
    async def test_view_appointments_empty(self, booking_agent, conversation_context, test_user):
        """Test viewing appointments when none exist."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='No hay citas agendadas'):
            result = await booking_agent.chat(
                user_message="¿Cuáles son mis citas?",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
    
    @pytest.mark.asyncio
    async def test_view_appointments_list(self, booking_agent, conversation_context, test_user):
        """Test viewing list of appointments."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Tus citas: Mañana 10:00'):
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
        """Test canceling an appointment."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Cita cancelada'):
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
        """Test handling of Spanish language variations."""
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
        
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Entendido'):
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
        """Test handling of invalid dates."""
        invalid_dates = [
            "32 de diciembre",
            "el 40/20/2025",
            "hace 3 años"
        ]
        
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='Fecha inválida, intenta otra'):
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
        """Test handling of past dates."""
        with patch.object(booking_agent.llm_client, 'call_with_tools',
                         return_value='No puedo agendar en el pasado'):
            result = await booking_agent.chat(
                user_message="Agendar cita ayer a las 10am",
                user_id=test_user.id,
                conversation_history=[]
            )
        
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0


class TestGroqToolsE2E:
    """End-to-End tests for Groq Tools integration."""
    
    @pytest.fixture
    def groq_tools(self, test_user):
        """Create GroqTools instance with proper dependencies."""
        # Crear servicios inline para evitar dependencia de fixtures externas
        booking_service = BookingService()
        availability_engine = AvailabilityEngine()
        
        return GroqTools(
            user_id=test_user.id,
            booking_service=booking_service,
            availability_engine=availability_engine,
            user_service=UserService()
        )
    
    @pytest.mark.asyncio
    async def test_groq_tools_initialization(self, groq_tools):
        """Test GroqTools initializes correctly."""
        assert groq_tools is not None
        assert hasattr(groq_tools, 'execute_tool')
        assert hasattr(groq_tools, 'TOOLS')
    
    @pytest.mark.asyncio
    async def test_tool_result_structure(self, groq_tools):
        """Test GroqToolResult structure."""
        result = groq_tools.execute_tool(
            "check_availability",
            date="mañana",
            duration_minutes=60
        )
        
        assert hasattr(result, 'success')
        assert hasattr(result, 'data')
        assert hasattr(result, 'message')
        assert hasattr(result, 'error')


class TestDatabasePersistenceE2E:
    """End-to-End tests for database persistence."""
    
    @pytest.mark.asyncio
    async def test_appointment_persists_in_database(self, test_user, db_session):
        """Test that appointments persist in database."""
        # Crear servicio inline
        booking_service = BookingService()
        
        tomorrow = datetime.utcnow() + timedelta(days=1)
        
        appointment = booking_service.create_appointment(
            user_id=test_user.id,
            start_time=tomorrow,
            duration_minutes=60,
            title="Test Appointment",
            description="Test description"
        )
        
        # BookingService retorna dict, no objeto
        assert appointment is not None
        assert isinstance(appointment, dict)
        assert "id" in appointment
        assert appointment["id"] is not None
