from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.auth import UserCreate, UserResponse, LoginResponse, LoginRequest
from .handlers.register import register
from .handlers.login import login, login_for_swagger


auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return await register(user_data, db)


@auth_router.post("/login", response_model=LoginResponse)
async def login_user(user_credentials: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    return await login(user_credentials, db)


@auth_router.post("/token", response_model=LoginResponse)
async def login_for_swagger_ui(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Any:
    return await login_for_swagger(form_data, db)


@auth_router.post("/logout")
async def logout():
    # TODO: Complete this later
    pass


