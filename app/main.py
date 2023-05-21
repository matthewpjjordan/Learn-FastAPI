# uvicorn app.main:app --reload

from fastapi import FastAPI
from dotenv import load_dotenv
from . import models
from .routers import post, user, auth, vote
from .database import engine
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

# Not required once alembic setup
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # e.g. GET, POST etc
    allow_headers=["*"],
)

# Request will enter post file and check each route in turn.
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "That's better"}
