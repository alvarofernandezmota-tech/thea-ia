src/services/ - Business Services Module
Módulo de servicios de negocio (H04-H05)

📋 Overview
PLACEHOLDER H04-H05 - Este módulo se implementará en H04-H05.

Servicios de lógica de negocio compleja:

💳 Payment Service: Stripe, suscripciones

📧 Notification Service: Email, push, Telegram

🔐 Auth Service: JWT, permisos

📊 Analytics Service: Métricas uso

🎯 Propósito (H04-H05)
Centralizar lógica de negocio que no es específica de un agente:

Pagos y suscripciones

Notificaciones multi-canal

Autenticación y autorización

Analytics y métricas

📁 Estructura Planificada (H04-H05)
text
src/services/
│
├── __init__.py
│
├── auth_service.py ← H04
│   # JWT tokens
│   # API keys
│   # Permissions
│
├── payment_service.py ← H05
│   # Stripe integration
│   # Subscription management
│   # Webhook handling
│
├── notification_service.py ← H05
│   # Email notifications
│   # Telegram notifications
│   # Push notifications (H08+)
│
├── analytics_service.py ← H12
│   # Usage metrics
│   # User analytics
│   # Business intelligence
│
└── README.md
📦 Dependencias Planificadas
H04 (Auth):
text
python-jose[cryptography]==3.3.0  # JWT
passlib[bcrypt]==1.7.4            # Password hashing
H05 (Payment + Notifications):
text
stripe==7.4.0                     # Payment
sendgrid==6.11.0                  # Email
H12 (Analytics):
text
mixpanel==4.10.0
segment-analytics-python==2.2.3
💡 Uso Planificado
Auth Service (H04):
python
from src.services import AuthService

auth = AuthService()

# Generar JWT token
token = auth.create_access_token(user_id=123)
# → "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# Verificar token
user_id = auth.verify_token(token)
# → 123

# Generar API key
api_key = auth.generate_api_key(user_id=123)
# → "sk_live_..."

# Check permission
has_access = auth.check_permission(user_id=123, permission="create_reminder")
# → True (si subscription activa)
Payment Service (H05):
python
from src.services import PaymentService

payment = PaymentService()

# Crear suscripción
subscription = await payment.create_subscription(
    user_id=123,
    plan="pro",
    payment_method_id="pm_xxx"
)
# → Subscription(id="sub_xxx", status="active")

# Verificar suscripción activa
is_active = await payment.is_subscription_active(user_id=123)
# → True

# Cancelar suscripción
await payment.cancel_subscription(user_id=123)
# → True

# Webhook handling
@app.post("/webhooks/stripe")
async def stripe_webhook(request):
    event = await payment.handle_webhook(request)
    # Procesa eventos: invoice.paid, customer.subscription.deleted, etc
Notification Service (H05):
python
from src.services import NotificationService

notif = NotificationService()

# Enviar notificación reminder (Telegram)
await notif.send_telegram_notification(
    user_id=123,
    message="📅 Recordatorio: Reunión en 15 minutos"
)

# Enviar email
await notif.send_email(
    email="user@example.com",
    subject="Bienvenido a THEA IA",
    body="Gracias por registrarte...",
    template="welcome"  # Usa template pre-definido
)

# Notificación programada
await notif.schedule_notification(
    user_id=123,
    message="Recordatorio reunión",
    datetime=datetime(2025, 11, 12, 14, 45)  # 15 min antes
)
Analytics Service (H12):
python
from src.services import AnalyticsService

analytics = AnalyticsService()

# Track evento
analytics.track_event(
    user_id=123,
    event="reminder_created",
    properties={"title": "Reunión", "advance_minutes": 15}
)

# Get métricas usuario
metrics = analytics.get_user_metrics(user_id=123)
# → {
#     "reminders_created": 42,
#     "notes_created": 18,
#     "days_active": 15,
#     "subscription_tier": "pro"
# }
🎯 Features por Hito
H04 (20-23 Nov): Auth Service
Funcionalidades:

✅ JWT token generation/validation

✅ API key management

✅ Permission checking

✅ User roles (free, pro, business)

Uso:

API authentication (H08)

Permission checks en agents

Rate limiting por tier

H05 (24-27 Nov): Payment + Notifications
Payment Service:

✅ Stripe integration completa

✅ Create/cancel subscriptions

✅ Webhook handling (invoice.paid, etc)

✅ Check subscription status

Notification Service:

✅ Telegram notifications (via TelegramAdapter)

✅ Email notifications (SendGrid)

✅ Templates (welcome, reminder, payment)

✅ Schedule notifications

Uso:

Monetización (upgrade to pro/business)

Notificaciones reminders

Emails transaccionales

H12 (Mar 2026): Analytics
Funcionalidades:

Track usage events

User metrics dashboard

Business intelligence

Churn prediction

🔐 Variables de Entorno
H04 (Auth):
bash
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080  # 7 días
H05 (Payment):
bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_PRO=price_1234
STRIPE_PRICE_ID_BUSINESS=price_5678
H05 (Email):
bash
SENDGRID_API_KEY=SG.xxxxx
SENDGRID_FROM_EMAIL=noreply@thea-ia.com
📈 Planes de Suscripción (H05)
Plan	Precio	Features
Free	€0/mes	• 10 reminders/mes
• Funciones básicas
Pro	€9.99/mes	• Reminders ilimitados
• Notas ilimitadas
• Eventos
• Priority support
Business	€29.99/mes	• Todo Pro +
• API access
• Team features
• Analytics
🔄 Flujo Pago (H05)
text
Usuario → "Upgrade to Pro"
    ↓
TelegramAdapter → PaymentService.create_subscription()
    ↓
Stripe Checkout Session
    ↓
Usuario paga
    ↓
Stripe Webhook → PaymentService.handle_webhook()
    ↓
Update User.subscription_tier = "pro"
    ↓
NotificationService.send_email("welcome_pro")
    ↓
Usuario recibe confirmación
⚠️ Antes de H04-H05
NO IMPLEMENTAR ESTE MÓDULO ANTES DE H04.

En H02-H03:

Sin autenticación (todos los usuarios acceso completo)

Sin pagos (todo gratis)

Notificaciones solo Telegram (via TelegramAdapter directo)

🧪 Testing (H04-H05)
python
# tests/unit/test_services/test_auth_service.py
def test_create_token():
    auth = AuthService()
    token = auth.create_access_token(user_id=123)
    assert isinstance(token, str)
    
    user_id = auth.verify_token(token)
    assert user_id == 123

# tests/unit/test_services/test_payment_service.py
@pytest.mark.asyncio
async def test_create_subscription(mock_stripe):
    payment = PaymentService()
    sub = await payment.create_subscription(
        user_id=123,
        plan="pro",
        payment_method_id="pm_test"
    )
    assert sub.status == "active"
📚 Recursos
Stripe Docs

SendGrid Docs

JWT.io

🎯 Roadmap
H04 (20-23 Nov): Auth Service

H05 (24-27 Nov): Payment + Notifications

H12 (Mar 2026): Analytics

H15+ (Jun 2026): Advanced features

Estado: Placeholder
Implementar en: H04-H05 (20-27 Nov 2025)
Versión: 0.1.0
Última actualización: 11 Nov 2025
Responsable: Álvaro Fernández Mota