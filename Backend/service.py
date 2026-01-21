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
    
    def get_all_messages(self) -> list[IMessage]:
        return self.repository.get_all()
    
    def get_message_by_id(self, message_id: str) -> Optional[IMessage]:
        return self.repository.get_by_id(message_id)