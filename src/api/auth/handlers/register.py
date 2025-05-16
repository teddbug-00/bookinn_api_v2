from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.profile import UserProfile
from src.models.user import User
from src.schemas.auth import UserCreateRequest, UserCreateResponse
from src.utils.passwords import passwords


async def register(user_data: UserCreateRequest, db: Session) -> UserCreateResponse:
    try:

        if user_data.password != user_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords don't match",
            )

        hashed_data = passwords.get_password_hash(user_data.password)

        user = User(
            email = user_data.email,
            hashed_password = hashed_data[0],
            password_salt = hashed_data[1]
        )

        profile = UserProfile(
            name = user_data.name,
            date_of_birth = user_data.date_of_birth,
            phone_number = user_data.phone_number
        )

        user.profile = profile

        db.add(user)
        db.commit()

        return UserCreateResponse(
            user_id = user.id,
            email = user.email,
            name = profile.name,
            date_of_birth = str(profile.date_of_birth),
            phone_number = profile.phone_number
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists"
        )