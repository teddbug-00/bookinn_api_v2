from .base import Base
from sqlalchemy import Enum, UUID, Text, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship, mapped_column

class NotificationType(str, Enum):
    SYSTEM = "SYSTEM"
    SECURITY = "SECURITY"
    ACCOUNT = "ACCOUNT"

class Notification(Base):
    __tablename__ = "notifications"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True)
    receiver_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = mapped_column(Enum(NotificationType.SYSTEM, NotificationType.SECURITY, NotificationType.ACCOUNT, name="notification_type_enum"), index=True)
    title = mapped_column(String(100))
    content = mapped_column(Text)
    is_read = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    receiver = relationship("User", back_populates="notifications")
