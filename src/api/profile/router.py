from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.api.profile.handlers.picture import set_profile_picture
from src.schemas.listing import ListingsListResponse

from .handlers.listings import get_user_listings
from src.core.db import get_db
from src.schemas.profiles import UserCreateProfile, UserProfileUpdateRequest, UserProfileUpdateResponse, \
    UserReviewsResponse
from .handlers.profile import get_profile
from .handlers.edit import edit_user_profile
from src.core.security import get_current_user_id
from .handlers.reviews import get_reviews

user_profile_router = APIRouter()


@user_profile_router.get("/profile", response_model=UserCreateProfile, status_code=status.HTTP_200_OK)
async def get_user_profile(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserCreateProfile:
    return await get_profile(user_id, db)


@user_profile_router.post("/profile/image", status_code=status.HTTP_200_OK)
async def add_profile_picture(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return await set_profile_picture(user_id, db)


@user_profile_router.get("/listings", status_code=status.HTTP_200_OK, response_model=List[ListingsListResponse])
async def get_user_properties(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> List[ListingsListResponse]:
    return await get_user_listings(user_id, db)


@user_profile_router.get("/reviews", status_code=status.HTTP_200_OK, response_model=List[UserReviewsResponse])
async def get_user_reviews(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)) -> List[UserReviewsResponse]:
    return await get_reviews(user_id, db)


@user_profile_router.patch("/profile/update", status_code=status.HTTP_200_OK, response_model=UserProfileUpdateResponse)
async def update_user_profile(update_data: Optional[UserProfileUpdateRequest] = None, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserProfileUpdateResponse:
    return await edit_user_profile(user_id, update_data, db)
