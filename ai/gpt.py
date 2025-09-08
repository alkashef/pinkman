from typing import Any
import time

from config import get_openai_config
from logger import ChatLogger
from .base import AI


class AI_GPT(AI):
    """Concrete AI implementation using OpenAI GPT models."""

    def __init__(self, config: Any = None) -> None:
        super().__init__(config)
        cfg = get_openai_config()
        self.api_key = cfg["api_key"]
        self.model = cfg["model"]
        self.client = cfg["client"]
        try:
            ChatLogger().event(
                "ai_gpt.init", model=self.model, key_suffix=self.api_key[-6:] if self.api_key else ""
            )
        except Exception:
            pass

    def generate_reply(self, messages: list, context: dict | None = None) -> str:
        if not messages:
            return ""

        chat_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if not content:
                continue
            if role == "ai":
                role = "assistant"
            elif role not in ("user", "system", "assistant"):
                role = "user"
            chat_messages.append({"role": role, "content": content})

        if not chat_messages:
            return ""

        try:
            ChatLogger().event("ai_gpt.call", model=self.model, msgs=str(len(chat_messages)))
        except Exception:
            pass

        # Retry transient connection errors a few times with backoff
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                resp = self.client.chat.completions.create(
                    model=self.model,
                    messages=chat_messages,
                    temperature=0,
                )
                break
            except Exception as e:  # Broad catch to avoid SDK version issues
                last_err = e
                try:
                    ChatLogger().event(
                        "ai_gpt.call.error", error=f"{e.__class__.__name__}: {e}", attempt=str(attempt + 1)
                    )
                except Exception:
                    pass
                if attempt < 2:
                    time.sleep(0.5 * (2 ** attempt))
                else:
                    raise
        msg = resp.choices[0].message
        return getattr(msg, "content", "") or ""
