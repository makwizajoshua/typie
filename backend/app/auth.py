"""Auth flow:
1. POST /auth/register  -> create a user (password is stored hashed)
2. POST /auth/login     -> check password, get back a JWT token
3. GET  /auth/me        -> send the token in the "Authorization: Bearer <token>"
                           header; the server tells you who you are
"""

import os
from datetime import UTC, datetime, timedelta

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import get_db
from .models import User

SECRET_KEY = os.environ["SECRET_KEY"]
TOKEN_HOURS = os.environ["TOKEN_HOURS"]

router = APIRouter(prefix="/auth", tags=["auth"])
# Tells FastAPI where to find the token (and adds the "Authorize" button in /docs)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


class Credentials(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=72)


class UserOut(BaseModel):
    id: int
    username: str

    model_config = {"from_attributes": True}


def make_token(user_id: int) -> str:
    expires = datetime.now(UTC) + timedelta(hours=TOKEN_HOURS)
    return jwt.encode(
        {"sub": str(user_id), "exp": expires}, SECRET_KEY, algorithm="HS256"
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """Use as a dependency on any route that needs a logged-in user."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = db.get(User, int(payload["sub"]))
    except (jwt.PyJWTError, KeyError, ValueError):
        user = None
    if user is None:
        raise HTTPException(401, "Invalid or expired token")
    return user


@router.post("/register", response_model=UserOut, status_code=201)
def register(body: Credentials, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.username == body.username)):
        raise HTTPException(400, "Username already taken")
    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    user = User(username=body.username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == form.username))
    if not user or not bcrypt.checkpw(
        form.password.encode(), user.password_hash.encode()
    ):
        raise HTTPException(401, "Wrong username or password")
    return {"access_token": make_token(user.id), "token_type": "bearer"}


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
