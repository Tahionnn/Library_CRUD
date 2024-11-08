from pydantic import BaseModel, Field
from enum import Enum


class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    publication: int
    status: bool = Field(default=True)


class UserRole(Enum):
    user = 'user'
    admin = 'admin'
