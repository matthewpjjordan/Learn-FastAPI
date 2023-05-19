"""add foreign-key to posts table

Revision ID: 153b980cc60c
Revises: c7fa7ad46e10
Create Date: 2023-05-19 15:46:24.174914

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "153b980cc60c"
down_revision = "c7fa7ad46e10"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id", sa.Integer(), nullable=False))
    op.create_foreign_key(
        "post_users_fk",
        source_table="posts",
        referent_table="users",
        local_cols=["owner_id"],
        remote_cols=["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint("post_users_fk", table_name="posts")
    op.drop_column("posts", "owner_id")
