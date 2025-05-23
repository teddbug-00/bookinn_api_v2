from typing import List, Optional
from uuid import UUID
from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.orm import Session

from app.api.profile.handlers.activities import fetch_user_activities
from app.api.profile.handlers.bookmarks import fetch_user_bookmarks
from app.api.profile.handlers.picture import set_profile_picture
from app.schemas.bookmarks import BookmarksListResponse
from app.schemas.listing import ListingsListResponse

from .handlers.listings import get_user_listings
from app.core.db import get_db
from app.schemas.profiles import UserActivitiesResponse, UserCreateProfile, UserProfileUpdateRequest, UserProfileUpdateResponse, \
    UserReviewsResponse
from .handlers.profile import get_profile
from .handlers.edit import edit_user_profile
from app.core.security.tokens import get_current_user_id
from .handlers.reviews import get_reviews

user_profile_router = APIRouter()


@user_profile_router.get("/profile", response_model=UserCreateProfile, status_code=status.HTTP_200_OK)
async def get_user_profile(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserCreateProfile:
    return await get_profile(user_id, db)


@user_profile_router.post("/profile/image", status_code=status.HTTP_200_OK)
async def add_profile_picture(
    user_id: str = Depends(get_current_user_id), 
    db: Session = Depends(get_db),
    image: UploadFile = File(...)):
    return await set_profile_picture(user_id, image, db)


@user_profile_router.get("/listings", status_code=status.HTTP_200_OK, response_model=List[ListingsListResponse])
async def get_user_properties(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> List[ListingsListResponse]:
    return await get_user_listings(user_id, db)


@user_profile_router.get("/bookmarks", status_code=status.HTTP_200_OK, response_model=List[BookmarksListResponse])
async def get_user_bookmarks(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> List[BookmarksListResponse]:
    return await fetch_user_bookmarks(user_id, db)


@user_profile_router.get("/reviews", status_code=status.HTTP_200_OK, response_model=List[UserReviewsResponse])
async def get_user_reviews(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)) -> List[UserReviewsResponse]:
    return await get_reviews(user_id, db)


@user_profile_router.get("/activities", status_code=status.HTTP_200_OK, response_model=List[UserActivitiesResponse])
async def get_user_activities(user_id: UUID = Depends(get_current_user_id), db: Session = Depends(get_db)) -> List[UserActivitiesResponse]:
    return await fetch_user_activities(user_id, db)


@user_profile_router.patch("/profile/update", status_code=status.HTTP_200_OK, response_model=UserProfileUpdateResponse)
async def update_user_profile(update_data: Optional[UserProfileUpdateRequest] = None, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> UserProfileUpdateResponse:
    return await edit_user_profile(user_id, update_data, db)
