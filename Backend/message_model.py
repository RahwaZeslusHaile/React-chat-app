from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import uuid4

from validators import UsernameValidator, MessageContentValidator


@dataclass
class Timestamp:
    value: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        return self.value.strftime("%H:%M")

    def to_dict(self) -> str:
        return str(self)

    def __gt__(self, other):
        if isinstance(other, Timestamp):
            return self.value > other.value
        if isinstance(other, datetime):
            return self.value > other
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Timestamp):
            return self.value < other.value
        if isinstance(other, datetime):
            return self.value < other
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, Timestamp):
            return self.value == other.value
        if isinstance(other, datetime):
            return self.value == other
        return NotImplemented


@dataclass
class Message:
    id: str = field(default_factory=lambda: str(uuid4()))
    username: str = ""
    content: str = ""
    timestamp: Timestamp = field(default_factory=Timestamp)
    parent_message_id: Optional[str] = None
    likes: int = 0
    dislikes: int = 0
    scheduled_for: Optional[datetime] = None
    text_color: Optional[str] = None
    is_bold: bool = False
    is_italic: bool = False

    def __post_init__(self):
        if not UsernameValidator.validate(self.username):
            raise ValueError(f"Invalid username: {self.username}")
        if not MessageContentValidator.validate(self.content):
            raise ValueError(f"Invalid message content: {self.content}")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "content": self.content,
            "timestamp": str(self.timestamp),
            "timestamp_iso": self.timestamp.value.isoformat(),
            "parent_message_id": self.parent_message_id,
            "likes": self.likes,
            "dislikes": self.dislikes,
            "scheduled_for": self.scheduled_for.isoformat() if self.scheduled_for else None,
            "text_color": self.text_color,
            "is_bold": self.is_bold,
            "is_italic": self.is_italic,
        }

    def get_username(self) -> str:
        return self.username

    def get_content(self) -> str:
        return self.content

    def get_timestamp(self) -> str:
        return str(self.timestamp)
