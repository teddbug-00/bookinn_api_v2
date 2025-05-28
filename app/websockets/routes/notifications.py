from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from app.core.db import DBSession
from app.core.security.tokens import get_current_user_ws
from app.models.notifications import Notification, NotificationType
from app.websockets.connections.connection_manager import manager

router = APIRouter()

@router.websocket("ws_n/notifications")
async def notification_endpoint(
    websocket: WebSocket
):
    try:
        current_user_id = await get_current_user_ws(websocket) # type: ignore
        await manager.connect(websocket, str(current_user_id))
        
        try:
            while True:
                # Keep connection alive and wait for server-pushed notifications
                data = await websocket.receive_json()

        except WebSocketDisconnect:
            await manager.disconnect(websocket, str(current_user_id))
            
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)

# async def save_notification(user_id: str, type: NotificationType, title: str, content: str):
#     db = DBSession()

#     notification = Notification(
#         receiver_id=user_id,
#     )
#     try:
#         await db.add(
#             db=db,
#             chat_id=chat_id,
#             sender_id=sender_id,
#             message=message
#         )
#     finally:
#         db.close()

# Example of how to send a notification from anywhere in your application:
async def send_notification(user_id: str, notification_type: str, message: str):
    """
    Send notification to specific user
    Example: await send_notification("user123", "new_message", "You have a new message")
    """
    notification = {
        "type": notification_type,
        "message": message
    }
    await manager.send_personal_message(notification, user_id)