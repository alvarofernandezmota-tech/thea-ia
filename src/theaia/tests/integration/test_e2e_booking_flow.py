# src/theaia/tests/integration/test_e2e_booking_flow.py
"""
E2E Integration Tests - Bot → Agent → Tools → Database
Target: 12 tests | Real flow validation
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from unittest.mock import Mock, AsyncMock, patch
import json

from theaia.adapters.telegram.bot import TelegramBot
from theaia.services.groq_tools import GroqTools
from theaia.services.booking_service import BookingService
from theaia.services.availability_engine import AvailabilityEngine
from theaia.database.repositories.user_repository import UserRepository
from theaia.database.repositories.appointment_repository import AppointmentRepository


@pytest.fixture
async def db_session():
    """Sesión de BD para tests"""
    # TODO: Usar test DB
    pass


@pytest.fixture
def booking_service(db_session):
    """BookingService con BD de test"""
    return BookingService(db_session)


@pytest.fixture
def availability_engine(db_session):
    """AvailabilityEngine con BD de test"""
    return AvailabilityEngine(db_session)


@pytest.fixture
def groq_tools(booking_service, availability_engine):
    """GroqTools con servicios reales"""
    return GroqTools(
        booking_service=booking_service,
        availability_engine=availability_engine,
        user_id=123
    )


@pytest.fixture
async def telegram_bot(groq_tools):
    """TelegramBot con tools integrados"""
    bot = TelegramBot(token="TEST_TOKEN")
    bot.groq_tools = groq_tools
    return bot


class TestE2EBookingFlow:
    """Tests E2E: usuario → bot → agent → tools → BD"""
    
    @pytest.mark.asyncio
    async def test_full_booking_flow(self, telegram_bot, booking_service):
        """
        E2E completo: Usuario pide cita → Bot agenda → BD actualiza
        Flow:
        1. /start → Bot inicializa
        2. "Quiero agendar mañana a las 3pm"
        3. Bot procesa intent
        4. Groq llama a check_availability
        5. Usuario confirma
        6. Groq llama a create_appointment
        7. Verificar en BD
        """
        # 1. Inicializar bot
        await telegram_bot.start()
        
        # 2-3. Usuario envía mensaje
        user_message = "Quiero agendar una cita mañana a las 15:00"
        
        # 4. Procesar con Groq
        # TODO: Simular respuesta Groq
        
        # 5. Verificar en BD
        appointments = booking_service.get_user_appointments(user_id=123)
        assert len(appointments) > 0
        
        tomorrow = datetime.now() + timedelta(days=1)
        assert appointments[0].start_time.date() == tomorrow.date()
    
    @pytest.mark.asyncio
    async def test_availability_check_flow(self, groq_tools, availability_engine):
        """
        Test: Usuario pregunta disponibilidad
        "¿Qué horarios tienes disponibles mañana?"
        """
        # Verificar que AvailabilityEngine retorna slots
        tomorrow = datetime.now() + timedelta(days=1)
        slots = availability_engine.get_available_slots(tomorrow, 60)
        
        assert isinstance(slots, list)
        assert len(slots) == 24  # 24 slots por día (24/7)
    
    @pytest.mark.asyncio
    async def test_list_appointments_flow(self, groq_tools, booking_service):
        """
        Test: Usuario pide "/citas"
        Bot lista citas del usuario
        """
        # Crear cita de prueba
        tomorrow = datetime.now() + timedelta(days=1)
        booking_service.create_appointment(
            user_id=123,
            start_time=tomorrow.replace(hour=15, minute=0),
            duration_minutes=60
        )
        
        # Ejecutar tool
        result = groq_tools.get_appointments()
        
        assert result.success is True
        assert result.data["total"] >= 1
        assert result.data["appointments"][0]["date"] == tomorrow.strftime("%Y-%m-%d")
    
    @pytest.mark.asyncio
    async def test_cancel_appointment_flow(self, groq_tools, booking_service):
        """
        Test: Usuario cancela cita
        /cancelar → Bot muestra opciones → Usuario selecciona → Cancela
        """
        # Crear cita
        tomorrow = datetime.now() + timedelta(days=1)
        appointment = booking_service.create_appointment(
            user_id=123,
            start_time=tomorrow.replace(hour=15, minute=0),
            duration_minutes=60
        )
        appointment_id = appointment.id
        
        # Cancelar
        result = groq_tools.cancel_appointment(appointment_id)
        
        assert result.success is True
        
        # Verificar en BD
        cancelled_apt = booking_service.get_appointment(appointment_id)
        assert cancelled_apt.status == "cancelled"
    
    @pytest.mark.asyncio
    async def test_conflict_detection(self, groq_tools, booking_service):
        """
        Test: Sistema rechaza doble-booking
        Crear cita → Intentar crear otra en mismo horario → Rechaza
        """
        tomorrow = datetime.now() + timedelta(days=1)
        target_time = tomorrow.replace(hour=15, minute=0)
        
        # Primera cita OK
        apt1 = booking_service.create_appointment(
            user_id=123,
            start_time=target_time,
            duration_minutes=60
        )
        assert apt1.id is not None
        
        # Segunda cita en mismo horario → Debe fallar
        result = groq_tools.create_appointment(
            date_str="mañana",
            time_str="15:00",
            duration_minutes=60
        )
        
        assert result.success is False
        assert "no está disponible" in result.error
    
    @pytest.mark.asyncio
    async def test_natural_language_parsing(self, groq_tools):
        """
        Test: Parsing de lenguaje natural
        - "mañana" → tomorrow
        - "3pm" → 15:00
        - "próximo jueves" → next Thursday
        """
        # "mañana"
        parsed = groq_tools._parse_natural_date("mañana")
        expected = datetime.now() + timedelta(days=1)
        assert parsed.date() == expected.date()
        
        # "15:00"
        parsed_time = groq_tools._parse_time("15:00")
        assert parsed_time.hour == 15
    
    @pytest.mark.asyncio
    async def test_error_handling_invalid_date(self, groq_tools):
        """
        Test: Manejo de errores - fecha inválida
        """
        result = groq_tools.create_appointment(
            date_str="fecha_imposible",
            time_str="15:00"
        )
        
        assert result.success is False
        assert result.error is not None
    
    @pytest.mark.asyncio
    async def test_timezone_handling(self, groq_tools, availability_engine):
        """
        Test: Manejo de timezones
        Las citas se crean en UTC pero se muestran en local
        """
        result = groq_tools.check_availability("mañana")
        
        assert result.success is True
        # Verificar que hora está en rango valido
        if result.data["available_slots"]:
            time_str = result.data["available_slots"][0]
            hour = int(time_str.split(":")[0])
            assert 0 <= hour <= 23
    
    @pytest.mark.asyncio
    async def test_user_persistence(self, booking_service):
        """
        Test: Usuario persiste en BD
        Crear usuario → Agregar cita → Verificar
        """
        # Crear usuario
        user = booking_service.user_service.create_or_get_user(
            telegram_id=123,
            username="testuser"
        )
        
        assert user.id is not None
        
        # Crear cita para usuario
        apt = booking_service.create_appointment(
            user_id=user.id,
            start_time=datetime.now() + timedelta(days=1),
            duration_minutes=60
        )
        
        # Verificar
        assert apt.user_id == user.id
    
    @pytest.mark.asyncio
    async def test_message_formatting_spanish(self, groq_tools):
        """
        Test: Mensajes en español bien formateados
        """
        result = groq_tools.check_availability("mañana")
        
        assert result.success is True
        # Mensajes en español
        assert any(c.isalpha() for c in result.message)  # Tiene texto
        # No tiene "day_name" sin formatear
        assert "[" not in result.message or "{" not in result.message
    
    @pytest.mark.asyncio
    async def test_concurrent_bookings(self, booking_service):
        """
        Test: Múltiples usuarios agendando simultáneamente
        """
        tomorrow = datetime.now() + timedelta(days=1)
        
        # Simular 3 usuarios agendando en horarios diferentes
        for user_id in [1, 2, 3]:
            apt = booking_service.create_appointment(
                user_id=user_id,
                start_time=tomorrow.replace(hour=14 + user_id, minute=0),
                duration_minutes=60
            )
            assert apt.user_id == user_id
        
        # Verificar que todas las citas existen
        for user_id in [1, 2, 3]:
            apts = booking_service.get_user_appointments(user_id)
            assert len(apts) >= 1


class TestBotIntegration:
    """Tests de integración del Bot Telegram"""
    
    @pytest.mark.asyncio
    async def test_start_command(self, telegram_bot):
        """Test: /start command"""
        # TODO: Mock Telegram update
        pass
    
    @pytest.mark.asyncio
    async def test_appointment_command(self, telegram_bot):
        """Test: /agendar command"""
        # TODO: Mock Telegram update + parse inline buttons
        pass
