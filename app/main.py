from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.schemas import Book, User
from app.database import new_session
from app.models import BookPublic, UserRegister
from app.auth import *
from sqlalchemy import select, delete, update, insert
from datetime import datetime, timedelta, timezone

app = FastAPI()


@app.post("/add/{book_id}")
async def add_book(book_id: int, book: BookPublic, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        data = book.model_dump()
        new_book = Book(**data)
        session.add(new_book)
        await session.flush()
        await session.commit()
        return {'message': f'add book with id={new_book.id} at {new_book.created_at}'}
    

@app.get("/book/{book_id}") #, response_model=BookPublic
async def get_book_by_id(book_id: int):
    async with new_session() as session:
        query = select(Book).where(Book.id == book_id)
        result = await session.execute(query)
        result = result.scalars().all()
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="No matches found")
    return result


@app.delete("/delete/{book_id}")
async def delete_book_by_id(book_id: int, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        delete_query = delete(Book).where(Book.id == book_id)
        await session.execute(delete_query)
        await session.flush()
        await session.commit()
    return {'message': f'delete book with id={book_id}'}


@app.put("/update/{book_id}")
async def update_book_by_id(book_id: int, book: BookPublic, current_user: Annotated[User, Depends(get_current_admin_user)]):
    async with new_session() as session:
        data = book.model_dump()
        update_query = update(Book).where(Book.id == book_id).values(**data)
        await session.execute(update_query)
        await session.flush()
        await session.commit()
    return {'message': f'update book with id={book_id}'}


@app.post("/register/")
async def register_user(user_data: UserRegister):
    async with new_session() as session:
        result_user = await session.execute(select(User).where(User.email == user_data.email))
        user = result_user.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='A user with email address={user_data.email} already exists.'
        )
    user_dict = user_data.model_dump()
    user_dict['password']  = get_password_hash(user_data.password)
    new_user = User(**user_dict)
    session.add(new_user)
    await session.flush()
    await session.commit()
    return {'message': f'{user_data.username} has been  registered'}


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = await authenticate_user(username_or_email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}, 
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=UserRegister)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user


@app.put("/take/{book_id}")
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
