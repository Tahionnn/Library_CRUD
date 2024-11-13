from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from enum import Enum


class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    publication: int
    status: bool = Field(default=True)
    user_id: Optional[int] = 'null' 


class UserRole(Enum):
    user = 'user'
    admin = 'admin'

class UserRegister(BaseModel):
    id: int
    username: str = Field(..., min_length=1, max_length=50)
    email: EmailStr = Field(...)
    password: str 
    role: UserRole


