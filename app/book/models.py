from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.user.models import User
else:
    User = "User"

from app.database import Base
from typing import List
from sqlalchemy import ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime, timedelta


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]
    publication: Mapped[int]
    status: Mapped[bool] = mapped_column(default=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    user: Mapped["User"] = relationship("User", back_populates="books")


class TakenBook(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), nullable=True)
    taken_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow()) 
    return_date: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.utcnow()+timedelta(days=30)) 