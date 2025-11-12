Estructura Planificada - src/services/
Módulo: Services (Servicios de Negocio)
Propósito: Lógica negocio compleja
Patrón: Service Classes

⚠️ PLACEHOLDER - NO implementar antes H04

📋 Estado Actual (11 Nov 2025 - H01)
text
src/services/
├── __init__.py (placeholder)
├── README.md ✅
├── ROADMAP.md ✅
├── CHANGELOG.md ✅
├── STRUCTURE.md ✅ (este archivo)
└── DEPENDENCIES.md ✅
🎯 H04-H05: Services Implementation
Estructura Objetivo:
text
src/services/
│
├── __init__.py
│   from .auth_service import AuthService
│   from .payment_service import PaymentService
│   from .notification_service import NotificationService
│
├── auth_service.py ← 🆕 H04
│   class AuthService:
│       def create_access_token(user_id: int) -> str
│       def verify_token(token: str) -> int
│       def generate_api_key(user_id: int) -> str
│       def check_permission(user_id, permission) -> bool
│
├── payment_service.py ← 🆕 H05
│   class PaymentService:
│       def create_subscription(user_id, plan) -> Subscription
│       def cancel_subscription(user_id) -> bool
│       def is_subscription_active(user_id) -> bool
│       def handle_webhook(event) -> None
│
├── notification_service.py ← 🆕 H05
│   class NotificationService:
│       def send_telegram(user_id, message) -> bool
│       def send_email(email, subject, body) -> bool
│       def schedule_notification(...) -> None
│
├── analytics_service.py ← 🆕 H12
│   class AnalyticsService:
│       def track_event(user_id, event) -> None
│       def get_user_metrics(user_id) -> dict
│
└── [docs]/
🔗 Dependencias Internas
text
src/services/ depende de:
├── src/config (settings)
├── src/database (User model)
└── src/adapters (TelegramAdapter para notif)
text
src/services/ es usado por:
├── src/agents/ (check permissions, send notif)
├── src/adapters/ (auth tokens)
└── src/api/ (H08 - auth endpoints)
⚠️ NO IMPLEMENTAR ANTES DE H04

Última actualización: 11 Nov 2025