from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.user.models import User
from app.book.models import Book, TakenBook
from app.database import new_session
from app.user.schemas import UserRegister
from app.auth.router import *
from sqlalchemy import select, delete, update, join
from datetime import datetime, timedelta, timezone


user_router = APIRouter(prefix='/user', tags=['Users methods'])


@user_router.get("/users/me/", response_model=UserRegister)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@user_router.delete("/delete/{user_id}")
async def delete_user_by_id(user_id: int, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        delete_query = delete(User).where(User.id == user_id, User.role != "admin")
        await session.execute(delete_query)
        await session.flush()
        await session.commit()
    return {'message': f'delete user with id={user_id}'}


@user_router.get("/get/books_list")
async def get_books_list(user: Annotated[User, Depends(get_current_user)]):
    async with new_session() as session:
        query = (
            select(
                Book.id.label("id"),
                Book.title.label("title"),
                Book.author.label("author"),
                TakenBook.taken_at.label("taken_at"),
                TakenBook.return_date.label("return_date")
            )
            .join(TakenBook, Book.id == TakenBook.book_id)
            .where(TakenBook.user_id == user.id)
        )
        result = await session.execute(query)
        result = result.all()
        if not result:
            raise HTTPException(status_code=404, detail="No matches found")
        return [
            {
                "book_id": result.id,
                "book_title": result.title,
                "book_author": result.author,
                "borrowed_at": result.taken_at,
                "returned_at": result.return_date
            }
            for result in result
        ]     