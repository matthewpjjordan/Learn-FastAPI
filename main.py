from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def root():
    return {"message": "That's better"}

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

@app.get("/posts")
def get_posts():
    return {"data": "These are your posts"}

@app.post("/createposts")
def create_posts(post: Post):
    print(post.dict())
    return {"data": post}