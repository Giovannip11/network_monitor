def detect_device(vendor, open_ports):

    vendor = vendor.lower()

    if "ubiquiti" in vendor:
        return "Access Point"

    if "huawei" in vendor:
        return "Router"

    if 9100 in open_ports:
        return "Printer"

    if 445 in open_ports:
        return "Windows PC"

    if 22 in open_ports:
        return "Linux Device"

    return "Desconhecido"


SERVICES = {
    22: "SSH",
    53: "DNS",
    80: "HTTP",
    135: "RPC",
    139: "NetBIOS",
    443: "HTTPS",
    445: "SMB",
    3389: "RDP",
    9100: "Printer"
}


def get_service_name(port):
    return SERVICES.get(port, "Desconhecido")