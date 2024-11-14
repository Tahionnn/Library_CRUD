from pydantic import BaseModel, Field
from typing import Optional

class BookPublic(BaseModel):
    title: str
    author: str
    publication: int
    status: bool = Field(default=True)
    user_id: Optional[int] = 'null' 