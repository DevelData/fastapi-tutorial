from fastapi import status
from jose import jwt
import pytest
from app import schemas
from app.config import settings
from tests.database import client, session


@pytest.fixture
def test_user(client):
    user_data = {
        "email": "john.smith@gmail.com", 
        "password": "password123"
        }
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to my first API"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "email": "hello123@gmail.com",
            "password": "password123"
            })
    new_user = schemas.UserOut(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert new_user.email == "hello123@gmail.com"


def test_login_user(client, test_user):
    response = client.post(
        url="/login",
        data={
            "username": test_user["email"],
            "password": test_user["password"]
            })
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(
        login_response.access_token,
        settings.secret_key,
        algorithms=[settings.algorithm])
    user_id = payload.get("user_id")
    assert response.status_code == status.HTTP_200_OK
    assert user_id == test_user["id"]
    assert login_response.token_type == "bearer"