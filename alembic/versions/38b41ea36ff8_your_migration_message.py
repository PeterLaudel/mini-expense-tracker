"""Your migration message

Revision ID: 38b41ea36ff8
Revises:
Create Date: 2024-12-23 13:47:02.141836

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "38b41ea36ff8"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "expense",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column("date", sa.DateTime(), nullable=False),
        sa.Column("category", sa.String(), nullable=False),
        sa.Column("amount", sa.Float(), nullable=False),
        sa.Column("description", sa.String(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("expense")
