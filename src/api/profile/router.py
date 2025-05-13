from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from .handlers.list_user_listings import get_user_listings
from src.core.db import get_db
from src.schemas.user_profile import UserProfile, UserProfileUpdateRequest, UserProfileUpdateResponse
from .handlers.user_profile import get_profile
from .handlers.edit_user_profile import edit_user_profile
from src.core.security import get_current_user_id

user_profile_router = APIRouter()


@user_profile_router.get("/profile", response_model=UserProfile, status_code=status.HTTP_200_OK)
async def get_user_profile(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserProfile:
    return await get_profile(user_id, db)


@user_profile_router.get("/listings", status_code=status.HTTP_200_OK)
async def get_user_properties(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return await get_user_listings(user_id, db)


@user_profile_router.patch("/profile/update", status_code=status.HTTP_200_OK)
async def update_user_profile(update_data: Optional[UserProfileUpdateRequest] = None, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return await edit_user_profile(user_id, update_data, db)
