import uuid
from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, func, Integer, Text

from .base import Base

class Chat(Base):
    __tablename__ = "chats"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    listing_id = mapped_column(UUID(as_uuid=True), ForeignKey("listings.id"), nullable=False)
    user_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    host_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    unread_count = mapped_column(Integer, default=0)
    last_message = mapped_column(Text, nullable=True)
    last_message_at = mapped_column(DateTime, nullable=True)
    created_at = mapped_column(DateTime, server_default=func.now())
    updated_at = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    listing = relationship("PropertyListing", back_populates="chats")
    user = relationship("User", foreign_keys=[user_id], back_populates="guest_chats")
    host = relationship("User", foreign_keys=[host_id], back_populates="host_chats")
    messages = relationship("ChatMessage", back_populates="chat", cascade="all, delete")
    

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = mapped_column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)

    chat_id = mapped_column(UUID(as_uuid=True), ForeignKey("chats.id"), nullable=False)
    sender_id = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    message = mapped_column(Text, nullable=False)
    is_read = mapped_column(Boolean, default=False)
    created_at = mapped_column(DateTime, server_default=func.now())

    chat = relationship("Chat", back_populates="messages")
    sender = relationship("User", back_populates="sent_messages")
