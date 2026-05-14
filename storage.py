import json
import os

FILE_PATH = "data/devices.json"


def save_devices(devices):
    
    os.makedirs("data", exist_ok=True)
    
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