"""Add manager PIN settings.

Revision ID: 0003_manager_pin
Revises: 0002_product_attributes
"""
from alembic import op
import sqlalchemy as sa
revision = '0003_manager_pin'
down_revision = '0002_product_attributes'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table('security_settings', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('pin_hash', sa.String(256), nullable=False), sa.Column('must_change_pin', sa.Boolean(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False))

def downgrade():
    op.drop_table('security_settings')
