"""H02: Fix multi-tenant constraints and add user_id

Revision ID: dbc963a8ddad
Revises: e0a17d850507
Create Date: 2025-11-15 16:02:32.874903+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dbc963a8ddad'
down_revision = 'e0a17d850507'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Añadir user_id a message_history
    op.add_column('message_history', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_index('ix_message_history_user_id', 'message_history', ['user_id'], unique=False)
    op.create_foreign_key('fk_message_history_user_id', 'message_history', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    
    # 2. Constraint multi-tenant en users
    op.drop_constraint('users_telegram_id_key', 'users', type_='unique')
    op.create_unique_constraint('uq_user_tenant_telegram', 'users', ['tenant_id', 'telegram_id'])
    
    # 3. Index unique en conversations.session_id
    op.drop_constraint('conversations_session_id_key', 'conversations', type_='unique')
    op.drop_index('ix_conversations_session_id', table_name='conversations')
    op.create_index('ix_conversations_session_id', 'conversations', ['session_id'], unique=True)


def downgrade() -> None:
    # Revertir en orden inverso
    
    # 3. Revertir index conversations
    op.drop_index('ix_conversations_session_id', table_name='conversations')
    op.create_index('ix_conversations_session_id', 'conversations', ['session_id'], unique=False)
    op.create_unique_constraint('conversations_session_id_key', 'conversations', ['session_id'])
    
    # 2. Revertir constraint users
    op.drop_constraint('uq_user_tenant_telegram', 'users', type_='unique')
    op.create_unique_constraint('users_telegram_id_key', 'users', ['telegram_id'])
    
    # 1. Revertir message_history
    op.drop_constraint('fk_message_history_user_id', 'message_history', type_='foreignkey')
    op.drop_index('ix_message_history_user_id', table_name='message_history')
    op.drop_column('message_history', 'user_id')
