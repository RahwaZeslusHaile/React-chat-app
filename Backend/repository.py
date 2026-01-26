from repository_base import IMessageRepository
from repository_inmemory import InMemoryMessageRepository

__all__ = [
    "IMessageRepository",
    "InMemoryMessageRepository",
]
    

    def save(self, message: IMessage) -> None:

        if not isinstance(message, Message):

