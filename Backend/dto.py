from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class MessageRequest(BaseModel):
    username: str
    content: str
    scheduled_for: Optional[str] = None
    text_color: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False


class ReplyRequest(BaseModel):
    username: str
    content: str
    scheduled_for: Optional[str] = None
    text_color: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False


class ReactionRequest(BaseModel):
    reaction_type: str  # "like" or "dislike"


class MessageResponse(BaseModel):
    id: str
    username: str
    content: str
    timestamp: str
    timestamp_iso: str
    parent_message_id: Optional[str] = None
    likes: int = 0
    dislikes: int = 0
    scheduled_for: Optional[str] = None
    text_color: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False
