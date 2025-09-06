from __future__ import annotations

import os
from pathlib import Path
from typing import Final

try:
    # Load environment variables from .env if available
    from dotenv import load_dotenv

    # Load from config/.env explicitly
    _env_path = Path(__file__).parent / "config" / ".env"
    load_dotenv(dotenv_path=_env_path)
except Exception:
    # If dotenv isn't installed, environment variables must be set externally
    pass


def _env_path(name: str, default: str) -> Path:
    value = os.getenv(name, default).strip()
    return Path(value)


LOG_FILE: Final[Path] = _env_path("LOG_FILE", "log.txt")
