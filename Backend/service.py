from datetime import datetime
import time
from typing import Optional, List
from models import IMessage, Message, IMessageRepository, UsernameValidator, MessageContentValidator

class MessageService:
  
    def __init__(self, repository: IMessageRepository):
        self.repository = repository
    
    def create_message(self, username: str, content: str, parent_message_id: Optional[str] = None) -> IMessage:
        if not UsernameValidator.validate(username):
            raise ValueError(f"Invalid username: {username}")
        if not MessageContentValidator.validate(content):
            raise ValueError(f"Invalid message content: {content}")
        
        message = Message(username=username, content=content, parent_message_id=parent_message_id)
        self.repository.save(message)
        return message
    
    def get_message_by_id(self, message_id: str) -> Optional[IMessage]:
        return self.repository.get_by_id(message_id)
    
    def get_all_messages(self):
        return self.repository.get_all()

    def get_messages_after(self, after_dt: datetime):
        messages = [msg for msg in self.repository.get_all() if msg.timestamp > after_dt]
        return sorted(messages, key=lambda m: m.timestamp.value, reverse=True)
    
    def get_replies(self, parent_message_id: str) -> List[IMessage]:
        """Get all replies to a parent message"""
        all_messages = self.repository.get_all()
        replies = [msg for msg in all_messages if msg.parent_message_id == parent_message_id]
        return sorted(replies, key=lambda m: m.timestamp.value)
    
    def create_reply(self, username: str, content: str, parent_message_id: str) -> IMessage:
        """Create a reply to an existing message"""
        parent = self.get_message_by_id(parent_message_id)
        if not parent:
            raise ValueError(f"Parent message not found: {parent_message_id}")
        return self.create_message(username=username, content=content, parent_message_id=parent_message_id)
    
    def add_reaction(self, message_id: str, reaction_type: str) -> Optional[IMessage]:
        """Add a like or dislike reaction to a message"""
        message = self.get_message_by_id(message_id)
        if not message:
            raise ValueError(f"Message not found: {message_id}")
        
        if reaction_type == "like":
            message.likes += 1
        elif reaction_type == "dislike":
            message.dislikes += 1
        else:
            raise ValueError(f"Invalid reaction type: {reaction_type}")
        
        self.repository.save(message)
        return message