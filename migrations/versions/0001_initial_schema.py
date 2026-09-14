"""Initial Local Commerce Core schema.

Revision ID: 0001_initial_schema
"""
from alembic import op
from backend.app.database import Base
import backend.app.models  # noqa: F401 -- registers mapped tables

revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

INITIAL_TABLES = {
    'store_settings', 'document_sequences', 'categories', 'units', 'products',
    'customers', 'suppliers', 'accounts', 'purchases', 'purchase_items',
    'sales', 'sale_items', 'payments', 'inventory_movements', 'expenses',
    'audit_logs', 'sales_returns', 'return_items',
}


def upgrade():
    tables = [table for table in Base.metadata.sorted_tables if table.name in INITIAL_TABLES]
    Base.metadata.create_all(bind=op.get_bind(), tables=tables)


def downgrade():
    tables = [table for table in reversed(Base.metadata.sorted_tables) if table.name in INITIAL_TABLES]
    Base.metadata.drop_all(bind=op.get_bind(), tables=tables)
