from typing import Optional

from fastapi import FastAPI
#from fastapi.params import Body : works fine, but My Vscode is not happy
from pydantic import BaseModel
#the randrange is cause we have no database and have to assign an id
from random import randrange
#Global variables
app = FastAPI()
#No database for now, luckily RAM exists
my_posts = [{"title":"Somerandom Title", "content":"This post is not random", "id": 1}, 
            {"title":"Not Random Title", "content":"This random is a post", "id": 2}]

#temp functions
def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


#defines how a post should look
# Makes sure the value is a str and makes sure that title and content are explicitly used
#FastAPI is noice
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts/{id}")
def get_post(id: int):
    post = find_posts(id) # becomes str so we change to int
    return {"data" : post}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

@app.post("/posts")
def create_post(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,9999)
    my_posts.append(post_dict)
    return {"data": post_dict}
