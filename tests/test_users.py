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


def test_login_user(client, test_user):
    res = client.post(
        "/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"],
        },
    )
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(
        login_res.access_token, settings.SECRET_KEY, [settings.ALGORITHM]
    )
    id = payload.get("user_id")
    assert id == test_user["id"]
    assert res.status_code == 200
    assert login_res.token_type == "bearer"


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "supersafestring", 403),
        ("hello3@gmail.com", "wrongpasswordcase", 403),
        ("wrongemail@gmail.com", "wrongpasswordtoo", 403),
        (None, "password123", 422),
        ("wrongemail@gmail.com", None, 422),
    ],
)
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
