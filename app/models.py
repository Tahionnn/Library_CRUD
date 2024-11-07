from pydantic import BaseModel, Field


class BookPublic(BaseModel):
    id: int
    title: str
    author: str
    publication: int
    status: str = Field(default='free')