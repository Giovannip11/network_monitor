from app.logger import log_event
def compare_devices(old,new):
    old_ips = {device["ip"] for device in old}
    new_ips = {device["ip"] for device in new}
    
    novos = new_ips - old_ips
    removidos = old_ips - new_ips
    
    for ip in novos:
        log_event(f"NOVOS DISPOSITIVOS {ip}")
    for ip in removidos:
        log_event(f"DISPOSITIVO DESCONECTADO: {ip}")
    
    return novos, removidos