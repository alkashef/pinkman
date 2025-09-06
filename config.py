from __future__ import annotations
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv


class Config:
    """Helper to strictly load and expose environment-backed settings from config/.env.

    - Requires config/.env to exist, else raises FileNotFoundError.
    - Uses python-dotenv to load variables into the process environment.
    """

    def __init__(self, env_path: Path, log_enabled: bool, log_file: Path) -> None:
        self.env_path = env_path
        self.log_enabled = log_enabled
        self.log_file = log_file

    @staticmethod
    def _env_bool(name: str, default: str = "false") -> bool:
        return os.getenv(name, default).strip().lower() in {"1", "true", "yes", "on"}

    @classmethod
    def load(cls, base_dir: Optional[Path] = None) -> "Config":
        base = base_dir or Path(__file__).parent
        env_path = base / "config" / ".env"
        if not env_path.exists():
            raise FileNotFoundError(f"Config file not found: {env_path}")

        load_dotenv(dotenv_path=env_path)

        log_enabled = cls._env_bool("LOG_ENABLED", "false")
        log_file = Path(os.getenv("LOG_FILE", "log.txt").strip())
        return cls(env_path=env_path, log_enabled=log_enabled, log_file=log_file)
