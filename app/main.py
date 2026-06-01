from fastapi import FastAPI

from app.oauth2 import SECRET_KEY
#the randrange is cause we have no database and have to assign an id
#from random import randrange --goodtimes
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#Creates tables base on defined schema in models
models.Base.metadata.create_all(bind=engine)  # type: ignore

#Global variables
app = FastAPI()

#App routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Hello World"}



