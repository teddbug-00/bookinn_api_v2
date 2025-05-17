from sqlalchemy.orm import Session
from typing import List

from src.models import Notification
from src.schemas.notifications import NotificationListResponse


async def fetch_notifications(user_id: str, db: Session) -> List[NotificationListResponse]:
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
        raise e