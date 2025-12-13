"""add availability config

Revision ID: 3a39fe275414
Revises: c220b492a57a
Create Date: 2025-12-13 23:24:00.000000
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3a39fe275414'
down_revision = 'c220b492a57a'  # Depende de appointments
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create availability configuration tables"""
    
    # Create availability_config table
    op.create_table(
        'availability_config',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.Time(), nullable=False),
        sa.Column('end_time', sa.Time(), nullable=False),
        sa.Column('slot_duration', sa.Integer(), nullable=False, server_default='60'),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('day_of_week BETWEEN 0 AND 6', name='check_day_of_week'),
        sa.CheckConstraint('slot_duration > 0', name='check_slot_duration'),
        sa.UniqueConstraint('day_of_week', name='unique_day_config')
    )
    
    # Create indexes
    op.create_index('idx_availability_day_of_week', 'availability_config', ['day_of_week'])
    op.create_index('idx_availability_active', 'availability_config', ['is_active'])
    
    # Create trigger for updated_at
    op.execute("""
        CREATE OR REPLACE FUNCTION update_availability_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = CURRENT_TIMESTAMP;
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
    """)
    
    op.execute("""
        CREATE TRIGGER availability_updated_at
            BEFORE UPDATE ON availability_config
            FOR EACH ROW
            EXECUTE FUNCTION update_availability_updated_at();
    """)
    
    # Insert default business hours (Monday to Friday, 9am-6pm)
    op.execute("""
        INSERT INTO availability_config (day_of_week, start_time, end_time, slot_duration, is_active) VALUES
        (0, '09:00:00', '18:00:00', 60, TRUE),  -- Monday
        (1, '09:00:00', '18:00:00', 60, TRUE),  -- Tuesday
        (2, '09:00:00', '18:00:00', 60, TRUE),  -- Wednesday
        (3, '09:00:00', '18:00:00', 60, TRUE),  -- Thursday
        (4, '09:00:00', '18:00:00', 60, TRUE)   -- Friday
        ON CONFLICT (day_of_week) DO NOTHING;
    """)
    
    # Create blocked_time_slots table
    op.create_table(
        'blocked_time_slots',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=False),
        sa.Column('reason', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.CheckConstraint('end_time > start_time', name='valid_time_range')
    )
    
    # Create index for blocked slots
    op.create_index('idx_blocked_slots_time_range', 'blocked_time_slots', ['start_time', 'end_time'])


def downgrade() -> None:
    """Drop availability configuration tables"""
    
    # Drop blocked_time_slots
    op.drop_index('idx_blocked_slots_time_range', table_name='blocked_time_slots')
    op.drop_table('blocked_time_slots')
    
    # Drop availability_config
    op.execute("DROP TRIGGER IF EXISTS availability_updated_at ON availability_config;")
    op.execute("DROP FUNCTION IF EXISTS update_availability_updated_at();")
    op.drop_index('idx_availability_active', table_name='availability_config')
    op.drop_index('idx_availability_day_of_week', table_name='availability_config')
    op.drop_table('availability_config')
