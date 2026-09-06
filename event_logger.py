import json
from datetime import datetime
from pathlib import Path


LOG_FILE = Path("events.jsonl")


def log_event(event_type, severity, message, details=None):
    event = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "event_type": event_type,
        "severity": severity,
        "message": message,
        "details": details or {}
    }

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(event) + "\n")