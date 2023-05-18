# uvicorn app.main:app --reload

from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .routers import post, user, auth, vote
from .database import engine

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Request will enter post file and check each route in turn.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "That's better"}
