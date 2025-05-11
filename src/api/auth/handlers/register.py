from fastapi import HTTPException, status
from src.models.profile import UserProfile
from src.models.user import User
from src.schemas.auth import UserCreate, UserResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.utils.passwords import passwords


async def register(user_data: UserCreate, db: Session) -> UserResponse:
    try:

        if user_data.password != user_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords don't match",
            )

        hashed_data = passwords.get_password_hash(user_data.password)

        new_user = User(
            email = user_data.email,
            hashed_password = hashed_data[0],
            password_salt = hashed_data[1]
        )

        profile = UserProfile(
            name = user_data.name,
            date_of_birth = user_data.date_of_birth,
            phone_number = user_data.phone_number
        )

        new_user.profile = profile

        db.add(new_user)
        db.commit()
        
        response = UserResponse(
            user_id = str(new_user.id),
            email = new_user.email,
            name = profile.name,
            date_of_birth = str(profile.date_of_birth),
            phone_number = profile.phone_number
        )

        return response

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists"
        )