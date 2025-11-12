"""Initial schema with tenant support

Revision ID: e0a17d850507
Revises: 
Create Date: 2025-11-12 16:05:00.000000

THEA IA 2.0 - H02 Database Schema
==================================
Primera migración del sistema THEA IA.

Crea:
- users: Usuarios de Telegram con multi-tenant
- events: Eventos/recordatorios de agenda
- notes: Notas del usuario con tags
- conversations: Sesiones FSM de conversación
- message_history: Auditoría completa de mensajes

Elimina:
- Schema antiguo (usuarios, citas, conversaciones antiguas) con CASCADE

Decisiones arquitectónicas:
- Multi-tenant: tenant_id en todas las tablas (Sesión 5)
- Timestamps: created_at, updated_at automáticos
- JSONB: Metadatos flexibles (preferences, extra_data)
- CASCADE: Delete orphans automático
- Índices: Optimizados para queries frecuentes
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic
revision = 'e0a17d850507'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Crea el schema completo de THEA IA 2.0.
    
    Orden de creación:
    1. users (tabla padre)
    2. events, notes, conversations (dependen de users)
    3. message_history (depende de conversations)
    4. Elimina schema antiguo con CASCADE
    """
    
    # ==========================================
    # TABLA: users
    # Usuario del sistema (Telegram)
    # ==========================================
    op.create_table('users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('telegram_id', sa.BigInteger(), nullable=False),
        sa.Column('username', sa.String(length=255), nullable=True),
        sa.Column('first_name', sa.String(length=255), nullable=True),
        sa.Column('last_name', sa.String(length=255), nullable=True),
        sa.Column('language_code', sa.String(length=10), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('preferences', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('telegram_id')
    )
    op.create_index('ix_users_is_active', 'users', ['is_active'], unique=False)
    op.create_index('ix_users_telegram_id', 'users', ['telegram_id'], unique=False)
    op.create_index('ix_users_tenant_id', 'users', ['tenant_id'], unique=False)
    
    # ==========================================
    # TABLA: events
    # Eventos y recordatorios de la agenda
    # ==========================================
    op.create_table('events',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('start_datetime', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_datetime', sa.DateTime(timezone=True), nullable=True),
        sa.Column('location', sa.String(length=500), nullable=True),
        sa.Column('event_type', sa.String(length=50), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=True),
        sa.Column('reminder_minutes', sa.Integer(), nullable=True),
        sa.Column('recurrence_rule', sa.String(length=200), nullable=True),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_events_start_datetime', 'events', ['start_datetime'], unique=False)
    op.create_index('ix_events_status', 'events', ['status'], unique=False)
    op.create_index('ix_events_tenant_id', 'events', ['tenant_id'], unique=False)
    op.create_index('ix_events_user_id', 'events', ['user_id'], unique=False)
    
    # ==========================================
    # TABLA: notes
    # Notas del usuario con categorías y tags
    # ==========================================
    op.create_table('notes',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=True),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.Text()), nullable=True),
        sa.Column('priority', sa.Integer(), nullable=True),
        sa.Column('is_pinned', sa.Boolean(), nullable=True),
        sa.Column('reminder_datetime', sa.DateTime(timezone=True), nullable=True),
        sa.Column('extra_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_notes_category', 'notes', ['category'], unique=False)
    op.create_index('ix_notes_is_pinned', 'notes', ['is_pinned'], unique=False)
    op.create_index('ix_notes_tenant_id', 'notes', ['tenant_id'], unique=False)
    op.create_index('ix_notes_user_id', 'notes', ['user_id'], unique=False)
    
    # ==========================================
    # TABLA: conversations
    # Sesiones de conversación FSM
    # ==========================================
    op.create_table('conversations',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('session_id', sa.String(length=255), nullable=False),
        sa.Column('current_state', sa.String(length=50), nullable=False),
        sa.Column('context_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('last_message_id', sa.String(length=255), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('session_id')
    )
    op.create_index('ix_conversations_current_state', 'conversations', ['current_state'], unique=False)
    op.create_index('ix_conversations_is_active', 'conversations', ['is_active'], unique=False)
    op.create_index('ix_conversations_session_id', 'conversations', ['session_id'], unique=False)
    op.create_index('ix_conversations_tenant_id', 'conversations', ['tenant_id'], unique=False)
    op.create_index('ix_conversations_user_id', 'conversations', ['user_id'], unique=False)
    
    # ==========================================
    # TABLA: message_history
    # Auditoría completa de mensajes
    # ==========================================
    op.create_table('message_history',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('tenant_id', sa.String(length=50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('conversation_id', sa.Integer(), nullable=False),
        sa.Column('message_id', sa.String(length=255), nullable=False),
        sa.Column('user_message', sa.Text(), nullable=True),
        sa.Column('bot_response', sa.Text(), nullable=True),
        sa.Column('intent_detected', sa.String(length=100), nullable=True),
        sa.Column('entities_extracted', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('confidence_score', sa.Float(), nullable=True),
        sa.Column('processing_time_ms', sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(['conversation_id'], ['conversations.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_message_history_conversation_id', 'message_history', ['conversation_id'], unique=False)
    op.create_index('ix_message_history_intent_detected', 'message_history', ['intent_detected'], unique=False)
    op.create_index('ix_message_history_message_id', 'message_history', ['message_id'], unique=False)
    op.create_index('ix_message_history_tenant_id', 'message_history', ['tenant_id'], unique=False)
    
    # ==========================================
    # ELIMINAR SCHEMA ANTIGUO CON CASCADE
    # Tablas del prototipo pre-H02
    # Usa CASCADE para eliminar foreign keys automáticamente
    # ==========================================
    op.execute('DROP TABLE IF EXISTS historial_citas CASCADE')
    op.execute('DROP TABLE IF EXISTS automatizaciones CASCADE')
    op.execute('DROP TABLE IF EXISTS servicios CASCADE')
    op.execute('DROP TABLE IF EXISTS logs CASCADE')
    op.execute('DROP TABLE IF EXISTS usuarios CASCADE')
    op.execute('DROP TABLE IF EXISTS citas CASCADE')
    op.execute('DROP TABLE IF EXISTS integraciones CASCADE')
    op.execute('DROP TABLE IF EXISTS mensajes_sistema CASCADE')
    op.execute('DROP TABLE IF EXISTS conversaciones CASCADE')


def downgrade() -> None:
    """
    Revierte la migración (NO RECOMENDADO en producción).
    
    ADVERTENCIA: Esto eliminará TODOS los datos de THEA IA 2.0
    y NO restaurará los datos antiguos (solo schema vacío).
    """
    
    # Eliminar tablas nuevas en orden inverso (por foreign keys)
    op.drop_index('ix_message_history_tenant_id', table_name='message_history')
    op.drop_index('ix_message_history_message_id', table_name='message_history')
    op.drop_index('ix_message_history_intent_detected', table_name='message_history')
    op.drop_index('ix_message_history_conversation_id', table_name='message_history')
    op.drop_table('message_history')
    
    op.drop_index('ix_conversations_user_id', table_name='conversations')
    op.drop_index('ix_conversations_tenant_id', table_name='conversations')
    op.drop_index('ix_conversations_session_id', table_name='conversations')
    op.drop_index('ix_conversations_is_active', table_name='conversations')
    op.drop_index('ix_conversations_current_state', table_name='conversations')
    op.drop_table('conversations')
    
    op.drop_index('ix_notes_user_id', table_name='notes')
    op.drop_index('ix_notes_tenant_id', table_name='notes')
    op.drop_index('ix_notes_is_pinned', table_name='notes')
    op.drop_index('ix_notes_category', table_name='notes')
    op.drop_table('notes')
    
    op.drop_index('ix_events_user_id', table_name='events')
    op.drop_index('ix_events_tenant_id', table_name='events')
    op.drop_index('ix_events_status', table_name='events')
    op.drop_index('ix_events_start_datetime', table_name='events')
    op.drop_table('events')
    
    op.drop_index('ix_users_tenant_id', table_name='users')
    op.drop_index('ix_users_telegram_id', table_name='users')
    op.drop_index('ix_users_is_active', table_name='users')
    op.drop_table('users')
