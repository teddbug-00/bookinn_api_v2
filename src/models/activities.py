from sqlalchemy.orm import mapped_column, relationship, Mapped
from sqlalchemy import JSON, UUID, DateTime, Enum, ForeignKey, String, func
import uuid

from .base import Base


class ActivityType(str, Enum):
    LISTING = "LISTING"
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"
    REVIEW = "REVIEW"


class ActivityAction(str, Enum):
    CREATE = "CREATE"
    RECEIVE = "RECEIVE"
    DELETE = "DELETE"
    SENT = "SENT"


class Activity(Base):
    __tablename__ = "activities"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    type = mapped_column(Enum(ActivityType.BOOKING, ActivityType.LISTING, ActivityType.PAYMENT, ActivityType.REVIEW, name="activity_type_enum"))
    action = mapped_column(Enum(ActivityAction.CREATE, ActivityAction.RECEIVE, ActivityAction.DELETE, ActivityAction.SENT, name="activity_action_type_enum"))
    entity_id = mapped_column(UUID(as_uuid=True), nullable=True)
    entity_type = mapped_column(String(50), nullable=True)
    metadatas = mapped_column(JSON, nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="activities")