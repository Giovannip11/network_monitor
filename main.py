from scanner import scan_network
from storage import save_devices,load_services
from monitor import compare_devices
import time
from dotenv import load_dotenv
import os
load_dotenv()
NET = os.getenv("NETWORK")
scan_interval = 60

def main():
    
    print("Monitor de rede iniciando...")
    while True:
        antigos=load_services()
        dispositivos = scan_network(NET) 
        save_devices(dispositivos)  
        novos,removidos =compare_devices(
            antigos,
            dispositivos
        ) 
        print("\n===DISPOSITIVOS ONLINE===\n")
        for d in dispositivos:
            print(
                f"{d['ip']} |"
                f"{d['vendor']} |"
                f"{d['os']}"
            )
        print("===EVENTOS===")
        if novos:
            for ip in novos:
                print(f"[NOVO] {ip}")
        
        if removidos:
            for ip in removidos:
                print(f"[NOVO] {ip}")
        if not novos and not removidos:
            print("Nenhuma mudança.")
            
        print(f"\nPróximo scan em {scan_interval}s...\n")
        time.sleep(scan_interval)
if __name__ == "__main__":
    main()
    