from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column


class Book(Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    author: Mapped[str]
    publication: Mapped[int]
    status: Mapped[str] = mapped_column(default='free')