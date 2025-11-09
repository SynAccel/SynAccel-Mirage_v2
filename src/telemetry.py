import json
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("logs/perception_log.jsonl")

async def log_event(event_data: dict):
    """
    Save an interaction (probe + Mirage response) to the perception log.
    """
    # Add a timestamp
    event_data["timestamp"] = datetime.utcnow().isoformat()

    # Convert to JSON line and append to file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        json.dump(event_data, f)
        f.write("\n")
