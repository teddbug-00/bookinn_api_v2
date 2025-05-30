from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models import User, Notification
from app.schemas.notifications import NotificationsReadRequest


async def mark_notifications_as_read(user_id: str, notification_ids: NotificationsReadRequest, db: Session):
    if not db.get(User, user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    unread_notifications = db.query(Notification).filter(False == Notification.is_read).all()
    print(unread_notifications)

    for notification in unread_notifications:
        if str(notification.id) in str(notification_ids):
            notification.is_read = True
            db.commit()
