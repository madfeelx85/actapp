"""add fields into template

Revision ID: 622dbbe73a65
Revises: 292643b1a1d5
Create Date: 2025-05-12 20:49:25.116330

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "622dbbe73a65"
down_revision: Union[str, None] = "292643b1a1d5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    op.add_column("templates", sa.Column("fields", sa.JSON(), nullable=True))



def downgrade() -> None:

    op.drop_column("templates", "fields")

