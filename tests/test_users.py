from fastapi import status
from jose import jwt
import pytest
from app import schemas
from app.config import settings


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


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', status.HTTP_403_FORBIDDEN),
    ('john.smith@gmail.com', 'wrongpassword', status.HTTP_403_FORBIDDEN),
    ('wrongemail@gmail.com', 'wrongpassword', status.HTTP_403_FORBIDDEN),
    (None, 'password123', status.HTTP_422_UNPROCESSABLE_ENTITY),
    ('john.smith@gmail.com', None, status.HTTP_422_UNPROCESSABLE_ENTITY)
])
def test_incorrect_login(client, email, password, status_code):
    response = client.post(
        url="/login",
        data={
            "username":email,
            "password": password
            })
    assert response.status_code == status_code
    #assert response.json().get("detail") == "Invalid credentials"