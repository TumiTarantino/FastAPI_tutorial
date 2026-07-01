from app import schemas
from jose import jwt 
from app.config import settings
import pytest
#Fixtures are in the conftest file, somehow are already across any test files
# Just read fastapi if you want to know how this happened
def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "buddy"}

#For now issue exists as if user already exists, you can't create the same user
#"/users/" and "/users" are not the same
def test_create_user(client):
    response = client.post("/users/", json={"email": "timmy@gmail.com", "password" : "Password123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "timmy@gmail.com"
    assert response.status_code == 201


def test_login_user(client, test_user):           #not json as in postman its form data
    response = client.post("/login/", data={"username": test_user['email'], "password" : test_user['password']})

    login_res = schemas.Token(**response.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == 'bearer'
    assert response.status_code == 200

@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'Password123', 403),
    ('timmy@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'Password123', 422),
    ('timmy@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    response = client.post("/login/", data={"username": email, "password": password})
    assert response.status_code == status_code
    #This route only tests passwords but should be fine for tutorial
    #assert response.json().get('detail') == "Invaild Credentials"