"""add content column to post table

Revision ID: 5ce2d7dd4796
Revises: 2b7e062a8518
Create Date: 2023-05-19 15:07:08.151071

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "5ce2d7dd4796"
down_revision = "2b7e062a8518"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("content", sa.String(), nullable=False))


def downgrade() -> None:
    op.drop_column("posts", "content")
