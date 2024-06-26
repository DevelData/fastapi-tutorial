from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from app import models
from app.config import settings
from app.database import get_db, Base
from app.main import app
from app.oauth2 import create_access_token


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.test_database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


@pytest.fixture(scope="session")
def database():
    if not database_exists(engine.url):
        create_database(engine.url)
    
    yield None

    drop_database(engine.url)

@pytest.fixture(scope="function")
def session(database):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


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


@pytest.fixture
def test_user2(client):
    user_data = {
        "email": "blanket@rmail.com", 
        "password": "password1234"
        }
    res = client.post("/users/", json=user_data)

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
        }
    
    return client


@pytest.fixture
def test_posts(session, test_user, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id'],
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "User 2 post",
        "content": "My content",
        "owner_id": test_user2['id']
    }]

    create_post_model = lambda x: models.Post(**x)
    posts = list(map(create_post_model, posts_data))
    session.add_all(posts)
    session.commit()
    db_posts = session.query(models.Post).all()

    return db_posts