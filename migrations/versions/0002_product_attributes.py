"""Add generic product attributes.

Revision ID: 0002_product_attributes
Revises: 0001_initial_schema
"""
from alembic import op
import sqlalchemy as sa

revision = '0002_product_attributes'
down_revision = '0001_initial_schema'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('attribute_definitions', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('name', sa.String(100), nullable=False, unique=True), sa.Column('data_type', sa.String(20), nullable=False), sa.Column('is_searchable', sa.Boolean(), nullable=False), sa.Column('is_filterable', sa.Boolean(), nullable=False), sa.Column('show_on_card', sa.Boolean(), nullable=False), sa.Column('created_at', sa.DateTime(), nullable=False), sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.create_table('product_attribute_values', sa.Column('id', sa.Integer(), primary_key=True), sa.Column('product_id', sa.Integer(), sa.ForeignKey('products.id', ondelete='CASCADE'), nullable=False), sa.Column('attribute_definition_id', sa.Integer(), sa.ForeignKey('attribute_definitions.id'), nullable=False), sa.Column('value', sa.Text(), nullable=False))
    op.create_index('ix_product_attribute_values_product_id', 'product_attribute_values', ['product_id'])


def downgrade():
    op.drop_index('ix_product_attribute_values_product_id', table_name='product_attribute_values')
    op.drop_table('product_attribute_values')
    op.drop_table('attribute_definitions')
