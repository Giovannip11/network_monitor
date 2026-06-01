from pathlib import Path

ROOT = Path(r"C:/projetos/network_monitor")

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
HISTORY_DIR = ROOT / "history"

DATA_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)
HISTORY_DIR.mkdir(exist_ok=True)