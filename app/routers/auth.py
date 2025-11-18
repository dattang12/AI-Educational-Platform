from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.services.auth_service import (
    get_db,
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from app.models.schemas import UserCreate, UserOut, Token
from app.core.config import settings
from app.models.user_model import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing_account = db.query(User).filter(
        (User.email == user_in.email) | (User.username == user_in.username)
    ).first()

    if existing_account:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or Username are already registered"
        )
    
    user = create_user(db, user_in)
    return user

@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)):

    user = authenticate_user(db, email=form_data.username, password=form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or Password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        data = {"sub" : user.email}, 
        expires_delta= expire
    )

    return Token(access_token=token)

@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

