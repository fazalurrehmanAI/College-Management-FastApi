# ============================================
#  routers/auth.py
#  Registration + login.
#  Registered in main.py with prefix /auth
# ============================================
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schema, model
from ..database import get_db
from ..auth_utils import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post("/register", response_model=schema.UserResponse, status_code=201)
def register(user: schema.UserCreate, db: Session = Depends(get_db)):
    """
    Create a new login account.
    1. Check the username isn't already taken.
    2. Hash the password — the plain password is
       never written to the database.
    3. Save the User row and return it (schema.UserResponse
       has no password field, so none leaks back).
    """
    existing = db.query(model.User).filter(model.User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")

    db_user = model.User(
        username=user.username,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=schema.Token)
def login(credentials: schema.UserLogin, db: Session = Depends(get_db)):
    """
    Check username + password, and if correct,
    issue a signed JWT the frontend will store
    and attach to every future request.
    """
    user = db.query(model.User).filter(model.User.username == credentials.username).first()

    # Deliberately the SAME error whether the username doesn't exist
    # or the password is wrong — never reveal which one was incorrect.
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schema.UserResponse)
def read_current_user(current_user: model.User = Depends(get_current_user)):
    """
    A protected route — Depends(get_current_user) means
    this only runs if a valid token was sent. The frontend
    calls this on page load to check "is my saved token
    still valid?" before showing the app.
    """
    return current_user
