"""Storage helpers for saving raw, processed, and cleaned data."""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Make sure the project root is importable even when this module is run directly.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection.config import get_config


def _safe_filename(name: str) -> str:
    """Return a filesystem-safe filename for Windows and POSIX systems."""
    safe_name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
    return safe_name.strip("._-") or "file"


def ensure_dirs(config: dict) -> None:
    """Create the raw, processed, and cleaned output folders if they do not exist."""
    raw_dir = Path(config["raw_data_dir"])
    processed_dir = Path(config["processed_data_dir"])
    cleaned_dir = Path(config.get("cleaned_data_dir", "data/cleaned"))

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    cleaned_dir.mkdir(parents=True, exist_ok=True)


def save_raw(url: str, html: str, config: dict) -> str:
    """Save raw HTML content as a JSON file inside the raw-data directory."""
    ensure_dirs(config)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H_%M_%SZ")
    filename = Path(config["raw_data_dir"]) / f"{_safe_filename(timestamp)}.json"

    payload = {
        "url": url,
        "html": html,
        "fetched_at": timestamp,
    }

    filename.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(filename)


def save_processed(records: list, config: dict, name: str = "product") -> str:
    """Save parsed records as a JSON file inside the processed-data directory."""
    ensure_dirs(config)

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H_%M_%SZ")
    filename = Path(config["processed_data_dir"]) / f"{_safe_filename(name)}_{_safe_filename(timestamp)}.json"

    filename.write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(filename)


def save_cleaned(record: dict, filename: str, config: Optional[dict] = None) -> str:
    """Save a cleaned product record as a JSON file inside the cleaned-data directory."""
    if config is None or not config:
        config = get_config()

    ensure_dirs(config)

    cleaned_dir = Path(config.get("cleaned_data_dir", "data/cleaned"))
    output_path = cleaned_dir / filename
    output_path.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    return str(output_path)
