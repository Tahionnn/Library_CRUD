from app.database import Base
from app.models import UserRole
from typing import List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM 


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(ENUM(UserRole, create_type=False))
    books: Mapped[List["Book"]] = relationship("Book", back_populates="user")


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]
    publication: Mapped[int]
    status: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="books")
