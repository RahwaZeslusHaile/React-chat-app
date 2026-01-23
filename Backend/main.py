from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
import os

from models import Message
from repository import InMemoryMessageRepository
from service import MessageService
from long_polling.poller import LongPoller

app = FastAPI(title="Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
            "https://rahwafrontendchatapp.hosting.codeyourfuture.io"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = InMemoryMessageRepository()
message_service = MessageService(repository)
poller = LongPoller(message_service)

class MessageRequest(BaseModel):
    username: str
    content: str

class MessageResponse(BaseModel):
    id: str
    username: str
    content: str
    timestamp: str
    
@app.get("/messages", response_model=List[MessageResponse])
def get_messages(after: Optional[str] = Query(None)):
    try:
        if after:
            after_dt = datetime.fromisoformat(after)
            messages = message_service.get_messages_after(after_dt)
        else:
            messages = message_service.get_all_messages()
        messages = sorted(messages, key=lambda m: m.timestamp.value, reverse=True)
        return [MessageResponse(**msg.to_dict()) for msg in messages]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages/{message_id}", response_model=MessageResponse)
def get_message(message_id: str):
    try:
        message = message_service.get_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageResponse(**message.to_dict())
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/messages", response_model=MessageResponse)
def create_message(request: MessageRequest):
    try:
        message = message_service.create_message(username=request.username, content=request.content)
        return MessageResponse(**message.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/messages/longpoll", response_model=List[MessageResponse])
def long_poll_messages(after: str = Query(...)):
    try:
        after_dt = datetime.fromisoformat(after)
        new_messages = poller.wait_for_new_messages(after_dt)
        return [MessageResponse(**m.to_dict()) for m in new_messages]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid timestamp format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
