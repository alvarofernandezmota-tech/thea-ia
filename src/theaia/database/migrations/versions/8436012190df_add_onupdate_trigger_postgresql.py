"""add_onupdate_trigger_postgresql

Revision ID: 8436012190df
Revises: 9ed4975f2bd7
Create Date: 2025-11-19 20:38:00.000000
"""
from alembic import op

revision = '8436012190df'
down_revision = '9ed4975f2bd7'
branch_labels = None
depends_on = None

def upgrade() -> None:
    """Crear triggers para updated_at - SEPARADO por AsyncPG."""
    
    # 1. Eliminar triggers existentes (UNO POR UNO)
    op.execute("DROP TRIGGER IF EXISTS update_events_updated_at ON events")
    op.execute("DROP TRIGGER IF EXISTS update_users_updated_at ON users")
    op.execute("DROP TRIGGER IF EXISTS update_notes_updated_at ON notes")
    op.execute("DROP TRIGGER IF EXISTS update_conversations_updated_at ON conversations")
    op.execute("DROP TRIGGER IF EXISTS update_message_history_updated_at ON message_history")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
    
    # 2. Crear función trigger
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ language 'plpgsql'
    """)
    
    # 3. Crear triggers (UNO POR UNO)
    op.execute("""
        CREATE TRIGGER update_events_updated_at
        BEFORE UPDATE ON events
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)
    
    op.execute("""
        CREATE TRIGGER update_users_updated_at
        BEFORE UPDATE ON users
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)
    
    op.execute("""
        CREATE TRIGGER update_notes_updated_at
        BEFORE UPDATE ON notes
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)
    
    op.execute("""
        CREATE TRIGGER update_conversations_updated_at
        BEFORE UPDATE ON conversations
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)
    
    op.execute("""
        CREATE TRIGGER update_message_history_updated_at
        BEFORE UPDATE ON message_history
        FOR EACH ROW
        EXECUTE FUNCTION update_updated_at_column()
    """)

def downgrade() -> None:
    """Eliminar triggers."""
    op.execute("DROP TRIGGER IF EXISTS update_events_updated_at ON events")
    op.execute("DROP TRIGGER IF EXISTS update_users_updated_at ON users")
    op.execute("DROP TRIGGER IF EXISTS update_notes_updated_at ON notes")
    op.execute("DROP TRIGGER IF EXISTS update_conversations_updated_at ON conversations")
    op.execute("DROP TRIGGER IF EXISTS update_message_history_updated_at ON message_history")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column()")
