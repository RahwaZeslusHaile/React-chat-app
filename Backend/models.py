from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field
from uuid import uuid4

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
        elif isinstance(other, datetime):
            return self.value > other
        return NotImplemented
    
    def __lt__(self, other):
        if isinstance(other, Timestamp):
            return self.value < other.value
        elif isinstance(other, datetime):
            return self.value < other
        return NotImplemented
    
    def __eq__(self, other):
        if isinstance(other, Timestamp):
            return self.value == other.value
        elif isinstance(other, datetime):
            return self.value == other
        return NotImplemented
    
class UsernameValidator:
    
    MIN_LENGTH = 1
    MAX_LENGTH = 50
    
    @staticmethod
    def validate(username: str) -> bool:
        if not isinstance(username, str):
            return False
        if not (UsernameValidator.MIN_LENGTH <= len(username) <= UsernameValidator.MAX_LENGTH):
            return False
        return True

class MessageContentValidator:
    
    MAX_LENGTH = 1000
    
    @staticmethod
    def validate(content: str) -> bool:
        if not isinstance(content, str):
            return False
        if len(content) == 0 or len(content) > MessageContentValidator.MAX_LENGTH:
            return False
        return True
    
class IMessage(ABC):
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
    
    @abstractmethod
    def get_username(self) -> str:
        pass
    
    @abstractmethod
    def get_content(self) -> str:
        pass
    
    @abstractmethod
    def get_timestamp(self) -> str:
        pass
@dataclass
class Message(IMessage):

    id: str = field(default_factory=lambda: str(uuid4()))
    username: str = ""
    content: str = ""
    timestamp: Timestamp = field(default_factory=Timestamp)
    parent_message_id: Optional[str] = None
    likes: int = 0
    dislikes: int = 0
    
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
            "timestamp": self.get_timestamp(),
            "timestamp_iso": self.timestamp.value.isoformat(),
            "parent_message_id": self.parent_message_id,
            "likes": self.likes,
            "dislikes": self.dislikes
        }
    
    def get_username(self) -> str:
        return self.username
    
    def get_content(self) -> str:
        return self.content
    
    def get_timestamp(self) -> str:
        return str(self.timestamp)

class IMessageRepository(ABC):
    
    @abstractmethod
    def save(self, message: IMessage) -> None:
        pass
    
    @abstractmethod
    def get_all(self) -> list[IMessage]:
        pass
    
    @abstractmethod
    def get_by_id(self, message_id: str) -> Optional[IMessage]:
        pass
