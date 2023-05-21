"""add last few columns to posts table

Revision ID: 33a4c348e9c8
Revises: 153b980cc60c
Create Date: 2023-05-19 16:04:57.148606

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "33a4c348e9c8"
down_revision = "153b980cc60c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "posts",
        sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),
    )
    op.add_column(
        "posts",
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.text("NOW()"),
        ),
    )


def downgrade() -> None:
    op.drop_column("posts", "published")
    op.drop_column("posts", "created_at")
