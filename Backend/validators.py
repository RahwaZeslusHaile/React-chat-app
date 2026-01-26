from typing import Any

class UsernameValidator:
    MIN_LENGTH = 1
    MAX_LENGTH = 50

    @staticmethod
    def validate(username: Any) -> bool:
        if not isinstance(username, str):
            return False
        return UsernameValidator.MIN_LENGTH <= len(username) <= UsernameValidator.MAX_LENGTH


class MessageContentValidator:
    MAX_LENGTH = 1000

    @staticmethod
    def validate(content: Any) -> bool:
        if not isinstance(content, str):
            return False
        return 0 < len(content) <= MessageContentValidator.MAX_LENGTH
