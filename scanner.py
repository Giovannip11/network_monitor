import nmap
import socket

from concurrent.futures import ThreadPoolExecutor


PORTAS_IMPORTANTES = "22,53,80,135,139,443,445,3389,9100"


def scan_host(host):

    scanner = nmap.PortScanner()

    try:
        #Scan baseado no NMAP, argumentos e portas importantes da rede.
        scanner.scan(
            host,
            arguments=f'-O -sS -Pn -p {PORTAS_IMPORTANTES}'
        )

        if host not in scanner.all_hosts():
            return None

        # =========================
        # HOSTNAME
        # =========================
        try:
            hostname = socket.gethostbyaddr(host)[0]
        except:
            hostname = "Desconhecido"

        # =========================
        # MAC / VENDOR
        # =========================
        mac = "N/A"
        vendor = "Desconhecido"

        if "addresses" in scanner[host]:

            mac = scanner[host]["addresses"].get("mac", "N/A")

            if (
                "vendor" in scanner[host]
                and mac in scanner[host]["vendor"]
            ):
                vendor = scanner[host]["vendor"][mac]

        # =========================
        # SISTEMA OPERACIONAL
        # =========================
        os_name = "Desconhecido"

        if (
            "osmatch" in scanner[host]
            and len(scanner[host]["osmatch"]) > 0
        ):
            os_name = scanner[host]["osmatch"][0]["name"]

        # =========================
        # PORTAS ABERTAS
        # =========================
        open_ports = []

        if "tcp" in scanner[host]:

            for port in scanner[host]["tcp"]:

                if scanner[host]["tcp"][port]["state"] == "open":
                    open_ports.append(port)

        # =========================
        # LATÊNCIA
        # =========================
        latency = scanner[host].get(
            "times",
            {}
        ).get(
            "srtt",
            "N/A"
        )

        return {
            "ip": host,
            "hostname": hostname,
            "mac": mac,
            "vendor": vendor,
            "os": os_name,
            "open_ports": open_ports,
            "status": scanner[host].state(),
            "latency": latency
        }

    except Exception as e:
        print(f"Erro em {host}: {e}")
        return None


def discover_hosts(network):

    scanner = nmap.PortScanner()

    scanner.scan(
        hosts=network,
        arguments='-sn'
    )

    return scanner.all_hosts()


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

                print(
                    f"[OK] "
                    f"{result['ip']} | "
                    f"{result['vendor']} | "
                    f"{result['os']}"
                )

    return devices