from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(
    prefix="/login",
    tags=['Authentication']
)

@router.post("/", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    #Notes on this function:
    #if the hashed_password parameter is not a hash, there will be a internal server error,
    #I did find the issue, but it wasn't easily found out
    #After adding OA2PassRequestForm, when using Postman, the login args are on longer expected in raw(body),
    #but in the form-data(body), idk why.
    #End of notes-----------
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() #type: ignore

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invaild Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invaild Credentials")
    #TODO: Create JWT Token, return token
    access_token = oauth2.create_access_token(data= {"user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}