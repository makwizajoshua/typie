import os
from datetime import UTC, datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models.user import User

load_dotenv()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


### Authentication utility functions ###
def make_token(user_id: int) -> str:
    """
    Returns a JWT based on the TOKEN HOURS (how long JWT remain valid in hours) environment variable, SECRET_KEY (another environment variable) user id passed as an argument.
    Generated using the HS256 algorithm.

    Args:
        user_id (int): ID number of the user.
    """
    TOKEN_HOURS = int(os.environ["TOKEN_HOURS"])
    SECRET_KEY = os.environ["SECRET_KEY"]
    expires = datetime.now(UTC) + timedelta(hours=TOKEN_HOURS)
    return jwt.encode(
        {"sub": str(user_id), "exp": expires}, SECRET_KEY, algorithm="HS256"
    )


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    """
    Returns the current user based on the JWT provided form the database.
    Use as a dependency that requires a logged-in the user
    Args:
        token (str): _description_
        db (Session): _description_
    """
    SECRET_KEY = os.environ["SECRET_KEY"]
    try:
        payload = jwt.decode(token, SECRET_KEY, "HS256")
        user = db.get(User, payload["sub"])
    except (jwt.PyJWTError, ValueError, KeyError):
        user = None
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Invalid or expired token submitted."
        )
    return user
