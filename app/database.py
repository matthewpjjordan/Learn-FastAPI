from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from time import sleep
import psycopg2
import os
from .config import settings

POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_DB = settings.POSTGRES_DB
POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD

sqlalchemy_database_url = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

engine = create_engine(sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# reference for using psycopg2 driver instead of sqlalchemy
# while True:
#     try:
#         conn = psycopg2.connect(
#             host=os.getenv("POSTGRES_HOST"),
#             database=os.getenv("POSTGRES_DB"),
#             user=os.getenv("POSTGRES_USER"),
#             password=os.getenv("POSTGRES_PASSWORD"),
#             cursor_factory=RealDictCursor,
#         )
#         cursor = conn.cursor()
#         print("Database connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to database failed.")
#         print(f"Error: {error}")
#         sleep(2)
