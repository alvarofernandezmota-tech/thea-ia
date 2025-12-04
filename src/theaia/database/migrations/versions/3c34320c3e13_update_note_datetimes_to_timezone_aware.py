"""update_note_datetimes_to_timezone_aware

Revision ID: 3c34320c3e13
Revises: 9ed4975f2bd7
Create Date: 2025-11-24 20:21:01

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '3c34320c3e13'
down_revision = '8436012190df'  # Cambiar de 9ed4975f2bd7 a 8436012190df
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
