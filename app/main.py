# uvicorn app.main:app --reload

from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from time import sleep
from dotenv import load_dotenv
from . import models
from .routers import post, user
from .database import engine
import psycopg2
import os

models.Base.metadata.create_all(bind=engine)

load_dotenv()

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            database=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed.")
        print(f"Error: {error}")
        sleep(2)

# Request will enter post file and check each route in turn.
app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "That's better"}
