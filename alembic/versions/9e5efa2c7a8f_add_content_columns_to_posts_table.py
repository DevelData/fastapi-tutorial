"""add content columns to posts table

Revision ID: 9e5efa2c7a8f
Revises: ba217ba94b66
Create Date: 2024-04-19 20:57:36.883233

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e5efa2c7a8f'
down_revision: Union[str, None] = 'ba217ba94b66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("content", sa.String, nullable=False)
        )
    
    return


def downgrade() -> None:
    op.drop_column(
        table_name="posts",
        column_name="content"
        )
    
    return
