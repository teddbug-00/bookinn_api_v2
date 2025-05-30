from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status, BackgroundTasks
import asyncio
from app.core.db import DBSession
from app.core.security.tokens import get_current_user_ws
from app.logging.logger import logger
from app.models.notifications import Notification, NotificationType
from app.websockets.connections.connection_manager import manager

router = APIRouter()

@router.websocket("/ws_n/notifications")
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
