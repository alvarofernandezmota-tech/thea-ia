"""add_last_activity_to_users

Revision ID: 9ed4975f2bd7
Revises: dbc963a8ddad
Create Date: 2025-11-19 15:47:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ed4975f2bd7'
down_revision = 'dbc963a8ddad'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Añade columna last_activity a tabla users."""
    op.add_column(
        'users',
        sa.Column('last_activity', sa.DateTime(timezone=True), nullable=True)
    )


def downgrade() -> None:
    """Elimina columna last_activity de tabla users."""
    op.drop_column('users', 'last_activity')
