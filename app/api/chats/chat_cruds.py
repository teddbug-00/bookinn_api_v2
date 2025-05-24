from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc

from app.models.chats import Chat, ChatMessage
from app.schemas.chats import ChatCreate

class ChatCRUD:
    async def create(self, db: Session, *, obj_in: ChatCreate) -> Chat:
        db_obj = Chat(
            listing_id=obj_in.listing_id,
            user_id=obj_in.user_id,
            host_id=obj_in.host_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get(self, db: Session, id: UUID) -> Optional[Chat]:
        return db.query(Chat).filter(Chat.id == id).first()

    async def get_user_chats(
        self, 
        db: Session, 
        user_id: UUID, 
        skip: int = 0, 
        limit: int = 20
    ) -> List[Chat]:
        return db.query(Chat).filter(
            or_(Chat.user_id == user_id, Chat.host_id == user_id)
        ).order_by(desc(Chat.last_message_at)).offset(skip).limit(limit).all()

    async def create_message(
        self, 
        db: Session, 
        *, 
        chat_id: UUID, 
        sender_id: UUID, 
        message: str
    ) -> ChatMessage:
        # Create message
        db_msg = ChatMessage(
            chat_id=chat_id,
            sender_id=sender_id,
            message=message
        )
        db.add(db_msg)

        # Update chat metadata
        chat = await self.get(db, chat_id)
        if chat is not None:
            chat.last_message = message
            chat.last_message_at = db_msg.created_at
            chat.unread_count += 1

        db.commit()
        db.refresh(db_msg)
        db.close()
        return db_msg

    async def mark_as_read(
        self, 
        db: Session, 
        *, 
        chat_id: UUID, 
        user_id: UUID
    ) -> Chat | None:
        # Update all unread messages
        db.query(ChatMessage).filter(
            ChatMessage.chat_id == chat_id,
            ChatMessage.sender_id != user_id,
            ChatMessage.is_read == False
        ).update({"is_read": True})

        # Reset unread count
        chat = await self.get(db, chat_id)
        if chat is not None:
            chat.unread_count = 0
        
            db.commit()
            db.refresh(chat)
            return chat

chat = ChatCRUD()
