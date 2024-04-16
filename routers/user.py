from fastapi import APIRouter, status, HTTPException, Depends

from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.schemas import UserCreate, UserOut
from app.utils import hash


router = APIRouter()


@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user:UserCreate, db:Session=Depends(get_db)):
    user.password = hash(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{id}", response_model=UserOut)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    print(user)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{id}' could not be found."
            )

    return user