from sys import int_info

from pydantic import BaseModel, EmailStr
from datetime import datetime

#Defines how a post should look
#Makes sure the value is a str and makes sure that title and content are explicitly used
#FastAPI is noice
#Schema/Pydantic models define the structure of a request and response
#This class extends Pydantic's BaseModel and will thus be a Pydantic Model for the request

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
#Taking advantage of inheritance, to have different PostCRUD models
class PostCreate(PostBase):
    pass

#Response Schema
class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

#Schema when a user is created
class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Reponse Schema for users
class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

