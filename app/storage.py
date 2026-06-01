import json
import os

DATA_DIR = r"C:/projetos/network_monitor/data"
FILE_PATH = os.path.join(DATA_DIR,"devices.json")
os.makedirs(DATA_DIR,exist_ok=True)

def save_devices(devices):
    
    with open(FILE_PATH, "w") as f:
        json.dump(devices,f,indent=4)
    

def load_services():
    if not os.path.exists(FILE_PATH):
        return []
    
    with open(FILE_PATH,"r") as f:
        try:
            return json.load(f)        
        except json.JSONDecodeError:
            return []