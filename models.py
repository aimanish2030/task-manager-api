from pydantic import BaseModel, EmailStr
from typing import Optional


# ── Task Models ──────────────────────────
class Task(BaseModel):
    title: str
    description: Optional[str] = ""
    completed: bool = False


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


# ── User Models ──────────────────────────
class UserRegister(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"