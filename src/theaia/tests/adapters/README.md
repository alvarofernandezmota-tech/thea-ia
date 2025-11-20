# adapters/ - Adapter Tests

Tests de adaptadores de entrada (Telegram, Web, WhatsApp).

---

## 📋 Overview

Tests específicos de adaptadores con características:

- 🔌 **Interfaces externas** (Telegram, Web, etc.)
- 🔄 **Message normalization** (external → internal format)
- 🎭 **Mocking services** (no llamadas reales a Telegram API)
- ⚡ **Rápidos** (~1-5ms por test)

---

## 📁 Estructura

adapters/
└── test_telegram_adapter.py # ✅ TelegramAdapter (10 tests)

text

**Total Adapter Tests: 10 tests**

---

## 🚀 Quick Start

Ejecutar todos los adapter tests
pytest src/theaia/tests/adapters/ -v

Solo Telegram adapter
pytest src/theaia/tests/adapters/test_telegram_adapter.py -v

Con markers
pytest -m adapter -v

text

---

## ✅ Tests Implementados

### **📱 TelegramAdapter (10 tests)**
`test_telegram_adapter.py` - Telegram adapter functionality:

#### Initialization & Setup (2 tests)
- ✅ `test_adapter_initialization` - Adapter se inicializa correctamente
- ✅ `test_adapter_configuration` - Configuración válida

#### Message Handling (4 tests)
- ✅ `test_handle_text_message` - Maneja mensajes de texto
- ✅ `test_handle_command` - Maneja comandos (/start, /help)
- ✅ `test_message_handler_responds` - Handler responde correctamente
- ✅ `test_empty_message_handling` - Maneja mensajes vacíos

#### User Management (2 tests)
- ✅ `test_user_extraction` - Extrae datos de usuario de update
- ✅ `test_user_persistence` - Usuario persiste en DB

#### Error Handling (2 tests)
- ✅ `test_invalid_update_format` - Maneja formato inválido
- ✅ `test_error_recovery` - Se recupera de errores

---

## 💡 Ejemplo Adapter Test

test_telegram_adapter.py
import pytest
from unittest.mock import AsyncMock, MagicMock
from src.theaia.adapters.telegram import TelegramAdapter

@pytest.mark.asyncio
async def test_handle_text_message(db_session, mock_bot):
"""
Test que el adapter maneja mensajes de texto correctamente.

text
Verifica:
1. Adapter recibe update de Telegram
2. Extrae texto del mensaje
3. Normaliza formato interno
4. Pasa a CoreManager
5. Retorna respuesta
"""
# Arrange
adapter = TelegramAdapter(bot=mock_bot, db_session=db_session)

telegram_update = {
    "update_id": 123456,
    "message": {
        "message_id": 1,
        "from": {
            "id": 999999,
            "username": "test_user",
            "first_name": "Test"
        },
        "chat": {
            "id": 999999,
            "type": "private"
        },
        "text": "Recordar reunión mañana"
    }
}

# Act
response = await adapter.handle_update(telegram_update)

# Assert
assert response is not None
assert response["status"] == "success"
assert "message" in response

# Verify bot called to send response
mock_bot.send_message.assert_called_once()
call_args = mock_bot.send_message.call_args
assert call_args == 999999  # chat_id
assert len(call_args) > 0   # message text
text

---

## ✅ Características Adapter Tests

**✅ Debe:**
- Mock servicios externos (Telegram API)
- Testear normalización de mensajes
- Verificar extracción de datos de usuario
- Validar error handling

**❌ NO debe:**
- Hacer llamadas reales a Telegram API
- Depender de conexión a internet
- Testear lógica de negocio (→ agents)
- Tardar >100ms por test

---

## 🔧 Mocking Telegram

### Mock Bot
@pytest.fixture
def mock_bot():
"""Mock Telegram bot for testing."""
bot = MagicMock()
bot.send_message = AsyncMock(return_value={"ok": True})
bot.get_me = AsyncMock(return_value={"username": "test_bot"})
return bot

text

### Mock Update
def create_telegram_update(text: str, user_id: int = 999999):
"""Create a mock Telegram update."""
return {
"update_id": 123456,
"message": {
"message_id": 1,
"from": {
"id": user_id,
"username": "test_user",
"first_name": "Test"
},
"chat": {"id": user_id, "type": "private"},
"text": text
}
}

text

---

## 📊 Coverage Stats (15 Nov 2025)

| Component | Tests | Coverage | Status |
|-----------|-------|----------|--------|
| TelegramAdapter | 10 | 39% | ✅ |
| **TOTAL** | **10** | **39%** | ✅ |

**Note:** Coverage parcial es esperado - muchas partes del adapter requieren integración real que se testea en integration/ y e2e/

---

## 🎯 Test Patterns

### Adapter Test Pattern
@pytest.mark.asyncio
async def test_adapter_feature(mock_bot, db_session):
# Arrange
adapter = Adapter(bot=mock_bot, db=db_session)
external_input = create_mock_input()

text
# Act
result = await adapter.handle(external_input)

# Assert - Adapter behavior
assert result is not None
assert result["status"] == "success"

# Assert - External service called correctly
mock_bot.method.assert_called_once()
text

### Message Normalization
def test_message_normalization():
"""Test adapter normalizes external format to internal."""
# External format (Telegram)
telegram_msg = {
"message": {"text": "hola", "from": {"id": 123}}
}

text
# Normalize
internal = adapter.normalize(telegram_msg)

# Assert internal format
assert internal["user_id"] == 123
assert internal["message"] == "hola"
assert "timestamp" in internal
text

---

## 🎯 Future Tests (Phase 4+)

**Additional Adapter Tests:**
- [ ] WhatsApp adapter tests
- [ ] Web adapter tests
- [ ] File upload handling
- [ ] Media message handling
- [ ] Inline keyboards
- [ ] Callback queries

---

## 📚 Convenciones

### Test Naming
def test_adapter_<action>_<expected>():
"""Test that adapter <action> results in <expected>."""

text

### Async Tests
@pytest.mark.asyncio
async def test_async_adapter():
"""All adapter tests are async."""
result = await adapter.async_method()
assert result is not None

text

---

**Implementado:** H02 (12-14 Nov 2025)  
**Última actualización:** 15 Nov 2025, 23:59 CET
