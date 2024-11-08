from app.database import Base
from app.models import UserRole
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM 


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[int]
    role: Mapped[UserRole] = mapped_column(ENUM(UserRole, create_type=False))
    books: Mapped[List["Book"]] = relationship()


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]
    publication: Mapped[int]
    status: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
