from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from src.models import User
from src.schemas.profiles import UserCreateProfile


async def get_profile(user_id: UUID, db: Session) -> UserCreateProfile:
    try:
        user = db.get(User, user_id)

        if not user:            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        
        return UserCreateProfile(
            user_id=user.id,
            email=user.email,
            name=user.profile.name,
            date_of_birth=str(user.profile.date_of_birth),
            phone_number=user.profile.phone_number,
            profile_picture_url=user.profile.profile_picture_url,
        )

    except Exception as e:
        raise e