from fastapi import status
from app import schemas
from tests.database import client, session


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