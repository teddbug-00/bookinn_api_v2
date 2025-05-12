from datetime import date
from typing import Optional
from pydantic import BaseModel
from src.schemas.auth import UserResponse

class UserProfile(UserResponse):
    # More fields to be added later to store user's settings and extra data
    pass

class UserProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    date_of_birth: Optional[date] = None
    phone_number: Optional[str] = None


class UserProfileUpdateResponse(BaseModel):
    user_id: str
    name: str
    date_of_birth: str
    phone_number: str
    profile_picture_url: str | None