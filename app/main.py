from fastapi import FastAPI, HTTPException
from app.schemas import Book
from app.database import new_session
from app.models import BookPublic
#from sqlalchemy.orm import Session
from sqlalchemy import select, delete, update

app = FastAPI()


@app.post("/add/{book_id}")
async def add_book(book_id: int, book: BookPublic):
    async with new_session() as session:
        data = book.model_dump()
        new_book = Book(**data)
        session.add(new_book)
        await session.flush()
        await session.commit()
        return {'message': f'add book with id={new_book.id} at {new_book.created_at}'}
    

@app.get("/book/{book_id}", response_model=BookPublic)
async def get_book_by_id(book_id: int):
    async with new_session() as session:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        result = result.scalars().all()
        if result is None:
            raise Exception
    return result


@app.delete("/delete/{book_id}")
async def delete_book_by_id(book_id: int):
    async with new_session() as session:
        delete_query = delete(Book).where(Book.id == book_id)
        await session.execute(delete_query)
        await session.flush()
        await session.commit()
    return {'message': f'delete book with id={book_id}'}


@app.put("/update/{book_id}")
async def update_book_by_id(book_id: int, book: BookPublic):
    async with new_session() as session:
        data = book.model_dump()
        update_query = update(Book).where(Book.id == book_id).values(**data)
        await session.execute(update_query)
        await session.flush()
        await session.commit()
    return {'message': f'update book with id={book_id}'}