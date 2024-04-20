"""add last few columns to posts table

Revision ID: c59732e40e51
Revises: da538861345d
Create Date: 2024-04-20 03:51:45.849146

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c59732e40e51'
down_revision: Union[str, None] = 'da538861345d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("published",
                                     sa.Boolean,
                                     nullable=False,
                                     server_default="true"))
    op.add_column("posts", sa.Column("created_at",
                                     sa.TIMESTAMP(timezone=True),
                                     nullable=False,
                                     server_default=sa.text("now()")))
    
    return


def downgrade() -> None:
    op.drop_column("posts", "created_at")
    op.drop_column("posts", "published")

    return
