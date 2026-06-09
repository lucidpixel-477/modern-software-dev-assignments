from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    app_title: str = "Action Item Extractor"
    base_dir: Path = Path(__file__).resolve().parents[1]
    ollama_action_items_model: str = os.getenv(
        "OLLAMA_ACTION_ITEMS_MODEL",
        "llama3.1:8b",
    )

    @property
    def data_dir(self) -> Path:
        return self.base_dir / "data"

    @property
    def db_path(self) -> Path:
        return self.data_dir / "app.db"

    @property
    def frontend_dir(self) -> Path:
        return self.base_dir / "frontend"

    @property
    def index_html_path(self) -> Path:
        return self.frontend_dir / "index.html"


settings = Settings()
