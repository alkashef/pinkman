from __future__ import annotations

import os
import datetime as dt
from pathlib import Path
from typing import Optional
from config import Config


class ChatLogger:
    """Simple logger that appends chat messages to a text file.

    Each log line format:
        [YYYY-MM-DDTHH:MM:SSZ] role: content
    """

    # Class-level configuration loaded from environment
    _CFG: Config = Config.load()

    def __init__(self, file_path: Optional[Path | str] = None) -> None:
        """Initialize the logger with a file path.

        Args:
            file_path: Optional override for the log file path. If None, uses LOG_FILE from config.
        """
        # Resolve path: explicit argument wins; otherwise use configured path
        self._path = Path(file_path) if file_path is not None else self._CFG.log_file

    def log(self, role: str, content: str) -> None:
        """Append a single message to the log file.

        Args:
            role: Message role, e.g., 'user' or 'assistant'.
            content: Message content.
        """
        if not self._CFG.log_enabled:
            return

        timestamp = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        safe_content = content.replace("\r", " ").replace("\n", " ")
        line = f"[{timestamp}] {role}: {safe_content}\n"

        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(line)
