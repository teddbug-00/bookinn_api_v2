from enum import Enum

from pydantic import BaseModel

class NotificationType(str, Enum):
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"
    ACCOUNT = "ACCOUNT"

class NotificationListResponse(BaseModel):
    id: str
    type: NotificationType
    title: str
    content: str
    is_read: bool
