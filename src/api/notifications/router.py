from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.notifications.handlers.list import fetch_notifications
from src.core.db import get_db
from src.core.security import get_current_user_id

notifications_router = APIRouter()

@notifications_router.get("")
async def get_notifications(
        user_id: str = Depends(get_current_user_id),
        db: Session = Depends(get_db)):
    return await fetch_notifications(user_id, db)