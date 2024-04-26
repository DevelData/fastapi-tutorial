from fastapi import status
import pytest
from app import models


@pytest.fixture
def vote_fixture(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()

    return


def test_vote_on_post(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        url="/votes",
        json={"post_id": test_posts[3].id, "dir":1}
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_vote_twice_post(authorized_client, test_posts, vote_fixture):
    response = authorized_client.post(
        url="/votes",
        json={"post_id": test_posts[3].id, "dir":1}
        )
    assert response.status_code == status.HTTP_409_CONFLICT


def test_delete_vote(authorized_client, test_posts, vote_fixture):
    response = authorized_client.post(
        url="/votes",
        json={"post_id": test_posts[3].id, "dir":0}
        )
    assert response.status_code == status.HTTP_201_CREATED


def test_delete_vote_non_exist(authorized_client, test_posts):
    response = authorized_client.post(
        url="/votes",
        json={"post_id": test_posts[3].id, "dir":0}
        )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    

def test_vote_post_non_exist(authorized_client):
    response = authorized_client.post(
        url="/votes",
        json={"post_id": 999999999, "dir":0}
        )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_vote_unauthorized_user(client, test_posts):
    response = client.post(
        url="/votes",
        json={"post_id": test_posts[3].id, "dir":0}
        )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED