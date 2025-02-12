"""New Migration

Revision ID: 0688cb50c9ed
Revises: 
Create Date: 2025-01-16 21:49:34.936780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0688cb50c9ed'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('displaced_families', sa.Column('matched', sa.Boolean(), nullable=True))
    op.add_column('host_families', sa.Column('matched', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('host_families', 'matched')
    op.drop_column('displaced_families', 'matched')
    # ### end Alembic commands ###
