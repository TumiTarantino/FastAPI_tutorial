from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    #Notes on this function:
    #if the hashed_password parameter is not a hash, there will be a internal server error,
    #I did find the issue, but it wasn't easily found out
    #End of notes-----------
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first() #type: ignore

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invaild Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invaild Credentials")
    #TODO: Create JWT Token, return token
    return {"Login Detail": "Success"}