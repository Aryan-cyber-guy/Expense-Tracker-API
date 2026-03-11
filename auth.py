from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from db_models import Db_Users
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

# load secrets from .env; SECRET_KEY must be set for JWT to work
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

# JWT settings
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTE = 60

# password hashing/verification context (bcrypt)
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
# dependency to extract bearer token from authorization header
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="user/auth/login")

def hash_password(password: str):
    """Return a bcrypt hash of the supplied plain password."""
    return pwd.hash(password)


def verify_password(plain_password: str, hash_password: str):
    """Compare a plaintext password against a stored hash."""
    return pwd.verify(plain_password, hash_password)


def create_access_token(data: dict):
    """Generate a short‑lived JWT from the provided payload.

    The payload should be a dictionary; the "sub" key is expected to contain
    the user id. An expiration claim is added automatically.
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth_2_scheme), db: Session = Depends(get_db)):
    """Dependency that returns the authenticated user object.

    The function decodes the bearer token, verifies it, and loads the user
    record from the database. HTTP 401 is raised for any problem.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid Token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")

    user = db.query(Db_Users).filter(Db_Users.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid User ID")
    return user