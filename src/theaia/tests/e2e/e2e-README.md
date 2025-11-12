e2e/ - End-to-End Tests
Tests end-to-end (10% de la suite)

📋 Overview
Tests de flujos completos de usuario:

🎭 Flujos reales usuario completos

🌐 Todo el stack (Telegram → DB → Response)

🐌 Lentos (~1-5 segundos por test)

🎯 Pocos pero críticos (10% total)

📁 Estructura
text
e2e/
├── test_user_journey/
│   ├── test_new_user_onboarding.py
│   ├── test_reminder_lifecycle.py
│   ├── test_note_lifecycle.py
│   └── test_multi_agent_flow.py
├── test_telegram_bot_complete.py
└── test_subscription_flow.py       # (H05)
🚀 Quick Start
bash
# Ejecutar E2E tests
pytest src/tests/e2e/ -v

# Solo user journeys
pytest src/tests/e2e/test_user_journey/ -v

# Skip E2E (lentos)
pytest -m "not e2e" -v
💡 Ejemplo
python
# test_user_journey/test_reminder_lifecycle.py
import pytest

@pytest.mark.e2e
@pytest.mark.asyncio
async def test_user_creates_views_completes_reminder(
    telegram_client,
    db_session
):
    """
    Flujo completo usuario:
    1. Usuario nuevo envía /start
    2. Crea reminder
    3. Ve sus reminders
    4. Completa reminder
    5. Ve historial
    """
    # Step 1: Onboarding
    await telegram_client.send_message("/start")
    response = await telegram_client.get_last_message()
    assert "Bienvenido a THEA IA" in response.text
    
    # Step 2: Crear reminder
    await telegram_client.send_message("Recuérdame reunión mañana 15:00")
    response = await telegram_client.get_last_message()
    assert "✅ Recordatorio creado" in response.text
    assert "Reunión" in response.text
    assert "Mañana 15:00" in response.text
    
    # Verificar en database
    from src.database.models import Reminder
    reminders = await db_session.execute(
        select(Reminder).where(Reminder.user_id == telegram_client.user_id)
    )
    reminders = list(reminders.scalars())
    assert len(reminders) == 1
    assert "reunión" in reminders.title.lower()
    
    # Step 3: Ver reminders
    await telegram_client.send_message("Ver mis recordatorios")
    response = await telegram_client.get_last_message()
    assert "📅 Reunión" in response.text
    assert "Mañana 15:00" in response.text
    
    # Step 4: Completar reminder
    await telegram_client.click_button("Completar")
    response = await telegram_client.get_last_message()
    assert "✅ Completado" in response.text
    
    # Verificar completed en DB
    await db_session.refresh(reminders)
    assert reminders.completed is True
    assert reminders.completed_at is not None
    
    # Step 5: Ver historial
    await telegram_client.send_message("Ver completados")
    response = await telegram_client.get_last_message()
    assert "✅ Reunión" in response.text
    assert "Completado" in response.text
✅ Características
✅ Debe:
Simular usuario real completo

Testear happy paths críticos

Verificar UI + DB consistency

Cubrir journey completo (start → finish)

❌ NO debe:
Testear todos los edge cases (unit tests)

Depender de servicios externos reales

Tardar >10 segundos por test

Tener más de 10-15 E2E tests totales

🎭 Mock Telegram Client
python
# conftest.py
@pytest.fixture
async def telegram_client(db_session):
    """Mock Telegram client para E2E"""
    from tests.mocks import MockTelegramClient
    
    client = MockTelegramClient(
        user_id=123456,
        username="test_user"
    )
    
    # Setup user en DB
    user = await create_test_user(db_session, telegram_user_id=123456)
    client.db_user = user
    
    yield client
    
    # Cleanup
    await cleanup_test_user(db_session, user.id)
🎯 Coverage Target
>70% en E2E tests

Foco en:

User journeys críticos

Happy paths principales

Features core (reminder, note)

Onboarding + offboarding

📊 Tests por Journey
test_new_user_onboarding.py:
/start → welcome message

User profile creado en DB

Primera interacción funciona

Settings default aplicados

test_reminder_lifecycle.py:
Create → View → Update → Complete → Archive

Notificaciones enviadas

Database consistency

UI responde correctamente

test_note_lifecycle.py:
Create → View → Edit → Delete

Tags funcionan

Search funciona

Pinned notes

test_multi_agent_flow.py:
Usuario usa múltiples agentes

Context switching funciona

Agents no interfieren

test_telegram_bot_complete.py:
Bot responde a todos comandos

Error handling correcto

Performance aceptable

🐌 Performance
E2E tests son lentos:

Target: <5 segundos por test

Total E2E suite: <2 minutos

Optimizaciones:

Parallel execution donde posible

Mock external services (Telegram API)

Database fixtures rápidos

Skip en CI fast mode

📚 Por Implementar
H07 (29-30 Nov)

Orden implementación:

Setup mock Telegram client

test_new_user_onboarding.py

test_reminder_lifecycle.py

test_note_lifecycle.py

test_multi_agent_flow.py

test_telegram_bot_complete.py

🎯 Prioridad E2E Tests
Must Have (H07):
✅ New user onboarding

✅ Reminder lifecycle

✅ Note lifecycle

✅ Bot responde

Nice to Have (H09+):
Multi-agent flow

Error recovery

Subscription flow (H05+)

Long-running sessions

Implementar en: H07 (29-30 Nov)
Última actualización: 11 Nov 2025