"""add participants to events and remove reminder_minutes

Revision ID: 8f5df1273465
Revises: 3c34320c3e13
Create Date: 2025-12-04 16:28:00

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '8f5df1273465'
down_revision = '3c34320c3e13'
branch_labels = None
depends_on = None


def upgrade():
    """
    Agrega participants y elimina reminder_minutes.
    
    NOTE: tenant_id YA EXISTE en la BD desde H02, no lo tocamos.
    """
    # Agregar participants (JSONB, nullable, default lista vacía)
    op.add_column('events', 
        sa.Column('participants', 
                  postgresql.JSONB(astext_type=sa.Text()), 
                  nullable=True,
                  server_default='[]')
    )
    
    # Eliminar reminder_minutes (movido a ReminderAgent)
    op.drop_column('events', 'reminder_minutes')


def downgrade():
    """
    Revierte cambios:
    - Elimina participants
    - Restaura reminder_minutes
    """
    # Restaurar reminder_minutes
    op.add_column('events',
        sa.Column('reminder_minutes', sa.INTEGER(), nullable=True)
    )
    
    # Eliminar participants
    op.drop_column('events', 'participants')
