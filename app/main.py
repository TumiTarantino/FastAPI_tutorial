from multiprocessing import synchronize
from typing import Optional

from fastapi import FastAPI, HTTPException, Response, status, Depends
#from fastapi.params import Body : works fine, but My Vscode is not happy
from pydantic import BaseModel
#the randrange is cause we have no database and have to assign an id
from random import randrange
import time

import psycopg2 # Database Driver
from psycopg2.extras import RealDictCursor

from . import models
from sqlalchemy.orm import Session
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)  # type: ignore

#Global variables
app = FastAPI()



        
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
#This class extends Pydantic's BaseModel and will thus be a Pydantic Model
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None (Removed was only for testing)


@app.get("/")
def root():
    return {"message": "Hello World"}

@app.get("/sqll")
def test_sql(db: Session= Depends(get_db)):
    temp = db.query(models.Post).all()
    return {"Status":temp}



@app.get("/posts/{id}")
def get_post(id: int, db: Session= Depends(get_db)):
    #Commented because of ORM, don't delete
    #cursor.execute("""SELECT * FROM posts WHERE id = %s """,(id,))
    #post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first() #type: ignore
    
    if not post:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"post with {id} is not found")
    return {"data" : post}

@app.get("/posts")
def get_posts(db: Session= Depends(get_db)):
    #Commented out since we are using ORMs now, don't delete
    #cursor.execute("""SELECT * FROM posts """)
    #posts = cursor.fetchall()

    #ORMS way
    posts = db.query(models.Post).all()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post:Post,db: Session= Depends(get_db)):
    #Try to sanitize the statement(NO SQL INJECTION PLZ)[Commented out because ORM, don't delete]
    #cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))
    #new_post = cursor.fetchone()#Saves the executed result in a variable, fetchall gets the result of the execute
    #conn.commit()# Saves changes to the actual database

    #ORM way:
    new_post = models.Post(**post.dict())#use post.model_dump after tutorial
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session= Depends(get_db)):
    #Replaced with ORM logic, don't delete
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(id,))
    #deleted_post = cursor.fetchone()
    #conn.commit() (put after the exception check but it commented out now)
    post = db.query(models.Post).filter(models.Post.id == id).first() #type: ignore

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    #post.delete(synchronize_session=False)
    db.delete(post)
    db.commit()
    #Apparently if you delete data or 204 is the status code, you don't want to return anything
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, updated_post: Post,db: Session= Depends(get_db)):
    #Replaced with ORM, don't delete
    #cursor.execute("""UPDATE posts SET title= %s, content= %s, published= %s WHERE id = %s RETURNING * """,
    #              (post.title, post.content, post.published, id,))
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)#type: ignore
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exist"
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    
    return{"data": post_query.first()}
