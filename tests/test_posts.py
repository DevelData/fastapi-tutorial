from fastapi import status



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