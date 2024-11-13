from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.book.models import Book
else:
    Book = "Book"


from app.database import Base
from app.user.schemas import UserRole
#from app.book.models import Book
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