"""auto-vote

Revision ID: a0c2e7dfeed8
Revises: 33a4c348e9c8
Create Date: 2023-05-21 16:59:56.185401

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "a0c2e7dfeed8"
down_revision = "33a4c348e9c8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "votes",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("post_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["post_id"], ["posts.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "post_id"),
    )
    op.add_column("posts", sa.Column("user_id", sa.Integer(), nullable=False))
    op.drop_constraint("post_users_fk", "posts", type_="foreignkey")
    op.create_foreign_key(
        None, "posts", "users", ["user_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("posts", "owner_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "posts",
        sa.Column("owner_id", sa.INTEGER(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "posts", type_="foreignkey")
    op.create_foreign_key(
        "post_users_fk", "posts", "users", ["owner_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_column("posts", "user_id")
    op.drop_table("votes")
    # ### end Alembic commands ###