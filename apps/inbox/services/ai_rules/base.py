from abc import ABC, abstractmethod


class BaseSuggestionRule(ABC):
    patterns = []

    @classmethod
    def matches(cls, message: str) -> bool:
        message = message.lower()

        return any(
            pattern.search(message)
            for pattern in cls.patterns
        )

    @classmethod
    @abstractmethod
    def generate_reply(cls) -> str:
        pass