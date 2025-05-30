from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from fastapi import status

from app.models import Notification, User
from app.schemas.notifications import NotificationListResponse


async def fetch_notifications(user_id: str, db: Session) -> List[NotificationListResponse]:
    if not db.get(User, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found."
        )

    try:
        notifications = db.query(Notification).filter(user_id == Notification.receiver_id).all()

        if not notifications:
            return []

        return [NotificationListResponse(
            id=notification.id,
            type=notification.type,
            title=notification.title,
            content=notification.content,
            is_read=notification.is_read

        ) for notification in notifications]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )