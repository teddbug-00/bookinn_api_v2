import uuid
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import UUID, DateTime, func

from .base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    # Need help completing this to work with the app, so we could have a chat functinality
