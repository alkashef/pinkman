from __future__ import annotations

from typing import Dict, List, Optional


Message = Dict[str, str]


def generate_reply(messages: List[Message], context: Optional[Dict] = None) -> str:
    """Backend agent implementation: always reply with a constant string.

    Ignores inputs and returns the same response for any message.
    """

    return "Yeah science!"
