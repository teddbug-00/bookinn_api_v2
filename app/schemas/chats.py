from datetime import datetime
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel

class ChatCreate(BaseModel):
    listing_id: str
    user_id: str
    host_id: str


class MessageCreate(BaseModel):
    message: str


class MessageResponse(BaseModel):
    # id: UUID ignore this for now. Could be used to implement message deletion and messae editing
    message: str
    sender_id: UUID
    is_read: bool
    created_at: datetime


class ChatResponse(BaseModel):
    id: UUID
    listing_id: UUID
    user_id: UUID
    host_id: UUID
    unread_count: int
    last_message: Optional[str]
    last_message_at: Optional[datetime]
    created_at: datetime


class ChatMessages(ChatResponse):
    messages: List[MessageResponse]
