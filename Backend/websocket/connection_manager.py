from fastapi import WebSocket
from typing import List, Dict
import json
import logging

logger = logging.getLogger(__name__)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New WebSocket connection. Total connections: {len(self.active_connections)}")
        
    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        logger.info(f"WebSocket disconnected. Total connections: {len(self.active_connections)}")
        
    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
    async def broadcast(self, message: Dict):
        disconnected = []
        message_str = json.dumps(message)
        
        for connection in self.active_connections:
            try:
                await connection.send_text(message_str)
            except Exception as e:
                logger.error(f"Error sending message to client: {e}")
                disconnected.append(connection)
        
        for conn in disconnected:
            self.disconnect(conn)
            
    async def broadcast_new_message(self, message_data: Dict):
        await self.broadcast({
            "type": "new_message",
            "data": message_data
        })
        
    async def broadcast_new_reply(self, reply_data: Dict, parent_id: str):
        await self.broadcast({
            "type": "new_reply",
            "data": reply_data,
            "parent_id": parent_id
        })
        
    async def broadcast_reaction(self, message_data: Dict):
        await self.broadcast({
            "type": "reaction_update",
            "data": message_data
        })
