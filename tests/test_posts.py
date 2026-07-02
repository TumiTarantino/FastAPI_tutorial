from app import schemas

#test_posts fixture uses test_user as an arg, so all test_posts already have a user
def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    def validate(post):
        return schemas.PostOut(**post)
    
    #hm idk what this does?
    posts_map = map(validate, response.json())

    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401

def test_get_one_non_existing_post(authorized_client, test_posts):
    response = authorized_client.get("/posts/67677997")
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(response.json())
    post = schemas.PostOut(**response.json())
    assert response.status_code == 200
    assert post.post.id == test_posts[0].id
    assert post.post.content == test_posts[0].content