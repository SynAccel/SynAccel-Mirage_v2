import asyncio
import json
import os
import threading
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = Path(os.environ.get("MIRAGE_LOG_FILE", str(BASE_DIR / "logs/perception_log.jsonl")))
_WRITE_LOCK = threading.Lock()


def _append_event(event_data: dict) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(event_data, ensure_ascii=True) + "\n"
    with _WRITE_LOCK, LOG_FILE.open("a", encoding="utf-8") as log_file:
        log_file.write(line)


async def log_event(event_data: dict):
    """Append a timestamped interaction without blocking the event loop."""
    record = dict(event_data)
    record["timestamp"] = datetime.now(timezone.utc).isoformat()
    await asyncio.to_thread(_append_event, record)
