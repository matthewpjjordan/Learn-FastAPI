import pytest
from app import schemas
from .database import client, session


@pytest.fixture()
def create_test_user(client):
    user_data = {"email": "hello3@gmail.com", "password": "supersafestring"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


def test_root(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "That's better"}
    print(res.json())


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "hello3@gmail.com", "password": "supersafestring"}
    )
    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "hello3@gmail.com"


def test_login_user(client, create_test_user):
    res = client.post(
        "/login",
        data={
            "username": create_test_user["email"],
            "password": create_test_user["password"],
        },
    )
    assert res.status_code == 200
