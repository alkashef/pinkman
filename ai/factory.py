from .base import AI
from .gpt import AI_GPT
from config import get_ai_backend
from logger import ChatLogger


def get_ai() -> AI:
    backend = get_ai_backend()
    try:
        ChatLogger().event("ai.backend.select", backend=backend)
    except Exception:
        pass
    if backend == "gpt":
        return AI_GPT()
    raise ValueError(f"Unknown AI backend: {backend}")
