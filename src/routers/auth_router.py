from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user_model import User
from src.schemas.user_schema import UserCreate, UserLogin, UserResponse

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserResponse)
def reigster_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User).where(User.username == user.username))
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )

    result = db.execute(select(User).where(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")

    new_user = User(username=user.username, email=user.email)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # TODO: Implement JWT auth part here


@router.post("/login", response_model=UserResponse)
def login_user(user: UserLogin, db: Annotated[Session, Depends(get_db)]):
    check_user_result = db.execute(select(User).where(User.username == user.username))
    if not check_user_result.scalar():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Username not found in database"
        )

    check_user_result = db.execute(select(User).where(User.email == user.email))
    if not check_user_result.scalar():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Email not found in database"
        )

    # TODO: Implement JWT auth part here once password hashing is implemented, also check if the password is correct
