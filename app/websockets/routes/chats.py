from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from uuid import UUID
import json
import asyncio
from enum import Enum

from app.core.security.tokens import get_current_user_ws
from app.websockets.connections.connection_manager import manager
from app.api.chats.chat_cruds import chat as chat_crud
from app.core.db import DBSession

class MessageType(Enum):
    MESSAGE = "message"
    TYPING = "typing"
    READ = "read"

router = APIRouter()

@router.websocket("/chats/{chat_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    chat_id: UUID
):
    try:
        current_user_id = await get_current_user_ws(websocket)
        await manager.connect(websocket, str(current_user_id))
        
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
                    event_data = json.loads(data)
                    if not isinstance(event_data, dict) or "type" not in event_data:
                        continue

                    event_type = event_data.get("type")

                    match event_type:

                        case MessageType.MESSAGE.value:

                            if "message" not in event_data:
                                continue
                                
                            message_out = {
                                "type": MessageType.MESSAGE.value,
                                "message": event_data["message"],
                                "sender_id": str(current_user_id)
                            }

                            print(f"Sending message: {message_out}")

                            # Send to both users immediately
                            await asyncio.gather(
                                manager.send_personal_message(message_out, str(current_user_id)),
                                manager.send_personal_message(message_out, other_user_id)
                            )

                            # Save to DB in background
                            asyncio.create_task(save_message(
                                chat_id=chat_id,
                                sender_id=current_user_id,
                                message=event_data["message"]
                            ))

                        case MessageType.TYPING.value:
                            
                            typing_status = {
                                "type": MessageType.TYPING.value,
                                "sender_id": str(current_user_id),
                                "is_typing": event_data.get("is_typing", True)
                            }
                            await manager.send_personal_message(typing_status, other_user_id)

                        case MessageType.READ.value:
                          
                            if "message_id" not in event_data:
                                continue
                                
                            read_status = {
                                "type": MessageType.READ.value,
                                "message_id": event_data["message_id"],
                                "reader_id": str(current_user_id)
                            }
                            await manager.send_personal_message(read_status, other_user_id)

                except json.JSONDecodeError:
                    continue

        except WebSocketDisconnect:
            message = {
                "message": "Other user disconnected"
            }
            await manager.send_personal_message(message, other_user_id)
            await manager.disconnect(websocket, str(current_user_id))
            
    except Exception:
        await websocket.close(code=1008)


async def save_message(chat_id: UUID, sender_id: UUID, message: str):
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
              