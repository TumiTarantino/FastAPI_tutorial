from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status
#from fastapi.params import Body : works fine, but My Vscode is not happy
from pydantic import BaseModel
#the randrange is cause we have no database and have to assign an id
from random import randrange
import time

import psycopg2 # Database Driver
from psycopg2.extras import RealDictCursor
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
        
#----------------DATABASE STUFF---------------------------------------------------
while True:#Tries untils connection is successful then breaks out of loop
    try:
        # stuff is hardcoded which is eww, will change later since we dk how yet, ooof,
        conn = psycopg2.connect(host = 'localhost', database='FastAPI', user='postgres', password='tumitino',
                               cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful!")
        break
    except Exception as error:
        print("Connection to database was unsuccessful.")
        print("Error", error) #Prints what was caught
        time.sleep(3)# waits for 3 seconds until restarting loop
    
#----------------DATABASE END-----------------------------------------------------



#defines how a post should look
# Makes sure the value is a str and makes sure that title and content are explicitly used
#FastAPI is noice
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None (Removed was only for testing)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/posts/{id}")
def get_post(id: int,):
    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with {id} is not found")
    return {"data" : post}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data" : posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post):
    #Try to sanitize the statement(NO SQL INJECTION PLZ)
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()#Saves the executed result in a variable, fetchall gets the result of the execute
    conn.commit()# Saves changes to the actual database
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    deleted_post = cursor.fetchone()
    

    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    conn.commit()
    #Apparently if you delete data or 204 is the status code, you don't want to return anything
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, id,))
    updated_post = cursor.fetchone()
    if updated_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    conn.commit()
    return{"data": updated_post}
