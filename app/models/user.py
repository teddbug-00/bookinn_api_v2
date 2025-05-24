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
    notifications = relationship("Notification", back_populates="receiver")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")

    bookmarked_listings = relationship(
        "PropertyListing", 
        secondary="bookmarks", 
        back_populates="bookmarked_by",
        overlaps="bookmarks"
    )

    activities = relationship("Activity", back_populates="user")
        
    guest_chats = relationship("Chat", foreign_keys="[Chat.user_id]", back_populates="user")
    host_chats = relationship("Chat", foreign_keys="[Chat.host_id]", back_populates="host")
    sent_messages = relationship("ChatMessage", back_populates="sender")
    