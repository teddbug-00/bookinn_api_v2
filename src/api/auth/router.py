from typing import Dict, Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.auth import UserCreate, UserResponse, LoginResponse, LoginRequest
from .handlers.register import register
from .handlers.login import login


auth_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return await register(user_data, db)


@auth_router.post("/login")
async def login_user(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    return await login(user_credentials, db)
