from abc import ABC, abstractmethod
from typing import Any


class AI(ABC):
    def __init__(self, config: Any = None) -> None:
        self.config = config

    @abstractmethod
    def generate_reply(self, messages: list, context: dict | None = None) -> str:  # pragma: no cover - abstract
        raise NotImplementedError
