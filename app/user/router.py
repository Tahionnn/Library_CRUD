from fastapi import FastAPI, HTTPException, status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from app.user.models import User
from app.database import new_session
from app.user.schemas import UserRegister
from app.auth.router import *
from sqlalchemy import select, delete, update
from datetime import datetime, timedelta, timezone


user_router = APIRouter(prefix='/user', tags=['Users methods'])


@user_router.get("/users/me/", response_model=UserRegister)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user