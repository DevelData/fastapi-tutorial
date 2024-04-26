from fastapi import status
import pytest
from app import schemas



def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get(url="/posts/")
    #validate = lambda x: schemas.PostOut(**x)
    #posts = list(map(validate, response.json()))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client):
    response = client.get("/posts/")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_one_post_not_exist(authorized_client):
    response = authorized_client.get(f"/posts/88888")
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**response.json())
    assert response.status_code == status.HTTP_200_OK
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True)
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post(
        url="/posts/",
        json={
            "title": title,
            "content": content,
            "published": published
            }
        )
    created_post = schemas.Post(**response.json())
    assert response.status_code == status.HTTP_201_CREATED
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]