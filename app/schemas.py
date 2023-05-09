from pydantic import BaseModel, EmailStr
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class PostDelete(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime

    # Pydantic works with dicts. Data returned by ORM query is a sqlalchemy model.
    # Below has Pydantic read data even if its not a dict, but an ORM model.
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
