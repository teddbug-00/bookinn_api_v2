from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.db import get_db
from src.schemas.user_profile import UserProfile
from .handlers.user_profile import get_profile
from ...core.security import get_current_user_id

user_profile_router = APIRouter()

@user_profile_router.get("/profile", response_model=UserProfile)
async def get_user_profile(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserProfile:
    return await get_profile(user_id, db)