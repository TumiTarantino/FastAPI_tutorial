from app import schemas
from .database import client, session
    

# Just read fastapi if you want to know how this happened
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "buddy"}

#For now issue exists as if user already exists, you can't create the same user
def test_create_user(client):
    response = client.post("/users/", json={"email": "timmy@gmail.com", "password" : "Password123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "timmy@gmail.com"
    assert response.status_code == 201