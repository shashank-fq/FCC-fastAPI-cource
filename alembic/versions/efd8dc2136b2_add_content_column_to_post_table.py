"""add content column to post table

Revision ID: efd8dc2136b2
Revises: e611fa449b79
Create Date: 2026-06-03 01:51:45.041680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'efd8dc2136b2'
down_revision: Union[str, Sequence[str], None] = 'e611fa449b79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))

    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass
