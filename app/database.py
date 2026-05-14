#These are the recommended imports that the current FastAPI Documentation reccommends,but...
#from typing import Annotated
#from fastapi import Depends, FastAPI, HTTPException, Query
#from sqlmodel import Field, Session, SQLModel, create_engine, select

#This is what we'll use as we're following the tutorial
from sqlalchemy import create_engine 
#from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker, declarative_base

#This declaration is bad practice, needs environmental variables
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:tumitino@localhost/FastAPI"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

#dependancy, import to main.py
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()