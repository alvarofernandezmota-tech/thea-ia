CHANGELOG — TelegramAdapter
v1.0.0 — 2025-11-12 🎉
Added
TelegramAdapter completo (~400 LOC)

Bot funcional con python-telegram-bot 20.7

Persistencia usuarios automática

get_or_create_from_telegram()

UserRepository integration

Telegram ID único por tenant

Preferences JSONB (timezone, language)

Persistencia conversaciones

ConversationRepository integration

Session ID: telegram_{user_id}

FSM state persistente

Context JSONB con merge inteligente

Auditoría mensajes completa

MessageHistoryRepository integration

Intent detectado (placeholder)

Entities extraídas JSONB (placeholder)

Confidence score

Processing time ms

Comandos básicos

/start - Registrar usuario + iniciar conversación

/help - Mostrar comandos disponibles

/reset - Reiniciar conversación (limpiar context)

Error handling

Try-catch en todos los handlers

Rollback automático en fallos database

Logging detallado

Async/await completo

python-telegram-bot Application

Async handlers

Async database operations

Primera conversación real

Usuario: Entu

Telegram ID: 6961767622

Fecha: 12 Nov 2025, 17:02 CET

Mensajes: 2 guardados PostgreSQL

Estado: Funcional

Technical Details
Framework: python-telegram-bot 20.7

Database: PostgreSQL via asyncpg

ORM: SQLAlchemy 2.0 async

Repositories: UserRepository, ConversationRepository, MessageHistoryRepository

Multi-tenant: tenant_id obligatorio en todas las queries

Changed
Reemplazado aiogram por python-telegram-bot (mayor estabilidad)

Arquitectura adapter pattern consolidada

Fixed
Module imports con python -m

Database connection Windows (127.0.0.1 vs localhost)

AsyncSession context manager SQLAlchemy 2.0

Dependencies
text
python-telegram-bot==20.7
SQLAlchemy==2.0.44
asyncpg==0.29.0
alembic==1.12.1
Refs
Hito: H02 - Database + Telegram Integration

Commit: feat(H02) 12 nov 2025

Milestone: docs/roadmap/milestones/H02.md

Tests: 12/12 database pasando (100%)

Roadmap
v1.1.0 (H03): CoreRouter integration + NLP real

v1.2.0 (H05-H06): Inline keyboards + media handling

v1.3.0 (H10): Webhooks production + rate limiting

v2.0.0 (H12): Grupos/canales + admin commands

Última actualización: 14 Nov 2025
Responsable: Álvaro Fernández Mota (CEO THEA IA)