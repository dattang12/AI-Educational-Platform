from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.database import SessionLocal
from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.schemas import UserCreate
from app.core.config import settings


# OAuth2 token URL (will match route in auth.py)
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Use bcrypt to hash passwords + Handle upgrades automatically in the future
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Password helpers ----------

def get_password_hash(password: str) -> str:
    password = password[:72]
    return password_context.hash(password)

def verify_password(plain_password: str, hash_password: str) -> bool:
    plain_password = plain_password[:72]
    return password_context.verify(plain_password, hash_password)

# ---------- DB session helper ----------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- User helpers ----------

def get_user_by_email(db: Session, email: str) -> str:
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> str:
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, user_in: UserCreate) -> User:
    hashed_pw  = get_password_hash(user_in.password)

    db_user = User (
        email = user_in.email,
        username = user_in.username,
        hashed_password = hashed_pw
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


# ---------- JWT helpers ----------

""" creates a JWT token for your user after they log in.
take user data
set expiration time
add expiration to payload
signs in using secret key
return jwt token string
"""
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # default set in config
    
    # jwt must come with expire time
    to_encode.update({"exp" : expire})

    encode_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return encode_jwt # send this long token to frontend

# ---------- Dependency: current user ----------

from fastapi import Depends, HTTPException, status
"""
Read the JWT token from the request

Decode the token and get the user's email

Find that user in the database and return it

"""
async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)) -> User:
    
    credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        ) 
        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        
        token_data = token_data(email=email)
    
    except JWTError:
        raise credentials_exception
    
    user = get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user






