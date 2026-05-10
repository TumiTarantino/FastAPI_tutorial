from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
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
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i



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
def get_post(id: int,): #response: Response):
    post = find_posts(id)
    if not post:
        #response.status_code = status.HTTP_404_NOT_FOUND/same difference, slightly cleaner
        #return {"message": f"post with {id} is not found"}
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with {id} is not found")
    return {"data" : post}

@app.get("/posts")
def get_posts():
    return {"data" : my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0,9999)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    my_posts.pop(index)
    return {"message": "Post was successfully deleted"}
