import json
import sys
from pathlib import Path


CONFIG_FILE = Path("config.json")


def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        print("[ERROR] Configuration file not found: config.json")
        sys.exit(1)

    except json.JSONDecodeError as error:
        print(f"[ERROR] Invalid JSON in config.json: {error}")
        sys.exit(1)