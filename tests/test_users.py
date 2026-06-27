from app.main import app
from fastapi.testclient import TestClient
from app import schemas

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.database import get_db, Base

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine) #type: ignore

#dependancy, import to main.py
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)
# Just read fastapi if you want to know how this happened
def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "buddy"}

#For now issue exists as if user already exists, you can't create the same user
def test_create_user():
    response = client.post("/users/", json={"email": "timmy@gmail.com", "password" : "Password123"})
    new_user = schemas.UserOut(**response.json())
    assert new_user.email == "timmy@gmail.com"
    assert response.status_code == 201