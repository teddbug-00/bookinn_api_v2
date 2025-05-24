from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.db import get_db
from app.core.security.tokens import get_current_user_id
from app.models.user import User

from .chat_cruds import chat as chat_crud


from app.schemas.chats import (
    ChatCreate, 
    ChatResponse, 
    ChatMessages, 
    MessageCreate, 
    MessageResponse
)

chats_router = APIRouter()

@chats_router.post("/", response_model=ChatResponse)
async def create_chat(
    chat_in: ChatCreate,
    db: Session = Depends(get_db),
    current_user_id = Depends(get_current_user_id)
):
    if str(current_user_id) != chat_in.user_id and str(current_user_id) != chat_in.host_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Not authorized"
        )
    
    if not db.get(User, chat_in.host_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Host not found"
        )
    
    if not db.get(User, chat_in.user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    return await chat_crud.create(db, obj_in=chat_in)

@chats_router.get("/me", response_model=List[ChatResponse])
async def get_my_chats(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    current_user_id = Depends(get_current_user_id)
):
    return await chat_crud.get_user_chats(
        db, user_id=current_user_id, skip=skip, limit=limit
    )


@chats_router.get("/{chat_id}/messages", response_model=List[MessageResponse])
async def get_chat_messages(
    chat_id: UUID,
    db: Session = Depends(get_db),
    current_user_id = Depends(get_current_user_id)
):
    chat = await chat_crud.get(db, id=chat_id)
    if not db.get(User, current_user_id):
        raise HTTPException(status_code=404, detail="User not found")
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user_id != chat.user_id and current_user_id != chat.host_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return [
            MessageResponse(
            message=message.message,
            sender_id=message.sender_id,
            is_read=message.is_read,
            created_at=message.created_at
        ) for message in chat.messages
    ]


@chats_router.post("/{chat_id}/messages", response_model=MessageResponse)
async def create_message(
    chat_id: UUID,
    message: MessageCreate,
    db: Session = Depends(get_db),
    current_user_id = Depends(get_current_user_id)
):
    chat = await chat_crud.get(db, id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    if current_user_id != chat.user_id and current_user_id != chat.host_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    return await chat_crud.create_message(
        db=db,
        chat_id=chat_id,
        sender_id=current_user_id,
        message=message.message
    )