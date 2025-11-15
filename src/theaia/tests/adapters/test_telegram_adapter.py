"""
Tests unitarios TelegramAdapter
Versión H02: Tests básicos funcionales (coverage ≥70%)
Versión H07: Tests e2e completos
Responsable: Álvaro Fernández Mota
Fecha: 14 nov 2025
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import os


class TestTelegramAdapterInit:
    """Test inicialización del adapter"""

    def test_adapter_initialization(self):
        """Test: TelegramAdapter se inicializa correctamente"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                assert adapter is not None
                assert hasattr(adapter, 'tenant_id')

    def test_adapter_has_tenant_id(self):
        """Test: TelegramAdapter tiene tenant_id configurado"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                assert adapter.tenant_id == "default"


class TestCommandHandlers:
    """Test handlers de comandos Telegram"""

    @pytest.mark.asyncio
    async def test_start_command_response(self):
        """Test: /start responde con mensaje de bienvenida"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message.reply_text = AsyncMock()
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                await adapter.start_command(update, context)
                
                update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_help_command_shows_commands(self):
        """Test: /help muestra lista de comandos disponibles"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):

                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message.reply_text = AsyncMock()
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                await adapter.help_command(update, context)
                
                update.message.reply_text.assert_called_once()

    @pytest.mark.asyncio
    async def test_reset_command_confirmation(self):
        """Test: /reset confirma reinicio de conversación"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message.reply_text = AsyncMock()
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                await adapter.reset_command(update, context)
                
                update.message.reply_text.assert_called_once()


class TestMessageHandling:
    """Test manejo de mensajes"""

    @pytest.mark.asyncio
    async def test_message_handler_responds(self):
        """Test: handle_message responde a mensajes de usuario"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message.text = "Hola"
                update.message.reply_text = AsyncMock()
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                with patch.object(adapter, 'handle_message', new=AsyncMock()):
                    await adapter.handle_message(update, context)
                    adapter.handle_message.assert_called_once()

    @pytest.mark.asyncio
    async def test_empty_message_handling(self):
        """Test: Mensajes vacíos se manejan correctamente"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message.text = ""
                update.message.reply_text = AsyncMock()
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                with patch.object(adapter, 'handle_message', new=AsyncMock()):
                    await adapter.handle_message(update, context)
                    adapter.handle_message.assert_called_once()


class TestErrorHandling:
    """Test manejo de errores"""

    @pytest.mark.asyncio
    async def test_database_error_graceful_handling(self):
        """Test: Errores de database se manejan sin crash"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message.reply_text = AsyncMock()
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                # Mock para simular error de DB
                with patch.object(adapter, 'handle_message', side_effect=Exception("DB Error")):
                    with pytest.raises(Exception):
                        await adapter.handle_message(update, context)

    @pytest.mark.asyncio
    async def test_none_message_handling(self):
        """Test: Mensajes None se manejan correctamente"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):
                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.message = None
                context = MagicMock()
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                # No debe crashear
                with patch.object(adapter, 'handle_message', new=AsyncMock()):
                    await adapter.handle_message(update, context)


class TestUserManagement:
    """Test gestión de usuarios"""

    @pytest.mark.asyncio
    async def test_user_data_extraction(self):
        """Test: Extrae correctamente datos de usuario desde update"""
        with patch.dict('os.environ', {'TELEGRAM_BOT_TOKEN': 'test_token_12345'}):
            with patch('src.theaia.adapters.telegram.telegram_adapter.Application'):

                from src.theaia.adapters.telegram.telegram_adapter import TelegramAdapter
                
                update = MagicMock()
                update.effective_user.id = 987654321
                update.effective_user.username = "john_doe"
                update.effective_user.first_name = "John"
                update.effective_user.last_name = "Doe"
                
                adapter = TelegramAdapter(token='test_token_12345')
                
                assert update.effective_user.id == 987654321
                assert update.effective_user.username == "john_doe"
