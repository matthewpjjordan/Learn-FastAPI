import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.database import Base


POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_DB = settings.POSTGRES_DB
POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD

sqlalchemy_database_url = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/FastAPI_pytest"
)

engine = create_engine(sqlalchemy_database_url)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Establishes a DB session to query the DB.
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)  # drop tables
    Base.metadata.create_all(bind=engine)  # create tables
    db = TestingSessionLocal()  #
    try:
        yield db
    finally:
        db.close()


# Establishes a client that allows us to make API requests like in Postman but programatically.
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture()
def create_test_user(client):
    user_data = {"email": "hello3@gmail.com", "password": "supersafestring"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user
