Dependencias - src/services/
Módulo: Services
Versión actual: 0.1.0 (H01 - Placeholder)

⚠️ PLACEHOLDER - NO instalar deps antes H04

📦 Dependencias Python
H04 (20-23 Nov): Auth Service
text
# Authentication
python-jose[cryptography]==3.3.0   # JWT tokens
passlib[bcrypt]==1.7.4              # Password hashing
H05 (24-27 Nov): Payment + Notifications
text
# Payment
stripe==7.4.0                       # Stripe integration

# Email
sendgrid==6.11.0                    # Email service
H12 (Mar 2026): Analytics
text
# Analytics
mixpanel==4.10.0
segment-analytics-python==2.2.3
🔗 Dependencias Internas
Módulos que usa:
python
from src.config import get_settings
from src.database.models import User
from src.adapters import TelegramAdapter
Usado por:
python
# src/agents/
from src.services import PaymentService, NotificationService

# src/adapters/
from src.services import AuthService

# src/api/ (H08)
from src.services import AuthService, PaymentService
🔐 Variables de Entorno
H04 (Auth):
bash
JWT_SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080  # 7 days
H05 (Payment):
bash
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_PRICE_ID_PRO=price_...
STRIPE_PRICE_ID_BUSINESS=price_...
H05 (Email):
bash
SENDGRID_API_KEY=SG....
SENDGRID_FROM_EMAIL=noreply@thea-ia.com
🚀 Instalación (H04-H05)
⚠️ NO INSTALAR ANTES
bash
# Cuando llegue H04:
pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4

# Cuando llegue H05:
pip install stripe==7.4.0 sendgrid==6.11.0
📊 Tabla Resumen
Hito	Deps	Services
H04	2	1 (auth)
H05	+2	+2 (payment, notif)
H12	+2	+1 (analytics)
⚠️ RECUERDA: NO IMPLEMENTAR ANTES DE H04

Última actualización: 11 Nov 2025