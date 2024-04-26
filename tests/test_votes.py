from fastapi import status



def test_vote_on_post(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        url="/votes",
        json={"post_id": test_posts[3].id, "dir":1}
        )
    assert response.status_code == status.HTTP_201_CREATED