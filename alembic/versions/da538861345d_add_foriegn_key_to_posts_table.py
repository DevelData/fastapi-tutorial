"""add foriegn key to posts table

Revision ID: da538861345d
Revises: 2db8e1f0e161
Create Date: 2024-04-19 21:11:54.311664

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'da538861345d'
down_revision: Union[str, None] = '2db8e1f0e161'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.Integer, nullable=False)
        )
    op.create_foreign_key(
        "posts_users_fkey",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE"
        )
    
    return


def downgrade() -> None:
    op.drop_constraint(
        "posts_users_fkey",
        table_name="posts")
    op.drop_column(
        table_name="posts",
        column_name="owner_id"
        )
    
    return
