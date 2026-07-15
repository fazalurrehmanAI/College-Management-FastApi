# ============================================
#  auth_utils.py
#  Two separate jobs live here:
#
#  1) PASSWORD HASHING
#     Turn a plain password into a one-way bcrypt
#     hash for storage, and check a plain password
#     against a stored hash at login time.
#
#  2) JWT TOKENS
#     After a successful login, issue a signed
#     token the frontend stores and sends back on
#     every future request, instead of resending
#     the username/password each time.
# ============================================

import os
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
from dotenv import load_dotenv
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from . import model

load_dotenv()

# --------------------------------------------
# Secret key used to SIGN tokens. Anyone with
# this key could forge valid tokens, so it must
# stay in .env and never be committed to git.
# --------------------------------------------
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-your-env-file")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # tokens are valid for 1 hour


def hash_password(plain_password: str) -> str:
    """
    Turn 'mypassword123' into a bcrypt hash like '$2b$12$...'.
    Uses the bcrypt library directly (not passlib) — passlib's
    bcrypt backend is unmaintained and breaks on bcrypt>=4.1.
    bcrypt only hashes the first 72 bytes of input, so we
    truncate first to avoid a ValueError on long passwords.
    """
    password_bytes = plain_password.encode("utf-8")[:72]
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check a login attempt's password against the stored hash."""
    try:
        password_bytes = plain_password.encode("utf-8")[:72]
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except (TypeError, ValueError):
        return False


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Build a signed JWT.
    'data' usually looks like {"sub": "the_username"}.
    'sub' (subject) is the standard JWT field for "who this token belongs to".
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# --------------------------------------------
# This tells FastAPI: "expect a Bearer token in
# the Authorization header". tokenUrl is only
# used to generate the /docs 'Authorize' button.
# --------------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> model.User:
    """
    A reusable dependency. Any route that adds
    'current_user: model.User = Depends(get_current_user)'
    as a parameter becomes a PROTECTED route —
    FastAPI runs this first, and rejects the
    request with 401 before your route body ever runs
    if the token is missing, expired, or invalid.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(model.User).filter(model.User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
