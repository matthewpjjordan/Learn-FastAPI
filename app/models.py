from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, Time, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship


# sqlalchemy only performs these actions if the table does not exist.
# It will not detect differences in setup and update the database.
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    # Foreign key uses 'users' table name
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # ORM relationship uses 'User' class name
    # SQLAlchemy automatically forms the relationship between current and
    # provided tables.
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"

    # user_id = relationship("User")
    # post_id = relationship("Post")

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey("posts.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
