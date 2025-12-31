"""init trading tables

Revision ID: 53967d03dbe0
Revises: 
Create Date: 2025-12-31 10:48:05.503471

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '53967d03dbe0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # trades table
    op.create_table(
        "trades",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("symbol", sa.String(length=10), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=True),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("side", sa.String(length=6), nullable=False),
        sa.Column("account_balance", sa.Float(), nullable=False),
    )

    # strategies table
    op.create_table(
        "strategies",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("indicators", sa.JSON(), nullable=True),
    )

    # equity table
    op.create_table(
        "equity",
        sa.Column("id", sa.Integer(), primary_key=True, nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("equity")
    op.drop_table("strategies")
    op.drop_table("trades")