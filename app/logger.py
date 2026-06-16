import os
from datetime import datetime
from config import LOG_DIR

LOG_FILE = os.path.join(LOG_DIR, "monitor.log")


def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")