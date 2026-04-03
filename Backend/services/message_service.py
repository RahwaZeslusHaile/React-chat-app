from datetime import datetime
import time
from typing import Optional, List
from domain import Message, Timestamp
from repository.repository_base import IMessageRepository

class MessageService:
  
    def __init__(self, repository: IMessageRepository):
        self.repository = repository
    
    def create_message(
        self,
        username: str,
        content: str,
        parent_message_id: Optional[str] = None,
        scheduled_for: Optional[datetime] = None,
        text_color: Optional[str] = None,
        is_bold: bool = False,
        is_italic: bool = False,
    ) -> Message:
        
        timestamp = Timestamp(value=scheduled_for) if scheduled_for else Timestamp()

        message = Message(
            username=username,
            content=content,
            parent_message_id=parent_message_id,
            timestamp=timestamp,
            scheduled_for=scheduled_for,
            text_color=text_color,
            is_bold=is_bold,
            is_italic=is_italic,
        )
        self.repository.save(message)
        return message
    
    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        return self.repository.get_by_id(message_id)
    
    def _is_available(self, message: Message) -> bool:
        if message.scheduled_for:
            current_time = datetime.now()
            if message.scheduled_for > current_time:
                return False
        return True

    def get_all_messages(self)->List[Message]:
        messages = [
            msg for msg in self.repository.get_all() 
            if self._is_available(msg)
            ]
        return sorted(messages, key=lambda m: m.timestamp.value, reverse=True)

    def get_messages_after(self, after_dt: datetime)->List[Message]:
        messages = [
            msg for msg in self.repository.get_all()
            if self._is_available(msg) and msg.timestamp > after_dt
        ]
        return sorted(messages, key=lambda m: m.timestamp.value, reverse=True)
    
    def get_replies(self, parent_message_id: str) -> List[Message]:
        all_messages = self.repository.get_all()
        replies = [
            msg for msg in all_messages
            if msg.parent_message_id == parent_message_id and self._is_available(msg)
        ]
        return sorted(replies, key=lambda m: m.timestamp.value)
    
    def create_reply(
        self,
        username: str,
        content: str,
        parent_message_id: str,
        scheduled_for: Optional[datetime] = None,
        text_color: Optional[str] = None,
        is_bold: bool = False,
        is_italic: bool = False,
    ) -> Message:
        parent = self.get_message_by_id(parent_message_id)
        if not parent:
            raise ValueError(f"Parent message not found: {parent_message_id}")
        return self.create_message(
            username=username,
            content=content,
            parent_message_id=parent_message_id,
            scheduled_for=scheduled_for,
            text_color=text_color,
            is_bold=is_bold,
            is_italic=is_italic,
        )
    
    def get_due_scheduled_messages(self) -> List[Message]:
        now = datetime.now()
        due = []
        for msg in self.repository.get_all():
            if msg.scheduled_for and msg.scheduled_for <= now:
                msg.scheduled_for = None       
                self.repository.save(msg)
                due.append(msg)
        return due

    def add_reaction(self, message_id: str, reaction_type: str) -> Optional[Message]:
        message = self.get_message_by_id(message_id)
        if not message:
            raise ValueError(f"Message not found: {message_id}")
        
        message.add_reaction(reaction_type)
        self.repository.save(message)
        return message