import socket
import threading
from concurrent.futures import ThreadPoolExecutor

import nmap3

PORTAS_IMPORTANTES = "22,53,80,135,139,443,445,3389,9100"

cancel_event = threading.Event()

def scan_host(host):
    nmap = nmap3.Nmap()

    try:
        resultado_scan = nmap.scan_top_ports(
            host, args=f"-O -sS -Pn -p {PORTAS_IMPORTANTES}"
        )

        if host not in resultado_scan:
            return None
            
        dados_host = resultado_scan[host]
        
     
        if not isinstance(dados_host, dict):
            return None

        try:
            hostname = socket.gethostbyaddr(host)[0]
        except:
            hostname = "Desconhecido"

        mac = "N/A"
        vendor = "Desconhecido"
        
       
        addresses = dados_host.get("addresses", [])
        if isinstance(addresses, list): 
            for addr in addresses:
                if isinstance(addr, dict) and addr.get("addrtype") == "mac":
                    mac = addr.get("addr", "N/A")
                    vendor = addr.get("vendor", "Desconhecido")
                    break

        os_name = "Desconhecido"
        osmatches = dados_host.get("osmatch", [])
        if isinstance(osmatches, list) and osmatches:
            if isinstance(osmatches[0], dict):
                os_name = osmatches[0].get("name", "Desconhecido")

        open_ports = []
        ports = dados_host.get("ports", [])
        
      
        if isinstance(ports, list):
            for p in ports:
                if isinstance(p, dict) and p.get("state") == "open":
                    open_ports.append(int(p.get("portid")))

        state_info = dados_host.get("state", {})
        status = "unknown"
        if isinstance(state_info, dict):
            status = state_info.get("state", "unknown")

        runtime_info = dados_host.get("runtime", {})
        latency = "N/A"
        if isinstance(runtime_info, dict):
            latency = runtime_info.get("elapsed", "N/A")

        return {
            "ip": host,
            "hostname": hostname,
            "mac": mac,
            "vendor": vendor,
            "os": os_name,
            "open_ports": open_ports,
            "status": status,
            "latency": latency,
        }

    except Exception as e:
        print(f"Erro em {host}: {e}")
        return None


def discover_hosts(network):

    nmap_discover = nmap3.NmapHostDiscovery()
    try:
        resultado = nmap_discover.nmap_no_portscan(network, args="-sn")
    
    except Exception as e:
        print(f"ERRO na descoberta{e}")

    hosts_ativos = []
    
    if not resultado or not isinstance (resultado,dict):
        return hosts_ativos

    for ip, info in resultado.items():
        if ip in ["stats", "runtime", "nmaprun"]:
            continue

       
        if isinstance(info, dict):
            state_info = info.get("state", {})
            if state_info.get("state") == "up":
                hosts_ativos.append(ip)
        elif isinstance (info,list) and ip:
            hosts_ativos.append(ip)

    return hosts_ativos


def scan_network(network):
    cancel_event.clear()
    
    print(f"Descobrindo hosts na rede {network}...")
    hosts = discover_hosts(network)
    
    if cancel_event.is_set():
        print("Escaneamento cancelado na fase de descoberta")
        return []

    print(f"{len(hosts)} hosts encontrados.\n")
    devices = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_host, host) for host in hosts]

        for future in futures:
            if cancel_event.is_set():
                print("Cancelando tarefas pendentes de ThreadPool")
                break
            try:
                result = future.result()
                if result:
                    devices.append(result)
                    print(f"[OK] {result['ip']} | {result ['vendor']} | {result['os']}")
            except Exception:
                pass
    
    return devices

