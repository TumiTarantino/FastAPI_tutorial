def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get("/posts/")
    print(response.json())
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200