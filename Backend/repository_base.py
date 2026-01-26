from abc import ABC, abstractmethod
from typing import Optional

from message_model import Message


class IMessageRepository(ABC):
    @abstractmethod
    def save(self, message: Message) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Message]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, message_id: str) -> Optional[Message]:
        raise NotImplementedError
