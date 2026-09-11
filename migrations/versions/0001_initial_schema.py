"""Initial Local Commerce Core schema.

Revision ID: 0001_initial_schema
"""
from alembic import op
from backend.app.database import Base
import backend.app.models  # noqa: F401 -- registers every mapped table

revision = '0001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    Base.metadata.create_all(bind=op.get_bind())


def downgrade():
    Base.metadata.drop_all(bind=op.get_bind())
