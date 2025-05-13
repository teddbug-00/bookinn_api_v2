import uuid
from .base import Base
from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import mapped_column, relationship

class User(Base):
    __tablename__ = "users"

    id = mapped_column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    email = mapped_column(String, unique=True, index=True)
    hashed_password = mapped_column(String(255))
    password_salt = mapped_column(String(64))
    external_provider_id = mapped_column(String(128), nullable=True, index=True)
    is_active = mapped_column(Boolean, default=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    listings = relationship("PropertyListing", back_populates="owner")