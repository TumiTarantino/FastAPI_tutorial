from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

#The Login is from your login route in auth.py
oath2_scheme = OAuth2PasswordBearer(tokenUrl='login')
#Check FASTAPI documentation if you want more details

#We need 3 things: SECRET_KEY, Algorithm, Expiration Time

#Use 'openssl rand -hex 32' to get string for secret key, later will become environment variable
SECRET_KEY = "e848dee6a666d02df92d8fc618d3d9b10b6ee9af23e6ba131adaf73abbcedc27"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    #utcnow is deprecated...
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY ,algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        #id: str = payload.get("user_id") #type: ignore tutorial version
        id = payload.get("user_id") #type: ignore

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id) 
    except JWTError:
        raise credentials_exception

    return token_data
    
def get_current_user(token: str = Depends(oath2_scheme), db: Session = Depends(database.get_db)):
    #don't ask me about this function, i am confused too
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",
                                          headers={"WWW-Authenticate":"Bearer"})
    
    token = verify_access_token(token, credentials_exception) #type: ignore

    user = db.query(models.User).filter(models.User.id == token.id).first() #type: ignore
    return user
