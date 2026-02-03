from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
import json
import logging

from websocket.connection_manager import ConnectionManager
from service.service import MessageService

logger = logging.getLogger(__name__)

async def handle_websocket(
    websocket: WebSocket,
    manager: ConnectionManager,
    message_service: MessageService
):
    await manager.connect(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
                action = message_data.get("action")
                
                if action == "ping":
                    await websocket.send_text(json.dumps({"type": "pong"}))
                    
                elif action == "get_messages":
                    messages = message_service.get_all_messages()
                    sorted_messages = sorted(
                        messages, 
                        key=lambda m: m.timestamp.value, 
                        reverse=True
                    )
                    await websocket.send_text(json.dumps({
                        "type": "messages_list",
                        "data": [msg.to_dict() for msg in sorted_messages]
                    }))
                    
                else:
                    logger.warning(f"Unknown action: {action}")
                    
            except json.JSONDecodeError:
                logger.error(f"Invalid JSON received: {data}")
            except Exception as e:
                logger.error(f"Error handling message: {e}")
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        manager.disconnect(websocket)
