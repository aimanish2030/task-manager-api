from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from database import user_collection
from models import UserRegister, TokenResponse
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
TOKEN_EXPIRE_HOURS = 24

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token!")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token!")
    user = await user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="User not found!")
    return user


@router.post("/register", status_code=201)
async def register(user: UserRegister):
    existing = await user_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered!")
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hash_password(user.password)
    }
    await user_collection.insert_one(new_user)
    return {"message": f"User '{user.username}' registered successfully!"}


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = await user_collection.find_one({"email": form_data.username})
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found!")
    if not verify_password(form_data.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Wrong password!")
    token = create_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}