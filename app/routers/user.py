from .. import models, schemas, utils
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db 

#Throwaway everything you thought you knew, we got routers, baby!
router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session= Depends(get_db)):

    #Hash User's password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())#use post.model_dump after tutorial
 #Um, an exception or something needs to happen if the email is already in use
 #At the moment, an Internal Server Error happens, which is oof
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first() #type: ignore
    # is it possible to differ between a not found and an id not typed?
    if not user:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"user with {id} is not found")
    
    return user
