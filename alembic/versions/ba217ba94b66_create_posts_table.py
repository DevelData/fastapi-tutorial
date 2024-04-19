"""create posts table

Revision ID: ba217ba94b66
Revises: 
Create Date: 2024-04-19 20:46:36.897722

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ba217ba94b66'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "posts",
        sa.Column("id",sa.Integer, nullable=False, primary_key=True),
        sa.Column("title", sa.String, nullable=False)
        )
    
    return


def downgrade() -> None:
    op.drop_table("posts")

    return
