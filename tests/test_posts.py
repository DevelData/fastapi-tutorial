from fastapi import status



def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get(url="/posts/")
    #validate = lambda x: schemas.PostOut(**x)
    #posts = list(map(validate, response.json()))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == len(test_posts)