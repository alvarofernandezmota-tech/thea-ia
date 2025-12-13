"""remove default availability make flexible

Revision ID: c4aea4158c23
Revises: 3a39fe275414
Create Date: 2025-12-13 23:28:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c4aea4158c23'
down_revision = '3a39fe275414'
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Remove default availability hours.
    Make calendar 100% flexible - user decides ALL scheduling.
    No restrictions on days or hours.
    """
    
    # Remove all predefined business hours
    op.execute("DELETE FROM availability_config;")
    
    # Drop the unique constraint on day_of_week
    # (allows multiple configurations per day if needed in future)
    op.drop_constraint('unique_day_config', 'availability_config', type_='unique')
    
    # Make availability_config optional by allowing NULL values
    # This signals: if empty = 24/7 availability, user decides everything
    op.alter_column('availability_config', 'day_of_week',
                    existing_type=sa.Integer(),
                    nullable=True)
    
    # Add comment explaining the flexible nature
    op.execute("""
        COMMENT ON TABLE availability_config IS 
        'Optional user-defined scheduling preferences. 
        If empty, user can schedule 24/7 conversationally.
        If populated, these are user preferences, NOT hard restrictions.';
    """)
    
    op.execute("""
        COMMENT ON COLUMN availability_config.is_active IS 
        'User preference flag. Even if false, user can still override conversationally.';
    """)


def downgrade() -> None:
    """
    Restore default business hours (if needed for rollback)
    """
    
    # Restore unique constraint
    op.create_unique_constraint('unique_day_config', 'availability_config', ['day_of_week'])
    
    # Make day_of_week NOT NULL again
    op.alter_column('availability_config', 'day_of_week',
                    existing_type=sa.Integer(),
                    nullable=False)
    
    # Restore default business hours (Monday-Friday, 9am-6pm)
    op.execute("""
        INSERT INTO availability_config (day_of_week, start_time, end_time, slot_duration, is_active) VALUES
        (0, '09:00:00', '18:00:00', 60, TRUE),  -- Monday
        (1, '09:00:00', '18:00:00', 60, TRUE),  -- Tuesday
        (2, '09:00:00', '18:00:00', 60, TRUE),  -- Wednesday
        (3, '09:00:00', '18:00:00', 60, TRUE),  -- Thursday
        (4, '09:00:00', '18:00:00', 60, TRUE)   -- Friday
        ON CONFLICT DO NOTHING;
    """)
