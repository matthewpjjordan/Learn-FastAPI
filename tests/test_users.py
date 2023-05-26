import pytest
from app import schemas
from jose import jwt
from app.config import settings


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
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.SECRET_KEY, [settings.ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == create_test_user["id"]
    assert res.status_code == 200
    assert login_res.token_type == "bearer"
