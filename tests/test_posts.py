from fastapi import status


def test_get_all_posts(authorized_client):
    response = authorized_client.get(url="/posts/")
    assert response.status_code == status.HTTP_200_OK