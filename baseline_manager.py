import json
from pathlib import Path


BASELINE_FILE = Path("baseline.json")


def save_baseline(data):
    with open(BASELINE_FILE, "w") as file:
        json.dump(data, file, indent=4)


def load_baseline():
    if not BASELINE_FILE.exists():
        return None

    with open(BASELINE_FILE, "r") as file:
        return json.load(file)


def compare_listening_ports(previous_ports, current_ports):
    previous_set = {
        (port["ip"], port["port"], port["process_name"])
        for port in previous_ports
    }

    current_set = {
        (port["ip"], port["port"], port["process_name"])
        for port in current_ports
    }

    new_ports = current_set - previous_set
    removed_ports = previous_set - current_set

    return {
        "new_ports": list(new_ports),
        "removed_ports": list(removed_ports)
    }