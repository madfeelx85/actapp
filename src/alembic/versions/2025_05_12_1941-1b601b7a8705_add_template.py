"""add template

Revision ID: 1b601b7a8705
Revises: 9ae264b70711
Create Date: 2025-05-12 19:41:07.645071

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1b601b7a8705"
down_revision: Union[str, None] = "9ae264b70711"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "templates",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=True),
        sa.Column("path", sa.String(length=500), nullable=False),
        sa.Column("type", sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_templates")),
    )


def downgrade() -> None:
    op.drop_table("templates")
