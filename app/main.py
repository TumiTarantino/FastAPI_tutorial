from fastapi import FastAPI, HTTPException, Response, status, Depends
from typing import List
#from fastapi.params import Body : works fine, but My Vscode is not happy
from pydantic import BaseModel
#the randrange is cause we have no database and have to assign an id
from random import randrange
import time
import psycopg2 # Database Driver
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .database import engine, get_db
#And this is when it all changed...
from .routers import post, user, auth


#Creates tables base on defined schema in models
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



#App routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}



