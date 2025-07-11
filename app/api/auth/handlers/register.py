from fastapi import HTTPException, status, BackgroundTasks
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.profile import UserProfile
from app.models.user import User
from app.schemas.auth import UserCreateRequest, UserCreateResponse
from app.schemas.notifications import NotificationCreateRequest, NotificationType
from app.utils.notifications import save_notification
from app.utils.passwords import passwords
from app.websockets.connections.connection_manager import manager


async def register(user_data: UserCreateRequest, db: Session, background_tasks: BackgroundTasks) -> UserCreateResponse:
    try:

        if user_data.password != user_data.password_confirm:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
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
        db.refresh(user)

        notification = NotificationCreateRequest(
            type=NotificationType.ACCOUNT.value,
            title="Welcome to BookInn!",
            content=f"Welcome {user.profile.name}! Your new account has been created successfully."
        )

        background_tasks.add_task(
            manager.send_notification,
            notification,
            str(user.id)
        )

        background_tasks.add_task(
            save_notification,
            str(user.id),
            notification.type,
            notification.title,
            notification.content
        )

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
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with that email already exists"
        )