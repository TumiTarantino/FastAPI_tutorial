from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#the randrange is cause we have no database and have to assign an id
#from random import randrange --goodtimes
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings


#Creates tables base on defined schema in models at the start of the application
#If tables exist, no changes will be checked
# Commented out as is deprecated, alembic will handle stuff now 
#models.Base.metadata.create_all(bind=engine)  # type: ignore

#Global variables
app = FastAPI()

#Not recommended, but free plan is limiting
#----------------------Start
import subprocess
import os

app = FastAPI()

@app.on_event("startup")
def run_migrations():
    subprocess.run(["alembic", "upgrade", "head"], check=True)

#----------------------END

#Allows domains to get access to API via CORS
origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#App routers
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Kea is not dumb, maybe?"}



