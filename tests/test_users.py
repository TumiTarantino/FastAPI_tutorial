from app.main import app
from fastapi.testclient import TestClient
from app import schemas
import pytest

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



@pytest.fixture
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
@pytest.fixture
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