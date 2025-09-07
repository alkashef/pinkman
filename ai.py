"""
Module: ai.py
Defines the AI class for the project.
"""

from typing import Any

class AI:
    """AI class encapsulating the main agent logic."""

    def __init__(self, config: Any = None) -> None:
        """Initialize the AI agent with optional configuration."""
        self.config = config

    def generate_reply(self, messages: list, context: dict | None = None) -> str:
        """Backend agent implementation: always reply with a constant string.

        Ignores inputs and returns the same response for any message.
        """
        return "Yeah science!"
