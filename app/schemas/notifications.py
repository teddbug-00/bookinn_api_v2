from enum import Enum
from uuid import UUID
from typing import List
from pydantic import BaseModel


class NotificationType(str, Enum):
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"
    ACCOUNT = "ACCOUNT"


class NotificationCreateRequest(BaseModel):
    type: NotificationType
    title: str
    content: str


class NotificationListResponse(BaseModel):
    id: UUID
    type: NotificationType
    title: str
    content: str
    is_read: bool


class NotificationsReadRequest(BaseModel):
    notification_ids: List[UUID]
