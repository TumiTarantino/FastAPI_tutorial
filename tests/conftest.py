from app.main import app
from fastapi.testclient import TestClient

import pytest

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine) #type: ignore
    Base.metadata.create_all(bind=engine) #type: ignore
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

#The yield is important, diff between yield and return? Idk
#The session function will always run first since it is an arg in client
@pytest.fixture()
def client(session):
    #run our code before we run our test
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    #Runs our test, kinda
    yield TestClient(app)
    #run our code after the test finishes

@pytest.fixture
def test_user(client):
    user_data = {"email": "tomy@gmail.com", "password" : "Password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user