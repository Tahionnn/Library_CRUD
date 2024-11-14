from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import Depends
from typing import Annotated
from app.book.models import Book, TakenBook
from app.user.models import User
from app.database import new_session
from app.book.router import return_book_by_id
from app.auth.utils import get_current_user
from sqlalchemy import select, delete, update, insert
from datetime import datetime


scheduler = AsyncIOScheduler()


async def forced_return():
    async with new_session() as session:
        query = (
            select(
                Book.id.label("id"),
                TakenBook.user_id.label("user_id"),
                TakenBook.taken_at.label("taken_at"),
                TakenBook.return_date.label("return_date")
            )
            .join(TakenBook, Book.id == TakenBook.book_id)
            .where(TakenBook.return_date <= datetime.utcnow())
        )
        check = await session.execute(query)
        check = check.all()
        for rec in check:
            taken_at = rec[2]  
            return_date = rec[3]  
            book_id = rec[0]  
            update_book = update(Book).where(Book.id == book_id).values({"status": True, "user_id": None})
            await session.execute(update_book)
            await session.flush()
                
            delete_query = delete(TakenBook).where(TakenBook.book_id == book_id)
            await session.execute(delete_query)
            await session.flush()
                
            await session.commit()
