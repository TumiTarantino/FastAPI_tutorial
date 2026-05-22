from psycopg import Timestamp
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base

#This class is not the Pydantic model
#It is the sqlalchemy model and defines how a table looks like
#This one creates the columns and is for querying, creating, updating and deleting entries within the database
#BTW, when editing these tables, sqlalchemy doesn't check if the columns have been edited,
#rather it checks whether the table exists, and if it does, then it does nothing else.
#In order words, if the table exists, it won't be edited, if it doesn't exist, it will be created with how it's currently declared.
class Post(Base): #Extends the Base declared in the database file.
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),nullable=False)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()')) 
    