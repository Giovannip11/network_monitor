from pathlib import Path
import psutil
import ipaddress
import socket
ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
HISTORY_DIR = ROOT / "history"

DB_PATH = DATA_DIR / "network_monitor.db"
JSON_FILE_PATH = DATA_DIR / "devices.json"

DATA_DIR.mkdir(parents=True,exist_ok=True)
LOG_DIR.mkdir(parents=True,exist_ok=True)
HISTORY_DIR.mkdir(parents=True,exist_ok=True)

def get_network():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        
        current_ip = s.getsockname()[0]
        s.close()
        
        for _, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if (
                    addr.family == socket.AF_INET
                    and addr.address == current_ip
                ):
                    network = ipaddress.ip_network(
                        f"{addr.address}/{addr.netmask}",
                        strict=False
                    )
                    print(f"IP: {addr.address}")
                    print(f"Máscara: {addr.netmask}")
                    print(f"Rede: {network}")
                    
                    return str(network)
        
    except Exception as e:
        print(f"ERRO, ao detectar rede {e}")
        return None
