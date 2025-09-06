from __future__ import annotations

import datetime as dt
from pathlib import Path
from typing import Optional


class ChatLogger:
    """Simple logger that appends chat messages to a text file.

    Each log line format:
        [YYYY-MM-DDTHH:MM:SSZ] role: content
    """

    def __init__(self, file_path: Optional[Path | str] = "log.txt") -> None:
        """Initialize the logger with a file path.

        Args:
            file_path: Path to the log file; defaults to 'log.txt' in CWD.
        """

        self._path: Path = Path(file_path) if file_path is not None else Path("log.txt")

    def log(self, role: str, content: str) -> None:
        """Append a single message to the log file.

        Args:
            role: Message role, e.g., 'user' or 'assistant'.
            content: Message content.
        """

        timestamp = dt.datetime.utcnow().isoformat(timespec="seconds") + "Z"
        safe_content = content.replace("\r", " ").replace("\n", " ")
        line = f"[{timestamp}] {role}: {safe_content}\n"

        # Use a context manager to ensure the file is closed properly
        with self._path.open("a", encoding="utf-8") as fh:
            fh.write(line)
