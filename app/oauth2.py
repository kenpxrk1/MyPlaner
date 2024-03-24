import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app import schemas, database, models

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = os.getenv("SECRET_KEY") 
REFRESH_SECRET_KEY = os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60*24*7  # 7 days

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_refresh_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(datetime.UTC) + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id: str = payload.get("users_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not valid credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user


