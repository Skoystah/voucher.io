"""widen voucher duration column

Revision ID: b7d21e4a9c05
Revises: 70ba03f860a4
Create Date: 2026-10-21 10:12:04.518372

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b7d21e4a9c05"
down_revision: str | Sequence[str] | None = "70ba03f860a4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema.

    '12h' is three characters, so String(2) could not hold every valid
    duration on backends that enforce the declared length.
    """
    op.alter_column(
        "voucher",
        "duration",
        existing_type=sa.String(length=2),
        type_=sa.String(length=4),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "voucher",
        "duration",
        existing_type=sa.String(length=4),
        type_=sa.String(length=2),
        existing_nullable=False,
    )
