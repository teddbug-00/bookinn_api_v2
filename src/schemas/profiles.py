from datetime import date
from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from src.schemas.auth import UserCreateResponse


class UserCreateProfile(UserCreateResponse):
    # More fields to be added later to store user's settings and extra data
    pass


class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None


class UserProfileUpdateResponse(BaseModel):
    user_id: UUID
    name: str
    date_of_birth: date
    phone_number: str
    profile_picture_url: str | None


class UserReviewsResponse(BaseModel):
    review_id: UUID
    rating: float
    comment: str
