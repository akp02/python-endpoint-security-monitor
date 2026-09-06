import time
import subprocess
import sys
from config_manager import load_config

config = load_config()
SCAN_INTERVAL_SECONDS = config["scan_interval_seconds"]


def run_monitor():
    subprocess.run(
        [sys.executable, "system_health.py"]
    )


def start_scheduler():
    print("Endpoint monitor scheduler started.")

    try:
        while True:
            run_monitor()
            print(
                f"Next scan in {SCAN_INTERVAL_SECONDS} seconds..."
            )
            time.sleep(SCAN_INTERVAL_SECONDS)

    except KeyboardInterrupt:
        print("\n[INFO] Scheduler stopped by user.")


if __name__ == "__main__":
    start_scheduler()