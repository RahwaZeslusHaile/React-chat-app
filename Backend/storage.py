from typing import Optional
from Backend.models import IMessageRepository, IMessage, Message


class InMemoryMessageRepository(IMessageRepository):
    
    def __init__(self):
        self._messages: dict[str, IMessage] = {}
    
    def save(self, message: IMessage) -> None:
        if not isinstance(message, Message):
            raise ValueError("Invalid message type")
        self._messages[message.id] = message
    
    def get_all(self) -> list[IMessage]:
        return list(self._messages.values())
    
    def get_by_id(self, message_id: str) -> Optional[IMessage]:
        return self._messages.get(message_id)

