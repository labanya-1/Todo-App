"""create phone number for user column

Revision ID: 97ea92ed8374
Revises: 
Create Date: 2026-04-06 23:27:22.598165

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97ea92ed8374'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    # pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users','phone_number')
