from jose import JWTError, jwt
from datetime import datetime, timedelta
#Check FASTAPI documentation if you want more details

#We need 3 things: SECRET_KEY, Algorithm, Expiration Time

#Use 'openssl rand -hex 32' to get string for secret key
SECRET_KEY = "e848dee6a666d02df92d8fc618d3d9b10b6ee9af23e6ba131adaf73abbcedc27"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY ,algorithm=ALGORITHM)
    
    return encoded_jwt