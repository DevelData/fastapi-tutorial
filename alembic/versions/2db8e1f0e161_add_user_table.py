"""add user table

Revision ID: 2db8e1f0e161
Revises: 9e5efa2c7a8f
Create Date: 2024-04-19 21:03:38.510671

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2db8e1f0e161'
down_revision: Union[str, None] = '9e5efa2c7a8f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, nullable=False),
        sa.Column("email", sa.String, nullable=False),
        sa.Column("password", sa.String, nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email")
        )
    
    return


def downgrade() -> None:
    op.drop_table("users")

    return
