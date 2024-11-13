from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated
from app.book.models import Book
from app.user.models import User
from app.database import new_session
from app.book.schemas import BookPublic
from app.auth.router import *
from sqlalchemy import select, delete, update



book_router = APIRouter(prefix='/books', tags=['Books methods'])


@book_router.post("/add/{book_id}")
async def add_book(book_id: int, book: BookPublic, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        data = book.model_dump()
        new_book = Book(**data)
        session.add(new_book)
        await session.flush()
        await session.commit()
        return {'message': f'add book with id={new_book.id} at {new_book.created_at}'}
    

@book_router.get("/get/{book_id}") #, response_model=BookPublic
async def get_book_by_id(book_id: int):
    async with new_session() as session:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        result = result.scalars().all()
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="No matches found")
    return result


@book_router.delete("/delete/{book_id}")
async def delete_book_by_id(book_id: int, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        delete_query = delete(Book).where(Book.id == book_id)
        await session.execute(delete_query)
        await session.flush()
        await session.commit()
    return {'message': f'delete book with id={book_id}'}


@book_router.put("/update/{book_id}")
async def update_book_by_id(book_id: int, book: BookPublic, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        data = book.model_dump()
        update_query = update(Book).where(Book.id == book_id).values(**data)
        await session.execute(update_query)
        await session.flush()
        await session.commit()
    return {'message': f'update book with id={book_id}'}


@book_router.put("/take/{book_id}")
async def take_book_by_id(book_id: int, user_id: int):
    async with new_session() as session:
        result_book = await session.execute(select(Book).where(Book.id == book_id))
        result_user = await session.execute(select(User).where(User.id == user_id))
        book = result_book.scalar_one_or_none() 
        user = result_user.scalar_one_or_none() 
        
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        if book.status:
            update_book = (
                update(Book)
                .where(Book.id == book_id)
                .values(
                    {
                        "user_id": user_id,
                        "status": False,
                    }
                )
            )
            await session.execute(update_book)
            await session.flush()
            
            await session.commit()
        else:
            raise HTTPException(status_code=400, detail="Book is already taken")
    
    return {'message': f'{user_id} took a book with id={book_id}'}