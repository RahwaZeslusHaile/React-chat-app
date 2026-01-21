from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from Backend.models import Message
from Backend.storage import InMemoryMessageRepository
from Backend.service import MessageService

app = FastAPI(title="Chat API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repository = InMemoryMessageRepository()
message_service = MessageService(repository)
class MessageRequest(BaseModel):
    username: str
    content: str
class MessageResponse(BaseModel):
    id: str
    username: str
    content: str
    timestamp: str

@app.get("/")
async def root():
    return {"message": "Chat API is running"}

@app.get("/messages", response_model=list[MessageResponse])
async def get_messages():
    try:
        messages = message_service.get_all_messages()
        return [MessageResponse(**msg.to_dict()) for msg in messages]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: str):
    try:
        message = message_service.get_message_by_id(message_id)
        if not message:
            raise HTTPException(status_code=404, detail="Message not found")
        return MessageResponse(**message.to_dict())
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/messages", response_model=MessageResponse)
async def create_message(request: MessageRequest):
    try:
        message = message_service.create_message(
            username=request.username,
            content=request.content
        )
        return MessageResponse(**message.to_dict())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

