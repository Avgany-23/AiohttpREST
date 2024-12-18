"""add uniq title owner to record

Revision ID: 55d89c24c01d
Revises: 001
Create Date: 2024-12-17 19:00:09.506760

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '002'
down_revision: Union[str, None] = '001'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint('unique_title_owner', 'record', ['title', 'owner'])


def downgrade() -> None:
    op.drop_constraint('unique_title_owner', 'record', type_='unique')
