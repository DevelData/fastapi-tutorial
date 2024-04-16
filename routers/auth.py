from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import models, utils
from app.database import engine, get_db
from app.schemas import UserLogin


router = APIRouter(tags=["Authentication"])


@router.get("/login")
def login(
    user_credentials:UserLogin,
    db:Session=Depends(get_db)
    ):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
            )
    
    if not utils.verify(user_credentials.password, user.password): # type: ignore
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials"
            )
    
    # create a JWT token
    # return the JWT token
    return {"token": "example token"}