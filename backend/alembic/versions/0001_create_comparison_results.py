"""create comparison_results table

Revision ID: 0001
Revises:
Create Date: 2026-04-07
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "comparison_results",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("home_price", sa.Float(), nullable=False),
        sa.Column("monthly_rent", sa.Float(), nullable=False),
        sa.Column("mortgage_rate", sa.Float(), nullable=False),
        sa.Column("investment_return_rate", sa.Float(), nullable=False),
        sa.Column("buy_total_cost", sa.Float(), nullable=False),
        sa.Column("rent_total_cost", sa.Float(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
        ),
    )


def downgrade() -> None:
    op.drop_table("comparison_results")
