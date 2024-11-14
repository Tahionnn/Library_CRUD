from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum


class UserRole(Enum):
    user = 'user'
    admin = 'admin'

class UserRegister(BaseModel):
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    password: str 
    role: UserRole