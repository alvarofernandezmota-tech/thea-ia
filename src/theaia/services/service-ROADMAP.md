Roadmap - src/services/
Módulo: Services (Servicios de Negocio)
Versión actual: 0.1.0 (H01 - Placeholder)
Próxima versión: 0.4.0 (H04 - Auth Service)

📊 Estado Actual (11 Nov 2025 - H01)
Completado ✅
Estructura módulo definida

Servicios identificados

Documentación placeholder

Pendiente ⏳
TODO en H04-H05 - No implementar antes

⏸️ H02-H03: NO IMPLEMENTAR
Este módulo es placeholder hasta H04.

🎯 H04 (20-23 Nov): Auth Service
Objetivo: Autenticación y autorización

auth_service.py:
JWT token generation/validation

API key management

Permission checking

User roles (free, pro, business)

Criterios Done H04:
✅ JWT tokens funcionan

✅ API keys generados

✅ Permission system base

✅ Tests >85% coverage

💳 H05 (24-27 Nov): Payment + Notifications
Objetivo: Monetización y notificaciones

payment_service.py:
Stripe integration

Create subscription

Cancel subscription

Check subscription active

Webhook handling (Stripe events)

notification_service.py:
Send Telegram notification

Send email notification (SendGrid)

Schedule notifications

Notification templates

Criterios Done H05:
✅ Stripe integration funciona

✅ Subscriptions create/cancel OK

✅ Webhooks procesados correctamente

✅ Notifications enviadas

✅ Email templates listos

📊 H12 (Mar 2026): Analytics
analytics_service.py:

Usage tracking

User metrics

Business intelligence

Dashboard data

📈 Métricas de Éxito
Hito	Services	Integrations	Tests Coverage
H04	1 (auth)	0	>85%
H05	+2 (payment, notif)	2 (Stripe, SendGrid)	>85%
H12	+1 (analytics)	2 (Mixpanel, Segment)	>80%
🚧 Riesgos
Riesgo 1: Stripe webhooks fallan
Mitigación: Retry logic, webhook signature validation

Riesgo 2: Email delivery issues
Mitigación: Multiple providers (SendGrid primary, fallback)

📝 Decisiones Técnicas
¿Por qué Stripe vs otros?
Mejor developer experience

Documentación excelente

Popular en startups

Soporte internacional

¿Por qué SendGrid vs otros?
Free tier generoso

API simple

Templates

Analytics

Última actualización: 11 Nov 2025
Próxima revisión: H04 start (20 Nov 2025)
Responsable: Álvaro Fernández Mota