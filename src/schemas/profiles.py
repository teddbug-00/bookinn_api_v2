from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import BaseModel
from src.schemas.auth import UserCreateResponse


class ActivityType(str, Enum):
    LISTING = "LISTING"
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"
    REVIEW = "REVIEW"


class ActivityAction(str, Enum):
    CREATE = "CREATE"
    RECEIVE = "RECEIVE"
    DELETE = "DELETE"
    SENT = "SENT"


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


class UserActivitiesResponse(BaseModel):
    type: ActivityType
    action: ActivityAction
    entity_type: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
