"""update_note_datetimes_to_timezone_aware

Revision ID: <GENERADO_AUTO>
Revises: <REVISION_ANTERIOR>
Create Date: <FECHA_AUTO>

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '<DEJA_EL_GENERADO>'
down_revision = '<DEJA_EL_GENERADO>'
branch_labels = None
depends_on = None


def upgrade():
    # Convierte TIMESTAMP a TIMESTAMPTZ (con timezone)
    op.alter_column(
        'notes',
        'created_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(timezone=False),
        existing_nullable=False
    )
    
    op.alter_column(
        'notes',
        'updated_at',
        type_=sa.DateTime(timezone=True),
        existing_type=sa.DateTime(timezone=False),
        existing_nullable=False
    )


def downgrade():
    # Revierte a TIMESTAMP sin timezone
    op.alter_column(
        'notes',
        'created_at',
        type_=sa.DateTime(timezone=False),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )
    
    op.alter_column(
        'notes',
        'updated_at',
        type_=sa.DateTime(timezone=False),
        existing_type=sa.DateTime(timezone=True),
        existing_nullable=False
    )
