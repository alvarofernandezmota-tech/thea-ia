Changelog - src/services/
Placeholder Module - No se implementa hasta H04-H05

[Unreleased]
Planificado para H04 (20-23 Nov 2025)
Auth Service (JWT, API keys, permissions)

Planificado para H05 (24-27 Nov 2025)
Payment Service (Stripe)

Notification Service (Email, Telegram)

Planificado para H12 (Mar 2026)
Analytics Service

[0.5.0] - 2025-11-27 (H05 Target)
Added
payment_service.py:

create_subscription(user_id, plan)

cancel_subscription(user_id)

is_subscription_active(user_id)

handle_webhook(event)

Stripe integration completa

notification_service.py:

send_telegram_notification(user_id, message)

send_email(email, subject, body)

schedule_notification(user_id, message, datetime)

Email templates (reminder, welcome, payment)

Dependencies
stripe==7.4.0

sendgrid==6.11.0

[0.4.0] - 2025-11-23 (H04 Target)
Added
auth_service.py:

create_access_token(user_id) → str

verify_token(token) → user_id

generate_api_key(user_id) → str

check_permission(user_id, permission) → bool

User roles (free, pro, business)

Dependencies
python-jose[cryptography]==3.3.0

passlib[bcrypt]==1.7.4

[0.1.0] - 2025-11-03 (H01)
Added
Estructura placeholder

Documentación

Nota: Este módulo es placeholder hasta H04.

Última actualización: 11 Nov 2025