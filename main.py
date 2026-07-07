from app.scanner import scan_network
from app.storage import save_devices, load_devices_from_last_scan, init_db
from app.monitor import compare_devices
from app.config import get_network

from app.pdf_report import generate_pdf

import os
import time

NET = get_network()
SCAN_INTERVAL = 30


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():
    if NET is None:
        print("Not possible found network")
        return
    
    print(f"Monitor network starting {NET}")
    init_db()

    while True:

        

        olds = load_devices_from_last_scan()

        beginning = time.time()

        devices = scan_network(NET)

        end = time.time()
        
        save_devices(devices)
        
        clear()
        
        

        new, removed = compare_devices(
            olds,
            devices
        )

        print("=" * 60)
        print(f"ONLINE DEVICES({NET})")
        print("=" * 60)

        for d in devices:
            print(f"""IP: {d.get('ip', 'N/A')}
HOST: {d.get('hostname', 'Unknown')}
MAC: {d.get('mac', 'N/A')}
VENDOR: {d.get('vendor', 'Unknown')}
OS: {d.get('os', 'Unknown')}
{"-" * 60}""")

        print("\nEVENTS")
        print("=" * 60)
        if new:
            for ip in new: print(f"[NEW DEVICE] {ip}")
        if removed:
            for ip in removed: print(f"[DEVICE OFFLINE] {ip}")
        if not new and not removed:
            print("Nothing changes.")   

        print("\nINFO")
        print("=" * 60)
        print(f"Monitoring network ({NET})")
        print(f"Found devices: {len(devices)}")
        print(f"Scanning time: {end - beginning:.2f}s")
        print(f"Next scan in {SCAN_INTERVAL}s")

        try:
            generate_pdf()
        except Exception as e:
            print(f"Error generate pdf:{e}")
        
        time.sleep(SCAN_INTERVAL)

if __name__ == "__main__":
    main()
