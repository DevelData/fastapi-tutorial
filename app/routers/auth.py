from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, utils
from app.database import get_db
from app.oauth2 import create_access_token
from app.schemas import Token


router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def login(
    user_credentials:OAuth2PasswordRequestForm=Depends(),
    db:Session=Depends(get_db)
    ):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
        ).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
            )
    
    if not utils.verify(user_credentials.password, user.password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials"
            )
    
    access_token = create_access_token(data={"user_id": user.id})
    return {
        "access_token": access_token,
        "token_type": "bearer"
        }