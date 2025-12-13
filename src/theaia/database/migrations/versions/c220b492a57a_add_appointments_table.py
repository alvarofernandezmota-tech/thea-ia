"""add appointments table

Revision ID: c220b492a57a
Revises: f011b33ad061
Create Date: 2025-12-13 23:23:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c220b492a57a'
down_revision = 'f011b33ad061'  # Última migration existente
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create appointments table"""
    
    # Create appointments table
    op.create_table(
        'appointments',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('title', sa.Text(), nullable=False, server_default='Cita'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.String(20), nullable=False, server_default='scheduled'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.CheckConstraint("status IN ('scheduled', 'cancelled', 'completed', 'no_show')", name='check_appointment_status')
    )
    
    # Create indexes
    op.create_index('idx_appointments_user_id', 'appointments', ['user_id'])
    op.create_index('idx_appointments_start_time', 'appointments', ['start_time'])
    op.create_index('idx_appointments_status', 'appointments', ['status'])
    op.create_index('idx_appointments_user_status', 'appointments', ['user_id', 'status'])
    
    # Create trigger for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_appointments_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER appointments_updated_at
            BEFORE UPDATE ON appointments
            FOR EACH ROW
            EXECUTE FUNCTION update_appointments_updated_at();
    """)


def downgrade() -> None:
    """Drop appointments table"""
    
    op.execute("DROP TRIGGER IF EXISTS appointments_updated_at ON appointments;")
    op.execute("DROP FUNCTION IF EXISTS update_appointments_updated_at();")
    op.drop_index('idx_appointments_user_status', table_name='appointments')
    op.drop_index('idx_appointments_status', table_name='appointments')
    op.drop_index('idx_appointments_start_time', table_name='appointments')
    op.drop_index('idx_appointments_user_id', table_name='appointments')
    op.drop_table('appointments')
