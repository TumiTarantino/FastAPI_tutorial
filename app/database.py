#These are the recommended imports that the current FastAPI Documentation reccommends,but...
#from typing import Annotated
#from fastapi import Depends, FastAPI, HTTPException, Query
#from sqlmodel import Field, Session, SQLModel, create_engine, select

#Psycorg2stuff
#import psycopg2 # Database Driver
#from psycopg2.extras import RealDictCursor
#import time

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
"""
#----------------DATABASE STUFF(Deprecated)---------------------------------------------------
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
"""