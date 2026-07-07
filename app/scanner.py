import socket
import threading
from concurrent.futures import ThreadPoolExecutor

import nmap3

NETWORK_PORTS = "22,53,80,135,139,443,445,3389,9100"

cancel_event = threading.Event()

def scan_host(host):
    nmap = nmap3.Nmap()

    try:
        scan_result = nmap.scan_top_ports(
            host, args=f"-O -sS -Pn -p {NETWORK_PORTS}"
        )

        if host not in scan_result:
            return None
            
        host_data = scan_result[host]
        
     
        if not isinstance(host_data, dict):
            return None

        try:
            hostname = socket.gethostbyaddr(host)[0]
        except:
            hostname = "Unknown"

        mac = "N/A"
        vendor = "Unknown"
        
       
        addresses = host_data.get("addresses", [])
        if isinstance(addresses, list): 
            for addr in addresses:
                if isinstance(addr, dict) and addr.get("addrtype") == "mac":
                    mac = addr.get("addr", "N/A")
                    vendor = addr.get("vendor", "Unknown")
                    break

        os_name = "Unknown"
        osmatches = host_data.get("osmatch", [])
        if isinstance(osmatches, list) and osmatches:
            if isinstance(osmatches[0], dict):
                os_name = osmatches[0].get("name", "Unknown")

        open_ports = []
        ports = host_data.get("ports", [])
        
      
        if isinstance(ports, list):
            for p in ports:
                if isinstance(p, dict) and p.get("state") == "open":
                    open_ports.append(int(p.get("portid")))

        state_info = host_data.get("state", {})
        status = "unknown"
        if isinstance(state_info, dict):
            status = state_info.get("state", "unknown")

        runtime_info = host_data.get("runtime", {})
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
        result = nmap_discover.nmap_no_portscan(network, args="-sn")
    
    except Exception as e:
        print(f"ERRO na descoberta{e}")

    active_hosts = []
    
    if not result or not isinstance (result,dict):
        return active_hosts

    for ip, info in result.items():
        if ip in ["stats", "runtime", "nmaprun"]:
            continue

       
        if isinstance(info, dict):
            state_info = info.get("state", {})
            if state_info.get("state") == "up":
                active_hosts.append(ip)
        elif isinstance (info,list) and ip:
            active_hosts.append(ip)

    return active_hosts


def scan_network(network):
    cancel_event.clear()
    
    print(f"Descovering hosts on the network {network}...")
    hosts = discover_hosts(network)
    
    if cancel_event.is_set():
        print("Scan cancelled during the discovery phase")
        return []

    print(f"{len(hosts)} Hosts found.\n")
    devices = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(scan_host, host) for host in hosts]

        for future in futures:
            if cancel_event.is_set():
                print("Canceling pending ThreadPool tasks")
                break
            try:
                result = future.result()
                if result:
                    devices.append(result)
                    print(f"[OK] {result['ip']} | {result ['vendor']} | {result['os']}")
            except Exception:
                pass
    
    return devices

