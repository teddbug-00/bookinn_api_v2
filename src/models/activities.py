from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import UUID, Enum
import uuid

from .base import Base


class ActivityType(str, Enum):
    LISTING = "LISTING"
    BOOKING = "BOOKING"
    PAYMENT = "PAYMENT"


class Activity(Base):
    __tablename__ = "activities"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    type = mapped_column(Enum(ActivityType.LISTING, ActivityType.BOOKING, ActivityType.PAYMENT, name="activity_type_enum"))
    # I really am confused of what to do next