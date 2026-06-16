from pathlib import Path

ROOT = Path(r"C:/projetos/network_monitor")

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
HISTORY_DIR = ROOT / "history"

DB_PATH = DATA_DIR / "network_monitor.db"
JSON_FILE_PATH = DATA_DIR / "devices.json"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)