"""Auth flow:
1. POST /auth/register  -> create a user (password is stored hashed)
2. POST /auth/login     -> check password, get back a JWT token
3. GET  /auth/me        -> send the token in the "Authorization: Bearer <token>"
                           header; the server tells you who you are
"""

import bcrypt
from backend.app.schemas.auth_credentials import AuthenticatedUser, Credentials
from backend.app.util import get_current_user, make_token
from db import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.user import User
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter(prefix="auth", tags=["auth"])


@router.post("/register", response_model=AuthenticatedUser, status_code=status.HTTP_201_CREATED)
def register(body: Credentials, db: Session = Depends(get_db)):
    if db.scalar(select(User).where(User.username == body.username)):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already taken")
    hashed = bcrypt.hashpw(body.password.encode(), bcrypt.gensalt()).decode()
    user = User(username=body.username, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    user = db.scalar(select(User).where(User.username == body.username))
    if not user:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unexpectec server error")
    return {"access_token": make_token(user.id), "token_type": "bearer"}


@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == form.username))
    if not user or not bcrypt.checkpw(form.password.encode(), user.password_hash.encode()):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Username or password incorrect")
    return {"access_token": make_token(user.id), "token_type": "bearer"}


@router.get("/me", response_model=AuthenticatedUser)
def me(user: User = Depends(get_current_user)):
    return user
