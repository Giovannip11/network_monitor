from scanner import scan_network
from storage import save_devices, load_services
from monitor import compare_devices

from dotenv import load_dotenv
from pdf_report import generate_pdf

import os
import time

load_dotenv()

NET = os.getenv("NETWORK")
SCAN_INTERVAL = 30


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def main():

    print("Monitor de rede iniciando...")

    while True:

        

        antigos = load_services()

        inicio = time.time()

        dispositivos = scan_network(NET)

        fim = time.time()
        
        save_devices(dispositivos)
        
        clear()
        
        

        novos, removidos = compare_devices(
            antigos,
            dispositivos
        )

        print("=" * 60)
        print("DISPOSITIVOS ONLINE")
        print("=" * 60)

        for d in dispositivos:

            ip = d.get("ip", "N/A")
            hostname = d.get("hostname", "Desconhecido")
            mac = d.get("mac", "N/A")
            vendor = d.get("vendor", "Desconhecido")
            os_name = d.get("os", "Desconhecido")

            print(
                f"""
IP: {ip}
HOST: {hostname}
MAC: {mac}
FABRICANTE: {vendor}
SO: {os_name}
{"-" * 60}
                """
            )

        print("\nEVENTOS")
        print("=" * 60)

        if novos:
            for ip in novos:
                print(f"[NOVO DISPOSITIVO] {ip}")

        if removidos:
            for ip in removidos:
                print(f"[DISPOSITIVO OFFLINE] {ip}")

        if not novos and not removidos:
            print("Nenhuma mudança.")

        print("\nINFO")
        print("=" * 60)
        print(f"Dispositivos encontrados: {len(dispositivos)}")
        print(f"Tempo do scan: {fim - inicio:.2f}s")
        print(f"Próximo scan em {SCAN_INTERVAL}s")

        generate_pdf()
        
        time.sleep(SCAN_INTERVAL)
        
        


if __name__ == "__main__":
    main()