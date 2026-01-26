from typing import Optional

from message_model import Message
from repository_base import IMessageRepository


class InMemoryMessageRepository(IMessageRepository):
    def __init__(self):
        self._messages: dict[str, Message] = {}

    def save(self, message: Message) -> None:
        if not isinstance(message, Message):
            raise ValueError("Invalid message type")
        self._messages[message.id] = message

    def get_all(self) -> list[Message]:
        return list(self._messages.values())

    def get_by_id(self, message_id: str) -> Optional[Message]:
        return self._messages.get(message_id)
