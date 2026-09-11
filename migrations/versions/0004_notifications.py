"""Add local notification records.

Revision ID: 0004_notifications
Revises: 0003_manager_pin
"""
from alembic import op
import sqlalchemy as sa
revision = '0004_notifications'
down_revision = '0003_manager_pin'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('notifications', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('notification_type', sa.String(40), nullable=False), sa.Column('message', sa.Text(), nullable=False), sa.Column('is_read', sa.Boolean(), nullable=False), sa.Column('read_at', sa.DateTime()), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.create_index('ix_notifications_is_read', 'notifications', ['is_read'])

def downgrade():
    op.drop_index('ix_notifications_is_read', table_name='notifications')
    op.drop_table('notifications')
