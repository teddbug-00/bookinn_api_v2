from typing import Any, Coroutine
from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.models import User
from src.schemas.user_profile import UserProfile


async def get_profile(user_id: UUID, db: Session) -> UserProfile:
    try:
        user = db.get(User, user_id)

        if user is not None:
            return UserProfile(
                user_id=user_id,
                email=user.email,
                name=user.profile.name,
                date_of_birth=str(user.profile.date_of_birth),
                phone_number=user.profile.phone_number,
                profile_picture_url=user.profile.profile_picture_url,
            )

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )