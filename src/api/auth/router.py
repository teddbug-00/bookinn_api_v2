from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.core.db import get_db
from src.schemas.auth import UserCreate, UserResponse
from .handlers.register import register
auth_router = APIRouter()

@auth_router.post("/auth/register", response_model=UserResponse)
async def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> UserResponse:
    return register(user_data, db)