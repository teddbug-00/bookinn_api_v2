from fastapi import HTTPException, status
from src.models.profile import UserProfile
from src.models.user import User
from src.schemas.auth import UserCreate, UserResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


def register(user_data: UserCreate, db: Session) -> UserResponse:
    try:
        # Create user and profile instances
        new_user = User(
            email=user_data.email,
            hashed_password=user_data.password,
            password_salt=user_data.password
        )

        profile = UserProfile(
            name=user_data.name,
            date_of_birth=user_data.date_of_birth,
            phone_number=user_data.phone_number
        )

        new_user.profile = profile

        # Execute database operations
        db.add(new_user)
        db.commit()
        
        response = UserResponse(
            user_id=str(new_user.id),
            email=new_user.email,
            name=profile.name,
            date_of_birth=str(profile.date_of_birth),
            phone_number=profile.phone_number
        )

        print(response)

        # Create response after successful commit
        return response

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with that email already exists"
        )