from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
import json
import asyncio

from app.core.security.tokens import get_current_user_ws
from app.websockets.connections.connection_manager import manager
from app.api.chats.chat_cruds import chat as chat_crud
from app.core.db import DBSession

router = APIRouter()

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: UUID
):
    try:
        current_user_id = await get_current_user_ws(websocket)
        await manager.connect(websocket, str(current_user_id))
        
        # Get chat info once at connection time
        db = DBSession()
        chat = await chat_crud.get(db, chat_id)
        db.close()
        
        if not chat:
            await websocket.close(code=1008)
            return
            
        other_user_id = str(chat.user_id if chat.host_id == current_user_id else chat.host_id)
        
        try:
            while True:
                data = await websocket.receive_text()
                
                try:
                    message_data = json.loads(data)
                    if not isinstance(message_data, dict) or "message" not in message_data:
                        continue

                    # Simplified message payload
                    message_out = {
                        "message": message_data["message"],
                        "sender_id": str(current_user_id)
                    }

                    # Send message to both users immediately
                    await asyncio.gather(
                        manager.send_personal_message(message_out, str(current_user_id)),
                        manager.send_personal_message(message_out, other_user_id)
                    )

                    # Handle database in background
                    asyncio.create_task(save_message(
                        chat_id=chat_id,
                        sender_id=current_user_id,
                        message=message_data["message"]
                    ))

                except json.JSONDecodeError:
                    continue

        except WebSocketDisconnect:
            await manager.disconnect(websocket, str(current_user_id))
            
    except Exception as e:
        await websocket.close(code=1008)
        raise e

async def save_message(chat_id: UUID, sender_id: UUID, message: str):
    """Background task for database operations only"""
    db = DBSession()
    try:
        await chat_crud.create_message(
            db=db,
            chat_id=chat_id,
            sender_id=sender_id,
            message=message
        )
    finally:
        db.close()