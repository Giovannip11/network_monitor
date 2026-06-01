import os
from datetime import datetime

LOG_DIR = r"C:/projetos/network_monitor/logs"
LOG_FILE = os.path.join(LOG_DIR, "monitor.log")

os.makedirs(LOG_DIR, exist_ok=True)

def log_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")