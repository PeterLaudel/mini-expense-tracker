"""Add event table

Revision ID: d670c214fbd0
Revises: 38b41ea36ff8
Create Date: 2024-12-27 16:48:49.428237

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d670c214fbd0"
down_revision: Union[str, None] = "38b41ea36ff8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), nullable=False, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.sql.func.now(),
        ),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("json", sa.JSON(), nullable=False),  # type: ignore[misc]
    )


def downgrade() -> None:
    op.drop_table("event")
