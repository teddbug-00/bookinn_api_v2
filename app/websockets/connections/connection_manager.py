from typing import Dict, Set
from fastapi import WebSocket

from app.schemas.notifications import NotificationCreateRequest

class ConnectionManager:
    def __init__(self):
        self.active_chats: Dict[str, Set[WebSocket]] = {}
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        if "chats" in str(websocket.url):
            if user_id not in self.active_chats:
                self.active_chats[user_id] = set()
            self.active_chats[user_id].add(websocket)
        else:
            if user_id not in self.active_connections:
                self.active_connections[user_id] = set()
            self.active_connections[user_id].add(websocket)

    async def disconnect(self, websocket: WebSocket, user_id: str):
        if "chats" in str(websocket.url):
            self.active_chats[user_id].remove(websocket)
            if not self.active_chats[user_id]:
                del self.active_chats[user_id]
        else:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]

    async def send_personal_message(self, message: dict, user_id: str):
        if user_id in self.active_chats:
            for connection in self.active_chats[user_id]:
                await connection.send_json(message)

    
    async def send_notification(self, notification: NotificationCreateRequest, user_id: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(notification.model_dump())

manager = ConnectionManager()
