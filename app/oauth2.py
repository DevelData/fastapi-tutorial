import datetime as DT
from datetime import datetime, timedelta
from typing import Dict

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app import models
from app.config import settings
from app.schemas import TokenData
from app.database import get_db


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Not a good idea to store these in the code
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data:Dict):
    to_encode = data.copy()
    expire_time = datetime.now(DT.UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(
        token:str,
        credentials_exception
        ):
    try:
        payload = jwt.decode(
            token=token,
            key=SECRET_KEY,
            algorithms=ALGORITHM
            )
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception
        
        token_data = TokenData(id=id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data


def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:Session=Depends(get_db)
        ):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate:": "Bearer"} # What is this?
        )
    access_token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == access_token.id).first()

    return user