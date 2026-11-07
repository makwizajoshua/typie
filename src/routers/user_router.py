from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db import get_db
from src.models.user_model import User
from src.schemas.user_schema import UserResponse

router = APIRouter(prefix="/user")


@router.get("/user/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    result = db.execute(select(User).where(User.id == user_id))
    if not result.scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    response = UserResponse(username=result.scalar().username, email=result.scalar().email)  # type: ignore

    return response
