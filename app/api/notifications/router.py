from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.notifications.handlers.list import fetch_notifications
from app.api.notifications.handlers.mark_as_read import mark_notifications_as_read
from app.core.db import get_db
from app.core.security.tokens import get_current_user_id
from app.schemas.notifications import NotificationListResponse, NotificationsReadRequest

notifications_router = APIRouter()

@notifications_router.get("", response_model=List[NotificationListResponse], status_code=status.HTTP_200_OK)
async def get_notifications(
        user_id: str = Depends(get_current_user_id),
        db: Session = Depends(get_db)) -> List[NotificationListResponse]:
    return await fetch_notifications(user_id, db)


@notifications_router.post("/mark_as_read", status_code=status.HTTP_204_NO_CONTENT)
async def mark_as_read(notification_ids: NotificationsReadRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    return await mark_notifications_as_read(user_id, notification_ids, db)
