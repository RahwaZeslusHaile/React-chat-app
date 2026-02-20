from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException, Query, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from typing import Optional, List
import os

from models.dto import MessageRequest, MessageResponse, ReactionType, ReplyRequest, ReactionRequest
from models.message_model import Message
from repository.repository_inmemory import InMemoryMessageRepository
from service.service import MessageService
from long_polling.poller import LongPoller
from websocket.connection_manager import ConnectionManager
from websocket.handlers import handle_websocket

app = FastAPI(title="Chat API", version="1.0.0")

def parse_iso_datetime(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is not None:
        return parsed.astimezone(timezone.utc).replace(tzinfo=None)
    return parsed

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "https://rahwafrontendchatapp.hosting.codeyourfuture.io",
            "https://frontendwschat.hosting.codeyourfuture.io",
            "http://localhost:5173",
            "http://127.0.0.1:5173"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = InMemoryMessageRepository()
message_service = MessageService(repository)
poller = LongPoller(message_service)
ws_manager = ConnectionManager()

@app.get("/")
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "chat-api"}

@app.get("/messages", response_model=List[MessageResponse])
def get_messages(after: Optional[str] = Query(None)):
    try:
        if after:
            after_dt = parse_iso_datetime(after)
            messages = message_service.get_messages_after(after_dt)
        else:
            messages = message_service.get_all_messages()
        return [MessageResponse(**msg.to_dict()) for msg in messages]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/messages/longpoll", response_model=List[MessageResponse])
def long_poll_messages(after: str = Query(...)):
    try:
        after_dt = parse_iso_datetime(after)
        new_messages = poller.wait_for_new_messages(after_dt)
        sorted_messages = sorted(new_messages, key=lambda m: m.timestamp.value, reverse=True)
        return [MessageResponse(**m.to_dict()) for m in sorted_messages]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/messages/{message_id}", response_model=MessageResponse)
def get_message(message_id: str):
    try:
        message = message_service.get_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageResponse(**message.to_dict())
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/messages", response_model=MessageResponse)
async def create_message(request: MessageRequest):
    try:
        scheduled_dt = parse_iso_datetime(request.scheduled_for) if request.scheduled_for else None
        message = message_service.create_message(
            username=request.username,
            content=request.content,
            scheduled_for=scheduled_dt,
            text_color=request.text_color,
            is_bold=request.is_bold,
            is_italic=request.is_italic,
        )
        await ws_manager.broadcast_new_message(message.to_dict())
        return MessageResponse(**message.to_dict())
    except ValueError :
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/messages/{message_id}/replies", response_model=MessageResponse)
async def create_reply(message_id: str, request: ReplyRequest):
    try:
        scheduled_dt = parse_iso_datetime(request.scheduled_for) if request.scheduled_for else None
        reply = message_service.create_reply(
            username=request.username,
            content=request.content,
            parent_message_id=message_id,
            scheduled_for=scheduled_dt,
            text_color=request.text_color,
            is_bold=request.is_bold,
            is_italic=request.is_italic,
        )
        await ws_manager.broadcast_new_reply(reply.to_dict(), message_id)
        return MessageResponse(**reply.to_dict())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.get("/messages/{message_id}/replies", response_model=List[MessageResponse])
def get_replies(message_id: str):
    try:
        message = message_service.get_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        replies = message_service.get_replies(message_id)
        return [MessageResponse(**reply.to_dict()) for reply in replies]
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/messages/{message_id}/reactions", response_model=MessageResponse)
async def add_reaction(message_id: str, request: ReactionType):
    try:
        if not request.reaction_type:
            raise HTTPException(status_code=400, detail="Invalid reaction type. Must be 'like' or 'dislike'")
        message = message_service.add_reaction(message_id, request.reaction_type)
        await ws_manager.broadcast_reaction(message.to_dict())
        return MessageResponse(**message.to_dict())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid reaction type")
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await handle_websocket(websocket, ws_manager, message_service)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
