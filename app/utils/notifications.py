from app.core.db import DBSession
from app.logging.logger import logger
from app.models.notifications import NotificationType, Notification


async def save_notification(user_id: str, type: NotificationType, title: str, content: str):
    db = DBSession()

    notification = Notification(
        receiver_id=user_id,
        type=type,
        title=title,
        content=content
    )
    try:
        db.add(notification)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(e)
    finally:
        db.close()
