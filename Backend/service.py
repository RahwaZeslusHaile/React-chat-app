import datetime
from typing import Optional
from Backend.models import IMessage, Message, IMessageRepository, UsernameValidator, MessageContentValidator

class MessageService:
  
    def __init__(self, repository: IMessageRepository):
        self.repository = repository
    
    def create_message(self, username: str, content: str) -> IMessage:
        if not UsernameValidator.validate(username):
            raise ValueError(f"Invalid username: {username}")
        if not MessageContentValidator.validate(content):
            raise ValueError(f"Invalid message content: {content}")
        
        message = Message(username=username, content=content)
        self.repository.save(message)
        return message
    
    def get_messages_since(self, timestamp: datetime, timeout: int = 25):
        start = datetime.datetime.now()
        while datetime.datetime.now() - start < datetime.timedelta(seconds=timeout):
            all_messages = self.repository.get_all()
            new_messages = [
                m for m in all_messages 
                if m.timestamp.value > timestamp
            ]
            if new_messages:
                return new_messages
            datetime.time.sleep(0.5)
        return []
    
    def get_message_by_id(self, message_id: str) -> Optional[IMessage]:
        return self.repository.get_by_id(message_id)
    
    def get_all_messages(self):
        return self.repository.get_all()

    def get_messages_after(self, timestamp: datetime):
        return [
            m for m in self.repository.get_all()
            if m.timestamp.value > timestamp
        ]
