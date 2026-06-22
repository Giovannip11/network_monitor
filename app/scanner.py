import socket
from concurrent.futures import ThreadPoolExecutor

import nmap3

PORTAS_IMPORTANTES = "22,53,80,135,139,443,445,3389,9100"


def scan_host(host):

    nmap = nmap3.Nmap()

    try:
        resultado_scan = nmap.scan_top_ports(
            host, args=f"-O -sS -Pn -p {PORTAS_IMPORTANTES}"
        )

        if host not in resultado_scan:
            return None
        dados_host = resultado_scan[host]
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except:
            hostname = "Desconhecido"

        mac = "N/A"
        vendor = "Desconhecido"
        addresses = dados_host.get("addresses", [])

        for addr in addresses:
            if addr.get("addrtype") == "mac":
                mac = addr.get("addr", "N/A")
                vendor = addr.get("vendor", "Desconhecido")
                break

        os_name = "Desconhecido"

        osmatches = dados_host.get("osmatch", [])
        if osmatches:
            os_name = osmatches[0].get("name", "Desconhecido")

        open_ports = []

        ports = dados_host.get("ports", [])
        for p in ports:
            if p.get("state") == "open":
                open_ports.append(int(p.get("portid")))

        state_info = dados_host.get("state", {})
        status = state_info.get("state", "unknown")

        latency = dados_host.get("runtime", {}).get("elapsed", "N/A")

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

    resultado = nmap_discover.nmap_no_portscan(network, args="-sn -PR")

    hosts_ativos = []

    for ip, info in resultado.items():
        if ip in ["stats", "runtime", "nmaprun"]:
            continue

        # No nmap3, o status fica dentro de um dicionário na chave 'state'
        if isinstance(info, dict):
            state_info = info.get("state", {})
            if state_info.get("state") == "up":
                hosts_ativos.append(ip)

    return hosts_ativos


def scan_network(network):

    print(f"Descobrindo hosts na rede {network}...")

    hosts = discover_hosts(network)

    print(f"{len(hosts)} hosts encontrados.\n")

    devices = []

    with ThreadPoolExecutor(max_workers=20) as executor:
        results = executor.map(scan_host, hosts)

        for result in results:
            if result:
                devices.append(result)

                print(f"[OK] {result['ip']} | {result['vendor']} | {result['os']}")

    return devices
